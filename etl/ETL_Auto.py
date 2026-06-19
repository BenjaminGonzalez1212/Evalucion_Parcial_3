import pandas as pd
from sqlalchemy import create_engine

# configuración

DB_HOST = "100.59.201.22"
DB_PORT = "5432"
DB_NAME = "calorie_db"
DB_USER = "nutrition_user"
DB_PASSWORD = "1234"

# leer CSV

df = pd.read_csv(r"C:\Users\A\Documents\GitHub\Evalucion_Parcial_3\data\transformados\fastfood_clean.csv")

print("Filas:", len(df))
print("Columnas:", len(df.columns))

# normalizar nombres

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)

print(df.columns)

# conexion PostgreSQL

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# carga

df.to_sql(
    "nutrition_fastfood",
    engine,
    if_exists="replace",
    index=False
)

print("Tabla creada correctamente")