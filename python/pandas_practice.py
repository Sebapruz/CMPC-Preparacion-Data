import pandas as pd

#Cargar el Dataset
df = pd.read_csv("/Users/sebastianpalma/Desktop/CMPC-Preparacion/datasets/Titanic-Dataset.csv")

print("Primeras Filas: ")
print(df.head())

print("\nInfo del Dataset: ")
print(df.info())

print("\nDescripcion estadística: ")
print(df.describe())

#-----Limpieza---
df = df.drop_duplicates()

# Rellenar Edades Faltantes
df["Age"] = df["Age"].fillna(df["Age"].median())

# Convertir Tipo Survived a Entero
df["Survived"] = df["Survived"].astype(int)

# Renombrar Columna
df = df.rename(columns={"Pclass": "PassengerClass"})

# Nueva Columna = ¿Es adulto?
df["IsAdult"] = df["Age"] >= 18

#Exportar Dataset Limpio
df.to_csv("/Users/sebastianpalma/Desktop/CMPC-Preparacion/datasets/Titanic-Clean.csv", index=False)

print("\nArchivo limpio generado: titanic_clean.csv")