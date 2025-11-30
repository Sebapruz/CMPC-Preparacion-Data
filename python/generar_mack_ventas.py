import pandas as pd
import random
import os

# Generamos 50 ventas aleatorias para los usuarios con ID 1 al 10
data = {
    'sale_id': range(1001, 1051),
    'user_id': [random.randint(1, 10) for _ in range(50)], # IDs deben coincidir con dim_usuarios
    'amount': [random.randint(50, 2000) for _ in range(50)],
    'date': pd.date_range(start='2024-01-01', periods=50)
}

df = pd.DataFrame(data)
os.makedirs('/Users/sebastianpalma/Desktop/CMPC-Preparacion/datasets', exist_ok=True)
df.to_csv('/Users/sebastianpalma/Desktop/CMPC-Preparacion/datasets/ventas.csv', index=False)
print("/Users/sebastianpalma/Desktop/CMPC-Preparacion/datasets/ventas.csv' generado exitosamente.")