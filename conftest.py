import os
import shutil
import sys
import pytest

# Añadido para que pytest encuentre módulos que empiezan por 'src'
# Esta línea soluciona los errores 'ModuleNotFoundError: No module named 'src''
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# --- Tu código original para limpiar el contexto (conservado) ---

# Lista de posibles rutas donde se guarda el contexto.
POSSIBLE_CONTEXT_PATHS = [
    os.path.join(os.getcwd(), "context_store.db"),
    os.path.join(os.getcwd(), "context_store.sqlite"),
    os.path.join(os.getcwd(), "context_store.json"),
    os.path.join(os.getcwd(), "src", "theaia", "database", "repositories", "context_store.db"),
]

def _remove_if_exists(path: str):
    """Elimina un archivo o directorio si existe, ignorando errores."""
    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
    except OSError:
        pass

@pytest.fixture(scope="session", autouse=True)
def clear_context_before_suite():
    """Asegura que no haya contexto residual antes de que se ejecuten los tests."""
    for path in POSSIBLE_CONTEXT_PATHS:
        _remove_if_exists(path)
    yield
