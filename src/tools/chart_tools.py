from langchain_core.tools import tool
from services.schemas import ChartInput
from typing import List, Dict, Any

from engines.visualizers.charts.bar import generate_bar_chart
from engines.visualizers.charts.line import generate_line_chart
from engines.visualizers.charts.pie import generate_pie_chart


# ==========================================
# HELPER: Formato JSON para Frontend (Recharts)
# ==========================================

def _format_for_recharts(
    data: List[Dict[str, Any]], 
    x_col: str, 
    y_col: str, 
    title: str, 
    chart_type: str,
    color: str = "#4F46E5"
) -> dict:
    """
    Convierte los datos a formato JSON compatible con Recharts (React).
    Este formato permite que el frontend renderice graficos interactivos.
    """
    # Transformar datos al formato que espera Recharts
    chart_data = []
    for row in data:
        x_val = row.get(x_col, "")
        y_val = row.get(y_col, 0)
        
        # Asegurar que y_val sea numerico
        if isinstance(y_val, str):
            try:
                y_val = float(y_val.replace(",", "").replace("$", ""))
            except:
                y_val = 0
        
        chart_data.append({
            "name": str(x_val),  # Recharts usa 'name' para el eje X
            "value": float(y_val) if y_val else 0  # 'value' para el eje Y
        })
    
    return {
        "status": "success",
        "output_format": "json",
        "chart_type": chart_type,
        "title": title,
        "data": chart_data,
        "config": {
            "x_key": "name",
            "y_key": "value",
            "x_label": x_col,
            "y_label": y_col,
            "color": color or "#4F46E5",
            "show_grid": True,
            "show_tooltip": True,
            "show_legend": True
        }
    }


# Paleta de colores para Pie Charts
PIE_COLORS = ["#4F46E5", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899", "#06B6D4", "#84CC16"]


def _format_pie_for_recharts(
    data: List[Dict[str, Any]], 
    x_col: str, 
    y_col: str, 
    title: str
) -> dict:
    """Formato especial para Pie Charts con colores individuales."""
    chart_data = []
    for i, row in enumerate(data):
        x_val = row.get(x_col, "")
        y_val = row.get(y_col, 0)
        
        if isinstance(y_val, str):
            try:
                y_val = float(y_val.replace(",", "").replace("$", ""))
            except:
                y_val = 0
        
        chart_data.append({
            "name": str(x_val),
            "value": float(y_val) if y_val else 0,
            "fill": PIE_COLORS[i % len(PIE_COLORS)]  # Color ciclico
        })
    
    return {
        "status": "success",
        "output_format": "json",
        "chart_type": "pie",
        "title": title,
        "data": chart_data,
        "config": {
            "x_key": "name",
            "y_key": "value",
            "x_label": x_col,
            "y_label": y_col,
            "colors": PIE_COLORS,
            "show_tooltip": True,
            "show_legend": True,
            "inner_radius": 0,  # 0 = Pie, >0 = Donut
            "outer_radius": 80
        }
    }


# ==========================================
# TOOLS CON DOBLE FORMATO
# ==========================================

@tool(args_schema=ChartInput)
def analytics_chart_bar(
    data: list[dict], 
    x_col: str, 
    y_col: str, 
    title: str = "Barras", 
    color: str = "skyblue",
    output_format: str = "image"
) -> dict:
    """
    [ANALYTICS] Genera grafico de BARRAS vertical.
    - data: Lista de diccionarios con los datos (puede ser REF_ID)
    - x_col: Nombre de columna para eje X
    - y_col: Nombre de columna para eje Y
    - output_format: 'image' (PNG base64) o 'json' (para React/Recharts)
    """
    try:
        if output_format == "json":
            return _format_for_recharts(data, x_col, y_col, title, "bar", color)
        else:
            b64 = generate_bar_chart(data, x_col, y_col, title, color)
            return {"status": "success", "output_format": "image", "image_base64": b64}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@tool(args_schema=ChartInput)
def analytics_chart_line(
    data: list[dict], 
    x_col: str, 
    y_col: str, 
    title: str = "Linea", 
    color: str = "green",
    output_format: str = "image"
) -> dict:
    """
    [ANALYTICS] Genera grafico de LINEA temporal.
    - data: Lista de diccionarios con los datos (puede ser REF_ID)
    - x_col: Nombre de columna para eje X (usualmente fecha)
    - y_col: Nombre de columna para eje Y (valores)
    - output_format: 'image' (PNG base64) o 'json' (para React/Recharts)
    """
    try:
        if output_format == "json":
            return _format_for_recharts(data, x_col, y_col, title, "line", color)
        else:
            b64 = generate_line_chart(data, x_col, y_col, title, color)
            return {"status": "success", "output_format": "image", "image_base64": b64}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@tool(args_schema=ChartInput)
def analytics_chart_pie(
    data: list[dict], 
    x_col: str, 
    y_col: str, 
    title: str = "Pastel", 
    color: str = None,
    output_format: str = "image"
) -> dict:
    """
    [ANALYTICS] Genera grafico de PASTEL/PIE para distribuciones.
    - data: Lista de diccionarios con los datos (puede ser REF_ID)
    - x_col: Nombre de columna para categorias
    - y_col: Nombre de columna para valores
    - output_format: 'image' (PNG base64) o 'json' (para React/Recharts)
    """
    try:
        if output_format == "json":
            return _format_pie_for_recharts(data, x_col, y_col, title)
        else:
            b64 = generate_pie_chart(data, x_col, y_col, title)
            return {"status": "success", "output_format": "image", "image_base64": b64}
    except Exception as e:
        return {"status": "error", "error": str(e)}