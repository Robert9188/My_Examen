import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dashboard import (
    traiter_donnees_appartements_ as dash_traiter_apparts,
    traiter_donnees_villas_ as dash_traiter_villas,
    traiter_donnees_terrains_ as dash_traiter_terrains,
)
from scraping import scraper_appartements_raw, scraper_terrains_raw, scraper_villas_raw
from traitement import traiter_donnees_appartements, traiter_donnees_terrains, traiter_donnees_villas

# --- Configuration de l'app ---
st.set_page_config(page_title="Coinafrica - Scraper & Dashboard", layout="wide")

# --- Style personnalisé ---
st.markdown("""
<style>
    div[data-baseweb="tab-list"] { justify-content: space-evenly; }
    div[data-baseweb="tab"] { flex-grow: 1; text-align: center; }

    section[data-testid="stSidebar"] {
        background-color: #083c4a;
        color: white;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2 {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏗️ Coinafrica - Scraping & Analyse de données")

# --- Sidebar ---
st.sidebar.title("🔧 Paramètres")
action = st.sidebar.radio("Sélection d’action", [
    "Scraper les données",
    "Charger depuis fichier CSV",
    "Visualiser le tableau de bord",
    "Évaluer un bien"
])

def afficher_telechargement(df, nom_fichier, titre):
    st.subheader(titre)
    st.dataframe(df, use_container_width=True)
    st.download_button(
        label="💾 Télécharger les données",
        data=df.to_csv(index=False),
        file_name=nom_fichier,
        mime="text/csv"
    )

def afficher_dashboard(df, type_bien):
    st.markdown(f"### 📈 Données traitées - {type_bien}")
    st.dataframe(df.head(10))
    st.markdown(f"### Statistiques générales")
    
    if type_bien == "Villas":
        st.metric("Nombre de villas", len(df))
        st.metric("Superficie moyenne", f"{df['Superficie'].mean():.1f} m²")
        st.metric("Moyenne de pièces", f"{df['Pieces'].mean():.1f}")
        st.metric("Moyenne de salles de bain", f"{df['Salles_bain'].mean():.1f}")
    elif type_bien == "Terrains":
        st.metric("Nombre de terrains", len(df))
        st.metric("Superficie moyenne", f"{df['Superficie'].mean():.1f} m²")
    elif type_bien == "Appartements":
        st.metric("Nombre d'appartements", len(df))
        st.metric("Moyenne de pièces", f"{df['Pieces'].mean():.1f}")

    st.markdown("#### 🧭 Répartition géographique (top 5)")
    st.write(df["Adresse"].value_counts().head(5))

    st.markdown("#### 🔬 Corrélation")
    cols_num = df.select_dtypes(include=['int', 'float']).columns.tolist()
    if len(cols_num) >= 2:
        fig, ax = plt.subplots()
        sns.heatmap(df[cols_num].corr(), annot=True, cmap="Blues", ax=ax)
        st.pyplot(fig)
    else:
        st.info("Pas assez de données numériques pour une heatmap.")

if action == "Scraper les données":
    st.subheader("🕸️ Scraping via BeautifulSoup")
    nb_pages = st.sidebar.slider("Nombre de pages à parcourir", 1, 200, 10)

    bien = st.radio("Quel type de bien veux-tu scraper ?", ["Villas", "Terrains", "Appartements"])
    bouton_scraper = st.button("Lancer le scraping")

    if bouton_scraper:
        with st.spinner("⏳ Scraping en cours..."):
            if bien == "Villas":
                raw = scraper_villas_raw(nb_pages)
                df = traiter_donnees_villas(pd.DataFrame(raw))
                afficher_telechargement(df, "villas_nettoye.csv", "Résultat - Villas")
            elif bien == "Terrains":
                raw = scraper_terrains_raw(nb_pages)
                df = traiter_donnees_terrains(pd.DataFrame(raw))
                afficher_telechargement(df, "terrains_nettoye.csv", "Résultat - Terrains")
            elif bien == "Appartements":
                raw = scraper_appartements_raw(nb_pages)
                df = traiter_donnees_appartements(pd.DataFrame(raw))
                afficher_telechargement(df, "appartements_nettoye.csv", "Résultat - Appartements")

elif action == "Charger depuis fichier CSV":
    st.subheader("📂 Fichiers CSV existants")
    tabs = st.tabs(["🏠 Villas", "🌍 Terrains", "🏢 Appartements"])

    fichiers = {
        "Villas": "data/Scrapper_villas.csv",
        "Terrains": "data/Scrapper_Terrains.csv",
        "Appartements": "data/Scrapper_Appartements.csv"
    }

    for i, bien in enumerate(["Villas", "Terrains", "Appartements"]):
        with tabs[i]:
            try:
                df = pd.read_csv(fichiers[bien])
                afficher_telechargement(df, f"{bien.lower()}_non_nettoyes.csv", f"Raw data - {bien}")
            except Exception:
                st.error(f"Fichier {bien} introuvable ou corrompu.")

elif action == "Visualiser le tableau de bord":
    st.subheader("📊 Tableau de bord interactif")
    onglets = st.tabs(["🏠 Villas", "🌍 Terrains", "🏢 Appartements"])

    try:
        with onglets[0]:
            df_v = pd.read_csv("data/Scrapper_villas.csv")
            afficher_dashboard(dash_traiter_villas(df_v), "Villas")

        with onglets[1]:
            df_t = pd.read_csv("data/Scrapper_Terrains.csv")
            afficher_dashboard(dash_traiter_terrains(df_t), "Terrains")

        with onglets[2]:
            df_a = pd.read_csv("data/Scrapper_Appartements.csv")
            afficher_dashboard(dash_traiter_apparts(df_a), "Appartements")

    except Exception as e:
        st.error(f"Erreur lors du chargement : {e}")

elif action == "Évaluer un bien":
    st.subheader("📝 Formulaire d’évaluation (à venir)")
    st.info("Cette fonctionnalité sera ajoutée dans une version future.")

