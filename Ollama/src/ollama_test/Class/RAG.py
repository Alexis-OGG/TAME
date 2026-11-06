import chromadb
from chromadb.utils import embedding_functions
from .AI import Agent_AI
from docling_core.types.doc import DocItemLabel, SectionHeaderItem, TableItem, PictureItem
import re

MAX_CHARS = 1800  # ≈ 450 tokens
class Embeddings:
    def __init__(self,model_embbed='qwen3-embedding:0.6b',model_retrieve='qwen3.5:4b'):
        self.model_embbed=model_embbed
        self.client= chromadb.EphemeralClient()
        self.collection = self.client.get_or_create_collection("Datasheets",embedding_function=embedding_functions.OllamaEmbeddingFunction(model_name=model_embbed))
        self.model_retrieve=model_retrieve


    def __split_long_text(self,text, max_chars=MAX_CHARS):
        """Découpe un long texte sur les sauts de ligne puis sur les phrases."""
        parts, cur = [], ""
        for para in re.split(r"\n+|(?<=[.!?])\s+", text):
            if cur and len(cur) + len(para) + 1 > max_chars:
                parts.append(cur)
                cur = ""
            cur += (" " if cur else "") + para
        if cur:
            parts.append(cur)
        return parts


    def __split_table(self,md, max_chars=MAX_CHARS):
        """Découpe un tableau markdown par lignes en répétant l'en-tête."""
        lines = md.split("\n")
        if len(md) <= max_chars or len(lines) < 4:
            return [md]
        header = "\n".join(lines[:2])  # ligne d'en-têtes + séparateur |---|
        out, cur = [], header
        for row in lines[2:]:
            if len(cur) + len(row) + 1 > max_chars and cur != header:
                out.append(cur)
                cur = header
            cur += "\n" + row
        if cur != header:
            out.append(cur)
        return out


    def __chunk_docling(self,doc, max_chars=MAX_CHARS, part_regex=None):
        chunks = []
        stack = []          # pile de titres [(niveau, titre)]
        buffer, pages = [], set()
        TOC_HEADING = re.compile(
            r"^\s*(table\s+of\s+contents?|contents?|sommaire|table\s+des\s+mati[èe]res"
            r"|list\s+of\s+(figures|tables)|table\s+of\s+(figures|tables)"
            r"|index|revision\s+history|document\s+history)\s*$",
            re.IGNORECASE,
        )
        def path():
            return [t for _, t in stack]

        def emit(text, page_set, is_table):
            headings = path()
            if text not in headings :
                prefix = " > ".join(headings)
                full = f"{prefix}\n{text}" if prefix else text
                chunks.append({
                    "text": full,                       # à indexer (titres + contenu)
                    "headings": headings,
                    "page": min(page_set) if page_set else None,
                    "is_table": is_table,
                    "parts": sorted(set(re.findall(part_regex, text))) if part_regex else [],
                })

        def flush():
            nonlocal buffer, pages
            text = "\n".join(buffer).strip()
            if text:
                for piece in self.__split_long_text(text, max_chars):
                    emit(piece, pages, False)
            buffer, pages = [], set()
        SKIP_LABELS = {DocItemLabel.DOCUMENT_INDEX, DocItemLabel.PAGE_HEADER, DocItemLabel.PAGE_FOOTER}
        skipping = False
        for item, _ in doc.iterate_items():
            # print(item)
            if item.label in SKIP_LABELS: continue
            page = item.prov[0].page_no if getattr(item, "prov", None) else None

            if isinstance(item, SectionHeaderItem) or item.label == DocItemLabel.TITLE:
                flush()
                if TOC_HEADING.match(item.text):
                    skipping = True          
                    continue
                skipping = False
                lvl = getattr(item, "level", 0)
                stack[:] = [(l, t) for l, t in stack if l < lvl]
                stack.append((lvl, item.text.strip()))

            if skipping:
                continue

            elif isinstance(item, TableItem):
                flush()
                try:
                    md = item.export_to_markdown(doc=doc)
                except TypeError:                    # anciennes versions de docling-core
                    md = item.export_to_markdown()
                caption = ""
                try:
                    caption = item.caption_text(doc)
                except Exception:
                    pass
                for piece in self.__split_table(md, max_chars):
                    emit((caption + "\n" if caption else "") + piece,
                        {page} if page else set(), True)

            elif isinstance(item, PictureItem):
                continue                             

            elif getattr(item, "text", None):
                if sum(map(len, buffer)) + len(item.text) > max_chars:
                    flush()
                buffer.append(item.text.strip())
                if page:
                    pages.add(page)

        flush()
        return chunks
    
    def index_document(self,doc_id, text):
        chunks = self.__chunk_docling(text)
        BATCH_SIZE = 10 
        # for chunk in chunks:
        #     print("=======================================")
        #     print(chunk)
        print(f"Vectorisation de {len(chunks)} morceaux en lots de {BATCH_SIZE}...")
        not_finish=True
        while not_finish:
            try : 
                # 3. Tu boucles pour envoyer par lots
                for i in range(0, len(chunks), BATCH_SIZE):
                    batch_chunks = chunks[i:i + BATCH_SIZE]
                    
                    # On génère les IDs et métadonnées uniquement pour ce lot
                    batch_ids = [f"{doc_id}_{j}" for j in range(i, i + len(batch_chunks))]
                    batch_metadatas = [
                            {
                                "doc_id": doc_id,
                                "page": c["page"] or -1,                    # None interdit dans Chroma
                                "section": " > ".join(c["headings"] or []), # liste -> string
                                "is_table": c.get("is_table", False),
                                "parts": ",".join(c.get("parts", [])),      # liste -> string
                            }
                            for c in batch_chunks
                        ]
                    
                    # On upsert le petit lot. Ollama n'aura pas le temps de Timeout.
                    self.collection.upsert(
                        documents=[c["text"] for c in batch_chunks],
                        ids=batch_ids,
                        metadatas=batch_metadatas
                    )
                    print(f"Lot {i // BATCH_SIZE + 1} inséré avec succès.")
                not_finish=False
            except :
                if BATCH_SIZE==1: print("impossible")
                BATCH_SIZE=round(BATCH_SIZE/2)


        # self.collection.upsert(
        #     ids=[f"{doc_id}_{i}" for i in range(len(chunks))],
        #     documents=[c["text"] for c in chunks],
        #     embeddings=self.__embed([c["text"] for c in chunks]),
        #     metadatas=[
        #             {
        #                 "doc_id": doc_id,
        #                 "page": c["page"] or -1,                    # None interdit dans Chroma
        #                 "section": " > ".join(c["headings"] or []), # liste -> string
        #                 "is_table": c.get("is_table", False),
        #                 "parts": ",".join(c.get("parts", [])),      # liste -> string
        #             }
        #             for c in chunks
        #         ]
        #     )
       
        return len(chunks)

    def rag_query(self,question, n_docs=5):
        agent = Agent_AI(model= self.model_retrieve)
        
        results = self.collection.query(query_texts=[question], n_results=n_docs*2)
        context = "  \n\n  ".join(results['documents'][0][:n_docs])
        prompt = f"""You are a data extraction agent. Answer the question with the context.
        IF not found, answer null.
        CONTEXT :
        {context}
        QUESTION : {question}
        RESPONSE :"""

        print("============Question============")
        print(question)
        print("============context============")
        print("  \n-------------------\n  ".join(results['documents'][0][:n_docs]))
        content = agent.query_stream(message=prompt,temperature=0.1,think=False)

        #On laisse une chance 
        if content =="null":
            context = "  \n\n  ".join(results['documents'][0][n_docs:])
            prompt = f"""You are a data extraction agent. Answer the question with the context.
            IF not found, answer null.
            CONTEXT :
            {context}
            QUESTION : {question}
            RESPONSE :"""
            content= agent.query_stream(message=prompt,temperature=0.1,think=False)
        print("============RESPONSE============")
        print(content)
        return content

if __name__=="__main__":    
    import os
    test= Embeddings()
    OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),"assets")
    with open(os.path.join(OUT_DIR,"sortie.md"),"r",encoding='utf-8') as f:
        fichier = f.read()
    
        test.index_document("datasheet",fichier)
