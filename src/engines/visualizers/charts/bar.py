import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Dict, Any
from ..core import setup_style, save_and_close_plot

def generate_bar_chart(
    data: List[Dict[str, Any]],
    x_col: str,
    y_col: str,
    title: str = "Gráfico de Barras",
    color: str = "skyblue"
) -> str:
    # 1. Preparar
    df = pd.DataFrame(data)
    if df.empty: raise ValueError("Dataset vacío.")
    
    setup_style()
    plt.figure(figsize=(10, 6))

    # 2. Dibujar
    sns.barplot(data=df, x=x_col, y=y_col, color=color)
    
    # 3. Personalizar
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    
    # Rotar etiquetas si son muchas
    if len(df) > 5:
        plt.xticks(rotation=45, ha='right')

    # 4. Retornar Base64
    return save_and_close_plot()