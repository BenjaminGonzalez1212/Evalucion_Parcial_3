# Arquitectura del Sistema

El proyecto sigue una arquitectura de datos de tres capas:

## Capa de Ingesta

-Dataset CSV FastFoodNutritionMenuV3.csv
-USDA FoodData Central API

## Capa de Procesamiento

-ETL desarrollado en Python
-Limpieza y transformación de datos
-Cálculo de métricas nutricionales

## Capa de Persistencia

-PostgreSQL desplegado en AWS EC2

## Capa de Visualización

-Dashboard Ejecutivo (Streamlit)
-Dashboard Técnico (Streamlit)

## Flujo General

CSV + API → ETL → PostgreSQL → Dashboards
