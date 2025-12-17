import pandas as pd
from typing import List, Dict, Any

def process_data_for_chart(data: List[Dict[str, Any]], x_col: str, y_col: str) -> pd.DataFrame:
    """
    Convierte lista de diccionarios a DataFrame y limpia tipos de datos.
    """
    if not data:
        raise ValueError("El dataset está vacío.")

    df = pd.DataFrame(data)

    # 1. Validar columnas
    if x_col not in df.columns:
        raise ValueError(f"La columna X '{x_col}' no existe. Disponibles: {list(df.columns)}")
    if y_col not in df.columns:
        # Intento de fallback inteligente: buscar columna que contenga 'total', 'cant', 'valor'
        candidates = [c for c in df.columns if any(x in c.lower() for x in ['total', 'cant', 'stock', 'price'])]
        if candidates:
            y_col = candidates[0]
        else:
            raise ValueError(f"La columna Y '{y_col}' no existe.")

    # 2. Limpieza de Fechas (Eje X)
    # Si parece fecha (contiene 'date' o 'fecha'), intentamos formatear corto
    if any(k in x_col.lower() for k in ['date', 'fecha', 'time']):
        try:
            df[x_col] = pd.to_datetime(df[x_col]).dt.strftime('%Y-%m-%d')
        except:
            pass # Si falla, se queda como texto original

    # 3. Limpieza Numérica (Eje Y)
    # Forzamos conversión a número. Si hay basura ("$100", "N/A"), se convierte en NaN y luego en 0
    df[y_col] = pd.to_numeric(df[y_col], errors='coerce').fillna(0)

    return df, x_col, y_col