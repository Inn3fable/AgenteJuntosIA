# 🤝 Agente Virtual JUNTOS IA - RAG Basado en Arquitectura MVC y LangGraph
Sistema Inteligente de Asistencia Virtual basado en **RAG (Retrieval-Augmented Generation)** y **Grafos de Estado con LangGraph**, diseñado bajo el patrón de arquitectura **MVC (Modelo-Vista-Controlador)** para atender consultas operativas y procedimientos del **Programa Nacional JUNTOS (MIDIS)** a partir de sus directivas técnicas y documentos normativos oficiales.
---
## 📌 Visión General del Proyecto
El sistema automatiza el proceso de consultas y la resolución de dudas sobre los trámites del Programa JUNTOS (tales como la actualización de información de hogares, afiliación, desafiliación y gestión de transferencias). Combina modelos de embeddings locales de alto rendimiento, un LLM generativo avanzado (**Google Gemini**) y una orquestación de agentes con **LangGraph** para garantizar respuestas precisas, contextualizadas y fundamentadas con citas de las páginas del documento de origen.
---
## 🏗️ Arquitectura del Sistema (Patrón MVC)
El proyecto adopta un enfoque **Modelo-Vista-Controlador (MVC)** enriquecido con **Patrón Repositorio**, **Inyección de Dependencias (Factory Pattern)** y **Capas de Servicios e Interfaces**:
* **Modelo (`backend/models`):** Define los esquemas de datos del dominio (`agent_state.py`, `document.py`, `chat_response.py`, `citation.py`, `triage.py`, `user.py`).
* **Vista (`frontend`):** Interfaz web interactiva construida con **Streamlit** (`app.py`), encargada del renderizado del chat y la interacción con el usuario final.
* **Controladores (`backend/controllers`):** Orquestan las peticiones entre la Vista y los Servicios del Backend (`chat_controller.py`, `document_controller.py`).
* **Servicios e Interfaces (`backend/services` & `backend/interfaces`):** Lógica de negocio (indexación, embeddings, LLM, triaje, orquestación RAG).
* **Repositorios (`backend/repositories`):** Capa de abstracción para la gestión de persistencia vectorial en FAISS y documentos.
* **Grafo de Estado (`backend/graph`):** Define los nodos, clasificadores y rutas de decisión condicionales bajo **LangGraph**.
---
## 📐 Flujo del Agente RAG (LangGraph)
El procesamiento de las consultas sigue el flujo condicional representado:
![Diagrama del Modelo RAG](https://raw.githubusercontent.com/Inn3fable/AgenteJuntosIA/refs/heads/main/documents/ModeloRag.png)
### Explicación de los Nodos del Grafo:
1. **`__start__` ➔ `triaje`:** El nodo de triaje evalúa la intención de la consulta ingresada por el usuario.
2. **Evaluación de Rutas:**
   * **`AUTO_RESOLVER`:** Se activa cuando la consulta solicita procedimientos, requisitos o normativas institucionales. Redirige al nodo `auto_resolver`.
   * **`ABRIR_TIKECT`:** Se activa únicamente si el usuario solicita explícitamente atención por un asesor humano o realizar un reclamo formal. Redirige al nodo `abrir_ticket`.
   * **`PEDIR_INFO`:** Se activa si la entrada del usuario es ambigua, incompleta o requiere mayor precisión. Redirige al nodo `pedir_info`.
3. **`auto_resolver` ➔ `__end__`:** Ejecuta la búsqueda vectorial en FAISS (`index.faiss`), recupera los fragmentos normativos más relevantes, genera la respuesta mediante Gemini citando las páginas correspondientes y finaliza con estado `ok`.
---
## 📂 Estructura Completa del Proyecto

```text
.
├── backend
│   ├── config
│   │   └── settings.py                      # Configuración de variables globales
│   ├── controllers
│   │   ├── chat_controller.py               # Control de peticiones del Chat (MVC)
│   │   └── document_controller.py           # Control de procesamiento de documentos
│   ├── factories
│   │   └── rag_factory.py                   # Inyección de dependencias y ensamblado
│   ├── graph
│   │   ├── nodes.py                         # Definición de Nodos de LangGraph
│   │   ├── routers.py                       # Bordes condicionales y enrutamiento
│   │   ├── state.py                         # Definición de AgentState
│   │   └── workflow.py                      # Definición y compilación del Grafo
│   ├── interfaces                           # Abstracción e interfaces del dominio
│   │   ├── embedding_interface.py
│   │   ├── llm_interface.py
│   │   └── vector_repository_interface.py
│   ├── loaders
│   │   └── pdf_loader.py                    # Carga ultrarrápida de PDFs con PyMuPDF
│   ├── models                               # Modelos de Datos del Dominio (MVC)
│   │   ├── agent_state.py
│   │   ├── chat_response.py
│   │   ├── citation.py
│   │   ├── conversation.py
│   │   ├── document.py
│   │   ├── triage.py
│   │   └── user.py
│   ├── repositories                         # Capa de almacenamiento y persistencia
│   │   ├── document_repository.py
│   │   └── vector_repository.py             # Repositorio FAISS
│   └── services                             # Lógica de Negocio
│       ├── document_service.py
│       ├── document_state_service.py
│       ├── embedding_service.py
│       ├── indexing_service.py
│       ├── llm_service.py
│       ├── rag_service.py
│       ├── triage_service.py
│       └── workflow_service.py
├── data
│   └── documents                            # PDF normativos oficiales del Programa JUNTOS
│       ├── UOP-AFI-P01-V4_048-2026_Det_Hogares_Elegibles.pdf
│       ├── UOP-AFI-P02-V8_069-2026_Incorp_Hogares.pdf
│       ├── UOP-AFI-P03-V5_039-2026_Desafiliac_Egreso.pdf
│       ├── UOP-AFI-P04-V7_048-2026_Determinacion_PHA.pdf
│       ├── UOP-AIH-P01-V10_1_109-2026_ActualizInfoHogInter.pdf
│       ├── UOP-GPA-P01-V7_121-2026_GestionCtasLiquidyTransfIM.pdf
│       └── UOP-GPA-P02-V4_103-2026_RecuperacionAbonos.pdf
├── documents                                # Material gráfico y audiovisual del proyecto
│   ├── Captura2.PNG
│   ├── Capture.PNG
│   ├── ModeloRag.png
│   └── Presentación1.mp4
├── frontend
│   ├── app.py                               # Interfaz principal Streamlit (Vista MVC)
│   └── app_1.py
├── tests                                    # Pruebas unitarias de Nodos, Estado y Grafo
│   ├── test_document_adapter.py
│   ├── test_nodes.py
│   ├── test_routers.py
│   ├── test_state.py
│   └── test_workflow.py
├── vectorstore                              # Base vectorial persistente
│   ├── file_hashes.json
│   ├── index.faiss
│   └── index.pkl
├── .env                                     # Variables de entorno local
├── README.md
└── requirements.txt                         # Dependencias del proyecto
```
---
🛠️ Tecnologías Utilizadas
    Lenguaje: Python 3.10+
    Arquitectura: MVC + Clean Architecture + Factory Pattern
    Orquestador de Agentes: LangGraph, LangChain
    Modelo LLM: Google Gemini (gemini-3.1-flash-lite)
    Modelo de Embeddings: BAAI/bge-m3 (vía HuggingFace / SentenceTransformers)
    Vector Store: FAISS (index.faiss)
    Lector PDF: PyMuPDF (fitz)
    Frontend: Streamlit
    Pruebas: Pytest
---
💻 Guía Paso a Paso: Instalación, Ejecución y Pruebas
1. Clonar el Repositorio Git
```bash
git clone [https://github.com/Inn3fable/AgenteJuntosIA](https://github.com/Inn3fable/AgenteJuntosIA)
```
```bash
cd AgenteJuntosIA
```
2. Crear el Entorno Virtual
```bash
python3 -m venv .AgenteJuntosIA-env
```
3. Activar el Entorno Virtual
# Para Linux / macOS:
```bash
source .AgenteJuntosIA-env/bin/activate
```
# Para Windows (PowerShell / CMD):
# .AgenteJuntosIA-env\Scripts\activate
4. Actualizar Pip e Instalar Dependencias
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
5. Configurar el Archivo de Variables de Entorno (.env)
Crea un archivo llamado .env en el directorio raíz ejecutando:
```bash
cat <<EOT> .env
GEMINI_API_KEY=tu_api_key_de_gemini_aqui
```
(Reemplaza tu_api_key_de_gemini_aqui con tu API Key real de Google AI Studio).
6. Ejecutar la Suite de Pruebas Unitarias
Para verificar el funcionamiento de los nodos, estado, enrutadores y componentes del backend:
```bash
pytest tests/
```
7. Iniciar la Aplicación Frontend (Streamlit)
```bash
python -m streamlit run frontend/app.py
```
---
Abre en tu navegador la dirección indicada en la consola (por defecto: http://localhost:8501).
🚀 Guía Paso a Paso: Despliegue (Deploy) en Streamlit Community Cloud
Paso 1: Subir Cambios al Repositorio Git

Asegúrate de publicar tus últimos cambios en tu repositorio remoto en GitHub ejecutando:
```bash
git add .
git commit -m "feat: configuracion lista para despliegue en streamlit cloud"
git push origin main
```
Paso 2: Crear la Aplicación en Streamlit Cloud
    Accede a share.streamlit.io e inicia sesión con tu cuenta de GitHub.
    Haz clic en el botón "New app".
    Configura los datos del despliegue:
        Repository: tu-usuario/AgenteJuntosIA
        Branch: main
        Main file path: frontend/app.py
Paso 3: Configurar Secretos del Servidor (Secrets)
    Antes de realizar el despliegue, abre el menú Advanced settings ➔ Secrets.
    Ingresa tus credenciales en formato TOML:
```bash
Ini, TOML
GEMINI_API_KEY = "tu_api_key_de_gemini_aqui"
```
    Haz clic en Deploy!. Streamlit compilará e instalará automáticamente todas las dependencias definidas en requirements.txt y lanzará la aplicación de forma pública.

## 🎥 Demostración del Aplicativo

Puedes visualizar el funcionamiento en vivo del aplicativo, la interacción en la interfaz y la respuesta del grafo a través del video de demostración incluido en el proyecto:

🎬 **Video de presentación:**.
```bash
https://juntosia.streamlit.app/
```
![Demostración del aplicativo](https://raw.githubusercontent.com/Inn3fable/AgenteJuntosIA/refs/heads/main/documents/Captura2.PNG)
