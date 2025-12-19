from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import traceback
# Schemas
from services.schemas import (
    StatsInput, GroupingInput, ChartInput, StandardResponse, ExecutionRequest, 
    FilterInput, TopNInput, ForecastInput, ForecastResult
)

# Utils
from utils.tool_loader import load_tool_registry

# Motores (Engines) para uso directo
from engines.descriptive.central import get_smart_mean, get_smart_median, get_smart_mode
from engines.transform.grouping import group_and_aggregate
from engines.visualizers.charts.bar import generate_bar_chart
from engines.visualizers.charts.line import generate_line_chart
from engines.visualizers.charts.pie import generate_pie_chart
from engines.predictive.regression import analytics_linear_forecast
from engines.transform.filtering import apply_filter
from engines.transform.top_n_records import get_top_n_records

router = APIRouter()

# Cargar registro de tools (Para /execute)
TOOL_REGISTRY = load_tool_registry()

# ============================================================
# 0. ENDPOINT DE DESCUBRIMIENTO / INTROSPECCIÓN
# ============================================================
@router.get("/discovery/tools")
def discovery_endpoint():
    """
    Endpoint de Introspección.
    Devuelve la lista de tools registradas y su esquema JSON (argumentos requeridos).
    El Router usa esto para aprender qué puede hacer este microservicio.
    """
    tools_info = []
    
    for name, tool_instance in TOOL_REGISTRY.items():
        # Extraemos el esquema de argumentos (Pydantic -> JSON Schema)
        schema = tool_instance.args_schema.model_json_schema() if tool_instance.args_schema else {}
        
        tools_info.append({
            "name": name,
            "description": tool_instance.description,
            "schema": schema # Esto le dice al Router qué argumentos pedir (x_col, data, etc)
        })
        
    return {"status": "success", "tools": tools_info}

# ============================================================
# 1. ENDPOINT GENÉRICO (MCP / Gateway)
# ============================================================
@router.post("/execute")
async def execute_tool_endpoint(req: ExecutionRequest):
    """Ejecuta cualquier tool por su nombre, manejando la inyección de datos del Orquestador."""
    payload = req.payload
    # Mapeo de sinónimos para el LLM
    synonyms = {
        "x_axis": "x_col", "x_label": "x_col", "y_axis": "y_col", "y_label": "y_col",
        "group_by_column": "group_by", "column_to_operate": "target_column"
    }
    for old, new in synonyms.items():
        if old in payload and new not in payload:
            payload[new] = payload.pop(old)

    if req.tool_name not in TOOL_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Tool '{req.tool_name}' no encontrada.")

    try:
        target_tool = TOOL_REGISTRY[req.tool_name]
        
        # LOG DE SEGURIDAD: Verificar si la inyección de datos fue exitosa
        data_sample = req.payload.get("data", [])
        if isinstance(data_sample, list):
            print(f"   ✅ Inyección exitosa: Recibidos {len(data_sample)} registros.")
        else:
            print(f"   ⚠️ Alerta: El campo 'data' no es una lista. Tipo: {type(data_sample)}")

        # Ejecución a través de LangChain (invoca create_bar_chart, etc)
        result = await target_tool.ainvoke(req.payload)
        
        return {"status": "success", "data": result}

    except Exception as e:
        print(f"   💀 EXCEPCIÓN EN EXECUTE: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
# ============================================================
# 2. ENDPOINTS ESTADÍSTICOS (Descriptive)
# ============================================================
@router.post("/stats/mean", response_model=StandardResponse)
def endpoint_mean(payload: StatsInput):
    try:
        result = get_smart_mean(payload.data, payload.column)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@router.post("/stats/median", response_model=StandardResponse)
def endpoint_median(payload: StatsInput):
    try:
        result = get_smart_median(payload.data, payload.column)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@router.post("/stats/mode", response_model=StandardResponse)
def endpoint_mode(payload: StatsInput):
    try:
        result = get_smart_mode(payload.data, payload.column)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

# ============================================================
# 3. ENDPOINTS DE TRANSFORMACIÓN (Grouping)
# ============================================================
@router.post("/transform/aggregate", response_model=StandardResponse)
def endpoint_aggregate(payload: GroupingInput):
    try:
        result = group_and_aggregate(payload.data, payload.group_by, payload.target_column, payload.operation)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

# --- FILTRADO Y TOP N ---
@router.post("/transform/filter", response_model=StandardResponse)
def endpoint_filter(payload: FilterInput):
    try:
        result = apply_filter(payload.data, payload.column, payload.operator, payload.value)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@router.post("/transform/top_n", response_model=StandardResponse)
def endpoint_top_n(payload: TopNInput):
    try:
        result = get_top_n_records(payload.data, payload.column, payload.n, payload.ascending)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}
    

# ============================================================
# 4. ENDPOINTS PREDICTIVOS (Predictive)
# ============================================================

@router.post("/predict/linear", response_model=StandardResponse)
def endpoint_forecast(payload: ForecastInput):
    try:
        result = analytics_linear_forecast(payload.data, payload.x_col, payload.y_col, payload.periods)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}
    
# ============================================================
# 5. ENDPOINTS VISUALES (Charts)
# ============================================================
@router.post("/visuals/bar", response_model=StandardResponse)
def endpoint_bar_chart(payload: ChartInput):
    try:
        b64 = generate_bar_chart(payload.data, payload.x_col, payload.y_col, payload.title, payload.color or "skyblue")
        return {"status": "success", "data": {"image_base64": b64}}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@router.post("/visuals/line", response_model=StandardResponse)
def endpoint_line_chart(payload: ChartInput):
    try:
        b64 = generate_line_chart(payload.data, payload.x_col, payload.y_col, payload.title, payload.color or "green")
        return {"status": "success", "data": {"image_base64": b64}}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@router.post("/visuals/pie", response_model=StandardResponse)
def endpoint_pie_chart(payload: ChartInput):
    try:
        b64 = generate_pie_chart(payload.data, payload.x_col, payload.y_col, payload.title)
        return {"status": "success", "data": {"image_base64": b64}}
    except Exception as e:
        return {"status": "error", "error": str(e)}