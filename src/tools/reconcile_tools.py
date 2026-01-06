from langchain_core.tools import tool
from services.schemas import ReconcileInput
from engines.reconcile import reconcile_datasets


@tool(args_schema=ReconcileInput)
def analytics_reconcile_datasets(
    data_a: list[dict], 
    data_b: list[dict], 
    key_column_a: str = None,
    key_column_b: str = None,
    key_column: str = "CUFE", 
    mode: str = "missing_in_a"
) -> dict:
    """
    [ANALYTICS] RECONCILIA dos conjuntos de datos para encontrar discrepancias fiscales.
    
    Cruza dos datasets (ej: Facturas SAP vs Documentos DIAN) usando un campo clave común
    para identificar registros faltantes o coincidentes.
    
    - data_a: Primer conjunto de datos (ej: Facturas SAP). Puede ser REF_ID.
    - data_b: Segundo conjunto de datos (ej: Documentos DIAN). Puede ser REF_ID.
    - key_column_a: Nombre del campo clave en data_a (ej: 'U_CUFE'). Opcional.
    - key_column_b: Nombre del campo clave en data_b (ej: 'cufe'). Opcional.
    - key_column: Nombre del campo clave si ambos usan el mismo (ej: 'CUFE'). Default.
    - mode: Tipo de análisis:
        * 'missing_in_a': Muestra registros que existen en B pero NO en A (Default)
        * 'missing_in_b': Muestra registros que existen en A pero NO en B
        * 'intersection': Muestra registros que coinciden en AMBOS lados
    
    Casos de uso:
    - "¿Qué facturas están en DIAN pero no en SAP?" -> mode='missing_in_a'
    - "¿Qué facturas emitimos que no reportamos a DIAN?" -> mode='missing_in_b'
    - "¿Cuáles documentos coinciden perfectamente?" -> mode='intersection'
    
    Retorna:
    - summary: Descripción del resultado
    - match_count: Cantidad de registros encontrados
    - mode_used: El modo que se utilizó
    - data: Lista de registros que cumplen el criterio
    - metadata: Información adicional sobre los datasets
    
    Ejemplo de uso:
    Usuario: "Cruza las facturas de SAP del último mes con los documentos DIAN y 
              dime cuáles me faltan en SAP"
    
    El LLM llamará:
    1. sap_get_invoices(filters="DocDate ge '2024-12-01'") -> Retorna REF_SAP
    2. plclab_get_dian_documents(desde="2024-12-01") -> Retorna REF_DIAN
    3. analytics_reconcile_datasets(
         data_a=REF_SAP,  # El Orchestrator resuelve esto a datos reales
         data_b=REF_DIAN,  # El Orchestrator resuelve esto a datos reales
         key_column_a="U_CUFE",  # Campo en SAP
         key_column_b="cufe",     # Campo en DIAN
         mode="missing_in_a"
       )
    """
    try:
        result = reconcile_datasets(
            data_a=data_a,
            data_b=data_b,
            key_column_a=key_column_a,
            key_column_b=key_column_b,
            key_column=key_column,
            mode=mode
        )
        
        return {
            "status": "success",
            "summary": result["summary"],
            "match_count": result["match_count"],
            "mode_used": result["mode_used"],
            "key_column_a": result["key_column_a"],
            "key_column_b": result["key_column_b"],
            "data": result["data"],
            "metadata": result["metadata"]
        }
        
    except ValueError as ve:
        # User-friendly error handling
        return {
            "status": "error", 
            "error": str(ve),
            "summary": f"Error en la reconciliación: {str(ve)}"
        }
    except Exception as e:
        # Unexpected errors
        return {
            "status": "error", 
            "error": f"Error inesperado: {str(e)}",
            "summary": "Error al procesar la reconciliación de datos"
        }
