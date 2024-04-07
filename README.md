# Trabajo Practico N°2 Calculadora de Indice GINI

### Integrantes:

* Santiago Colque
* Joaquin Pary
* Jorge Angeloff

## Resumen
El objetivo del trabajo es diseñar e implementar una interfaz que muestre el indice GINI. La capa superior recuperara la informacion del banco mundial. Se utilizara API Rest con Python. Los datos de consulta obtenidos seran entregados a un programa en C que ejecutara rutinas en ensamblador para que hagan los calculos de conversion de float a enteros y devuelva el indice de un pais como Argentina u otro sumando (+1). Luego el programa en Python mostrara los datos obtenidos.   

### Que es una API REST?
Una API REST, es una interfaz de programacion de aplicaciones (API o API web) que se ajusta a los limites de la arquitectura REST y permite la interaccion con los servicion web de RESTful.
A su vez REST no es un protocolo ni un estandar, sino mas bien un conjunto de limites de arquitectura.

### Que es el indice GINI?
El indice o coeficiente de GINI es una medida que normalmente se utiliza para medir la desigualdad en los ingresos, dentro de un pais.
Aunque el coeficiente de GINI se ultiliza sobre todo para medir la degualdad en los ingresos, tambien puede utilizarse para medir la desigualdad en la riqueza. Este uso requiere que nadie disponga de una riqueza neta negativa.
## Desarrollo

Para obtener los datos del Banco Mundial se utilizo Python usando la libreria `request` y el enlace a la informacion suministrada por [Banco Mundial](https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22) definiendo la siguente funcion:

```python
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
```

La funcion `get_gini_index()` utiliza la url de la API para intentar obtener los datos en formato JSON utilizando un try catch, el status code `200` hace referencia a una accion de request que fue exitosa, por lo tanto si `response.status_code` obtiene un valor diferente a `200`, no devuelve nada.
La siguente lista muestra los codigos de estados mas comunes:
|Code|Meaning              |Description         |
|--- |---------------------|--------------------|
|200 |`OK`    | The requested action was successful|
|201 |`Created`| A new resource was created|
|202 |`Accepted`| The request was received, but no modification has ben made yet|
|204 |`No Content`| The request was successful, but the response ha nos content|
|400 |`Bad Request`| The request was malformed|
|401 |`Unautorize`| The client is not authorized to perform the requested action|
|404 |`Not found`| The requested resource was not found|
|415 |`Unsupported Media Type`| The request data format is not supported by the server|
|422 |`Unprocessable Entity`| The request data was properly formatted but contained invalid or missing data|
|500 |`Internal Server Error`| The server threw and error when processing the request|

Estos tienen una categoria que es la siguente:

|Code range| Category |
|----------|----------|
|2xx|Successful operation|
|3xx|Redirection|
|4xx|Client error|
|5xx|Server error|