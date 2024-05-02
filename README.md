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

### Python
Los datos fueron obtenidos con Python utilizando la libreria `request` y el enlace a la informacion suministrada por [Banco Mundial](https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22) definiendo la siguente funcion:

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

La funcion `get_gini_index()` utiliza la url de la API para obtener los datos en formato JSON mediante un try catch, el status code `200` hace referencia a una accion de request que fue exitosa, por lo tanto si `response.status_code` obtiene un valor diferente a `200`, no devuelve nada.
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

Los estados pueden clasificarse segun su categoria:

|Code range| Category |
|----------|----------|
|2xx|Successful operation|
|3xx|Redirection|
|4xx|Client error|
|5xx|Server error|

Posteriormente se realizo un filtrado de los datos obtenidos, se utilizo `gini_index[1]` dado que `gini_index[0]` posee informacion sobre la API:
```json
{
    "page": 1,
    "pages": 1,
    "per_page": 32500,
    "total": 2660,
    "sourceid": "2",
    "lastupdated": "2024-03-28"
}
```
```python
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
```
### C
El codigo C `lib_float_to_int.c` se compila usando:
```bash
gcc -c -Wall -Werror -fpic lib_float_to_int.c
gcc -shared -o lib_float_to_int.so lib_float_to_int.o float_to_int.o
```
La ultima parte es donde se utiliza la libreria `ctypes` para importar una libreria dinamica de C:
* Linkea la libreria dinamica
```python
lib_float_to_int = ctypes.CDLL('./lib_float_to_int.so')
```
* Setea el tipo de variable de entrada de la funcion `float_to_int`
```python
lib_float_to_int.float_to_int.argtypes = (ctypes.c_float,)
```
* Setea el tipo de variable de salida de la funcion `float_to_int`
```python
lib_float_to_int.float_to_int.restype = ctypes.c_int
```
Se define la funcion `float_to_int(value)`la cual llamara a la funcion homonima en C:
```python
def float_to_int(value):
    return lib_float_to_int.float_to_int(value)

for i in range(len(gini)):
    if gini[i] == None:
        gini[i] = 0
    gini[i] = float(gini[i])
    gini[i] = float_to_int(gini[i])

for i in range(len(country)):
    print(f"Country: {country[i]}")
    print(f"Year: {year[i]}") 
    print(f"GINI index: {gini[i]}")  
    print("")
```

El programa en C llama a rutina de ensamblador pasandole el numero de tipo `float` y obteniendolo en `int`:
```C
extern int asm_main(float);

int float_to_int(float num) {
    int int_num = 0;
    int_num = asm_main(num);
    return int_num;
}
```
### Assembler 64 bits
Se utilizo Assembler 64 bits para evitar problemas con el uso de `Python 32 bits` o librerias como `msl.loadlib`. En ASM32 se puede obtener el parametro que se paso por argumento en el codigo C a traves del `stack` pero en ASM64 esto no se puede hacer, para ello existe los registros `xmm (registros de datos de punto flotante SIMD)`. En nuestro caso, el argumento se guardo en el registro `xmm0`.

Posteriormente la instruccion `cvttss2si` transforma el valor `float` en uno de tipo `int` con signo y lo guarda en el registro `rax`, para finalmente sumarle +1:
```assembly
section .data
    int_num dd 0

global asm_main
section .text

asm_main:
    push rbp
    mov rbp, rsp
    cvttss2si rax, xmm0
    inc rax
    mov rsp, rbp
    pop rbp
    ret
```
La rutina de ensamblador se compilo:
```bash
nasm -f elf64 float_to_int.asm -g
```
### Depuracion
```bash
gcc -m64 -o main float_to_int.o main.c -g
```
Una vez obtenido el ejecutable, se ejecuta `gdb` para debugear el programa:
```bash
gdb main
(gdb) break lib_float_to_int.c:7
(gdb) run
```
Se ingresa el numero de tipo `float` a convertir, por ejemplo `13.43`:

![Imagen1](/img/img1.png)

Como se habia mencionado anteriormente, en ASM64 los valores de tipo `float` y `double` no se pueden ver en el `stack`, pero se pueden visualizar usando `info all-registers` donde se puede ver el registro `ymm0` que representa el mismo registro fisico que `xmm0`, pero estan en diferentes modos de extension.

![Imagen2](/img/img2.png)
![Imagen3](/img/img3.png)

Al seguir ejecuntado el codigo ASM con `stepi` y llegar a la direccion `0x0000555555555180` que es la direccion donde se encuentra la instruccion `ret`:

![Imagen4](/img/img4.png)

Se puede ver que el registro `rax` tiene el valor `14`, que seria el `float` transformado a entero y luego sumandole +1

![Imagen5](/img/img5.png)
## Anexo
* https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22
* https://realpython.com/api-integration-in-python/
* https://es.wikipedia.org/wiki/Coeficiente_de_Gini#:~:text=El%20coeficiente%20de%20Gini%20es,cualquier%20forma%20de%20distribuci%C3%B3n%20desigual.
* https://www.redhat.com/es/topics/api/what-is-a-rest-api
* https://stackoverflow.com/questions/14884126/build-so-file-from-c-file-using-gcc-command-line
* https://stackoverflow.com/questions/55773868/returning-a-value-in-x86-assembly-language
