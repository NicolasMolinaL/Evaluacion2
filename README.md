# Evaluacion2 - Software de Geolocalización con Graphhopper
Evaluacion N°2 de Maximiliano Marín y Nicolás Molina

Este repositorio contiene una aplicación desarrollada en Python que interactúa con la API REST de **Graphhopper Directions** para la planificación de rutas y geolocalización.

## Descripción del Proyecto
El sistema permite a los usuarios:
- Seleccionar perfiles de transporte (`auto`, `bicicleta`, `pie`).
- Ingresar puntos de origen y destino.
- Obtener las indicaciones paso a paso (narrativa del viaje) traducidas al español.
- Visualizar distancias y tiempos de viaje con precisión de dos decimales.
- Salir del programa de manera sencilla ingresando `s` o `salir`.

## Requisitos
- Python 3.x
- Librería `requests` (instalable con `pip install requests`)
- Conexión a Internet y un API Key válido de Graphhopper.

## Instrucciones de Ejecución
1. Clonar el repositorio(Ingresar una linea a la vez):
cd ~
git clone https://github.com/NicolasMolinaL/Evaluacion2
cd Evaluacion2
ls -la

2. Ejecutar el script:
python3

3. Ingresar unos de los transporte disponibles (car, bike o foot)

4. ingresar una ubicacion de origen:
ejemplo: santiago, chile

5. ingresar una ubicacion de destino
ejemplo: valparaiso, chile

6. para salir ingresar "s" o "salir"
