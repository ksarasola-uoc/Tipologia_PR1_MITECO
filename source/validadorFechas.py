from datetime import datetime

class ValidadorFechas:
    def validar_formato_fecha(fecha_str: str) -> bool:
        """
        Valida si una cadena tiene el formato de fecha 'dd/mm/yyyy'.

        Parámetros:
            fecha_str (str): Cadena a validar.

        Retorna:
            bool: 
                - True si la cadena cumple el formato y es una fecha válida.
                - False si no cumple el formato o es una fecha inválida.
        """
        try:
            datetime.strptime(fecha_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def validar_fechas(start_date: str, end_date: str) -> bool:
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
    
