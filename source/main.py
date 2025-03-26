import argparse
from datetime import datetime
from mitecoEmbalsesScraper import MitecoEmbalsesScraper

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def validar_fechas(start_date, end_date):
    """
    Verifica que la fecha de fin no sea mayor que la fecha actual y que sea posterior a la fecha de inicio.

    Parámetros:
    - start_date (str): Fecha de inicio en formato 'dd/mm/YYYY'.
    - end_date (str): Fecha de fin en formato 'dd/mm/YYYY'.

    Retorna:
    - bool: True si las fechas son válidas, False en caso contrario.
    """
    fecha_inicio = datetime.strptime(start_date, "%d/%m/%Y")
    fecha_fin = datetime.strptime(end_date, "%d/%m/%Y")
    fecha_actual = datetime.today()

    if fecha_fin < fecha_inicio:
        print("❌ Error: La fecha de fin no puede ser anterior a la fecha de inicio.")
        return False
    if fecha_fin > fecha_actual:
        print("❌ Error: La fecha de fin no puede ser mayor que la fecha actual.")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description="Scraper de embalses del MITECO")
    parser.add_argument("start_date", type=str, help="Fecha de inicio en formato DD/MM/YYYY")
    parser.add_argument("end_date", type=str, help="Fecha de fin en formato DD/MM/YYYY")
    parser.add_argument("--output", type=str, default="data", help="Directorio de salida para los archivos CSV")
    
    args = parser.parse_args()

    if not validar_fechas(args.start_date, args.end_date):
        print("❌ La aplicación no permite consultar datos con fechas errorenas.")
        return 1
    
    scraper = MitecoEmbalsesScraper(args.start_date, args.end_date, args.output)
    
    scraper.ajustar_fecha_fin()
    scraper.obtener_datos_semanales()

if __name__ == "__main__":
    main()
