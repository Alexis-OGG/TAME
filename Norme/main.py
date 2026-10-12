from mcp.server import MCPServer
import os
import re 
from pathlib import Path
mcp = MCPServer("Norme_MCP")


@mcp.resource("file:///normes")
def get_liste_norme_dispo()->str:
    fichiers = os.listdir(Path("./Ressources/md")) 
    normes =[]
    for filename in fichiers:
        normes.append(filename[:-3])
    return "\n".join(normes)

@mcp.tool(
        name="Get_sommaire",
        title="Sommaire Norme PDF",
        description="Renvoie le sommaire indenté")
def get_sommaire(name_norme:str)->str:
    try : 
        with open(Path(f"./Ressources/sommaire/{name_norme}.txt"),"r") as fichier:
            return fichier.read()
    except:
        return f"Le sommaire de la norme {name_norme} n'existe pas"

@mcp.tool(name = "Read_Section",
          title="Lire section",
          description="Renvoie toutes les lignes du texte d'une section à partir de sa ligne de début"
          )
def lire_section(name_norme:str, ligne_debut:int,nb_lignes_max: int = 150)->str:
    fichier = Path(f"./Ressources/md/{name_norme}.md")
    if not fichier.exists():
        return f"Erreur : La norme '{name_norme}' est introuvable."

    with open(fichier, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    if ligne_debut < 1 or ligne_debut > len(lignes):
        return "Numéro de ligne invalide."

    idx_debut = ligne_debut - 1
    extrait = [lignes[idx_debut]]

    match_depart = re.match(r'^(#{1,6})\s+', lignes[idx_debut].strip())
    niveau_depart = len(match_depart.group(1)) if match_depart else 6

    for ligne in lignes[idx_debut + 1 : idx_debut + nb_lignes_max]:
        match_suivant = re.match(r'^(#{1,6})\s+', ligne.strip())
        # Si on tombe sur un nouveau chapitre de niveau égal ou supérieur, on s'arrête !
        if match_suivant and len(match_suivant.group(1)) <= niveau_depart:
            break
        extrait.append(ligne)

    return "".join(extrait)

@mcp.tool(
        name="Get_Line_word",
        title="Outil Chercher mot",
        description="Renvoie une liste des lignes où est cité le mot dans la norme"
)
def chercher_mots_lignes(name_norme:str,mots:str)->list[int]|str:
    fichier = Path(f"./Ressources/md/{name_norme}.md")
    if not fichier.exists():
        return f"Erreur : La norme '{name_norme}' est introuvable."
    with open(fichier, "r", encoding="utf-8") as f:
        lignes = f.readlines()
    lignes_match=[]
    for index,ligne in enumerate(lignes):
        if mots in ligne:
            lignes_match.append(index+1)
    return lignes_match


if __name__ =="__main__" :
    print(chercher_mots_lignes("NF_EN_60601-1-2_12","plan d'essai"))