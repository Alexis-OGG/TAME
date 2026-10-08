from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

class Base(DeclarativeBase):
    pass

class FamilyType(Base):
    __tablename__ = "Family_Components"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    sub_family: Mapped[List["ComponentType"]] = relationship(back_populates="family")
    def __repr__(self) -> dict:
        return{
            "id" : self.id,
            "name":self.name,
            "sub_family": [composant.name for composant in self.sub_family]
        }

class ComponentType(Base):
    __tablename__ = "Type_Components"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    family_id:Mapped[int] = mapped_column(ForeignKey("Family_Components.id"))
    champs1: Mapped[str] = mapped_column(String(30))
    champs2: Mapped[str] = mapped_column(String(30))
    champs3: Mapped[str] = mapped_column(String(30))
    champs4: Mapped[str] = mapped_column(String(30))
    champs5: Mapped[str] = mapped_column(String(30))
    champs6: Mapped[str] = mapped_column(String(30))
    champs7: Mapped[str] = mapped_column(String(30))
    champs8: Mapped[str] = mapped_column(String(30))
    champs9: Mapped[str] = mapped_column(String(30))
    champs10: Mapped[str] = mapped_column(String(30))
    family : Mapped["FamilyType"] = relationship(back_populates="sub_family")
    def __repr__(self) -> str:
        return{
            "id" : self.id,
            "name":self.name,
            "family":self.family,
            "champs1:": self.champs1 ,
            "champs2:": self.champs2 ,
            "champs3:": self.champs3 ,
            "champs4:": self.champs4 ,
            "champs5:": self.champs5 ,
            "champs6:": self.champs6 ,
            "champs7:": self.champs7 ,
            "champs8:": self.champs8 ,
            "champs9:": self.champs9 ,
            "champs10:": self.champs10 ,

        }


if __name__ == '__main__':
    engine = create_engine("sqlite:///Components_db", echo=True)
    Base.metadata.create_all(engine)
