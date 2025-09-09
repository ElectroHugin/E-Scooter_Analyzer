# app.py

import streamlit as st
import pandas as pd
from scraper import get_escooter_data
from data_processor import process_dataframe
from translations import translations

# --- Page Configuration ---
st.set_page_config(
    page_title="E-Scooter Analyzer",
    page_icon="🛴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Data Loading with Cache ---
@st.cache_data(ttl="24h")
def load_and_process_data():
    raw_data = get_escooter_data("https://www.escooter-treff.de/tabelle/")
    if 'current' in raw_data:
        df = process_dataframe(raw_data['current'])
        return df
    return pd.DataFrame()

# --- Custom CSS ---
def load_css():
    st.markdown("""<style>.stApp{background-color:#1E1E1E}.stDataFrame{border:1px solid #4F4F4F;border-radius:8px}[data-testid="stSidebar"]{background-color:#2E2E2E}</style>""", unsafe_allow_html=True)

# --- Language Selection and Translation Function ---
if 'lang' not in st.session_state:
    st.session_state.lang = "de"

def t(key):
    return translations[st.session_state.lang][key]

# --- Main App Logic ---
load_css()
df_original = load_and_process_data()

# --- Sidebar ---
st.sidebar.title("⚙️ Settings")
selected_lang = st.sidebar.radio(
    "Sprache / Language",
    options=["de", "en"],
    format_func=lambda lang: "Deutsch" if lang == "de" else "English",
    index=0 if st.session_state.lang == "de" else 1
)
st.session_state.lang = selected_lang

st.sidebar.title(t("sidebar_title"))

# --- Header and Information ---
st.title(t("app_title"))
st.markdown(t("welcome_message"))
st.markdown(t("data_source_info"))
st.markdown(t("github_info"))
st.markdown("---")

if df_original.empty:
    st.error(t("error_loading_data"))
else:
    df = df_original.copy()

    # --- Filter Widgets ---
    weight_range = st.sidebar.slider(t("filter_weight"), int(df['gewicht_kg'].min()), int(df['gewicht_kg'].max()), (int(df['gewicht_kg'].min()), int(df['gewicht_kg'].max())))
    price_range = st.sidebar.slider(t("filter_price"), int(df['uvp'].min()), int(df['uvp'].max()), (int(df['uvp'].min()), int(df['uvp'].max())), step=50)
    akku_range = st.sidebar.slider(t("filter_battery"), int(df['akku_wh'].min()), int(df['akku_wh'].max()), (int(df['akku_wh'].min()), int(df['akku_wh'].max())), step=50)
    motor_range = st.sidebar.slider(t("filter_motor"), int(df['motor_w'].min()), int(df['motor_w'].max()), (int(df['motor_w'].min()), int(df['motor_w'].max())), step=50)

    suspension_types = sorted(df['federung'].dropna().unique().tolist())
    selected_suspension = st.sidebar.multiselect(t("filter_suspension"), suspension_types, default=suspension_types)
    
    blinker_options = sorted(df['blinker'].dropna().unique().tolist())
    selected_blinkers = st.sidebar.multiselect(t("filter_blinkers"), blinker_options, default=blinker_options)

    boolean_options = [t("option_any"), t("option_yes"), t("option_no")]
    has_brake_light = st.sidebar.selectbox(t("filter_brake_light"), options=boolean_options, index=0)
    has_swappable_battery = st.sidebar.selectbox(t("filter_swappable_battery"), options=boolean_options, index=0)

    # --- Apply filters ---
    df = df[df['gewicht_kg'].between(weight_range[0], weight_range[1])]
    df = df[df['uvp'].between(price_range[0], price_range[1])]
    df = df[df['akku_wh'].between(akku_range[0], akku_range[1])]
    df = df[df['motor_w'].between(motor_range[0], motor_range[1])]

    if selected_suspension: df = df[df['federung'].isin(selected_suspension)]
    if selected_blinkers: df = df[df['blinker'].isin(selected_blinkers)]

    if has_brake_light == t("option_yes"): df = df[df['bremslicht'] == True]
    elif has_brake_light == t("option_no"): df = df[df['bremslicht'] == False]
        
    if has_swappable_battery == t("option_yes"): df = df[df['wechselakku'] == True]
    elif has_swappable_battery == t("option_no"): df = df[df['wechselakku'] == False]
        
    # --- Main Page Display ---
    col1, col2, col3 = st.columns(3)
    col1.metric(t("metric_scooters_found"), f"{len(df)}")
    if not df.empty:
        col2.metric(t("metric_avg_price"), f"€{df['uvp'].mean():,.0f}")
        col3.metric(t("metric_avg_battery"), f"{df['akku_wh'].mean():.0f} Wh")

    # --- NEW: Prepare DataFrame for Display ---
    # 1. Define the order and selection of columns you want to show
    columns_to_show = [
        "model", "uvp", "gewicht_kg", "reichweite_km_offiziell", "akku_wh", 
        "motor_w", "federung", "blinker", "bremslicht", "wechselakku", "zuladung_bis_kg"
    ]
    
    # 2. Get the translation map for the current language
    column_map = t("column_names")

    # 3. Create a new DataFrame for display by selecting and renaming columns
    # We filter the map to only include columns that are actually in our display list
    display_df = df[columns_to_show].rename(columns={k: v for k, v in column_map.items() if k in columns_to_show})

    # 4. Display the prepared DataFrame
    st.dataframe(display_df, use_container_width=True)