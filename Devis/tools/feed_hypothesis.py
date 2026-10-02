from pptx.enum.text import MSO_AUTO_SIZE
from pptx.util import Pt
# ============================================================
# REMPLISSAGE HYPOTHESES
# ============================================================

def remplir_placeholder_hypotheses(placeholder, contenu: str) -> None:
    """
    Remplit un placeholder PowerPoint en conservant les styles définis
    dans le masque selon les niveaux de paragraphes.

    Niveau 0 :
        Titre de section défini dans le masque
        Exemple : bleu, 14 pt, sans puce.

    Niveau 1 :
        Élément de liste défini dans le masque
        Exemple : gris, 12 pt, avec une puce orange.
    """

    if not placeholder.has_text_frame:
        raise ValueError(
            f"La forme '{placeholder.name}' ne possède pas de zone de texte."
        )

    text_frame = placeholder.text_frame

    # Permet au texte de revenir automatiquement à la ligne.
    text_frame.word_wrap = True

    # Réduit automatiquement la taille du texte si celui-ci dépasse
    # de la zone prévue par le masque.
    text_frame.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE

    # Supprime l'ancien contenu tout en conservant le placeholder.
    text_frame.clear()

    lignes = [
        ligne.strip()
        for ligne in contenu.splitlines()
        if ligne.strip()
    ]

    if not lignes:
        return

    for index, ligne in enumerate(lignes):
        # clear() conserve un premier paragraphe vide.
        if index == 0:
            paragraphe = text_frame.paragraphs[0]
        else:
            paragraphe = text_frame.add_paragraph()

        if ligne.startswith("-"):
            # Élément de liste utilisant le niveau 2 du masque.
            paragraphe.text = ligne.removeprefix("-").strip()
            paragraphe.font.size = Pt(12)
            paragraphe.level = 1
        else:
            # Titre de section utilisant le niveau 1 du masque.
            paragraphe.text = ligne
            paragraphe.font.size = Pt(16)
            paragraphe.level = 0

if __name__ == "__main__" :
    pass