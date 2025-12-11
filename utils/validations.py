import pandas as pd
from utils.logger import get_logger

# Usamos un logger específico para validaciones
log = get_logger("VALIDATOR")

def validate_schema(df, required_columns):
    """
    Verifica que el DataFrame tenga las columnas obligatorias.
    Devuelve True si pasa, False si falla.
    """
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        log.error(f"❌ FALLÓ SCHEMA: Faltan las columnas {missing_cols}")
        return False
    
    log.info("✅ Schema validado correctamente.")
    return True

def validate_nulls(df, column_name, critical=True):
    """
    Revisa si una columna tiene nulos.
    critical=True  -> Es un error grave (ej: ID nulo).
    critical=False -> Es solo una advertencia (ej: Teléfono nulo).
    """
    null_count = df[column_name].isnull().sum()
    
    if null_count > 0:
        msg = f"⚠️ Columna '{column_name}' tiene {null_count} valores nulos."
        if critical:
            log.error(f"❌ {msg} (CRÍTICO - NO SE PUEDE CARGAR)")
            return False
        else:
            log.warning(f"{msg} (ADVERTENCIA - Se cargará igual)")
            return True # Pasa porque no es crítico
            
    return True