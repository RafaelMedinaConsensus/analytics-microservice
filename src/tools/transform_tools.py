from langchain_core.tools import tool
from services.schemas import GroupingInput
from engines.transform.grouping import group_and_aggregate
from services.schemas import FilterInput, TopNInput
from engines.transform.filtering import apply_filter, get_top_n_records

@tool(args_schema=GroupingInput)
def aggregate_data(data: list[dict], group_by: str, target_column: str, operation: str = "sum") -> dict:
    """
    Agrupa datos brutos basándose en una columna y realiza una operación matemática.
    Útil para: "Total de ventas por cliente", "Cantidad de facturas por fecha", etc.
    """
    try:
        result = group_and_aggregate(data, group_by, target_column, operation)
        return {
            "status": "success", 
            "data": result,
            "summary": f"Datos agrupados por '{group_by}' usando '{operation}'."
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}
    
@tool(args_schema=FilterInput)
def filter_data(data: list[dict], column: str, operator: str, value: float) -> dict:
    """Filtra una lista de datos (ej: ventas > 1000)."""
    try:
        result = apply_filter(data, column, operator, value)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@tool(args_schema=TopNInput)
def get_top_n(data: list[dict], column: str, n: int = 5, ascending: bool = False) -> dict:
    """Obtiene los N registros más altos o bajos."""
    try:
        result = get_top_n_records(data, column, n, ascending)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}