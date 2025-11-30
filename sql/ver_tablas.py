from sqlalchemy import create_engine, inspect

# Conectamos al archivo .db (La "Caja")
db_path = "/Users/sebastianpalma/Desktop/CMPC-Preparacion/datasets/cmpc_warehouse.db"
engine = create_engine(f"sqlite:///{db_path}")

# Creamos un inspector (como abrir el índice del libro)
inspector = inspect(engine)

# Le pedimos los nombres de las tablas
mis_tablas = inspector.get_table_names()

print(f"📂 CONTENIDO DEL ARCHIVO {db_path}:")
print("---------------------------------------")
for tabla in mis_tablas:
    print(f" - 📄 Tabla encontrada: {tabla}")