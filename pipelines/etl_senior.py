import pandas as pd
import requests
from sqlalchemy import create_engine
import sys

# IMPORTACIONES CRUZADAS
# Importamos variables desde onfig (que está en la raíz)
from config import API_USERS_URL, DB_CONNECTION_STRING, TIMEOUT
# Importamos el logger desde utils
from utils.logger import get_logger

# Inicializamos el logger
log = get_logger("ETL_SENIOR")

def extract_users():
    log.info(f" Iniciando extracción desde API...")
    try:
        #Usamos la variable TIMEOUT importada
        response = requests.get(API_USERS_URL, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        log.info(f"Extracción exitosa: {len(data)} registros")
        return data
    except Exception as e:
        # .error guarda el mensaje con etiqueta ERROR
        log.error(f"Error crítico en API: {e}", exc_info=True)
        sys.exit(1)

def transform_users(data):
    log.info("Iniciando transformación...")
    try:
        df = pd.json_normalize(data)

        # Limpieza
        df_clean = df[['id', 'name', 'email', 'company.name']].copy()
        df_clean = df_clean.rename(columns={'company.name': 'company_name'})
        df_clean['email'] = df_clean['email'].str.lower()

        log.info("Transformación completada.")
        return df_clean
    except KeyError as e:
        log.error(f"Error: JSON incompleto. Falta columna: {e}")
        sys.exit(1)

def load_users(df):
    log.info(f"Conectando a Base de Datos...")
    try:
        # Usamos la conexión centralizada
        engine = create_engine(DB_CONNECTION_STRING)

        with engine.connect() as conn:
            df.to_sql("dim_usuarios_senior", con=engine, if_exists='replace', index=False)
        log.info("Carga exitosa en tabla 'dim_usuarios_senior' .")
    except Exception as e:
        log.error(f"Falló la carga en BD: {e}")

if __name__ == "__main__":
    log.info("--- INICIO DEL PIPELINE PROFESIONAL ---")
    
    users_raw = extract_users()
    users_clean = transform_users(users_raw)
    load_users(users_clean)
    
    log.info("--- FIN DEL PROCESO ---")


