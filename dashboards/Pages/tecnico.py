import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Dashboard Tecnico",
    layout="wide"
)

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "nutrition"
DB_USER = "nutrition_user"
DB_PASSWORD = "1234"

@st.cache_data
def load_data():

    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    query = """
    SELECT *
    FROM nutrition_fastfood
    """

    return pd.read_sql(query, engine)

df = load_data()

st.title("Dashboard Tecnico")

# metricas

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Registros",
    len(df)
)

c2.metric(
    "Columnas",
    len(df.columns)
)

c3.metric(
    "Valores nulos",
    int(df.isnull().sum().sum())
)

c4.metric(
    "Duplicados",
    int(df.duplicated().sum())
)

st.divider()

# valores nulos

st.header("Valores Nulos")

nulls = (
    df.isnull()
    .sum()
    .reset_index()
)

nulls.columns = [
    "columna",
    "nulos"
]

fig = px.bar(
    nulls,
    x="columna",
    y="nulos"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# histograma

st.header("Distribucion de Calorias")

fig2 = px.histogram(
    df,
    x="calories",
    nbins=25
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# proteinas vs calorias

st.header("Proteina vs Calorias")

fig3 = px.scatter(
    df,
    x="calories",
    y="protein_g",
    color="company",
    hover_name="item"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# sodio por cadena

st.header("Sodio Promedio por Restaurante")

sodium = (
    df.groupby("company")
    .agg({
        "sodium_mg": "mean"
    })
    .reset_index()
)

fig4 = px.bar(
    sodium,
    x="company",
    y="sodium_mg",
    color="company"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# resumen estadistico

st.header("Resumen Estadistico")

st.dataframe(
    df.describe()
)