import pkgutil
import importlib
import inspect
import sys
import os
from typing import Dict
from langchain_core.tools import BaseTool
import src.tools as tools_package 

# Fix de rutas para imports internos
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def load_tool_registry() -> Dict[str, BaseTool]:
    registry = {}
    package_path = tools_package.__path__
    prefix = tools_package.__name__ + "." 

    print(f" REGISTRY: Escaneando tools en {package_path}...")

    for _, module_name, _ in pkgutil.iter_modules(package_path, prefix):
        try:
            module = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, BaseTool):
                    registry[obj.name] = obj
                    print(f"Tool registrada: '{obj.name}'")
        except Exception as e:
            print(f"Error cargando {module_name}: {e}")

    return registry