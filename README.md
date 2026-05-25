# 🚀 Agente Mistral - Asistente Inteligente para Análisis de Ventas

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1.0+-green.svg)
![Mistral AI](https://img.shields.io/badge/Mistral%20AI-Small%204-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Un agente conversacional que analiza datos de ventas usando LangChain y Mistral AI**

</div>

---

## 📋 Tabla de Contenidos

- [✨ Características](#-características)
- [🎯 Demo](#-demo)
- [📦 Requisitos Previos](#-requisitos-previos)
- [🔧 Instalación](#-instalación)
- [🚀 Uso Rápido](#-uso-rápido)
- [💬 Ejemplos de Preguntas](#-ejemplos-de-preguntas)
- [📊 Estructura del Proyecto](#-estructura-del-proyecto)
- [🔐 Configuración de API Key](#-configuración-de-api-key)
- [🐛 Solución de Problemas](#-solución-de-problemas)
- [🤝 Contribuciones](#-contribuciones)
- [📄 Licencia](#-licencia)

---

## ✨ Características

| Característica | Descripción |
|----------------|-------------|
| 🤖 **Agente Inteligente** | Usa LangChain + Mistral AI para entender lenguaje natural |
| 📊 **Limpieza Automática** | Normaliza fechas, texto, teléfonos y maneja nulos |
| 🔍 **Fuzzy Matching** | Unifica nombres similares de clientes automáticamente |
| 💰 **Cálculos Exactos** | Ejecuta código Python real (sumas, promedios, groupby) |
| 🌍 **Multipregunta** | Desde "Top 5 clientes" hasta "Ventas por país" |
| 📈 **Feature Engineering** | Crea márgenes de ganancia, flags y más |
| 🎯 **100% Español** | Interfaz y respuestas completamente en español |

---

## 🎯 Demo

```python
# Ejemplo de interacción
👤 Tú: ¿Cuál es el país con más ventas?

🤖 Bot: Según el análisis de los datos:
1. **USA** - $3,456,789.23 (34.5% del total)
2. **Spain** - $2,345,678.12 (23.4% del total)
3. **France** - $1,987,654.89 (19.8% del total)

Código utilizado:
top_paises = df.groupby('country')['sales'].sum().sort_values(ascending=False).head(3)
