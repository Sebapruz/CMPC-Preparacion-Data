import pandas as pd
from sqlalchemy import create_engine

# 1. Configuración 
csv_path = '/Users/sebastianpalma/Desktop/CMPC-Preparacion/datasets/ventas.csv'
db_path = '/Users/sebastianpalma/Desktop/CMPC-Preparacion/datasets/cmpc_warehouse.db'
engine= create_engine(f"sqlite:///{db_path}")

print("--- INICIO CARGA DE VENTAS ---")

# 1. Cargar CSV
df = pd.read_csv(csv_path)

# 2. Transformación de Fecha
# El CSV tiene la columna 'date' como texto. Vamos a convertirla.
print("Transformando tipos de datos...")

df['date'] = pd.to_datetime(df['date'])

# 3. Verificación
# Imprimimos el tipo de dato para asegurar que diga 'datetime64' y no 'object'
print("Tipos de datos actuales: ")
print(df.dtypes)

# 4. Guardar en SQL
print("Guardando en base de datos...")
df.to_sql("fact_ventas", con=engine, if_exists='replace', index=False)

print("Carga completada con fechas reales.")