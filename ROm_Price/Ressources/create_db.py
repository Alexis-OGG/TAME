from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    pass

class Input_X(Base):
    __tablename__ = "Input_X_base"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_name: Mapped[str] = mapped_column(String(30))
    # sub_family: Mapped[List["ComponentType"]] = relationship(back_populates="family")
    classe_DM:Mapped[int]
    criticite_patient:Mapped[int]
    complexite_mecanique:Mapped[int]
    complexite_electronique:Mapped[int]
    complexite_logicielle:Mapped[int]
    complexite_integration:Mapped[int]
    contrainte_reglementaires:Mapped[int]
    complexite_industrielle:Mapped[int]
    maturite_CdC:Mapped[int]
    complexite_moyens_essais:Mapped[int]
    nb_cycles_dev:Mapped[int]
    PM: Mapped[float]
    AQD_achats: Mapped[float]
    HW: Mapped[float] 
    SW: Mapped[float] 
    Meca: Mapped[float] 
    Test: Mapped[float] 
    CAO: Mapped[float] 
    Indus: Mapped[float] 
    Peer: Mapped[float] 
    V_and_V: Mapped[float] 
    SDF: Mapped[float] 
    Tech: Mapped[float] 
    def __input__(self) -> dict:
        return{
            "classe_DM":self.classe_DM,
            "criticite_patient":self.criticite_patient,
            "complexite_mecanique":self.complexite_mecanique,
            "complexite_electronique":self.complexite_electronique,
            "complexite_logicielle":self.complexite_logicielle,
            "complexite_integration":self.complexite_integration,
            "contrainte_reglementaires":self.contrainte_reglementaires,
            "complexite_industrielle":self.complexite_industrielle,
            "maturite_CdC":self.maturite_CdC,
            "complexite_moyens_essais":self.complexite_moyens_essais,

            # "family":self.family,
            # "champs1:": self.champs1 ,
            # "champs2:": self.champs2 ,
            # "champs3:": self.champs3 ,
            # "champs4:": self.champs4 ,
            # "champs5:": self.champs5 ,
            # "champs6:": self.champs6 ,
            # "champs7:": self.champs7 ,
            # "champs8:": self.champs8 ,
            # "champs9:": self.champs9 ,
            # "champs10:": self.champs10 ,
        }
    def __output__(self) -> dict:
            return{
                "PM":self.PM,
                "AQD_achats":self.AQD_achats,
                "HW":self.HW,
                "SW":self.SW,
                "Meca":self.Meca,
                "Test":self.Test,
                "CAO":self.CAO,
                "Indus":self.Indus,
                "Peer":self.Peer,
                "V_and_V":self.V_and_V,
                "SDF":self.SDF,
                "Tech":self.Tech,
            }

if __name__ == '__main__':
    engine = create_engine("sqlite:///Ressources/Project_db", echo=True)
    Base.metadata.create_all(engine)
