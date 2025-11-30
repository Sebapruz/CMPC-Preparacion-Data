import os

# --- 1. RUTAS DINÁMICAS (El secreto de la portabilidad) ---
# __file__ es este archivo. abspath obtiene su ruta real. dirname obtiene la carpeta.
# Esto dice: "La base es la carpeta donde vive este archivo config.py"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Definimos carpetas relativas a la base.
# os.path.join funciona en Mac (/) y Windows (\) automáticamente.
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Archivo de Base de Datos
DB_PATH = os.path.join(DATASETS_DIR, "cmpc_warehouse.db")
DB_CONNECTION_STRING = f"sqlite:///{DB_PATH}"

# Crear las carpetas automáticamente si no existen (Seguridad)
os.makedirs(DATASETS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# --- 2. VARIABLES DE NEGOCIO ---
API_USERS_URL = "https://jsonplaceholder.typicode.com/users"

# --- 3. CONFIGURACIÓN TÉCNICA ---
RETRIES = 3
TIMEOUT = 10