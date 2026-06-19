import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import requests
import os
from dotenv import load_dotenv 

load_dotenv()

# config

st.set_page_config(
    page_title="Fast Food Calorie Counter",
    layout="wide"
)

# databse

DB_HOST = "100.59.201.22"
DB_PORT = "5432"
DB_NAME = "calorie_db"
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

# title

st.title('Fast Food Calorie Counter')
st.caption("Comparacion nutricional entre cadenas de comida rapida")

# KPI

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Productos",
    len(df)
)

col2.metric(
    "Calorias promedio",
    round(df["calories"].mean(), 1)
)

col3.metric(
    "Proteina promedio",
    round(df["protein_g"].mean(), 1)
)

col4.metric(
    "Sodio promedio",
    round(df["sodium__mg"].mean(), 1)
)

st.divider()

# contador de calorias

st.header("Calorie Counter")

restaurant = st.selectbox(
    "Selecciona restaurante",
    sorted(df["company"].unique())
)

restaurant_df = df[
    df["company"] == restaurant
]

selected_items = st.multiselect(
    "Selecciona productos",
    restaurant_df["item"]
)

if selected_items:

    order = restaurant_df[
        restaurant_df["item"].isin(selected_items)
    ]

    total_calories = order["calories"].sum()
    total_protein = order["protein_g"].sum()
    total_sodium = order["sodium__mg"].sum()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Calorias",
        f"{total_calories:.0f}"
    )

    c2.metric(
        "Proteina",
        f"{total_protein:.1f} g"
    )

    c3.metric(
        "Sodio",
        f"{total_sodium:.0f} mg"
    )

    st.dataframe(
        order[
            [
                "item",
                "calories",
                "protein_g",
                "sodium__mg"
            ]
        ]
    )

st.divider()

st.header("🔍 Buscar Otros Alimentos (USDA API)")
st.caption("¿Consumiste algo casero o natural? Búscalo en la base de datos del Gobierno de EE.UU.")

# Creamos un campo de texto y un botón
api_query = st.text_input("Ingresa un alimento en inglés (ej. banana, rice, apple):")

if st.button("Buscar Alimento"):
    if api_query:
        # Llamamos a la API 
        API_KEY = os.getenv("USDA_API_KEY") 
        url = "https://api.nal.usda.gov/fdc/v1/foods/search"
        params = {
            'api_key': API_KEY,
            'query': api_query,
            'pageSize': 3 # Traemos solo los 3 mejores resultados para no saturar la pantalla
        }
        
        with st.spinner('Consultando base de datos nutricional externa...'):
            try:
                response = requests.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    foods = data.get('foods', [])
                    
                    if foods:
                        # Mostramos los resultados en tarjetas visuales
                        for food in foods:
                            nombre = food.get('description')
                            calorias = 0
                            
                            # Buscamos las calorías en la lista de nutrientes
                            for nutrient in food.get('foodNutrients', []):
                                if nutrient.get('nutrientName') == 'Energy':
                                    calorias = nutrient.get('value')
                                    break
                            
                            # Mostramos un recuadro verde con el resultado
                            st.success(f"🍏 **{nombre}**: {calorias} kcal (por porción estándar)")
                    else:
                        st.warning("No se encontraron resultados para esa búsqueda.")
                else:
                    st.error("Error al conectar con la API de USDA.")
            except Exception as e:
                st.error(f"Ocurrió un error en la conexión: {e}")
    else:
        st.warning("Por favor, ingresa un alimento antes de buscar.")

# comparacion de cadenas

st.header("Comparacion de Restaurantes")

company_stats = (
    df.groupby("company")
    .agg({
        "calories": "mean"
    })
    .reset_index()
)

fig = px.bar(
    company_stats,
    x="company",
    y="calories",
    color="company",
    title="Promedio de Calorías por Restaurante"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# top 10 caloricos

st.header("Top 10 Productos Mas Caloricos")

top10 = df.nlargest(
    10,
    "calories"
)

fig2 = px.bar(
    top10,
    x="calories",
    y="item",
    color="company",
    orientation="h"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# mas saludables

if "health_score" in df.columns:

    st.header("Top Productos Saludables")

    healthy = (
        df.sort_values(
            "health_score",
            ascending=False
        )
        .head(10)
    )

    fig3 = px.bar(
        healthy,
        x="health_score",
        y="item",
        color="company",
        orientation="h"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )