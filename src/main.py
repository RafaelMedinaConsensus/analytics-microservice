import sys
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- FIX DE RUTAS (Vital para evitar ModuleNotFoundError) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from services.routes import router

# Definimos la App
app = FastAPI(
    title="Analytics Microservice",
    description="Motor de análisis estadístico descriptivo para datos.",
    version="1.0.0"
)

# CORS (Permitir que cualquiera lo llame, útil para desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectamos las rutas
app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "online", "service": "analytics-engine"}

if __name__ == "__main__":
    print("🚀 Arrancando Analytics Engine en http://0.0.0.0:8004")
    uvicorn.run(app, host="0.0.0.0", port=8004)