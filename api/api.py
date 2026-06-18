import requests
from dotenv import load_dotenv
import os

# Configuración inicial
load_dotenv()

API_KEY = os.getenv('USDA_API_KEY')
BASE_URL = 'https://api.nal.usda.gov/fdc/v1/foods/search'

# Parámetros de la consulta
query_params = {
    'api_key': API_KEY,
    'query': 'banana',   
    'pageSize': 2        
}

# Llamada a la API (Petición GET)
response = requests.get(BASE_URL, params=query_params)

if response.status_code == 200:
    data = response.json() # Convertimos la respuesta a un diccionario de Python
    
    # Extrayendo los datos que nos importan
    for food in data.get('foods', []):
        nombre = food.get('description')
        fdc_id = food.get('fdcId')
        
        print(f"Alimento: {nombre} (ID: {fdc_id})")
        
        # Buscamos las calorías en la lista de nutrientes
        for nutrient in food.get('foodNutrients', []):
            if nutrient.get('nutrientName') == 'Energy': # 'Energy' suele ser Kcal
                calorias = nutrient.get('value')
                unidad = nutrient.get('unitName')
                print(f" -> Calorías: {calorias} {unidad}")
                break
        print("-" * 30)

else:
    print(f"Error en la API. Código de estado: {response.status_code}")
    print(response.text)