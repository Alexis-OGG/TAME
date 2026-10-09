#Outils Modèles
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler,PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
import pickle

from Ressources.create_db import Input_X
from sqlalchemy import create_engine,select
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///Ressources/Project_db")
session = Session(engine)



def create_Train_split_data():
    all_projects= session.scalars(select(Input_X)).all()
    X_data = []
    Y_data = []
    print(f"Nombre de Projets : {len(all_projects)}")
    for item in all_projects:
        X_data.append([item.classe_DM,item.criticite_patient,item.complexite_mecanique,item.complexite_electronique,item.complexite_logicielle,item.complexite_integration,item.contrainte_reglementaires,item.complexite_industrielle,item.maturite_CdC,item.complexite_moyens_essais,item.nb_cycles_dev])
        Y_data.append([item.PM,item.AQD_achats,item.HW,item.SW,item.Meca,item.Test,item.CAO,item.Indus,item.Peer,item.V_and_V,item.SDF,item.Tech])
    return (X_data,Y_data)

(X,Y) = create_Train_split_data()
#Entraînements
def RDM_fit(): 
    model_RDM = MultiOutputRegressor(
        RandomForestRegressor(
            n_estimators=100,
            max_depth=12,
            random_state=42
        )
    )
    model_RDM.fit(X, Y)
    # save the model to disk
    filename = './Tools/models/model_RDM.sav'
    pickle.dump(model_RDM, open(filename, 'wb'))
def KNN_fit(): 
    model_KNN = Pipeline([
        ("scaler", StandardScaler()),
        ("knn", KNeighborsRegressor(
            n_neighbors=3,
            weights="distance"
        ))
    ])
    model_KNN.fit(X, Y)
    # save the model to disk
    filename = './Tools/models/model_KNN.sav'
    pickle.dump(model_KNN, open(filename, 'wb'))
def PLR_fit(): 
    model_PLR = Pipeline([('poly', PolynomialFeatures(degree=4)),
                ('linear', LinearRegression(fit_intercept=False))])
    model_PLR.fit(X, Y)
    filename = './Tools/models/model_PLR.sav'
    pickle.dump(model_PLR, open(filename, 'wb'))
def LR_fit(): 
    model_LR = LinearRegression()
    model_LR.fit(X, Y)
    filename = './Tools/models/model_LR.sav'
    pickle.dump(model_LR, open(filename, 'wb'))
    

#Predictions

def RDM_predict(x_val): 
    filename = './Tools/models/model_RDM.sav'
    model_RDM = pickle.load(open(filename, 'rb'))
    model_RDM.fit(X, Y)
    liste1 = model_RDM.predict([x_val])
    return liste1

def KNN_predict(x_val): 
    filename = './Tools/models/model_KNN.sav'
    model_KNN = pickle.load(open(filename, 'rb'))
    model_KNN.fit(X, Y)
    liste1 = model_KNN.predict([x_val])
    return liste1

def PLR_predict(x_val): 
    filename = './Tools/models/model_PLR.sav'
    model_PLR = pickle.load(open(filename, 'rb'))
    model_PLR.fit(X, Y)
    liste1 = model_PLR.predict([x_val])
    return liste1

def LR_predict(x_val): 
    filename = './Tools/models/model_LR.sav'
    model_LR = pickle.load(open(filename, 'rb'))
    model_LR = LinearRegression()
    model_LR.fit(X, Y)
    liste1 = model_LR.predict([x_val])
    return liste1

if __name__=="__main__":
    RDM_fit()
    KNN_fit()
    LR_fit()
    PLR_fit()