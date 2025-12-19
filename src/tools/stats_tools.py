from langchain_core.tools import tool
from services.schemas import StatsInput
# Importamos la lógica pura desde el engine
from src.engines.descriptive.central import get_smart_mean, get_smart_median, get_smart_mode

# --- TOOL 1: MEDIA ---
@tool(args_schema=StatsInput)
def analytics_stat_mean(data: list[dict], column: str) -> dict:
    """
    [ANALYTICS] Calcula PROMEDIO aritmetico y volatilidad (desviacion estandar).
    - data: Lista de diccionarios con los datos (puede ser REF_ID)
    - column: Nombre de la columna numerica a analizar
    Retorna: mean, std_dev, count
    """
    try:
        # Llamamos al motor puro
        return get_smart_mean(data, column)
    except Exception as e:
        return {"error": str(e)}

# --- TOOL 2: MEDIANA ---
@tool(args_schema=StatsInput)
def analytics_stat_median(data: list[dict], column: str) -> dict:
    """
    [ANALYTICS] Calcula MEDIANA y rango intercuartil (IQR).
    - data: Lista de diccionarios con los datos (puede ser REF_ID)
    - column: Nombre de la columna numerica a analizar
    Retorna: median, q1, q3, iqr (ignora outliers)
    """
    try:
        return get_smart_median(data, column)
    except Exception as e:
        return {"error": str(e)}

# --- TOOL 3: MODA ---
@tool(args_schema=StatsInput)
def analytics_stat_mode(data: list[dict], column: str) -> dict:
    """
    [ANALYTICS] Identifica MODA (valor mas frecuente) y dominancia.
    - data: Lista de diccionarios con los datos (puede ser REF_ID)
    - column: Nombre de la columna a analizar
    Retorna: mode, frequency, percentage (para productos mas vendidos, categorias comunes)
    """
    try:
        return get_smart_mode(data, column)
    except Exception as e:
        return {"error": str(e)}