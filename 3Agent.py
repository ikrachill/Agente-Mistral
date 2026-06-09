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

"""# ETAPA 2: AUDITORÍA DE CALIDAD (EDA)"""

print("\n" + "■" * 70)
print("🔍 EVALUANDO INTEGRIDAD E INCONSISTENCIAS DE LOS DATOS")
print("■" * 70 + "\n")

def mapear_integridad_datos(dataframe):
    """Inspecciona y reporta el estado estructural de la información"""
    print("📋 1. RESUMEN DE TIPOS")
    print(f"   → {dict(dataframe.dtypes.value_counts())}\n")

    print("⚠️ 2. ANÁLISIS DE VACÍOS (Top 5)")
    conteo_nulos = dataframe.isnull().sum()
    porcentaje_nulos = (conteo_nulos / len(dataframe)) * 100
    resumen_vacios = pd.DataFrame({'Total_Vacios': conteo_nulos, 'Porcentaje_%': porcentaje_nulos})
    print(resumen_vacios[resumen_vacios['Total_Vacios'] > 0].sort_values('Total_Vacios', ascending=False).head(5).to_string())

    print("\n📊 3. MÉTRICAS VARIABLES NUMÉRICAS")
    print(dataframe.describe().to_string())

    print("\n🧪 4. MUESTRA DE DATOS COMPLEJOS")
    columnas_clave = ['original_price', 'recent_reviews', 'release_date', 'genre']
    for col in columnas_clave:
        if col in dataframe.columns:
            print(f"\n   → Muestra en {col}:")
            print(f"      {dataframe[col].dropna().head(3).tolist()}")

mapear_integridad_datos(df_origen)

"""# ETAPA 3: NÚCLEO DE TRANSFORMACIÓN (PROCESADOR)"""

print("\n" + "■" * 70)
print("⚙️  CONFIGURANDO EL MOTOR DE TRANSFORMACIÓN")
print("■" * 70 + "\n")

class SteamDataProcessor:
    """
    🏢 MOTOR ENCARGADO DE LA DEPURACIÓN Y NORMALIZACIÓN DEL DATASET
    - Normaliza tipos de datos numéricos y limpia cadenas de divisas.
    - Corrige problemas bilingües de parseo de fechas.
    - Extrae variables estructuradas cuantitativas de texto libre.
    """

    def __init__(self, df_entrada):
        self.fuente_raw = df_entrada.copy()
        self.df_salida = df_entrada.copy()
        self.registro_operaciones = []

    def emitir_log(self, accion):
        """Almacena un registro de auditoría del proceso ejecutado"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.registro_operaciones.append(f"[{timestamp}] {accion}")
        print(f"   ⚙️ {accion}")

    def limpiar_precios_base(self):
        """Convierte cadenas monetarias complejas a valores flotantes estandarizados"""
        self.emitir_log("Extrayendo importes numéricos y procesando gratuidad...")

        def parsear_moneda(item):
            if pd.isna(item):
                return np.nan

            cadena = str(item).lower().strip()

            if any(token in cadena for token in ['free', 'gratis', 'demo', 'free to play']):
                return 0.0

            # Eliminación de símbolos de divisa para evitar fallas del motor regex
            cadena = cadena.replace('$', '').replace('€', '').strip()

            match = re.search(r'(\d+[\.,]\d{2})|(\d+)', cadena)
            if match:
                num_str = match.group(0).replace(',', '.')
                try:
                    return float(num_str)
                except ValueError:
                    return np.nan
            return np.nan

        self.df_salida['precio_base'] = self.df_salida['original_price'].apply(parsear_moneda)

        if 'discount_price' in self.df_salida.columns:
            self.df_salida['precio_oferta'] = self.df_salida['discount_price'].apply(parsear_moneda)
            self.df_salida['precio_oferta'] = self.df_salida['precio_oferta'].fillna(self.df_salida['precio_base'])

            # Margen porcentual de descuento real
            condicion = (self.df_salida['precio_oferta'] < self.df_salida['precio_base']) & (self.df_salida['precio_base'] > 0)
            self.df_salida['descuento_aplicado'] = np.where(
                condicion,
                100 * (1 - self.df_salida['precio_oferta'] / self.df_salida['precio_base']),
                0
            )
        return self

    def segmentar_opiniones(self):
        """Mapea información cualitativa y cuantitativa de las reseñas de usuarios"""
        self.emitir_log("Segmentando textos analíticos de reviews...")

        def parsear_resenas(bloque_texto):
            if pd.isna(bloque_texto):
                return {'rating': 'Sin registros', 'votos': 0, 'ratio_ok': 0}

            bloque_texto = str(bloque_texto).strip()

            patron_rating = re.match(r'^([^,\-]+)', bloque_texto)
            rating = patron_rating.group(1).strip() if patron_rating else 'Indefinido'

            patron_votos = re.search(r'\(([\d,]+)\)', bloque_texto)
            votos = int(patron_votos.group(1).replace(',', '')) if patron_votos else 0

            patron_porcentaje = re.search(r'(\d+)%', bloque_texto)
            ratio_ok = float(patron_porcentaje.group(1)) if patron_porcentaje else 0

            return {'rating': rating, 'votos': votos, 'ratio_ok': ratio_ok}

        for col_review in ['recent_reviews', 'all_reviews']:
            if col_review in self.df_salida.columns:
                resultados_analisis = self.df_salida[col_review].apply(parsear_resenas)
                self.df_salida[f'{col_review}_categoria'] = resultados_analisis.apply(lambda x: x['rating'])
                self.df_salida[f'{col_review}_volumen'] = resultados_analisis.apply(lambda x: x['votos'])
                self.df_salida[f'{col_review}_porcentaje'] = resultados_analisis.apply(lambda x: x['ratio_ok'])
        return self

    def estructurar_lineas_temporales(self):
        """Convierte y extrae variables derivadas de la fecha de publicación original"""
        self.emitir_log("Homogeneizando fechas bilingües inglés-español...")

        def unificar_idioma_meses(fecha_str):
            if pd.isna(fecha_str):
                return np.nan
            fecha_str = str(fecha_str).lower().strip()

            dicc_meses = {
                'ene.': 'Jan', 'feb.': 'Feb', 'mar.': 'Mar', 'abr.': 'Apr',
                'may.': 'May', 'jun.': 'Jun', 'jul.': 'Jul', 'ago.': 'Aug',
                'sep.': 'Sep', 'oct.': 'Oct', 'nov.': 'Nov', 'dic.': 'Dec'
            }
            for es, en in dicc_meses.items():
                fecha_str = fecha_str.replace(es, en)
            return fecha_str

        fechas_convertidas = self.df_salida['release_date'].apply(unificar_idioma_meses)

        self.df_salida['fecha_publicacion'] = pd.to_datetime(
            fechas_convertidas,
            format='mixed',
            errors='coerce'
        )

        # Generación de variables analíticas de tiempo
        self.df_salida['año_publicacion'] = self.df_salida['fecha_publicacion'].dt.year
        self.df_salida['mes_publicacion'] = self.df_salida['fecha_publicacion'].dt.month
        self.df_salida['periodo_trimestre'] = self.df_salida['fecha_publicacion'].dt.quarter
        self.df_salida['dia_semana_num'] = self.df_salida['fecha_publicacion'].dt.dayofweek
        self.df_salida['es_fin_de_semana'] = (self.df_salida['dia_semana_num'] >= 5).astype(float)
        self.df_salida['es_retro'] = (self.df_salida['año_publicacion'] < 2010).astype(float)
        return self

    def deserializar_arreglos(self, tag_columna):
        """Normaliza textos emulando listas en estructuras nativas de Python"""
        if tag_columna not in self.df_salida.columns:
            return self

        self.emitir_log(f"Deserializando cadenas de arreglos en: {tag_columna}")

        def procesar_estructura(dato):
            if pd.isna(dato):
                return []
            cadena_limpia = str(dato).strip()
            if cadena_limpia.startswith('[') and cadena_limpia.endswith(']'):
                try:
                    return json.loads(cadena_limpia.replace("'", '"'))
                except:
                    return [x.strip().replace("'", "").replace('"', '') for x in cadena_limpia[1:-1].split(',')]
            else:
                return [x.strip() for x in cadena_limpia.split(',') if x.strip()]

        self.df_salida[f'{tag_columna}_coleccion'] = self.df_salida[tag_columna].apply(procesar_estructura)
        self.df_salida[f'{tag_columna}_total_items'] = self.df_salida[f'{tag_columna}_coleccion'].apply(len)
        return self

    def imputar_valores_faltantes(self):
        """Maneja y rellena registros vacíos por tipo de variable para evitar sesgos"""
        self.emitir_log("Ejecutando imputación de datos nulos/ausentes...")

        columnas_texto = ['developer', 'publisher', 'recent_reviews_categoria', 'all_reviews_categoria']
        for c in columnas_texto:
            if c in self.df_salida.columns:
                self.df_salida[c] = self.df_salida[c].fillna('Desconocido')

        columnas_info = ['desc_snippet', 'about_the_game']
        for c in columnas_info:
            if c in self.df_salida.columns:
                self.df_salida[c] = self.df_salida[c].fillna('')

        columnas_numeros = self.df_salida.select_dtypes(include=[np.number]).columns
        for c in columnas_numeros:
            if self.df_salida[c].isnull().any():
                valor_mediana = self.df_salida[c].median()
                self.df_salida[c] = self.df_salida[c].fillna(valor_mediana if not pd.isna(valor_mediana) else 0)
        return self

    def definir_variable_target(self):
        """Construye un índice escalar balanceado para análisis predictivos"""
        self.emitir_log("Estableciendo variable objetivo (Índice de Popularidad)...")

        if 'all_reviews_porcentaje' in self.df_salida.columns and 'all_reviews_volumen' in self.df_salida.columns:
            porc = self.df_salida['all_reviews_porcentaje'].fillna(0)
            vol = self.df_salida['all_reviews_volumen'].fillna(0)

            # Ecuación logarítmica de amortiguación
            self.df_salida['indice_bruto'] = porc * np.log1p(vol)
            maximo_valor = self.df_salida['indice_bruto'].max()

            if maximo_valor > 0:
                self.df_salida['score_final'] = 100 * self.df_salida['indice_bruto'] / maximo_valor
            else:
                self.df_salida['score_final'] = 0
        return self

    def empaquetar_datos(self):
        """Retorna los resultados depurados junto a la lista de logs"""
        return self.df_salida, self.registro_operaciones

    def exportar_al_disco(self, path_destino):
        """Escribe las salidas físicas codificando listas para compatibilidad Parquet"""
        df_escribir = self.df_salida.copy()
        for col in df_escribir.columns:
            if col.endswith('_coleccion'):
                df_escribir[col] = df_escribir[col].apply(json.dumps)

        df_escribir.to_parquet(path_destino, index=False)
        self.emitir_log(f"Exportación Parquet finalizada en: {path_destino}")

        path_bitacora = path_destino.replace('.parquet', '_logs.json')
        with open(path_bitacora, 'w') as archivo:
            json.dump(self.registro_operaciones, archivo, indent=2)
        return self

"""# ETAPA 4: PROCESAMIENTO ACTIVO"""

print("■" * 70)
print("⚙️  INICIANDO PIPELINE DE FLUJO DE DATOS")
print("■" * 70 + "\n")

# Instancia del procesador alternativo
procesador_sistema = SteamDataProcessor(df_origen)

# Encadenamiento estructurado del flujo
procesador_sistema \
    .limpiar_precios_base() \
    .segmentar_opiniones() \
    .estructurar_lineas_temporales() \
    .deserializar_arreglos('genre') \
    .deserializar_arreglos('popular_tags') \
    .deserializar_arreglos('languages') \
    .imputar_valores_faltantes() \
    .definir_variable_target()

# Desempaquetado de objetos limpios
datos_depurados, logs_auditoria = procesador_sistema.empaquetar_datos()

print("\n" + "■" * 70)
print("✨ FLUJO DE DATOS EJECUTADO CON ÉXITO")
print("■" * 70)
print(f"\n📊 Sumario operativo:")
print(f"   → Filas limpias obtenidas: {len(datos_depurados):,}")
print(f"   → Columnas generadas del motor: {len(datos_depurados.columns)}")
print(f"   → Operaciones en cola resueltas: {len(logs_auditoria)}")
print(f"   → Peso asignado en memoria RAM: {datos_depurados.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

print("\n👀 Datos procesados resultantes:")
display(datos_depurados.head())

"""# ETAPA 5: ALMACENAMIENTO DE SEGURIDAD"""

print("\n" + "■" * 70)
print("💾 ALMACENANDO EN UNIDADES DE DRIVE")
print("■" * 70 + "\n")

PATH_RAIZ = '/content/drive/MyDrive/steam_analytics_system/'
destino_parquet = PATH_RAIZ + 'steam_processed_dataset.parquet'
destino_csv = PATH_RAIZ + 'steam_processed_dataset.csv'

# Guardado físico en disco
procesador_sistema.exportar_al_disco(destino_parquet)
datos_depurados.to_csv(destino_csv, index=False)

print(f"\n📁 Rutas de almacenamiento del sistema: {PATH_RAIZ}")
print(f"   → [OK] Parquet Motor: steam_processed_dataset.parquet")
print(f"   → [OK] CSV Backup: steam_processed_dataset.csv")
print(f"   → [OK] Auditoría Logs: steam_processed_dataset_logs.json")

"""# ETAPA 6: GENERACIÓN DEL REPORTE VISUAL"""

print("\n" + "■" * 70)
print("📊 COMPILANDO DASHBOARD DE CONTROL GRÁFICO")
print("■" * 70 + "\n")

plt.style.use('seaborn-v0_8-darkgrid')

lienzo, ((panel1, panel2), (panel3, panel4)) = plt.subplots(2, 2, figsize=(16, 11))
lienzo.suptitle('📊 DASHBOARD DE RENDIMIENTO - INFRAESTRUCTURA STEAM', fontsize=16, fontweight='bold', color='#1a2530')

# Subplot 1: Precios de venta base
precios_filtrados = datos_depurados[datos_depurados['precio_base'] < 100]['precio_base'].dropna()
panel1.hist(precios_filtrados, bins=40, edgecolor='#0f171e', alpha=0.8, color='#1f77b4')
panel1.set_title('💰 Distribución Comercial de Precios (< $100)', fontsize=12, fontweight='bold')
panel1.set_xlabel('Valor de Venta Comercial (USD)')
panel1.set_ylabel('Frecuencia Absoluta')
panel1.axvline(precios_filtrados.median(), color='#d62728', linestyle='--', linewidth=2, label=f'Mediana: ${precios_filtrados.median():.2f}')
panel1.legend()

# Subplot 2: Target (Score)
if 'score_final' in datos_depurados.columns:
    panel2.hist(datos_depurados['score_final'].dropna(), bins=30, edgecolor='#0f171e', alpha=0.8, color='#2ca02c')
    panel2.set_title('⭐ Comportamiento del Score Ponderado', fontsize=12, fontweight='bold')
    panel2.set_xlabel('Índice Escalado Normalizado (0-100)')
    panel2.set_ylabel('Densidad de Registros')

# Subplot 3: Lanzamientos temporales anuales
conteo_temporal = datos_depurados['año_publicacion'].value_counts().sort_index()
conteo_temporal_filtrado = conteo_temporal[conteo_temporal.index >= 1995]
panel3.bar(conteo_temporal_filtrado.index, conteo_temporal_filtrado.values, alpha=0.8, color='#ff7f0e', edgecolor='#0f171e')
panel3.set_title('📅 Histórico de Lanzamientos Anuales', fontsize=12, fontweight='bold')
panel3.set_xlabel('Año Registrado')
panel3.set_ylabel('Volumen de Publicaciones')
panel3.set_xticks(conteo_temporal_filtrado.index[::2])
panel3.tick_params(axis='x', rotation=45)

# Subplot 4: Distribución de las 10 categorías de géneros dominantes
if 'genre_coleccion' in datos_depurados.columns:
    lista_maestra_generos = []
    for sublista in datos_depurados['genre_coleccion'].dropna():
        lista_maestra_generos.extend(sublista)

    frecuencia_generos = dict(Counter(lista_maestra_generos).most_common(10))
    paleta_colores = plt.cm.GnBu(np.linspace(0.4, 0.9, 10))
    panel4.barh(list(frecuencia_generos.keys()), list(frecuencia_generos.values()), color=paleta_colores, edgecolor='#0f171e')
    panel4.set_title('🎮 Frecuencia de los Top 10 Géneros', fontsize=12, fontweight='bold')
    panel4.set_xlabel('Presencia Mapeada en Dataset')
    panel4.invert_yaxis()

plt.tight_layout()
plt.savefig(PATH_RAIZ + 'analytics_dashboard.png', dpi=150, bbox_inches='tight')
plt.show()

print(f"✅ Imagen del reporte gráfico guardada en: {PATH_RAIZ}analytics_dashboard.png")
print("\n" + "■" * 70)
print("🎉 ¡SISTEMA OPERATIVO FINALIZADO INTEGRALMENTE!")
print("■" * 70 + "\n")