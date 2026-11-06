class Offre:
    def __init__(self,Distributeur:str="N/A",Conditionnement:str="N/A",Stock:int=0,MOQ:float=1,Prix_Unitaire:list=[]):
        self.Distributeur=Distributeur
        self.Conditionnement=Conditionnement
        self.Stock=Stock
        self.MOQ=MOQ
        self.Prix_Unitaire=Prix_Unitaire

    def __str__(self):
        return(f"""
            == Offres ==
            Distributeur : {self.Distributeur}
            Conditionnement : {self.Conditionnement}
            Stock : {self.Stock}
            MOQ : {self.MOQ}
            Prix_Unitaire : {self.Prix_Unitaire}
            """   )