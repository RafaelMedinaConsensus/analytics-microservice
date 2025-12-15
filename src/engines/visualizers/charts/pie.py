import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any
from ..core import setup_style, save_and_close_plot

def generate_pie_chart(
    data: List[Dict[str, Any]],
    x_col: str, # Categoría
    y_col: str, # Valor
    title: str = "Distribución"
) -> str:
    df = pd.DataFrame(data)
    if df.empty: raise ValueError("Dataset vacío.")

    # Agrupar automáticamente por si vienen datos repetidos
    df_grouped = df.groupby(x_col)[y_col].sum()

    setup_style()
    plt.figure(figsize=(8, 8))

    # Usar paleta de colores pastel de Seaborn
    colors = sns.color_palette('pastel')

    plt.pie(
        df_grouped, 
        labels=df_grouped.index, 
        autopct='%1.1f%%', 
        startangle=140,
        colors=colors,
        wedgeprops={'edgecolor': 'white'}
    )

    plt.title(title)
    return save_and_close_plot()