# Sistema Inteligente de Análisis de Reseñas con Arquitectura Multiagente

## Resumen

Este proyecto implementa una arquitectura multiagente para el análisis de sentimientos utilizando técnicas de Machine Learning, Deep Learning y Retrieval-Augmented Generation (RAG).

El sistema procesa reseñas del dataset Amazon Fine Food Reviews, compara distintos modelos de clasificación y permite realizar consultas inteligentes sobre los datos mediante Mistral AI.

---

## Objetivos

* Limpiar y preparar datos textuales para su análisis.
* Entrenar y evaluar múltiples modelos de clasificación.
* Seleccionar automáticamente el modelo con mejor desempeño.
* Implementar un sistema RAG para consultas en lenguaje natural.
* Generar respuestas basadas en evidencia recuperada del corpus.

---

## Componentes del Sistema

### Agente Normalizador

Encargado del preprocesamiento de datos.

Funciones principales:

* Eliminación de duplicados.
* Tratamiento de valores faltantes.
* Limpieza y normalización de texto.
* Construcción del dataset final.
* Balanceo de clases.

### Agente Comparador

Responsable de entrenar y evaluar diferentes algoritmos de clasificación.

Modelos evaluados:

* Regresión Logística
* LSTM
* DistilBERT

Métricas utilizadas:

* Accuracy
* Precision
* Recall
* F1-Score

El agente identifica automáticamente el modelo con mejor rendimiento.

### Agente Comunicador

Permite interactuar con el sistema mediante preguntas en lenguaje natural.

Utiliza:

* Embeddings semánticos
* ChromaDB
* RAG
* Mistral AI

Sus funciones incluyen:

* Consultas sobre el dataset.
* Resúmenes automáticos.
* Generación de reportes.
* Respuestas contextualizadas.

---

## Flujo de Trabajo

```text
Dataset Amazon Reviews
          │
          ▼
Preprocesamiento de Datos
          │
          ▼
Entrenamiento y Evaluación
          │
          ▼
Selección del Mejor Modelo
          │
          ▼
Creación del Corpus RAG
          │
          ▼
Embeddings + ChromaDB
          │
          ▼
Consultas Inteligentes con Mistral
```

---

## Herramientas y Librerías

* Python
* Pandas
* NumPy
* Scikit-Learn
* TensorFlow
* Keras
* Transformers
* DistilBERT
* Sentence Transformers
* ChromaDB
* Mistral AI
* Matplotlib
* Seaborn

---

## Dataset

**Amazon Fine Food Reviews**

Características principales:

* Más de 568.000 reseñas.
* Opiniones reales de clientes.
* Calificaciones de productos de 1 a 5 estrellas.
* Datos textuales adecuados para análisis de sentimientos.

---

## Requisitos

Instalar las dependencias necesarias:

```bash
pip install pandas numpy matplotlib seaborn
pip install scikit-learn tensorflow keras
pip install transformers torch
pip install sentence-transformers chromadb
pip install langchain-mistralai
```

---

## Configuración

Antes de ejecutar el proyecto se deben configurar las credenciales:

```python
KAGGLE_USERNAME
KAGGLE_KEY
MISTRAL_API_KEY
```

---

## Resultados

El sistema permite:

* Procesar automáticamente miles de reseñas.
* Clasificar sentimientos positivos y negativos.
* Comparar distintos enfoques de inteligencia artificial.
* Recuperar información relevante mediante RAG.
* Responder preguntas sobre el contenido del dataset.
* Generar reportes automáticos del análisis realizado.

---
