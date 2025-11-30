import pandas as pd
import random
import os

# Simulamos órdenes de compra (PO)
# supplier_id: 1 al 10 (coinciden con los usuarios de la API jsonplaceholder)
data = {
    'po_id': range(5000, 5100), # 100 órdenes
    'supplier_id': [random.randint(1, 10) for _ in range(100)],
    'total_amount': [random.randint(1000, 50000) for _ in range(100)],
    # Fechas mezcladas entre 2023 y 2024 para probar tu filtro
    'purchase_date': pd.date_range(start='2023-11-01', end='2024-04-30', periods=100)
}

df = pd.DataFrame(data)
os.makedirs('/Users/sebastianpalma/Desktop/CMPC-Preparacion/datasets', exist_ok=True)
df.to_csv('/Users/sebastianpalma/Desktop/CMPC-Preparacion/datasets/compras_logistica.csv', index=False)
print("✅ Archivo 'datasets/compras_logistica.csv' generado. ¡Suerte en el desafío!")