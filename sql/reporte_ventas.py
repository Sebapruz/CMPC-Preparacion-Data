import pandas as pd
from sqlalchemy import create_engine

# Setup
db_path = "/Users/sebastianpalma/Desktop/CMPC-Preparacion/datasets/cmpc_warehouse.db"
engine = create_engine(f"sqlite:///{db_path}")

print("\n--- REPORTE DE MEJORES CLIENTES (TOP 5) ---")

query = """
SELECT 
    u.name, 
    SUM(v.amount) as total_gastado
FROM dim_usuarios u
JOIN fact_ventas v ON u.id = v.user_id
GROUP BY u.name
ORDER BY total_gastado DESC
LIMIT 5
"""

# Ejecutamos la query
try:
    df_reporte = pd.read_sql(query, engine)
    print(df_reporte)
except Exception as e:
    print(f" Error en SQL: {e}")
