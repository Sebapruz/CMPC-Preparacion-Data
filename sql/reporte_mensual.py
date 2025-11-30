import pandas as pd
from sqlalchemy import create_engine

db_path = '/Users/sebastianpalma/Desktop/CMPC-Preparacion/datasets/cmpc_warehouse.db'
engine = create_engine(f"sqlite:///{db_path}")

# --- PARAMETROS DEL REPORTE (INPUTS) ---
fecha_inicio = '2023-01-01'
fecha_fin = '2025-12-31'

print(f"Generando reporte desde {fecha_inicio} hasta {fecha_fin}...")

# --- QUERY DINÁMICA ---
query = f"""
SELECT 
    u.name, 
    SUM(v.amount) as total_vendido,
    COUNT(v.sale_id) as cantidad_transacciones
FROM dim_usuarios u
JOIN fact_ventas v ON u.id = v.user_id
WHERE v.date BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
GROUP BY u.name
ORDER BY total_vendido DESC
"""

try: 
    df_reporte = pd.read_sql(query, engine)

    if df_reporte.empty:
        print("No se encontraron ventas en este rango de fechas.")
    else:
        print(df_reporte)
except Exception as e:
    print(f"Error en la consulta: {e}")