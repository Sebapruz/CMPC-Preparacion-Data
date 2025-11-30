#!/bin/bash

# 1. Definir dónde está el proyecto (LA RUTA SSD)
PROJECT_DIR = "/Volumes/SSD_Sandisk/CMPC-Preparacion"

echo "=========================================="
echo "🕒 [BASH] Iniciando script a las: $(date)"

# 2. Intentar entrar a la carpeta
echo "📂 [BASH] Navegando a: $PROJECT_DIR"
cd "$PROJECT_DIR" || { echo "❌ [BASH] Error: No existe la carpeta"; exit 1; }

# 3. Verificar si existe el entorno virtual
if [ -d "venv" ]; then
    echo "🐍 [BASH] Activando entorno virtual..."
    source venv/bin/activate
else
    echo "❌ [BASH] Error: No encuentro la carpeta 'venv'"
    exit 1
fi

# 4. Ejecutar el pipeline y mostrar el resultado
echo "🚀 [BASH] Ejecutando Python..."
python3 -m pipelines.etl_senior

# Capturar si Python falló
if [ $? -eq 0 ]; then
    echo "✅ [BASH] Python terminó con éxito."
else
    echo "❌ [BASH] Python falló. Revisa el error arriba."
fi

echo "=========================================="
deactivate