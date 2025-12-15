from langchain_core.tools import tool
from services.schemas import StatsInput
# Importamos la lógica pura desde el engine
from src.engines.descriptive.central import get_smart_mean, get_smart_median, get_smart_mode

# --- TOOL 1: MEDIA ---
@tool(args_schema=StatsInput)
def calculate_smart_mean(data: list[dict], column: str) -> dict:
    """
    Calcula el promedio aritmético y la volatilidad (desviación estándar) de una columna.
    Útil para entender la tendencia central y la estabilidad de los datos.
    """
    try:
        # Llamamos al motor puro
        return get_smart_mean(data, column)
    except Exception as e:
        return {"error": str(e)}

# --- TOOL 2: MEDIANA ---
@tool(args_schema=StatsInput)
def calculate_smart_median(data: list[dict], column: str) -> dict:
    """
    Calcula la mediana y el rango intercuartil (IQR).
    Útil para ignorar valores atípicos (outliers) en precios o salarios.
    """
    try:
        return get_smart_median(data, column)
    except Exception as e:
        return {"error": str(e)}

# --- TOOL 3: MODA ---
@tool(args_schema=StatsInput)
def calculate_smart_mode(data: list[dict], column: str) -> dict:
    """
    Identifica el valor más frecuente (Moda), su porcentaje de dominancia y si hay empates.
    Útil para encontrar productos más vendidos o categorías más comunes.
    """
    try:
        return get_smart_mode(data, column)
    except Exception as e:
        return {"error": str(e)}