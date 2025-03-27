import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class MitecoEmbalsesScraper:
    """
    Clase para extraer datos hidrológicos desde el servicio que ofrece el MITECO.
    Descarga información sobre embalses, agrupado por demarcaciones hidrográficas
    y guarda los datos en archivos CSV semanales.
    """

    def __init__(self, start_date, end_date, save="S", output_dir="data"):
        self.url = "https://sede.miteco.gob.es/BoleHWeb/bolehSRV"
        self.output_dir = output_dir
        self.start_date = datetime.strptime(start_date, "%d/%m/%Y")
        self.end_date = datetime.strptime(end_date, "%d/%m/%Y")
        self.save = save
        self.datos_acumulados = []
        self.demarcaciones = {
            "Cantabrico Oriental": "17",
            "Cantabrico Occidental": "12", 
            "Mino-Sil": "1",
            "Galicia Costa": "14",
            "Cuencas Internas del País Vasco": "11",
            "Duero": "2",
            "Tajo": "3",
            "Guadiana": "4",
            "Tinto, Odiel y Piedras": "16",
            "Guadalete-Barbate": "15",
            "Guadalquivir": "5",
            "Cuenca Mediterránea Andaluza": "6",
            "Segura": "7",
            "Júcar": "8",
            "Ebro": "9",
            "Cuencas Internas de Cataluña": "10"   
        }


    def get_headers(self):
        """
        Devuelve un diccionario con los headers HTTP necesarios para simular una petición desde un navegador.

        Retorna:
            dict: Un diccionario con los siguientes headers:
                - "User-Agent": Identifica el navegador y sistema operativo (simula Chrome en Windows 10).
                - "Accept-Language": Indica los idiomas preferidos por el cliente (español de España).
                - "Accept-Encoding": Especifica los métodos de compresión aceptados (gzip, deflate, br).
                - "Accept": Indica los tipos de contenido que el cliente puede procesar (HTML, XML, imágenes, etc.).
                - "Connection": Controla si la conexión se mantiene abierta después de la solicitud (keep-alive).
        """
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept-Language": "es-ES,es;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Connection": "keep-alive"
        }


    def obtener_ultima_semana_con_datos(self):
        """
        Obtiene la última semana con datos disponibles desde el servicio del MITECO.

        Retorna:
            tuple or bool: 
                - Si encuentra datos, retorna una tupla con (número_semana, año).
                - Si no encuentra datos, retorna False.
        """
        data = {"date": self.end_date.strftime("%d/%m/%Y")}
        response = requests.post(self.url, data=data, headers=self.get_headers(), verify=False)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            tabla = next((table for table in soup.find_all('table') if 'NÚMERO' in table.get_text()), None)

            if tabla:
                celda = soup.find("td", class_="tdblanco", align="center")
                if celda:
                    texto = celda.get_text(separator=" ").strip()
                    match = re.search(r"NÚMERO\s+(\d+)\s+AÑO\s+(\d{4})", texto)
                    if match:
                        return int(match.group(1)), int(match.group(2))

                return True
        return False  

    def ajustar_fecha_fin(self):
        """
        Ajusta la fecha de fin si es posterior a la última semana con datos disponibles.
        
        Utiliza los datos obtenidos de `obtener_ultima_semana_con_datos` para limitar
        la fecha de fin del scraping a la última semana con datos válidos.
        """
        ultima_semana, ultimo_ano = self.obtener_ultima_semana_con_datos()

        # Convertir la última semana con datos en una fecha real
        fecha_ultima_semana = datetime.strptime(f"{ultimo_ano}-{ultima_semana}-1", "%Y-%W-%w")
        if self.end_date > fecha_ultima_semana:
            print(f"⚠️ Advertencia: La fecha de fin {self.end_date.strftime('%d/%m/%Y')} es posterior a la última semana con datos ({fecha_ultima_semana.strftime('%d/%m/%Y')}). Se ajustará automáticamente.")
            self.end_date = fecha_ultima_semana


    def obtener_datos_semanales(self):
        """
        Ejecuta el proceso de scraping para cada semana en el rango de fechas configurado.
        
        Itera semana a semana desde la fecha de inicio hasta la fecha de fin (ajustada),
        generando un archivo CSV por semana con los datos de los embalses.
        """
        fecha_actual = self.start_date
        while fecha_actual <= self.end_date:
            fecha_str = fecha_actual.strftime("%d/%m/%Y")
            semana = fecha_actual.isocalendar()[1]  # El índice 1 es el número de semana
            archivo = f"../{self.output_dir}/embalses_{fecha_actual.year}_{semana}.csv"
            self.scrapear_boletin(fecha_str, archivo, fecha_actual.year, semana)
            fecha_actual += timedelta(weeks=1)

    def scrapear_boletin(self, fecha, archivo, anio, semana):
        """
        Procesa el boletín hidrológico de una fecha específica.

        Parámetros:
            fecha (str): Fecha en formato 'dd/mm/yyyy' a consultar.
            archivo (str): Ruta del archivo CSV donde se guardarán los datos.
            anio (int): Año actual del proceso de scraping.
            semana (int): Número de semana actual del proceso de scraping.

        Efectos secundarios:
            - Imprime mensajes de progreso en consola.
            - Llama a `guardar_o_acumular` para almacenar los datos.
        """
        datos = []
        for clave, valor in self.demarcaciones.items():
            response = self.preparar_request(fecha, clave, valor)
            
            if response.status_code == 200:
                self.procesar_respuesta(response.text, datos, clave, anio, semana)
                print(f"Procesando datos de {clave}: response:{response.status_code}, año:{anio}, semana:{semana}")
            else:
                print(f"Error al obtener datos de {clave}: {response.status_code}")
        
        self.guardar_o_acumular(datos, archivo)

    def guardar_o_acumular(self,datos,archivo):
        """
        Decide si guardar los datos en un archivo CSV o acumularlos en memoria.

        Parámetros:
            datos (list): Lista de diccionarios con datos de embalses.
            archivo (str): Ruta del archivo CSV para guardar (si save='S').
        """
        if datos:
            self.datos_acumulados.extend(datos)
            if self.save == "S":
                df = pd.DataFrame(datos)
                df.to_csv(archivo, index=False, encoding='utf-8')
                print(f"✅ Datos guardados en '{archivo}'")
            else:
                print(f"⏭️ Datos acumulados al fichero final")
        else:
            print("❌ No se encontraron datos")

    def guardar_datos_acumulados(self):
        """
        Guarda todos los datos acumulados en un único archivo CSV.

        Solo se ejecuta si el parámetro `save` fue configurado como 'A' (acumular).
        El archivo se guarda en `output_dir` con el nombre 'embalses_acumulado.csv'.
        """
        archivo = f"../{self.output_dir}/embalses_acumulado.csv"
        if self.save == "A":
            df = pd.DataFrame(self.datos_acumulados)
            df.to_csv(archivo, index=False, encoding='utf-8')
            print(f"✅ Datos guardados en '{archivo}'")     

    def preparar_request(self, fecha, clave, valor):
        """
        Prepara y envía una petición POST al servicio del MITECO.

        Parámetros:
            fecha (str): Fecha en formato 'dd/mm/yyyy'.
            clave (str): Nombre de la demarcación hidrográfica.
            valor (str): Código numérico de la demarcación.

        Retorna:
            Response: Objeto Response de la librería requests.
        """
        btn = f"btnMod_Reserva_Hidraulica_Datos_{valor}_X17"
        valorBtn = f"btnMod_Reserva_Hidraulica_Datos_{valor}"
        data = {"xVal": 17, "fechaCalendario": fecha, btn: valorBtn}
        response = requests.post(self.url, data=data, headers=self.get_headers(), verify=False)

        return response


    def procesar_respuesta(self, html, datos, clave, anio, semana):
        """
        Procesa el HTML de respuesta para extraer datos de embalses.

        Parámetros:
            html (str): Contenido HTML de la respuesta.
            datos (list): Lista donde se acumularán los datos extraídos.
            clave (str): Nombre de la demarcación hidrográfica.
            anio (int): Año actual del proceso de scraping.
            semana (int): Número de semana actual del proceso de scraping.
        """
        soup = BeautifulSoup(html, "html.parser")
        tabla = next((table for table in soup.find_all('table') if 'Embalsada (hm' in table.get_text()), None)
        
        if tabla:
            filas = tabla.find_all('tr')[2:]  # Omitimos cabeceras de 2 lineas
            for fila in filas:
                celdas = fila.find_all('td')
                if len(celdas) >= 6:
                    embalse = celdas[0].text.strip().replace("\n", "").replace("\r", "").replace("*\t\t\t", "*")
                    datos.append({
                        "Demarcación": clave,
                        "Embalse": embalse,
                        "Río": celdas[1].text.strip(),
                        "Capacidad": celdas[2].text.strip(),
                        "Actual": celdas[3].text.strip(),
                        "Diferencia s/anterior": celdas[4].text.strip(),
                        "Energía disponible": celdas[5].text.strip(),
                        "Capacidad energética": celdas[6].text.strip(),
                        "Año": anio,
                        "Semana": semana
                    })
        else:
            print(f"No se encontró la tabla para {clave} en la semana {semana}")

    '''
    def guardar_datos(self, datos, archivo):
        if datos:
            df = pd.DataFrame(datos)
            df.to_csv(archivo, index=False, encoding='utf-8')
            print(f"✅ Datos guardados en '{archivo}'")
        else:
            print("❌ No se encontraron datos.")
    '''