from langchain_core.tools import tool
from services.schemas import ForecastInput
from src.engines.predictive.regression import analytics_linear_forecast

@tool(args_schema=ForecastInput)
def analytics_linear_forecast(data: list[dict], x_col: str, y_col: str, periods: int = 3) -> dict:
    """Realiza una proyección lineal simple a futuro."""
    try:
        result = analytics_linear_forecast(data, x_col, y_col, periods)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}