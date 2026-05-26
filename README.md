# 🚀 Agente Mistral - Asistente Inteligente para Análisis de Ventas con RAG

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-1.3.1-green.svg)
![Mistral AI](https://img.shields.io/badge/Mistral%20AI-Small%204-purple.svg)
![RAG](https://img.shields.io/badge/RAG-Activado-orange.svg)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Store-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Un agente conversacional con búsqueda semántica (RAG) que analiza datos de ventas usando LangChain y Mistral AI**

</div>

---

## 📋 Tabla de Contenidos

- [✨ Novedades (v2.0)](#-novedades-v20)
- [🎯 Características Principales](#-características-principales)
- [🔍 Sistema RAG Implementado](#-sistema-rag-implementado)
- [🎥 Demo](#-demo)
- [📦 Requisitos Previos](#-requisitos-previos)
- [🔧 Instalación](#-instalación)
- [🚀 Uso Rápido](#-uso-rápido)
- [💬 Ejemplos de Preguntas](#-ejemplos-de-preguntas)
- [🛠 Comandos Interactivos](#-comandos-interactivos)
- [📊 Estructura del Proyecto](#-estructura-del-proyecto)
- [🔐 Configuración de API Key](#-configuración-de-api-key)
- [🐛 Solución de Problemas](#-solución-de-problemas)
- [📈 Comparativa de Versiones](#-comparativa-de-versiones)
- [🤝 Contribuciones](#-contribuciones)
- [📄 Licencia](#-licencia)

---

## ✨ Novedades (v2.0)

### 🎉 Sistema RAG Implementado

| Característica | Descripción |
|----------------|-------------|
| 🔍 **Búsqueda Semántica** | Encuentra documentos relevantes usando embeddings multilingües |
| 🗂️ **Vector Store FAISS** | Indexación eficiente de 2,823+ documentos |
| 🌍 **Embeddings Multilingües** | Modelo `paraphrase-multilingual-MiniLM-L12-v2` con soporte español |
| 🎛️ **Control Dinámico** | Activa/desactiva RAG con comandos (`rag_on` / `rag_off`) |
| 📊 **Contexto Enriquecido** | Las preguntas se combinan con documentos semánticamente similares |
| ⚡ **Rendimiento Optimizado** | Búsqueda rápida con índices FAISS |

---

## 🎯 Características Principales

| Característica | v1.0 | v2.0 (Actual) |
|----------------|------|----------------|
| 🤖 **Agente LangChain** | ✅ | ✅ |
| 📊 **Limpieza Automática** | ✅ | ✅ |
| 🔍 **Fuzzy Matching** | ✅ | ✅ |
| 💰 **Cálculos Exactos** | ✅ | ✅ |
| 🌍 **Español 100%** | ✅ | ✅ |
| 🔎 **Búsqueda Semántica (RAG)** | ❌ | ✅ |
| 🗂️ **Vector Store FAISS** | ❌ | ✅ |
| 🎛️ **Control RAG Dinámico** | ❌ | ✅ |
| 📈 **Contexto Enriquecido** | ❌ | ✅ |
| 🚀 **Mayor Precisión** | Buena | **Excelente** |

---

## 🔍 Sistema RAG Implementado

### ¿Cómo funciona el RAG en este proyecto?
=======================================================
   🤖 SALES BOT - LANGCHAIN + MISTRAL + RAG
=======================================================

👤 Tú: info

📊 Información del dataset:
   • Filas: 2,823
   • Columnas: 26
   • 💰 Ventas totales: $10,032,628.85
   • 🌎 Países: 19
   • 👥 Clientes: 91
   • 🔍 RAG: ACTIVADO

👤 Tú: ¿Cuál es el país con más ventas?

🤖 Bot: 🔍 [RAG] Procesando consulta...
🔍 Buscando documentos relevantes...
📄 Encontrados 3 documentos con relevancia >0.65

Analizando datos con el DataFrame 'df':

El país con más ventas es **USA** con un total de $3,456,789.23

Código utilizado:
```python
top_pais = df.groupby('country')['sales'].sum().sort_values(ascending=False).head(1)
