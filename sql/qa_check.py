import pandas as pd
from sqlalchemy import create_engine

# Conexión a la base de datos que creamos
db_path = "../datasets/cmpc_warehouse.db"
engine = create_engine(f"sqlite:///{db_path}")

print("\n🔍 --- REPORTE DE QA (CONTROL DE CALIDAD) ---")

# CONSULTA 1: Conteo simple
# SQL puro dentro de Python
query_count = "SELECT COUNT(*) as total FROM dim_usuarios"
df_count = pd.read_sql(query_count, engine)
total = df_count['total'][0]
print(f"Total de usuarios cargados: {total}")

# CONSULTA 2: Filtrado (Simulando un requerimiento de negocio)
# "Muéstrame los usuarios que viven en Gwenborough"
query_filter = """
SELECT id, name, email, city 
FROM dim_usuarios 
WHERE city = 'Gwenborough'
"""
df_gwen = pd.read_sql(query_filter, engine)

print("\nUsuarios en Gwenborough:")
print(df_gwen)

# Validación automática
if total > 0:
    print("\n TEST APROBADO: La tabla tiene datos.")
else:
    print("\n TEST FALLIDO: La tabla está vacía.")