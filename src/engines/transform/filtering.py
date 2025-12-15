import pandas as pd
from typing import List, Dict, Any, Union

def apply_filter(
    data: List[Dict[str, Any]], 
    column: str, 
    operator: str, 
    value: Union[float, int, str]
) -> List[Dict[str, Any]]:
    df = pd.DataFrame(data)
    if df.empty or column not in df.columns: return []

    # Conversión inteligente: si el valor filtro es número, la columna debe ser número
    if isinstance(value, (int, float)):
        df[column] = pd.to_numeric(df[column], errors='coerce')

    # Aplicación del filtro
    if operator == ">":
        df = df[df[column] > value]
    elif operator == "<":
        df = df[df[column] < value]
    elif operator == "==":
        df = df[df[column] == value]
    elif operator == "!=":
        df = df[df[column] != value]
    elif operator == ">=":
        df = df[df[column] >= value]
    elif operator == "<=":
        df = df[df[column] <= value]
    else:
        raise ValueError(f"Operador '{operator}' no soportado.")
    
    return df.to_dict(orient="records")