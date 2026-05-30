import streamlit as st
import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt

# ── Configuration page ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Churn Prediction",
    page_icon="🔮",
    layout="wide"
)

# ── Chargement modèle ────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model         = joblib.load("../models/best_model.pkl")
    scaler        = joblib.load("../models/scaler.pkl")
    feature_names = joblib.load("../models/feature_names.pkl")
    return model, scaler, feature_names

model, scaler, feature_names = load_model()

# ── Header ───────────────────────────────────────────────────────────────
st.title("🔮 Churn Prediction — Telco Customer")
st.markdown("Remplis le profil d'un client pour obtenir son **score de risque de départ**.")
st.divider()

# ── Sidebar : formulaire client ──────────────────────────────────────────
st.sidebar.header("👤 Profil client")

gender          = st.sidebar.selectbox("Genre", ["Male", "Female"])
senior          = st.sidebar.selectbox("Senior citizen", ["Non", "Oui"])
partner         = st.sidebar.selectbox("A un partenaire", ["Yes", "No"])
dependents      = st.sidebar.selectbox("A des personnes à charge", ["Yes", "No"])
tenure          = st.sidebar.slider("Ancienneté (mois)", 0, 72, 12)
phone_service   = st.sidebar.selectbox("Service téléphonique", ["Yes", "No"])
multiple_lines  = st.sidebar.selectbox("Plusieurs lignes", ["Yes", "No", "No phone service"])
internet        = st.sidebar.selectbox("Service Internet", ["Fiber optic", "DSL", "No"])
online_sec      = st.sidebar.selectbox("Sécurité en ligne", ["Yes", "No", "No internet service"])
online_bkp      = st.sidebar.selectbox("Sauvegarde en ligne", ["Yes", "No", "No internet service"])
device_prot     = st.sidebar.selectbox("Protection appareil", ["Yes", "No", "No internet service"])
tech_support    = st.sidebar.selectbox("Support technique", ["Yes", "No", "No internet service"])
streaming_tv    = st.sidebar.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
streaming_mov   = st.sidebar.selectbox("Streaming Films", ["Yes", "No", "No internet service"])
contract        = st.sidebar.selectbox("Type de contrat", ["Month-to-month", "One year", "Two year"])
paperless       = st.sidebar.selectbox("Facture dématérialisée", ["Yes", "No"])
payment         = st.sidebar.selectbox("Mode de paiement", [
    "Electronic check", "Mailed check",
    "Bank transfer (automatic)", "Credit card (automatic)"])
monthly_charges = st.sidebar.slider("Charges mensuelles (€)", 18.0, 120.0, 65.0)
total_charges   = st.sidebar.slider("Charges totales (€)", 0.0, 9000.0,
                                     float(monthly_charges * tenure))

# ── Bouton prédiction ────────────────────────────────────────────────────
predict_btn = st.sidebar.button("🔮 Prédire le risque", type="primary", use_container_width=True)

# ── Construction du vecteur de features ──────────────────────────────────
def build_input():
    avg_monthly_spend = total_charges / (tenure + 1)
    spend_drift       = monthly_charges - avg_monthly_spend
    service_vals = [phone_service, multiple_lines, online_sec,
                    online_bkp, device_prot, tech_support,
                    streaming_tv, streaming_mov]
    nb_services   = sum(1 for v in service_vals if v == "Yes")
    no_protection = int(online_sec == "No" and tech_support == "No" and device_prot == "No")
    tenure_seg    = 0 if tenure <= 12 else 1 if tenure <= 36 else 2 if tenure <= 60 else 3
    value_seg     = 0 if monthly_charges < 35 else 1 if monthly_charges < 65 else 2

    row = {
        "gender":            0 if gender == "Female" else 1,
        "SeniorCitizen":     1 if senior == "Oui" else 0,
        "Partner":           1 if partner == "Yes" else 0,
        "Dependents":        1 if dependents == "Yes" else 0,
        "tenure":            tenure,
        "PhoneService":      1 if phone_service == "Yes" else 0,
        "MultipleLines":     {"No": 0, "No phone service": 1, "Yes": 2}[multiple_lines],
        "InternetService":   {"DSL": 0, "Fiber optic": 1, "No": 2}[internet],
        "OnlineSecurity":    {"No": 0, "No internet service": 1, "Yes": 2}[online_sec],
        "OnlineBackup":      {"No": 0, "No internet service": 1, "Yes": 2}[online_bkp],
        "DeviceProtection":  {"No": 0, "No internet service": 1, "Yes": 2}[device_prot],
        "TechSupport":       {"No": 0, "No internet service": 1, "Yes": 2}[tech_support],
        "StreamingTV":       {"No": 0, "No internet service": 1, "Yes": 2}[streaming_tv],
        "StreamingMovies":   {"No": 0, "No internet service": 1, "Yes": 2}[streaming_mov],
        "Contract":          {"Month-to-month": 0, "One year": 1, "Two year": 2}[contract],
        "PaperlessBilling":  1 if paperless == "Yes" else 0,
        "PaymentMethod":     {"Bank transfer (automatic)": 0, "Credit card (automatic)": 1,
                              "Electronic check": 2, "Mailed check": 3}[payment],
        "MonthlyCharges":    monthly_charges,
        "TotalCharges":      total_charges,
        "avg_monthly_spend": avg_monthly_spend,
        "spend_drift":       spend_drift,
        "nb_services":       nb_services,
        "no_protection":     no_protection,
        "tenure_segment":    tenure_seg,
        "value_segment":     value_seg,
    }
    return pd.DataFrame([row])[feature_names]
# ── Affichage résultat ────────────────────────────────────────────────────
if predict_btn:
    input_df = build_input()
    proba    = model.predict_proba(input_df)[0][1]
    risk_pct = proba * 100

    col1, col2, col3 = st.columns(3)

    # Score principal
    with col1:
        color = "#e74c3c" if risk_pct > 60 else "#f39c12" if risk_pct > 30 else "#2ecc71"
        level = "🔴 RISQUE ÉLEVÉ" if risk_pct > 60 else "🟡 RISQUE MODÉRÉ" if risk_pct > 30 else "🟢 RISQUE FAIBLE"
        st.markdown(f"""
        <div style='background:{color}22; border-left: 5px solid {color};
                    padding: 20px; border-radius: 8px;'>
            <h2 style='color:{color}; margin:0'>{risk_pct:.1f}%</h2>
            <p style='margin:4px 0 0 0; font-weight:bold'>{level}</p>
            <p style='margin:4px 0 0 0; color:#666'>Probabilité de départ</p>
        </div>
        """, unsafe_allow_html=True)

    # Métriques clés
    with col2:
        st.metric("Ancienneté", f"{tenure} mois")
        st.metric("Charges mensuelles", f"{monthly_charges:.0f} €")

    with col3:
        st.metric("Nb. services", f"{int((input_df['nb_services'].values[0]))}")
        st.metric("Contrat", contract)

    st.divider()

    # SHAP — explication de la prédiction
    st.subheader("🔍 Pourquoi ce score ? (Explication SHAP)")
    explainer   = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(input_df)

    fig, ax = plt.subplots(figsize=(10, 4))
    shap.waterfall_plot(
        shap.Explanation(
            values        = shap_values[0],
            base_values   = explainer.expected_value,
            data          = input_df.iloc[0],
            feature_names = feature_names
        ),
        show=False
    )
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.info("💡 Les barres **rouges** poussent vers le churn · Les barres **bleues** retiennent le client")

else:
    st.info("👈 Remplis le profil client dans la barre latérale puis clique sur **Prédire le risque**")

    # Affiche les stats globales par défaut
    st.subheader("📊 Vue d'ensemble du dataset")
    df = pd.read_csv("../data/raw/churn_raw.csv")
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df = df.dropna()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total clients",    f"{len(df):,}")
    c2.metric("Taux de churn",    f"{(df['Churn']=='Yes').mean()*100:.1f}%")
    c3.metric("Charge moy/mois",  f"{df['MonthlyCharges'].mean():.0f} €")
    c4.metric("Ancienneté moy.",  f"{df['tenure'].mean():.0f} mois")