from fastapi import FastAPI 
from pydantic import BaseModel 
import joblib
import pandas as pd
import numpy as np
import os




app= FastAPI(
    title= " API sur un modèle de classification GradientBoostingClassification ",
    description= "API pour faire des prédictions sur les clients qui vont quitter ou non l'entreprise",
    version='2.0'
)


# Acceuil
@app.get("/")
def read_root():
    """
    Message de Bienvenue
    """
    return {"message": "Bienvenue sur l'api du Churn predictor !"}


# chargement du modèle
def load():
   
    model_path = "./FastApi/model_churn.joblib"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Le modèle {model_path} est introuvable.")
    model = joblib.load(model_path)
    return model

# importation
model = load()

# Définition du format d'entréé
class ChurnInput(BaseModel):
   
    gender: int
    SeniorCitizen: int
    Partner: int
    Dependents: int
    tenure: int
    PhoneService: int
    MultipleLines: int
    InternetService: int
    OnlineSecurity: int
    OnlineBackup: int
    DeviceProtection: int
    TechSupport: int
    StreamingTV: int
    StreamingMovies: int
    Contract: int
    PaperlessBilling: int
    PaymentMethod: int
    MonthlyCharges: float
    TotalCharges: float



@app.post("/predict")
async def predict(input_data: ChurnInput):
    """
    Modèle de prédiction du churn
    """
    try:
        # Conversion en DataFrame (le modèle attend un tableau 2D)
        data_dict = input_data.dict()
        data_df = pd.json_normalize([data_dict])

        # Prédiction
        prediction = model.predict(data_df)
        proba = model.predict_proba(data_df)

        churn = int(prediction[0])
        probability = float(proba[0, churn])

        message = (
            f"Le client {'va quitter' if churn == 1 else 'ne va pas quitter'} "
            f"l'entreprise avec une probabilité de {100 * probability:.2f}%."
        )

        return {
            "prediction": churn,
            "probability": round(probability, 4),
            "message": message
        }

    except Exception as e:
        return {"error": str(e)}



"""
    if predictions[0]== 1:
        print(f"classe {predictions[0]},",f"le client va quitter l'entreprise avec une probabilité de {100*proba[0,1]:.2f} %.")
    else:
        print(f"classe {predictions[0]},",f"le client ne va pas quitter l'entreprise avec une probabilité de {100*proba[0, 0]:.2f} % .") 
"""
    



   

    
    









