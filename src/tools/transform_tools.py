from langchain_core.tools import tool
from services.schemas import GroupingInput
from engines.transform.grouping import group_and_aggregate
from services.schemas import FilterInput, TopNInput
from engines.transform.filtering import apply_filter
from engines.transform.top_n_records import get_top_n_records

@tool(args_schema=GroupingInput)
def analytics_transform_aggregate(data: list[dict], group_by: str, target_column: str, operation: str = "sum") -> dict:
    """
    [ANALYTICS] AGRUPA datos y aplica operacion matematica.
    - data: Lista de diccionarios (puede ser REF_ID)
    - group_by: Columna para agrupar (ej: CardName, DocDate)
    - target_column: Columna numerica a operar (ej: DocTotal)
    - operation: sum, avg, count, min, max
    Ejemplo: "Total ventas por cliente" -> group_by=CardName, target=DocTotal, op=sum
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
def analytics_transform_filter(data: list[dict], column: str, operator: str, value: float) -> dict:
    """
    [ANALYTICS] FILTRA datos por condicion numerica.
    - data: Lista de diccionarios (puede ser REF_ID)
    - column: Columna a filtrar
    - operator: gt, lt, gte, lte, eq, ne
    - value: Valor de comparacion
    Ejemplo: "Ventas mayores a 1000" -> column=DocTotal, operator=gt, value=1000
    """
    try:
        result = apply_filter(data, column, operator, value)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@tool(args_schema=TopNInput)
def analytics_transform_top_n(data: list[dict], column: str, n: int = 5, ascending: bool = False) -> dict:
    """
    [ANALYTICS] Obtiene TOP N registros (mayores o menores).
    - data: Lista de diccionarios (puede ser REF_ID)
    - column: Columna para ordenar
    - n: Cantidad de registros (default 5)
    - ascending: False=mayores primero, True=menores primero
    Ejemplo: "Top 5 clientes por ventas" -> column=DocTotal, n=5, ascending=False
    """
    try:
        result = get_top_n_records(data, column, n, ascending)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}