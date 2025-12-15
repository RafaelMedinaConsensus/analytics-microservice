import matplotlib
# Configuración CRÍTICA: Backend 'Agg' para servidores (sin pantalla)
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

def setup_style():
    """Configura la estética global una sola vez."""
    sns.set_theme(style="whitegrid", context="notebook")

def save_and_close_plot() -> str:
    """
    Toma la figura actual de Matplotlib, la convierte a Base64 y limpia la memoria.
    """
    buffer = io.BytesIO()
    
    # bbox_inches='tight' recorta bordes blancos innecesarios
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    plt.close() # ¡Vital! Cierra la figura para liberar RAM
    
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64