# Analytics Microservice

Este microservicio proporciona un motor de análisis estadístico, predictivo y de visualización de datos, diseñado para ser consumido por agentes de IA o aplicaciones cliente.

## 🛠️ Herramientas Disponibles

Las herramientas están organizadas en módulos dentro de `src/tools/`. Cada una está diseñada para una tarea específica de análisis de datos.

### 📊 Descriptivas (`stats_tools.py`)
Encargadas de entender la distribución y tendencia central de los datos.
- **calculate_smart_mean**: Calcula el promedio artimético y la desviación estándar (volatilidad).
- **calculate_smart_median**: Calcula la mediana y el rango intercuartil (IQR), robusto ante outliers.
- **calculate_smart_mode**: Identifica el valor más frecuente (moda) y su dominancia.

### 🔄 Transformación (`transform_tools.py`)
Permiten manipular y estructurar los datos.
- **aggregate_data**: Agrupa datos por una columna y aplica operaciones de agregación (suma, promedio, conteo, etc.).
- **filter_data**: Filtra el conjunto de datos basándose en condiciones lógicas (>, <, ==, etc.).
- **get_top_n**: Obtiene los N registros más altos o bajos basados en una columna numérica.

### 🔮 Predictivas (`predictive_tools.py`)
- **linear_forecast**: Genera proyecciones futuras simples basadas en regresión lineal.

### 📈 Visualización (`chart_tools.py`)
Generan gráficos en formato Base64 listos para renderizar.
- **create_bar_chart**: Gráfico de barras (comparación de categorías).
- **create_line_chart**: Gráfico de líneas (evolución temporal).
- **create_pie_chart**: Gráfico de pastel (distribución porcentual).

---

## 🔗 Endpoints API

El servicio expone una API REST construida con FastAPI.

### Endpoint Genérico (MCP / Agentes)
Este endpoint permite ejecutar **cualquier** herramienta registrada enviando su nombre y parámetros. Ideal para integración con LLMs.

- `POST /execute`
    - **Payload**: `{ "tool_name": "nombre_de_la_tool", "payload": { ...argumentos... } }`

### Endpoints Específicos
Endpoints dedicados para consumo directo por frontend u otros servicios.

#### 📊 Estadísticas
- `POST /stats/mean`
- `POST /stats/median`
- `POST /stats/mode`

#### 🔄 Transformación
- `POST /transform/aggregate`
- `POST /transform/filter`
- `POST /transform/top_n`

#### 🔮 Predicción
- `POST /predict/linear`

#### 📈 Visualización (Retornan imagen en Base64)
- `POST /visuals/bar`
- `POST /visuals/line`
- `POST /visuals/pie`

---

## 🚀 Paso a paso: Crear una nueva herramienta

El sistema cuenta con un **gestor de herramientas dinámico** que detecta y registra automáticamente nuevas capacidades.

### 1. Ubicación
Navega al directorio `src/tools/`. Puedes crear un nuevo archivo `.py` (ej: `text_tools.py`) o agregar tu herramienta a uno existente si encaja en la categoría.

### 2. Definición (`@tool`)
Utiliza el decorador `@tool` de LangChain. Esto es **obligatorio** para que el registro automático funcione.

```python
from langchain_core.tools import tool

# (Opcional) Define un esquema de entrada para validación estricta
from pydantic import BaseModel, Field

class MyInput(BaseModel):
    text: str = Field(..., description="Texto a procesar")

@tool(args_schema=MyInput)
def my_custom_tool(text: str) -> dict:
    """
    Docstring descriptivo: Explica QUÉ hace la herramienta. 
    Esto es usado por los agentes para saber cuándo usarla.
    """
    try:
        # Tu lógica aquí
        processed = text.upper()
        return {"status": "success", "data": processed}
    except Exception as e:
        return {"status": "error", "error": str(e)}
```

### 3. ¡Listo!
No necesitas registrarla manualmente en ningún lugar.
- Al reiniciar el servidor, el sistema escaneará `src/tools/`.
- Tu función `my_custom_tool` estará disponible inmediatamente en el endpoint `POST /execute`.

### 4. (Opcional) Exponer endpoint dedicado
Si quieres que tu herramienta tenga su propia ruta (ej: `/text/uppercase`):

1. Abre `src/services/routes.py`.
2. Importa tu lógica (o la tool).
3. Agrega la ruta:
   ```python
   @router.post("/text/uppercase")
   def endpoint_uppercase(payload: MyInput):
       # ... lógica ...
       return {"status": "success", ...}
   ```
