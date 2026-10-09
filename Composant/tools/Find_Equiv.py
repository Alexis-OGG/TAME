from tools.API_Distrib import query_digikey_sub

def Recherche_substitut_digikey(mpn_obs,token_digykey,type):
    liste_substituts = query_digikey_sub(mpn_obs,token_digykey)

def Recherche_eq_gen(mpn_obs,token_digykey):
    pass