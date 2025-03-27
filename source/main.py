import argparse
from datetime import datetime
from mitecoEmbalsesScraper import MitecoEmbalsesScraper
from validadorFechas import ValidadorFechas  # Importamos la nueva clase

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    parser = argparse.ArgumentParser(description="Scraper de embalses del MITECO")
    parser.add_argument("start_date", type=str, help="Fecha de inicio en formato DD/MM/YYYY")
    parser.add_argument("end_date", type=str, help="Fecha de fin en formato DD/MM/YYYY")
    parser.add_argument("--save", type=str, default="S", help="S guardar ficheros separados o A para acumulado en un fichero")
    parser.add_argument("--output", type=str, default="data", help="Directorio de salida para los archivos CSV")
    
    args = parser.parse_args()

    if not ValidadorFechas.validar_formato_fecha(args.start_date) or not ValidadorFechas.validar_formato_fecha(args.end_date):
        print("❌ Error: Las fechas deben tener el formato 'dd/mm/YYYY'.")
        return 1

    if not ValidadorFechas.validar_fechas(args.start_date, args.end_date):
        print("❌ La aplicación no permite consultar datos con fechas errorenas.")
        return 1
    
    scraper = MitecoEmbalsesScraper(args.start_date, args.end_date, args.save, args.output)
    
    scraper.ajustar_fecha_fin()
    scraper.obtener_datos_semanales()
    scraper.guardar_datos_acumulados()

if __name__ == "__main__":
    main()
