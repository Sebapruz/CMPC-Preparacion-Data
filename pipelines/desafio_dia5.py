import pandas as pd
import requests
from sqlalchemy import create_engine
import os
import sys

# --- Configuracion Inicial ---
API_URL= "https://jsonplaceholder.typicode.com/users"
csv_path = "/Users/sebastianpalma/Desktop/CMPC-Preparacion/datasets/compras_logistica.csv"
db_path = "/Users/sebastianpalma/Desktop/CMPC-Preparacion/datasets/cmpc_warehouse.db"
engine= create_engine(f"sqlite:///{db_path}")

# Extraccion de Datos desde la API
def extract_from_api(url):
    print(f" [API] Descargando proveedores desde: {url}...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error API: {e}")
        sys.exit(1)

def transform_json_to_df(data_json):
   print(" [API] Transformando JSON de proveedores...")
   df = pd.json_normalize(data_json)
   # Seleccionamos ID y Nombre de la empresa (que es lo que nos importa)
   df_clean = df[['id', 'company.name']].copy()
   df_clean = df_clean.rename(columns={'company.name': 'company_name'})
   return df_clean

# --- EJECUCIÓN DEL PIPELINE ---

print("\n--- PASO 1: PROCESAR PROVEEDORES (API) ---")
# [CORRECIÓN] Hay que LLAMAR a las funciones para que trabajen
raw_users = extract_from_api(API_URL)
df_proveedores = transform_json_to_df(raw_users)

# Guardamos proveedores en SQL (Tabla Maestra)
print("Guardando proveedores en DB...")
df_proveedores.to_sql("dim_proveedores", con=engine, if_exists='replace', index=False)

print("\n--- PASO 2: PROCESAR COMPRAS (CSV) ---")
# Carga de Datos archivo Local
df_compras = pd.read_csv(csv_path)

# Limpieza de fechas
print("Normalizando fechas...")
df_compras['purchase_date'] = pd.to_datetime(df_compras['purchase_date'])

# Si no haces esto, SQL no puede leer los datos
print("Guardando compras en DB (Tabla: stg_compras)...")
df_compras.to_sql("stg_compras", con=engine, if_exists='replace', index=False)

print("\n--- PASO 3: ANÁLISIS SQL (JOIN & REPORT) ---")

# Parámetros del requerimiento (Q1 2024: Enero a Marzo)
fecha_inicio = '2024-01-01'
fecha_fin = '2024-03-31'

# 1. Usamos 'dim_proveedores' (la que acabamos de crear)
# 2. Usamos 'stg_compras' (la del CSV)
# 3. El JOIN es: proveedores.id = compras.supplier_id
query = f"""
SELECT 
    p.company_name as Empresa, 
    SUM(c.total_amount) as Total_Gastado
FROM dim_proveedores p
JOIN stg_compras c ON p.id = c.supplier_id
WHERE c.purchase_date BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
GROUP BY p.company_name
ORDER BY Total_Gastado DESC
"""

try: 
    print(" Ejecutando Query de Negocio...")
    df_reporte = pd.read_sql(query, engine)

    # Guardamos el resultado final en la tabla KPI solicitada
    df_reporte.to_sql("kpi_gastos_q1", con=engine, if_exists='replace', index=False)
    
    print("\n REPORTE GENERADO EXITOSAMENTE:")
    print(df_reporte)
    
except Exception as e:
    print(f"Error en la consulta SQL: {e}")
