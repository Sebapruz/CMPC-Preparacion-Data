import pandas as pd
import requests
from sqlalchemy import create_engine
import sys

# Importamos todo lo necesario
from config import API_USERS_URL, DB_CONNECTION_STRING, TIMEOUT
from utils.logger import get_logger
from utils.validations import validate_schema, validate_nulls # ¡NUEVO!

log = get_logger("ETL_ROBUST")

def extract_users():
    log.info("🚀 Iniciando extracción...")
    try:
        response = requests.get(API_USERS_URL, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        log.error(f"❌ Error API: {e}")
        sys.exit(1)

def transform_users(data):
    log.info("⚙️ Transformando...")
    
    # Convertimos el JSON crudo (data) en un DataFrame (df)
    df = pd.json_normalize(data)
    # --------------------------------------
    
    # Ahora sí podemos usar 'df'
    df_clean = df[['id', 'name', 'email', 'company.name', 'phone']].copy()
    df_clean = df_clean.rename(columns={'company.name': 'company_name'})
    
    # --- SABOTAJE TEMPORAL ---
    # log.warning("😈 INYECTANDO DATOS CORRUPTOS PARA PRUEBA...")
    # Borramos el ID del primer usuario para probar que el validador lo detecte
    #df_clean.loc[0, 'id'] = None 
    # -------------------------
    
    return df_clean

def validate_data(df):
    """
    Etapa de CONTROL DE CALIDAD (Aduana)
    """
    log.info("🛡️ Iniciando Validaciones de Calidad...")
    is_valid = True
    
    # 1. Validar que existan las columnas obligatorias
    required_cols = ['id', 'name', 'email', 'company_name']
    if not validate_schema(df, required_cols):
        is_valid = False
        
    # 2. Validar reglas de negocio
    # ID no puede ser nulo (CRÍTICO)
    if not validate_nulls(df, 'id', critical=True):
        is_valid = False
        
    # Email no debería ser nulo (CRÍTICO para nosotros)
    if not validate_nulls(df, 'email', critical=True):
        is_valid = False

    # Phone puede ser nulo (NO CRÍTICO)
    validate_nulls(df, 'phone', critical=False)
    
    return is_valid

def load_users(df):
    log.info("💾 Intentando cargar en BD...")
    engine = create_engine(DB_CONNECTION_STRING)
    with engine.connect() as conn:
        df.to_sql("dim_usuarios_calidad", con=engine, if_exists='replace', index=False)
    log.info("✅ Carga exitosa.")

if __name__ == "__main__":
    log.info("--- START PIPELINE ROBUSTO ---")
    
    # 1. Extract
    raw_data = extract_users()
    
    # 2. Transform
    df_clean = transform_users(raw_data)
    
    # 3. Validate (¡El paso nuevo!)
    if validate_data(df_clean):
        # 4. Load (Solo si pasó la validación)
        load_users(df_clean)
    else:
        log.error("⛔ EL PIPELINE SE DETUVO POR MALA CALIDAD DE DATOS.")
        sys.exit(1) # Salimos con error para que el Cron o Airflow se enteren
        
    log.info("--- END PIPELINE ---")