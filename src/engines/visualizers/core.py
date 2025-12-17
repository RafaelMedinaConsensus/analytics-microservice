import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

def setup_style():
    """Configura el estilo visual una sola vez por gráfico."""
    sns.set_theme(style="whitegrid")
    # Evita que se abran ventanas de GUI en el servidor
    plt.switch_backend('Agg') 

def save_and_close_plot() -> str:
    """Extrae el base64 y limpia la memoria del servidor."""
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    
    # IMPORTANTE: Cerrar la figura y limpiar la memoria
    plt.clf()
    plt.close('all')
    
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')
    return img_str