import streamlit as st
import requests

# --- URL de ton API FastAPI ---
API_URL = "https://projet0-hjt9.onrender.com/predict"

# --- Configuration de la page ---
st.set_page_config(page_title="Prédiction Churn", layout="wide")

# --- En-tête ---
st.title("💡 Application de Prédiction du Churn (API FastAPI)")
st.image("./FastApi/prédire_churn.png", width=600)
st.markdown("Cette interface interagit avec votre modèle hébergé sur **Render** pour prédire le départ des clients.")

st.markdown("---")

# --- Organisation des colonnes principales ---
col_gauche, col_droite = st.columns(2)

# --- Mapping des variables encodées ---
gender_map = {"Female": 0, "Male": 1}
partner_map = {"No": 0, "Yes": 1}
dependents_map = {"No": 0, "Yes": 1}
phone_service_map = {"No": 0, "Yes": 1}
internet_service_map = {"No": 2, "DSL": 0, "Fiber optic": 1}
MultipleLines_map = {"No": 0, "Yes": 2, "No phone service": 1}
OnlineSecurity_map = {"Yes": 2, "No": 0, "No internet service": 1}
OnlineBackup_map = {"No": 0, "Yes": 2, "No internet service": 1}
DeviceProtection_map = {"No": 0, "Yes": 2, "No internet service": 1}
TechSupport_map = {"No": 0, "Yes": 2, "No internet service": 1}
StreamingTV_map = {"No": 0, "Yes": 2, "No internet service": 1}
StreamingMovies_map = {"No": 0, "Yes": 2, "No internet service": 1}
Contract_map = {"Month-to-month": 0, "One year": 1, "Two year": 2}
PaperlessBilling_map = {"Yes": 1, "No": 0}
PaymentMethod_map = {
    "Electronic check": 2,
    "Mailed check": 3,
    "Bank transfer (automatic)": 0,
    "Credit card (automatic)": 1
}

# --- Formulaire dans les colonnes ---
with col_gauche:
    st.subheader("👤 Informations personnelles")
    gender = st.selectbox("Genre", list(gender_map.keys()))
    SeniorCitizen = st.selectbox("Senior Citizen", [0, 1], help="0 = Non, 1 = Oui")
    Partner = st.selectbox("Partenaire", list(partner_map.keys()))
    Dependents = st.selectbox("Ayant des personnes à charge", list(dependents_map.keys()))
    tenure = st.number_input("Ancienneté (mois)", min_value=0, max_value=100, value=12)
    Contract = st.selectbox("Contrat", list(Contract_map.keys()))
    PaperlessBilling = st.selectbox("Facturation sans papier", list(PaperlessBilling_map.keys()))
    PaymentMethod = st.selectbox("Méthode de paiement", list(PaymentMethod_map.keys()))

with col_droite:
    st.subheader("📡 Informations sur les services")
    PhoneService = st.selectbox("Service téléphonique", list(phone_service_map.keys()))
    InternetService = st.selectbox("Type d'Internet", list(internet_service_map.keys()))
    MultipleLines = st.selectbox("Multiple lines", list(MultipleLines_map.keys()))
    OnlineSecurity = st.selectbox("Online Security", list(OnlineSecurity_map.keys()))
    OnlineBackup = st.selectbox("Online Backup", list(OnlineBackup_map.keys()))
    DeviceProtection = st.selectbox("Device Protection", list(DeviceProtection_map.keys()))
    TechSupport = st.selectbox("Tech Support", list(TechSupport_map.keys()))
    StreamingTV = st.selectbox("Streaming TV", list(StreamingTV_map.keys()))
    StreamingMovies = st.selectbox("Streaming Movies", list(StreamingMovies_map.keys()))
    MonthlyCharges = st.number_input("Facture mensuelle", min_value=0.0, max_value=500.0, value=70.0)
    TotalCharges = st.number_input("Total Charges", min_value=0.0, max_value=10000.0, value=800.0)

# --- Préparation des données ---
input_data = {
    "gender": gender_map[gender],
    "SeniorCitizen": SeniorCitizen,
    "Partner": partner_map[Partner],
    "Dependents": dependents_map[Dependents],
    "tenure": tenure,
    "PhoneService": phone_service_map[PhoneService],
    "InternetService": internet_service_map[InternetService],
    "MultipleLines": MultipleLines_map[MultipleLines],
    "OnlineSecurity": OnlineSecurity_map[OnlineSecurity],
    "OnlineBackup": OnlineBackup_map[OnlineBackup],
    "DeviceProtection": DeviceProtection_map[DeviceProtection],
    "TechSupport": TechSupport_map[TechSupport],
    "StreamingTV": StreamingTV_map[StreamingTV],
    "StreamingMovies": StreamingMovies_map[StreamingMovies],
    "Contract": Contract_map[Contract],
    "PaperlessBilling": PaperlessBilling_map[PaperlessBilling],
    "PaymentMethod": PaymentMethod_map[PaymentMethod],
    "MonthlyCharges": MonthlyCharges,
    "TotalCharges": TotalCharges
}

# --- Séparation ---
st.markdown("---")

# --- Section prédiction (centrée en bas) ---
st.subheader("🔮 Résultat de la prédiction")
if st.button("Lancer la prédiction"):
    with st.spinner("⏳ Envoi des données à l'API..."):
        try:
            response = requests.post(API_URL, json=input_data)
            if response.status_code == 200:
                result = response.json()
                st.success("✅ Prédiction réussie !")
                st.json(result)
            else:
                st.error(f"❌ Erreur {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"⚠️ Impossible de contacter l’API : {e}")

# --- Pied de page ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align:center; font-size: 15px; color: grey;'>
    👩🏽‍💻 Développé par <b>Wilga  MBANI</b> © 2025
    </div>
    """,
    unsafe_allow_html=True
)
