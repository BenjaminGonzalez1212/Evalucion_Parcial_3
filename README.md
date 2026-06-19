# Evalucion_Parcial_3
Evalucion_Parcial_3
Este proyecto es una solución integral de análisis de datos (End-to-End) diseñada para comparar el valor nutricional de las principales cadenas de comida rápida, complementada con datos en tiempo real de alimentos generales.

## Arquitectura del proyecto
El proyecto integra múltiples fuentes de datos mediante un pipeline ETL automatizado y despliega la información en dashboards interactivos diferenciados por audiencia.

* **Fuentes de Datos:**
    * Archivos estáticos (CSV) con el menú nutricional de cadenas de comida rápida.
    * API REST: Integración con la base de datos USDA FoodData Central del Gobierno de EE. UU. para buscar alimentos naturales o caseros.
* Almacenamiento: Base de datos relacional (PostgreSQL).
* Visualización: Aplicaciones web interactivas desarrolladas con Streamlit y Plotly.
* Despliegue: Contenedores Docker para garantizar la reproducibilidad del entorno.

## 📂 Estructura del Proyecto

/
├── api/                  # Scripts de extracción de la API de USDA
├── dashboards/           # Interfaces gráficas
│   ├── Pages/
│   │   ├── ejecutivo.py  # Dashboard de negocio y calculadora
│   │   └── tecnico.py    # Dashboard de calidad de datos y estadística
├── data/                 # Archivos CSV originales
├── docker/               # Dockerfile y docker-compose.yml
├── etl                   # Pipeline ETL automatizado  
├── .gitignore            # Exclusión de archivos sensibles y caché
└── README.md             # Esta documentación

## Dashboards
El sistema cuenta con dos vistas principales para diferentes audiencias. Para ejecutarlos, utiliza los siguientes comandos en la terminal:

Dashboard Ejecutivo (Visión de Negocio):
Calculadora interactiva de calorías e integración con API.

python -m streamlit run dashboards/Pages/ejecutivo.py

Dashboard Técnico (Calidad de Datos):
Análisis de nulos, distribución y correlación de variables.

python -m streamlit run dashboards/Pages/tecnico.py

## Equipo de desarrollo
Benjamin Gonzales
Cristopher Richasse