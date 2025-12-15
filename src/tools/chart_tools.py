from langchain_core.tools import tool
from services.schemas import ChartInput

from engines.visualizers.charts.bar import generate_bar_chart
from engines.visualizers.charts.line import generate_line_chart
from engines.visualizers.charts.pie import generate_pie_chart

@tool(args_schema=ChartInput)
def create_bar_chart(data: list[dict], x_col: str, y_col: str, title: str = "Barras", color: str = "skyblue") -> dict:
    """Genera gráfico de barras vertical."""
    try:
        b64 = generate_bar_chart(data, x_col, y_col, title, color)
        return {"status": "success", "image_base64": b64}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@tool(args_schema=ChartInput)
def create_line_chart(data: list[dict], x_col: str, y_col: str, title: str = "Línea", color: str = "green") -> dict:
    """Genera gráfico de línea."""
    try:
        b64 = generate_line_chart(data, x_col, y_col, title, color)
        return {"status": "success", "image_base64": b64}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@tool(args_schema=ChartInput)
def create_pie_chart(data: list[dict], x_col: str, y_col: str, title: str = "Pastel") -> dict:
    """Genera gráfico de pastel. x_col es categoría, y_col es valor."""
    try:
        b64 = generate_pie_chart(data, x_col, y_col, title)
        return {"status": "success", "image_base64": b64}
    except Exception as e:
        return {"status": "error", "error": str(e)}