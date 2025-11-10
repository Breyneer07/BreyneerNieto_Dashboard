# Autor: Breyneer Nieto Cardeño
# Proyecto: Activity 1 - Data Visualization and Dashboard Deployment
# Descripción: Dashboard interactivo de admisiones, retención y satisfacción estudiantil

import streamlit as st
import pandas as pd
import altair as alt
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="University Dashboard", layout="wide")

# --- RUTA COMPLETA DEL ARCHIVO CSV ---
DATA_PATH = r"C:\Users\ADMIN\Downloads\Teller 3corte\university_student_data.csv"

# --- VERIFICACIÓN DE EXISTENCIA DEL ARCHIVO ---
st.sidebar.header("📂 Verificación de datos")
st.sidebar.write("Ruta actual:", os.getcwd())
st.sidebar.write("Buscando archivo en:", DATA_PATH)
st.sidebar.write("¿Existe el archivo?", os.path.exists(DATA_PATH))

if not os.path.exists(DATA_PATH):
    st.error(f"❌ No se encontró el archivo CSV en la ruta:\n{DATA_PATH}")
    st.stop()  # Detiene la app si el archivo no existe
else:
    st.success("✅ Archivo encontrado correctamente. Cargando datos...")

# --- CARGAR DATOS ---
df = pd.read_csv(DATA_PATH)

# --- TÍTULO PRINCIPAL ---
st.title("📊 University Dashboard — Admissions, Retention & Satisfaction")
st.markdown("**Autor:** Breyneer Nieto Cardeño")

# --- FILTROS EN SIDEBAR ---
st.sidebar.header("🎚️ Filtros")
years = sorted(df["Year"].unique())
terms = sorted(df["Term"].unique())

year_sel = st.sidebar.multiselect("Selecciona año(s):", years, default=years)
term_sel = st.sidebar.multiselect("Selecciona periodo(s):", terms, default=terms)

# --- FILTRAR DATAFRAME ---
df_f = df[df["Year"].isin(year_sel) & df["Term"].isin(term_sel)]

# --- MÉTRICAS PRINCIPALES (KPIs) ---
col1, col2, col3 = st.columns(3)
col1.metric("Solicitudes totales", int(df_f["Applications"].sum()))
col2.metric("Tasa de retención promedio", f"{df_f['Retention Rate (%)'].mean():.2f}%")
col3.metric("Satisfacción promedio", f"{df_f['Student Satisfaction (%)'].mean():.2f}%")

st.markdown("---")

# --- GRÁFICA 1: TENDENCIA DE RETENCIÓN ---
st.subheader("📈 Tendencia de retención por año")
chart1 = alt.Chart(df_f).mark_line(point=True, color="#4e79a7").encode(
    x="Year:O",
    y="Retention Rate (%):Q",
    tooltip=["Year", "Retention Rate (%)"]
)
st.altair_chart(chart1, use_container_width=True)

# --- GRÁFICA 2: SATISFACCIÓN POR AÑO ---
st.subheader("😊 Satisfacción promedio por año")
chart2 = alt.Chart(df_f).mark_boxplot(color="#f28e2b").encode(
    x="Year:O",
    y="Student Satisfaction (%):Q",
    tooltip=["Year", "Student Satisfaction (%)"]
)
st.altair_chart(chart2, use_container_width=True)

# --- GRÁFICA 3: COMPARACIÓN SPRING VS FALL ---
st.subheader("🌸🌧️ Comparación entre Spring y Fall")
chart3 = alt.Chart(df_f).mark_bar(color="#e15759").encode(
    x="Term:O",
    y="Student Satisfaction (%):Q",
    tooltip=["Term", "Student Satisfaction (%)"]
)
st.altair_chart(chart3, use_container_width=True)

# --- MENSAJE FINAL ---
st.markdown("---")
st.info("✅ Dashboard ejecutado correctamente. Si ves las gráficas arriba, los datos se cargaron sin problemas.")
