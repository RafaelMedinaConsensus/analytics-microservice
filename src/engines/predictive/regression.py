import pandas as pd
import numpy as np
from typing import List, Dict, Any

def analytics_linear_forecast(
    data: List[Dict[str, Any]], 
    x_col: str, 
    y_col: str, 
    periods: int = 3
) -> Dict[str, Any]:
    df = pd.DataFrame(data)
    if df.empty: raise ValueError("Dataset vacío.")

    # Limpieza
    df[y_col] = pd.to_numeric(df[y_col], errors='coerce')
    df = df.dropna(subset=[y_col])

    # Preparamos X e Y numéricos para el cálculo
    y_values = df[y_col].values
    # Creamos un índice secuencial (0, 1, 2...) para simplificar el tiempo
    x_values = np.arange(len(y_values))

    # Regresión Lineal (Grado 1) -> y = mx + b
    # slope (m), intercept (b)
    slope, intercept = np.polyfit(x_values, y_values, 1)

    # Calcular R^2 (Calidad del ajuste)
    y_pred = slope * x_values + intercept
    ss_res = np.sum((y_values - y_pred) ** 2)
    ss_tot = np.sum((y_values - np.mean(y_values)) ** 2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0

    # Proyectar futuro
    last_x = x_values[-1]
    future_x_indices = np.arange(last_x + 1, last_x + 1 + periods)
    future_y_values = slope * future_x_indices + intercept

    # Construir respuesta
    forecast_list = []
    for i, val in enumerate(future_y_values):
        forecast_list.append({
            "step_future": int(i + 1),
            "predicted_value": round(float(val), 2)
        })

    trend_desc = "Estable"
    if slope > 0.1: trend_desc = "Creciente"
    elif slope < -0.1: trend_desc = "Decreciente"

    return {
        "trend": trend_desc,
        "slope": round(float(slope), 4),
        "r_squared": round(float(r2), 4),
        "forecast": forecast_list
    }