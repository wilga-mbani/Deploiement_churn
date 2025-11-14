import streamlit as st
import requests

# --- URL de ton API FastAPI ---
API_URL = "https://deploiement-churn.onrender.com/predict"

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

internet_service_map = {"No": 2, "DSL": 0, "Fiber optic": 1}
OnlineSecurity_map = {"Yes": 2, "No": 0, "No internet service": 1}
OnlineBackup_map = {"No": 0, "Yes": 2, "No internet service": 1}
TechSupport_map = {"No": 0, "Yes": 2, "No internet service": 1}
StreamingMovies_map = {"No": 0, "Yes": 2, "No internet service": 1}
Contract_map = {"Month-to-month": 0, "One year": 1, "Two year": 2}
PaymentMethod_map = {
    "Electronic check": 2,
    "Mailed check": 3,
    "Bank transfer (automatic)": 0,
    "Credit card (automatic)": 1
}

# --- Formulaire dans les colonnes ---
with col_gauche:
    st.subheader("👤 Informations personnelles")
    tenure = st.number_input("Ancienneté (mois)", min_value=0, max_value=100, value=12)
    Contract = st.selectbox("Contrat", list(Contract_map.keys()))
    PaymentMethod = st.selectbox("Méthode de paiement", list(PaymentMethod_map.keys()))

with col_droite:
    st.subheader("📡 Informations sur les services")
    InternetService = st.selectbox("Type d'Internet", list(internet_service_map.keys()))
    OnlineSecurity = st.selectbox("Online Security", list(OnlineSecurity_map.keys()))
    OnlineBackup = st.selectbox("Online Backup", list(OnlineBackup_map.keys()))
    TechSupport = st.selectbox("Tech Support", list(TechSupport_map.keys()))
    StreamingMovies = st.selectbox("Streaming Movies", list(StreamingMovies_map.keys()))
    MonthlyCharges = st.number_input("Facture mensuelle", min_value=0.0, max_value=500.0, value=70.0)
    TotalCharges = st.number_input("Total Charges", min_value=0.0, max_value=10000.0, value=800.0)

# --- Préparation des données ---
input_data = {
    
    "tenure": tenure,
    "InternetService": internet_service_map[InternetService],
    "OnlineSecurity": OnlineSecurity_map[OnlineSecurity],
    "OnlineBackup": OnlineBackup_map[OnlineBackup],
    "TechSupport": TechSupport_map[TechSupport],
    "StreamingMovies": StreamingMovies_map[StreamingMovies],
    "Contract": Contract_map[Contract],
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
