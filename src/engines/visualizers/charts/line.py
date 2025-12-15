import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Dict, Any
from ..core import setup_style, save_and_close_plot

def generate_line_chart(
    data: List[Dict[str, Any]],
    x_col: str,
    y_col: str,
    title: str = "Tendencia",
    color: str = "green"
) -> str:
    df = pd.DataFrame(data)
    if df.empty: raise ValueError("Dataset vacío.")

    # Intentar parsear fechas para que el eje X se vea bonito
    try:
        df[x_col] = pd.to_datetime(df[x_col])
    except Exception:
        pass # Si no es fecha, lo dejamos como está

    setup_style()
    plt.figure(figsize=(10, 6))

    sns.lineplot(
        data=df, 
        x=x_col, 
        y=y_col, 
        color=color, 
        marker="o",  # Puntos en cada dato
        linewidth=2
    )

    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.xticks(rotation=45)

    return save_and_close_plot()