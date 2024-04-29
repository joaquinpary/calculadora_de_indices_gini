# Link = https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22

import requests
import ctypes
import matplotlib.pyplot as plt
import numpy as np

def float_to_int(value):
    return lib_float_to_int.float_to_int(value)

def get_gini_index():
    try:
        api_url = f"https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2023&per_page=32500&page=1"
    
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.status_code, response.json()
        else:
            print(f'Error obtaining the gini index data. Status code: {response.status_code}')
            return response.status_code, None
    except requests.exceptions.RequestException as e:
        print(f'HTTP request exception: {e}')
        return response.status_code, None
    
lib_float_to_int = ctypes.CDLL('./lib_float_to_int.so')
lib_float_to_int.float_to_int.argtypes = (ctypes.c_float,)
lib_float_to_int.float_to_int.restype = ctypes.c_int


status_code, gini_index = get_gini_index()

country_to_find = input("Enter country: ")
country_to_find = country_to_find.capitalize()

country = []
year = []
gini = []

for i in gini_index[1]:
    if i['country']['value'] == country_to_find:
        country.append(i['country']['value'])
        year.append(i['date'])
        gini.append(i['value'])

y_plt_min = min(y for y in gini if y is not None) - 2
y_plt_max = max(y for y in gini if y is not None) + 4

for i in range(len(gini)):
    if gini[i] == None:
        gini[i] = int(0)
        continue
    gini[i] = float(gini[i])
    gini[i] = float_to_int(gini[i])

for i in range(len(country)):
    print(f"Country: {country[i]}")
    print(f"Year: {year[i]}") 
    print(f"GINI index: {gini[i]}")  
    print("")

year = year[::-1]
gini = gini[::-1]

plt.bar(year, gini)
plt.ylim(y_plt_min, y_plt_max)
plt.xticks(year[::2])
plt.xlabel('Year')
plt.ylabel('GINI Index')
plt.title(f'GINI Index for {country_to_find}')
plt.show()
