from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TableStructureOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from pathlib import Path
import os
from curl_cffi import requests





def lire_datasheet(reference:str,url:str,numero_page:int):
     pdf_filepath=f"files/{reference}.pdf"
     if not(os.path.isfile(pdf_filepath)):
          try : 
               response = requests.get(url, impersonate="chrome110", timeout=15)
               if response.status_code == 200:
                    content_type = response.headers.get("Content-Type", "")
               
                    if "application/pdf" in content_type.lower() or "application/octet-stream" in content_type.lower():
                         with open(pdf_filepath, "wb") as file:
                              file.write(response.content)
                    else:
                              return f"Erreur : Le pare-feu bloque toujours. Type reçu : {content_type[:50]}..."
               else:
                    return f"Erreur lors du téléchargement du fichier : Code HTTP {response.status_code}"
          except Exception as e:
               return f"Erreur lors du téléchargement du fichier : {str(e)}"
     try:
          pipeline_options = PdfPipelineOptions()
          pipeline_options.do_ocr = False
          pipeline_options.artifacts_path = Path("./docling_models")
          pipeline_options.do_table_structure = True
          pipeline_options.table_structure_options = TableStructureOptions(do_cell_matching=True)
          doc_converter = DocumentConverter(
               format_options={
                    InputFormat.PDF: PdfFormatOption(
                         pipeline_options=pipeline_options
                    )
               }
          )
          result = doc_converter.convert(pdf_filepath,page_range=(numero_page, numero_page))
          markdown_text = result.document.export_to_markdown()
          return markdown_text
     except Exception as e:
          return f"Erreur lors de la lecture du fichier PDF : {str(e)}"


print(lire_datasheet("bruh","https://www.mouser.com/catalog/specsheets/lnncs00024-1.pdf",3))