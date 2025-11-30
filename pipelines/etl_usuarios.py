import requests
import pandas as pd
from sqlalchemy import create_engine
import os
import sys

# --- CONFIGURACIÓN (CONTANTES) ---
# Simulamos una API de RRHH o Clientes
API_URL = "https://jsonplaceholder.typicode.com/users"
# Ruta de nuestra base de datos corporativa (simulada en SQLite)
DB_PATH = "/Users/sebastianpalma/Desktop/CMPC-Preparacion/datasets/cmpc_warehouse.db"

def extract_from_api(url):
    """
    PASO 1: EXTRACT (Extraer)
    Obtiene los datos crudos (JSON) desde la fuente.
    """

    print(f"[EXTRACT] Conectando la fuente: {url}...")
    try:
        response = requests.get(url, timeout=10) # Timeout evita que el script se cuelgue
        response.raise_for_status() # Lanza alerta si hay error 404 o 500
        data = response.json()
        print(f"  Datos descargados: {len(data)} registros.")
        return data
    except Exception as e:
        print(f" Error crítico en extracción: {e}")
        sys.exit(1) # Cierra el programa con error

def transform_json_to_df(data_json):
    """
    PASO 2: TRANSFORM
    Aplana el JSON jerárquico y aplica reglas de negocio.
    """
    print("[TRANSFORM] Normalizando datos...")
    
    # 1. Aplanar el JSON
    df = pd.json_normalize(data_json)
    
    # 2. Definir columnas útiles
    cols_negocio = [
        'id', 'name', 'username', 'email', 
        'phone', 'website', 
        'company.name', 'address.city'
    ]
    
    # --- AQUÍ ESTABA EL ERROR ---
    # 3. Crear df_clean seleccionando solo esas columnas
    # Asegúrate de copiar ESTA línea exactamente:
    df_clean = df[cols_negocio].copy() 
    
    # 4. Ahora sí podemos renombrar, porque df_clean ya existe
    df_clean = df_clean.rename(columns={
        'company.name': 'company_name',
        'address.city': 'city'
    })
    
    # 5. Limpieza de email
    df_clean['email'] = df_clean['email'].str.lower()
    
    print("   Transformación lista. Preview:")
    print(df_clean.head(2))
    return df_clean

def load_to_sql(df, db_path, table_name):
    """
    PASO 3: LOAD
    Guerda el dataframe limpio en SQL
    """
    print(f" [LOAD] Cargando en Data Warehouse: {table_name}...")

    #Creamos el motor de conexión (El puente entre Python y SQL)
    engine = create_engine(f"sqlite:///{db_path}")

    try:
        # if_exists='replace': Borra la tabla y la crea de nuevo (útil para cargas completas)
        # index=False: No guardamos el índice numérico de Pandas (0,1,2...)
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(" Carga exitosa en Base de Datos.")
    except Exception as e:
        print(f" Error en car SQL: {e}")

if __name__ == "__main__":
    print("--- INICINDO PIPELINE DIARIO ---") 

    # Aseguramos que la carpeta datasets exista   
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Orquestación
    raw_data = extract_from_api(API_URL)
    clean_df = transform_json_to_df(raw_data)
    load_to_sql(clean_df, DB_PATH, "dim_usuarios")
    
    print("--- FIN DEL PROCESO ---")
