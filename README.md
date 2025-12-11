# 🌲 CMPC Data Pipeline: Gastos Logísticos

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/Status-Production-green)
![Data Quality](https://img.shields.io/badge/Data%20Quality-Validated-orange)

## 📄 Descripción del Proyecto

Este proyecto implementa un pipeline de Ingeniería de Datos **ETL (Extract, Transform, Load)** completamente automatizado para la gestión y auditoría de gastos logísticos de proveedores externos.

El sistema fue diseñado con una arquitectura modular y defensiva, priorizando la **calidad de datos** y la **observabilidad**.  
Su objetivo es consolidar datos desde fuentes externas (APIs), validarlos mediante reglas de negocio estrictas y almacenarlos en un Data Warehouse local para análisis financiero.

---

## 🏗️ Arquitectura del Sistema

El flujo de datos sigue un proceso lineal con *Quality Gates* que detienen la ejecución ante problemas críticos:

```mermaid
graph LR
    A[🌍 API Externa] -->|JSON Raw| B(⚡ Extract)
    B --> C{🛡️ Data Quality Check}
    C -->|✅ Pass| D[⚙️ Transform]
    C -->|❌ Fail| E[⛔ Log Error & Stop]
    D -->|Datos Limpios| F[(🗄️ SQLite Warehouse)]
    F --> G[📊 KPI Reporting]
🛠️ Stack Tecnológico
Lenguaje: Python 3.x

Procesamiento: Pandas (DataFrames)

Almacenamiento: SQLite + SQLAlchemy

Orquestación: Bash + Cron (Unix Scheduling)

Logging: Sistema de logs rotativos customizado

Control de Versiones: Git & GitHub

🚀 Instalación y Configuración
Sigue estos pasos para desplegar el proyecto en un entorno local (macOS/Linux).

1. Clonar el repositorio
bash
Copiar código
git clone https://github.com/Sebapruz/CMPC-Preparacion-Data.git
cd CMPC-Preparacion-Data
2. Configurar el Entorno Virtual
bash
Copiar código
python3 -m venv venv
source venv/bin/activate
3. Instalar Dependencias
bash
Copiar código
pip install -r requirements.txt
💻 Uso y Ejecución
▶️ Ejecución Manual
Para correr el pipeline completo (incluyendo validaciones):

bash
Copiar código
python3 -m pipelines.etl_robust
Esto generará logs en logs/ y actualizará la base de datos en datasets/.

⏰ Automatización (Cron Job)
El proyecto incluye un Wrapper Script (run_pipeline.sh) diseñado para orquestar la ejecución mediante Cron.

Dar permisos de ejecución:
bash
Copiar código
chmod +x run_pipeline.sh
Configurar Cron (Ejemplo: Ejecutar todos los días a las 09:00 AM):
bash
Copiar código
crontab -e
Agregar la siguiente línea (ajustando tu ruta absoluta):

swift
Copiar código
0 9 * * * /ruta/absoluta/a/CMPC-Preparacion-Data/run_pipeline.sh
🛡️ Calidad de Datos (Data Quality)
El sistema implementa una capa de Programación Defensiva en utils/validations.py.
El pipeline se detendrá automáticamente (Exit Code 1) si detecta:

Schema Drift: Si la API cambia de formato o faltan columnas obligatorias.

Null Values Críticos: Si campos clave como ID o Email vienen vacíos.

Integridad Referencial: Extensible a reglas de negocio específicas.

Cualquier incidente de calidad queda registrado con nivel ERROR o CRITICAL en los logs.

📂 Estructura del Proyecto
plaintext
Copiar código
CMPC-Preparacion-Data/
├── config.py           # ⚙️ Configuración centralizada (Rutas dinámicas)
├── run_pipeline.sh     # 🤖 Wrapper para automatización con Cron
├── requirements.txt    # 📦 Lista de dependencias
├── datasets/           # 🗄️ Almacenamiento local (Base de Datos)
├── logs/               # 📝 Historial de ejecución (Auditoría)
├── pipelines/          # 🚀 Lógica de Negocio (ETL)
│   └── etl_robust.py   # Script principal con validaciones
├── utils/              # 🧰 Herramientas Reutilizables
│   ├── __init__.py
│   ├── logger.py       # Configuración de logging
│   └── validations.py  # Motor de reglas de calidad
└── sql/                # 🔍 Scripts de análisis y consultas
👤 Autor
Sebastián Palma
Ingeniero de Datos en formación | Enfocado en Arquitecturas Robustas y Automatización.

Este proyecto fue desarrollado como parte de una simulación intensiva de Ingeniería de Datos.