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
    # 1. Convertir a DataFrame
    df = pd.DataFrame(data)
    if df.empty: 
        raise ValueError("El dataset proporcionado está vacío.")
    
    # 2. LIMPIEZA DINÁMICA DE DATOS
    # Aseguramos que la columna Y sea numérica (quita basura como '$' o ',')
    df[y_col] = pd.to_numeric(df[y_col], errors='coerce').fillna(0)
    
    # Si la columna X parece una fecha (ISO de SAP), la acortamos a YYYY-MM-DD
    if any(k in x_col.lower() for k in ['date', 'fecha', 'time']):
        try:
            df[x_col] = pd.to_datetime(df[x_col]).dt.strftime('%Y-%m-%d')
        except:
            pass # Si no es fecha válida, se queda como texto

    # 3. Configuración Visual
    setup_style()
    plt.figure(figsize=(12, 7))

    # 4. Dibujar
    ax = sns.barplot(data=df, x=x_col, y=y_col, color=color, palette="viridis" if not color else None)
    
    # 5. Personalizar
    plt.title(title, fontsize=15, pad=20)
    plt.xlabel(x_col, fontsize=12)
    plt.ylabel(y_col, fontsize=12)
    
    # Añadir etiquetas de valor sobre las barras para mayor claridad
    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f', padding=3)

    # Rotar etiquetas si hay más de 4 registros
    if len(df) > 4:
        plt.xticks(rotation=45, ha='right')

    plt.tight_layout()

    # 6. Retornar Base64 y CERRAR plot (libera memoria)
    return save_and_close_plot()