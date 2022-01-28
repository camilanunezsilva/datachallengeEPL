# ETL English Premier League

El presente proyecto ETL, escrito en Python, tiene por objetivo generar 3 archivos de salida para responder a las 3 estadisticas planteadas en este desafio.

## Descripción Algoritmo

### Datos de entrada

Se consideran los archivos JSON contenidos en la carpeta input/dataset. Son 10 archivos, donde cada uno contempla la información asociada a cada temporada y encuentros del
campeonato del English Premier League, desde los años 2009 y 2019.

### Proceso

- Se leen los 10 archivos de entrada y los datos resultantes se dejan en un solo objeto.
- Se homologan los formatos y tipos de los datos. (En el caso de las fechas, estas venian con formato diferente desde los archivos).
- Se les da estructura a los datos, creando las entidades: partido y equipos. Esto para posteriormente procesar la data de forma más natural.
- Finalmente, se obtiene la data para responder a cada una de las estadisticas solicitadas:

    - Obtener data de tabla de posiciones.
    - Obtener data de los equipos con mejor relacion de disparos al arco, por temporada.
    - Obtener data de los equipos más goleados, por temporada.

### Datos de salida

Se generan 3 archivos CSV de salida en la carpeta output:

- tabla_posiciones.csv
- equipo_mejor_relacion_disparos_arco.csv
- equipo_mas_goleado.csv

## Comenzando 🚀

Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas.

### Pre-requisitos 📋

_Que software necesitas:

- Instalar python: Yo estoy utilizando la versión 3.9.6 y la descargué del sitio oficial https://www.python.org/

- Instalar Entorno de programación para compilar código python: Yo utilice Visual Studio Code 1.63 y lo descargué del sitio oficial https://code.visualstudio.com/

- Instalar libreria pandas: Yo utilicé la versión 1.3.2.

- Instalar jupyter notebook, para facilitar las pruebas del código y abrir el archivo oficial_v3.ipynb (está todo el código junto)

## Ejecutando el código ⚙️

Desde el terminal, ubicado en la raiz del proyecto, digitar:

```
python src/main.py
```

## Despliegue 📦

Especificado en carpeta deployment

