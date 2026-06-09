# -*- coding: utf-8 -*-
"""
# ETAPA 0: ENTORNO Y DEPENDENCIAS
"""

print("\n" + "★" * 70)
print("🚀 INICIALIZANDO PIPELINE DE PROCESAMIENTO DE DATOS")
print("★" * 70 + "\n")

# Instalación de librerías esenciales
!pip install -q pandas numpy scikit-learn matplotlib seaborn wordcloud openpyxl pyarrow

from google.colab import drive
drive.mount('/content/drive')

# Estructura de directorios del proyecto
!mkdir -p /content/drive/MyDrive/steam_analytics_system

import pandas as pd
import numpy as np
import re
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

print("⚡ Sistema listo para la ejecución")
print(f"⏰ Registro de inicio: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

"""# ETAPA 1: RECEPCIÓN DE ARCHIVOS"""

print("■" * 70)
print("📥 CARGANDO REPOSITORIO DE TITULOS DE STEAM")
print("■" * 70 + "\n")

RUTA_DATASET = '/content/drive/MyDrive/steam_games.csv'
df_origen = pd.read_csv(RUTA_DATASET)

print(f"📦 Datos cargados correctamente")
print(f"📈 Matriz inicial: {df_origen.shape[0]} registros × {df_origen.shape[1]} columnas")
print(f"📋 Primeros campos: {', '.join(df_origen.columns[:5])}...")
print("\n👀 Inspección inicial de registros:")
display(df_origen.head())

