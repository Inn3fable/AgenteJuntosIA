# 🤝 Agente Virtual JUNTOS IA - Sistema RAG con LangGraph

Sistema de Asistencia Virtual basado en **Arquitectura RAG (Retrieval-Augmented Generation)** y **Grafos de Estado Orquestados con LangGraph**, diseñado para responder consultas operativas y procedimientos del **Programa Nacional JUNTOS (MIDIS)** a partir de directivas y documentos normativos.

---

## 📌 Características Principales

* **Lógica de Decisiones basada en Grafos (LangGraph):** Implementación de un flujo de estados dinámico con nodos condicionales para triaje, auto-resolución, solicitudes de información adicional y generación de tickets.
* **Modelo LLM Eficiente:** Integración con **Google Gemini** (`gemini-3.1-flash-lite`) para clasificación rápida e inferencia precisa.
* **Vectorización Local:** Procesamiento de documentos con el modelo de embeddings multidocumento **`BAAI/bge-m3`** ejecutado localmente mediante `HuggingFaceEmbeddings`.
* **Procesamiento de Documentos Completo:** Extracción y segmentación optimizada de directivas institucionales PDF usando `PyMuPDFLoader` respetando metadatos y paginación.
* **Inyección de Dependencias (Factory Pattern):** Arquitectura limpia y desacoplada mediante `RAGFactory` para construir servicios, repositorios y nodos.
* **Interfaz Interactiva:** Frontend amigable desarrollado en **Streamlit**.

---

## 📐 Arquitectura del Sistema

El flujo de conversación sigue una estructura de grafo dirigida por decisiones:
