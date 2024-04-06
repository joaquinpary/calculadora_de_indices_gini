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
            print(f'Error obtaining the gini index data. Status code: {response.status_code}')
            return None
    except requests.exceptions.RequestException as e:
        print(f'HTTP request exception: {e}')
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

float_to_int = ctypes.CDLL('./lib_float_to_int.so')
float_to_int.float_to_int.argtypes = (ctypes.c_float)
float_to_int.float_to_int.restype = ctypes.c_int

def float_to_int(value):
    return float_to_int.float_to_int(value)

for i in range(len(gini)):
    gini[i] = float_to_int(gini[i])

for i in range(len(country)):
    print(f"Country: {country[i]}")
    print(f"Year: {year[i]}") 
    print(f"GINI index: {gini[i]}")  
    print("")
