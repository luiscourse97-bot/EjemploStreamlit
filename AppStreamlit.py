import streamlit as st
import pandas as pd
import plotly.express as px
import os
import kagglehub

# Configuración de la página
st.set_page_config(page_title="Análisis Hipertensión México", layout="wide")

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    path = kagglehub.dataset_download("frederickfelix/hipertensin-arterial-mxico")
    # Buscamos el archivo CSV en la carpeta descargada
    for file in os.listdir(path):
        if file.endswith(".csv"):
            full_path = os.path.join(path, file)
            df = pd.read_csv(full_path)
            return df
    return None

df = load_data()

# --- BARRA LATERAL (Navegación) ---
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a:", ["Inicio", "Dashboard Informativo"])
st.sidebar.info(f"**Autor:** Luis Vásquez\n**Curso:** Talento Tech Nivel Integrador")

# --- PÁGINA DE INICIO (Landing Page) ---
if page == "Inicio":
    st.title("🩺 Análisis de Hipertensión Arterial en México")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### Sobre este Proyecto
        Esta aplicación utiliza datos abiertos para analizar la prevalencia y factores de riesgo 
        de la hipertensión en la población mexicana. 
        
        **Objetivos del análisis:**
        * Identificar tendencias demográficas.
        * Visualizar la distribución geográfica de la condición.
        * Facilitar la toma de decisiones basada en datos de salud pública.
        """)
        if st.button("Explorar Dashboard 🚀"):
            st.toast("Cargando panel de control...")
            # En Streamlit, el cambio de radio en el sidebar maneja la navegación.
    
    with col2:
        # Aquí se carga la imagen que mencionaste
        try:
            st.image("imagen_inicio.png", caption="Análisis de Salud Pública - Talento Tech")
        except:
            st.warning("⚠️ No se encontró 'imagen_inicio.png'. Asegúrate de subirla al repositorio.")

    st.divider()
    st.subheader("Vista previa del Dataset")
    if df is not None:
        st.write(df.head(10))
    else:
        st.error("No se pudo cargar el dataset desde Kaggle.")

# --- DASHBOARD ---
elif page == "Dashboard Informativo":
    st.title("📊 Panel de Análisis de Datos")
    
    if df is not None:
        # Métricas rápidas
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Registros", f"{len(df):,}")
        m2.metric("Promedio Edad", f"{df['EDAD'].mean():.1f} años" if 'EDAD' in df.columns else "N/A")
        m3.metric("Columnas", len(df.columns))

        st.divider()

        # Gráficos
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Distribución por Género")
            if 'SEXO' in df.columns:
                fig_sex = px.pie(df, names='SEXO', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig_sex, use_container_width=True)
            else:
                st.info("Columna 'SEXO' no encontrada.")

        with c2:
            st.subheader("Distribución de Edad")
            if 'EDAD' in df.columns:
                fig_age = px.histogram(df, x='EDAD', nbins=20, color_discrete_sequence=['#ff4b4b'])
                st.plotly_chart(fig_age, use_container_width=True)

        st.subheader("Análisis de Correlación")
        # Selector de variables dinámico
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_cols) >= 2:
            var_x = st.selectbox("Selecciona Eje X", numeric_cols, index=0)
            var_y = st.selectbox("Selecciona Eje Y", numeric_cols, index=1)
            fig_scat = px.scatter(df, x=var_x, y=var_y, trendline="ols", opacity=0.5)
            st.plotly_chart(fig_scat, use_container_width=True)

    else:
        st.error("Error al cargar los datos para el dashboard.")
