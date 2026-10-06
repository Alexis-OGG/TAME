import pandas as pd


def get_excel_column_data(
    file_path,
    column_name
) -> list[str]:
    """Récupère la liste des composants depuis la bonne colonne."""
    try:
        df = pd.read_excel(file_path)
        
        if column_name not in df.columns:
            return [f"Erreur : La colonne '{column_name}' n'existe pas dans ce fichier."]
            
        # Supprime les cases vides et convertit tout en texte pur
        data = df[column_name].dropna().astype(str).tolist()
        return data
        
    except Exception as e:
        return [f"Erreur de lecture des données : {e}"]
