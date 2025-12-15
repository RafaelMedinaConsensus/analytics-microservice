import pandas as pd
from typing import List, Dict, Any

def group_and_aggregate(
    data: List[Dict[str, Any]], 
    group_by_col: str, 
    agg_col: str, 
    operation: str = "sum"
) -> List[Dict[str, Any]]:
    """
    Agrupa datos repetidos y aplica una operación matemática.
    Ej: Agrupar por 'Cliente' y sumar 'Ventas'.
    """
    df = pd.DataFrame(data)

    # Validaciones
    if df.empty: raise ValueError("Dataset vacío.")
    if group_by_col not in df.columns: raise ValueError(f"Columna '{group_by_col}' no existe.")
    if agg_col not in df.columns: raise ValueError(f"Columna '{agg_col}' no existe.")

    # Limpieza de nulos
    df = df.dropna(subset=[group_by_col, agg_col])
    
    # Asegurar que la columna a operar sea numérica
    df[agg_col] = pd.to_numeric(df[agg_col], errors='coerce')

    # La Magia de Pandas
    if operation == "sum":
        grouped = df.groupby(group_by_col)[agg_col].sum()
    elif operation == "count":
        grouped = df.groupby(group_by_col)[agg_col].count()
    elif operation == "mean":
        grouped = df.groupby(group_by_col)[agg_col].mean()
    else:
        raise ValueError("Operación no soportada. Usa: sum, count, mean.")

    # Convertir de vuelta a lista de diccionarios para el JSON
    # reset_index convierte el índice (ej: Cliente) de nuevo en columna
    return grouped.reset_index().to_dict(orient="records")