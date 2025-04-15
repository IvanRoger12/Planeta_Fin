
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
import matplotlib as mpl

st.set_page_config(
    page_title="Planeta Formation - Enquête Diplômés",
    page_icon="🎓",
    layout="wide",
)

def load_css():
    css = """
    body {
        background-color: #f8f9fa;
        color: #333;
        font-family: 'Segoe UI', sans-serif;
    }

    h1, h2, h3 {
        color: #1a73e8;
        font-weight: 600;
    }

    [data-testid="metric-container"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        text-align: center;
        margin: 10px 0;
    }

    .planeta-logo {
        max-width: 200px;
        display: block;
        margin: auto;
        padding-bottom: 1rem;
    }

    .planeta-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        border-bottom: 1px solid #e1e4e8;
    }

    .footer {
        text-align: center;
        font-size: 0.85rem;
        margin-top: 2rem;
        padding-top: 1rem;
        color: #888;
        border-top: 1px solid #ddd;
    }
    """
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

def img_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def set_matplotlib_styles():
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['axes.facecolor'] = '#F8FBFD'
    mpl.rcParams['axes.edgecolor'] = '#DDE6ED'
    mpl.rcParams['axes.labelcolor'] = '#2C3E50'
    mpl.rcParams['axes.grid'] = True
    mpl.rcParams['grid.color'] = '#E5E9F0'
    mpl.rcParams['grid.linestyle'] = '--'
    mpl.rcParams['grid.alpha'] = 0.6
    mpl.rcParams['xtick.color'] = '#2C3E50'
    mpl.rcParams['ytick.color'] = '#2C3E50'
    mpl.rcParams['figure.figsize'] = [10, 6]
    mpl.rcParams['figure.facecolor'] = '#FFFFFF'

load_css()
set_matplotlib_styles()
df = pd.read_csv("enquete_diplomes_planeta.csv")

logo_path = "logo_planeta.png"
logo_html = f'<img src="data:image/png;base64,{img_to_base64(logo_path)}" class="planeta-logo">'

st.markdown(f'''
<div class="planeta-header">
    {logo_html}
    <h1>Analyse Enquête Diplômés – Planeta Formation 🎓</h1>
    <p>Un aperçu interactif des données d'insertion professionnelle et de satisfaction des diplômés.</p>
</div>
''', unsafe_allow_html=True)

# Méthodologie
with st.expander("ℹ️ À propos de l'enquête / Méthodologie", expanded=False):
    st.markdown("""
    Les données utilisées ici sont issues d'une simulation d'enquête menée auprès de diplômés issus de plusieurs écoles du groupe Planeta Formation.  
    Les indicateurs principaux incluent le taux d'insertion professionnelle, la satisfaction des diplômés, le délai moyen avant l'emploi et le salaire moyen par secteur.  
    Cette démarche permettrait d'accompagner les rapports à France Compétences et d'optimiser l'évolution des cursus proposés.
    """)

# Filtres
st.markdown("💡 Astuce : Maintenez `Ctrl` (ou `Cmd` sur Mac) pour sélectionner plusieurs options dans les filtres.")
reset = st.button("🔄 Réinitialiser les filtres")

if reset:
    st.experimental_rerun()

ecoles = st.multiselect("Sélectionnez les écoles :", options=df["École"].unique(), default=df["École"].unique())
promos = st.multiselect("Sélectionnez les promotions :", options=df["Promo"].unique(), default=df["Promo"].unique())
df_filtered = df[(df["École"].isin(ecoles)) & (df["Promo"].isin(promos))]

if df_filtered.empty:
    st.warning("Aucune donnée à afficher avec les filtres actuels.")
else:
    # KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        taux_insertion = df_filtered["Emploi trouvé"].value_counts(normalize=True).get("Oui", 0) * 100
        st.metric("💼 Taux d'insertion", f"{taux_insertion:.1f}%")
    with col2:
        satisfaction_moy = df_filtered["Satisfaction (/5)"].mean()
        st.metric("😊 Satisfaction moyenne", f"{satisfaction_moy:.2f} / 5")
    with col3:
        salaire_moy = df_filtered["Salaire (€)"].mean()
        st.metric("💶 Salaire moyen", f"{salaire_moy:,.0f} €")

    st.divider()

    st.subheader("📊 Répartition des diplômés par école")
    fig1, ax1 = plt.subplots()
    df_filtered["École"].value_counts().plot(kind='bar', ax=ax1)
    st.pyplot(fig1)

    st.subheader("📈 Délai moyen d'insertion par école")
    fig2, ax2 = plt.subplots()
    df_filtered.groupby("École")["Délai (mois)"].mean().plot(kind='bar', ax=ax2)
    st.pyplot(fig2)

    st.subheader("📍 Satisfaction par promotion")
    fig3, ax3 = plt.subplots()
    df_filtered.groupby("Promo")["Satisfaction (/5)"].mean().plot(kind='line', marker='o', ax=ax3)
    st.pyplot(fig3)

    st.subheader("💰 Salaire moyen par secteur")
    fig4, ax4 = plt.subplots()
    df_filtered.groupby("Secteur")["Salaire (€)"].mean().plot(kind='bar', ax=ax4)
    st.pyplot(fig4)

# Pied de page
st.markdown("""
<div class="footer">
    © 2025 Grupo Planeta · Tableau de bord réalisé dans le cadre d'une simulation de projet d'analyse diplômés. <br>
    <a href='https://planetafin-8m9ry9fnf7pj2h5xxd7omk.streamlit.app/' target='_blank'>Voir la version en ligne</a>
</div>
""", unsafe_allow_html=True)
