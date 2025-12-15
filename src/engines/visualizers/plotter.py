import matplotlib
# Configuración CRÍTICA para servidores: Usar backend no interactivo
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import base64
from typing import List, Dict, Any

def generate_bar_chart(
    data: List[Dict[str, Any]],
    x_col: str,
    y_col: str,
    title: str = "Gráfico",
    color: str = "skyblue",
    xlabel: str = None,
    ylabel: str = None
) -> str:
    """
    Genera un gráfico de barras genérico y devuelve la imagen en Base64.
    """
    # 1. Preparar DataFrame
    df = pd.DataFrame(data)
    
    if df.empty:
        raise ValueError("El dataset está vacío.")
    
    if x_col not in df.columns or y_col not in df.columns:
        raise ValueError(f"Columnas '{x_col}' o '{y_col}' no encontradas.")

    # 2. Configurar Estilo
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6)) # Tamaño en pulgadas

    # 3. Dibujar (Genérico)
    # Usamos x_col e y_col dinámicamente
    ax = sns.barplot(
        data=df, 
        x=x_col, 
        y=y_col, 
        color=color
    )

    # 4. Personalización
    plt.title(title, fontsize=16, pad=20)
    plt.xlabel(xlabel if xlabel else x_col, fontsize=12)
    plt.ylabel(ylabel if ylabel else y_col, fontsize=12)
    
    # Rotar etiquetas si son muchas o muy largas
    if len(df) > 5 or df[x_col].astype(str).str.len().max() > 10:
        plt.xticks(rotation=45, ha='right')

    plt.tight_layout() # Ajustar márgenes automáticamente

    # 5. Convertir a Base64 (En Memoria)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100) # dpi=100 para web
    plt.close() # ¡CRÍTICO! Cerrar la figura para liberar memoria del servidor
    
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return image_base64