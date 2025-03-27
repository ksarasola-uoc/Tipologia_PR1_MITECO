# Tipologia_PR1_MITECO
## Proyecto 
Este es un ejercicio de escrapping sobre la web de MITECO que ofrece datos de información Hidrológica. El objetivo es la extracción de datos sobre las reservas hidrícas. Los datos son semanales y corresponden a embalses peninsulares con capacidad mayor a 5 hm3.

Se puede obtener más información sobre los datos en la web https://www.miteco.gob.es/es/agua/temas/evaluacion-de-los-recursos-hidricos/boletin-hidrologico.html


---

## Requisitos Previos

Antes de usar este proyecto, asegúrate de tener instaladas las siguientes dependencias:

- Python 3.8+
- Bibliotecas requeridas (instalación automática con `requirements.txt`):
  ```bash
  pip install -r requirements.txt

## Estructura del Proyecto

```
/source
    mitecoEmbalsesScraper.py # Módulo para la conexión y obtención de datos de la web del MITECO
    validadorFechas.py      # Módulo para la validación de fechas
    main.py                 # Módulo principal para la interacción
    README.md               # Documentación del proyecto
/data                       #Carpeta donde se descargan los datos en formato csv

```
## Uso

### **1. Configuración inicial**

1. Instala las dependencias:

   ```
   pip install -r requirements.txt 
   ```

### **2. Puesta en marcha**

**Información de la aplicación**

```
main.py --help
```
La aplicación permite 4 parámetros diferentes de los cuales 2 son obligatorios y han de ser en formato fecha. 

Se realiza la extracción de datos entre las dos fechas que se proporcionan como argumento
```
Scraper de embalses del MITECO

positional arguments:
  start_date       Fecha de inicio en formato DD/MM/YYYY
  end_date         Fecha de fin en formato DD/MM/YYYY

options:
  -h, --help       show this help message and exit
  --save SAVE      S guardar ficheros separados o A para acumulado en un fichero
  --output OUTPUT  Directorio de salida para los archivos CSV

```


**Forma de guardar los ficheros**

Los ficheros pueden guardarse de manera separada por semanas o conjunta (Acumulada) en un solo fichero todos los datos.

## Licencia

Este proyecto está licenciado bajo la **Licencia MIT**. Consulta el archivo opensource.org/licenses/MIT para más detalles.



## Autores

Creado por **Kepa Sarasola Bengoetxea** y **Tamara Perez Perez**.