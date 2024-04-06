# Link = https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22

import requests
import ctypes

def get_gini_index():
    try:
        api_url = f"https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2023&per_page=32500&page=1"
    
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error al obtener informacion del indice gini. Código de estado: {response.status_code}')
            return None
    except requests.exceptions.RequestException as e:
        print(f'Error de solicitud HTTP: {e}')
        return None


gini_index = get_gini_index()

country_to_find = input("Enter country: ")
country = []
year = []
gini = []

for i in gini_index[1]:
    if i['country']['value'] == country_to_find:
        country.append(i['country']['value'])
        year.append(i['date'])
        gini.append(i['value'])
    # print(f"Pais: {i['country']['value']}")
    # print(f"Año: {i['date']}") 
    # print(f"Indice Gini: {i['value']}")  
    # print("")


for i in range(len(country)):
    print(f"Pais: {country[i]}")
    print(f"Año: {year[i]}") 
    print(f"Indice Gini: {gini[i]}")  
    print("")

    