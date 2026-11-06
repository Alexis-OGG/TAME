from ..API_Distrib import query_digikey_sub,get_digikey_token

def Recherche_substitut_digikey(mpn_obs:str):
    try:
        token_digykey= get_digikey_token()
        return  query_digikey_sub(mpn_obs,token_digykey)
    except Exception as e :
        return {"Status": "Failed","content":f"Erreur Inconnu {e}"}
    
def Recherche_eq_gen(mpn_obs,token_digykey):
    pass


if __name__=="__main__":
    pass