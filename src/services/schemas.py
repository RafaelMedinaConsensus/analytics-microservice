from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union

# ==========================================
# 1. INPUTS (Entradas de datos)
# ==========================================

# --- ESTADÍSTICA (Stats) ---
class StatsInput(BaseModel):
    data: List[Dict[str, Any]] = Field(..., description="Lista de registros JSON.")
    column: str = Field(..., description="Nombre de la columna numérica a analizar.")

# --- AGRUPACIÓN (Grouping) ---
class GroupingInput(BaseModel):
    data: List[Dict[str, Any]] = Field(..., description="Datos crudos.")
    group_by: str = Field(..., description="Columna para agrupar (ej: 'vendedor').")
    target_column: str = Field(..., description="Columna a operar (ej: 'venta').")
    operation: str = Field("sum", description="Operación: 'sum', 'mean', 'count'.")

# --- GRÁFICOS (Charts)
class ChartInput(BaseModel):
    data: List[Dict[str, Any]] = Field(..., description="Lista de datos para graficar.")
    x_col: str = Field(..., description="Nombre de la columna Eje X (Categoría/Tiempo).")
    y_col: str = Field(..., description="Nombre de la columna Eje Y (Valor).")
    title: Optional[str] = Field("Gráfico Generado", description="Título del gráfico.")
    color: Optional[str] = Field(None, description="Color (ej: 'red', 'skyblue', '#FF5733').")

# --- FILTRADO ---
class FilterInput(BaseModel):
    data: List[Dict[str, Any]] = Field(..., description="Datos a filtrar.")
    column: str = Field(..., description="Columna a evaluar.")
    operator: str = Field(..., description="Operador: '>', '<', '==', '!=', '>=', '<='.")
    value: Union[float, int, str] = Field(..., description="Valor contra el cual comparar.")

# --- RANKING ---
class TopNInput(BaseModel):
    data: List[Dict[str, Any]] = Field(..., description="Datos a ordenar.")
    column: str = Field(..., description="Columna criterio para el ranking.")
    n: int = Field(5, description="Cuántos registros devolver.")
    ascending: bool = Field(False, description="False = De mayor a menor (Top). True = De menor a mayor (Bottom).")

# --- PREDICCIÓN ---
class ForecastInput(BaseModel):
    data: List[Dict[str, Any]] = Field(..., description="Datos históricos.")
    x_col: str = Field(..., description="Columna de tiempo o secuencia (Eje X).")
    y_col: str = Field(..., description="Columna a predecir (Eje Y).")
    periods: int = Field(3, description="Cuántos periodos futuros proyectar.")

# --- EJECUCIÓN GENÉRICA (Para /execute) ---
class ExecutionRequest(BaseModel):
    tool_name: str = Field(..., description="Nombre exacto de la tool a ejecutar.")
    payload: Dict[str, Any] = Field(..., description="Argumentos para la tool.")

# ==========================================
# 2. OUTPUTS (Salidas enriquecidas)
# ==========================================

class SmartMeanResult(BaseModel):
    mean: float
    volatility: float

class SmartMedianResult(BaseModel):
    median: float
    iqr: float

class SmartModeResult(BaseModel):
    top_value: Union[str, float, int]
    dominance_pct: float
    tie: bool

# --- OUTPUT PARA PREDICCIÓN ---
class ForecastResult(BaseModel):
    trend: str = Field(..., description="'Creciente', 'Decreciente' o 'Estable'.")
    slope: float = Field(..., description="Pendiente de la recta (m).")
    forecast: List[Dict[str, Any]] = Field(..., description="Lista de valores proyectados (x, y).")
    r_squared: float = Field(..., description="Coeficiente R2 (Confianza del ajuste 0-1).")

# ==========================================
# 3. RESPONSE WRAPPER (Respuesta Estándar)
# ==========================================

class StandardResponse(BaseModel):
    status: str
    data: Any 
    error: Optional[str] = None