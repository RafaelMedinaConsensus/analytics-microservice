import pandas as pd
from typing import List, Dict, Any

# --- HELPER ---
def _get_series(data: List[Dict[str, Any]], column: str) -> pd.Series:
    df = pd.DataFrame(data)
    if df.empty or column not in df.columns:
        raise ValueError(f"Columna '{column}' no encontrada o datos vacíos.")
    return df[column]

def _to_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors='coerce').dropna()

# --- 1. MEDIA CONTEXTUAL (Promedio + Volatilidad) ---
def get_smart_mean(data: List[Dict[str, Any]], column: str) -> Dict[str, Any]:
    series = _to_numeric(_get_series(data, column))
    if series.empty: raise ValueError("Sin datos numéricos.")

    return {
        "mean": round(float(series.mean()), 2),
        "volatility": round(float(series.std()), 2) 
    }

# --- 2. MEDIANA CONTEXTUAL (Centro + Concentración) ---
def get_smart_median(data: List[Dict[str, Any]], column: str) -> Dict[str, Any]:
    series = _to_numeric(_get_series(data, column))
    if series.empty: raise ValueError("Sin datos numéricos.")

    # IQR = Q3 - Q1 (Donde vive la mayoría de la gente normal)
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    
    return {
        "median": round(float(series.median()), 2),
        "iqr": round(float(q3 - q1), 2)
    }

# --- 3. MODA CONTEXTUAL (Ganador + Fuerza) ---
def get_smart_mode(data: List[Dict[str, Any]], column: str) -> Dict[str, Any]:
    series = _get_series(data, column).dropna() # Aceptamos texto y números
    if series.empty: raise ValueError("Columna vacía.")

    # Conteo rápido
    counts = series.value_counts()
    total = len(series)
    
    if counts.empty: return {"top_value": None, "dominance_pct": 0, "tie": False}

    top_val = counts.index[0]
    top_freq = counts.iloc[0]
    
    # Verificamos si hay empate en el primer lugar
    is_tie = False
    if len(counts) > 1:
        if counts.iloc[0] == counts.iloc[1]:
            is_tie = True

    return {
        "top_value": top_val,
        "dominance_pct": round((top_freq / total) * 100, 1), # Ej: 45.5%
        "tie": is_tie
    }