import sys
from pathlib import Path

# Registrar la ruta raíz
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st

# 1. Configuración de la página
st.set_page_config(page_title="Asistente JuntosIA - RAG", layout="wide")

# Rutas para los assets
ASSETS_DIR = Path(__file__).resolve().parent / "assets"
LOGO_PATH = ASSETS_DIR / "logo_juntos.png"

# 2. Importar módulos backend
from backend.factories.rag_factory import RAGFactory


def get_cite_attr(cite, attr, default="N/A"):
    if isinstance(cite, dict):
        return cite.get(attr, default)
    return getattr(cite, attr, default)


# ----------------------------------------------------------------------
# INICIALIZACIÓN SILENCIOSA DEL BACKEND AL ARRANCAR LA APLICACIÓN
# ----------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_rag_components():
    return RAGFactory.create_application()


# Se fuerza la carga a la memoria RAM inmediatamente al abrir la página
if "app_components" not in st.session_state:
    st.session_state.app_components = load_rag_components()

chat_controller = st.session_state.app_components["chat_controller"]
doc_controller = st.session_state.app_components["document_controller"]

# 3. Estilos CSS Institucionales
st.markdown("""
    <style>
    .main-title {
        color: #0B2F64;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0px;
    }
    .sub-header {
        color: #555555;
        font-size: 1.05rem;
        margin-top: 5px;
        margin-bottom: 10px;
    }
    .midis-bar {
        height: 6px;
        background: linear-gradient(90deg, #D92938 0%, #D92938 33%, #FFC107 33%, #FFC107 66%, #0B2F64 66%, #0B2F64 100%);
        border-radius: 3px;
        margin-top: 8px;
        margin-bottom: 20px;
    }
    .welcome-banner {
        background-color: #F8F9FA;
        border-left: 5px solid #D92938;
        border-right: 3px solid #FFC107;
        padding: 15px 20px;
        border-radius: 6px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .info-box-blue {
        background-color: #FFFFFF;
        border-left: 4px solid #0B2F64;
        padding: 10px 12px;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        font-size: 0.88rem;
        color: #333;
    }
    .info-box-red {
        background-color: #FFFFFF;
        border-left: 4px solid #D92938;
        padding: 10px 12px;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        font-size: 0.88rem;
        color: #333;
    }
    .info-box-yellow {
        background-color: #FFFDF0;
        border-left: 4px solid #FFC107;
        padding: 10px 12px;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        font-size: 0.88rem;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# 4. Encabezado principal
st.markdown("<h1 class='main-title'>🤖 Asistente Virtual del Programa JUNTOS</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='sub-header'>Consulte dudas sobre el Procedimiento de Actualización de Información de Hogares (V10 - 2026).</p>",
    unsafe_allow_html=True)
st.markdown("<div class='midis-bar'></div>", unsafe_allow_html=True)

# Bienvenida
st.markdown("""
    <div class='welcome-banner'>
        <h3 style='color: #0B2F64; margin-top:0px; margin-bottom: 5px;'>¡Bienvenido al Sistema de Consultas JuntosIA! 👋</h3>
        <p style='color: #555; margin-bottom: 0px;'>Estoy listo para ayudarte con información normativa, siglas y procedimientos operativos del Programa JUNTOS. Escribe tu pregunta abajo para comenzar.</p>
    </div>
""", unsafe_allow_html=True)

# Inicializar historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "¡Hola! Soy tu asistente JuntosIA del programa JUNTOS. ¿En qué puedo ayudarte hoy sobre normativas, siglas o procedimientos?",
            "citations": []
        }
    ]

# 5. Barra lateral (Sidebar)
with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)

    st.header("🔴 JUNTOSIA")
    st.markdown("<div class='midis-bar'></div>", unsafe_allow_html=True)

    if st.button("🗑️ Limpiar Conversación", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "¡Hola! Soy tu asistente JuntosIA del programa JUNTOS. ¿En qué puedo ayudarte hoy sobre normativas, siglas o procedimientos?",
                "citations": []
            }
        ]
        st.rerun()

    st.divider()

    st.subheader("🎯 Objetivo del Agente")
    st.markdown("""
    <div class='info-box-blue'>
        <b>¿Qué hace este agente?</b><br>
        Responde consultas normativas y operativas sobre el <b>Procedimiento de Actualización de Información de Hogares (UOP-AIH)</b> y conceptos clave del Programa JUNTOS.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box-yellow'>
        <b>💡 Sugerencia rápida:</b><br>
        Puedes preguntar por procedimientos específicos o pedir resúmenes de normativas vigentes.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box-blue'>
        <b>Ejemplos de preguntas:</b><br>
        • ¿Qué es un Miembro Objetivo en el programa JUNTOS?<br>
        • ¿Cuál es el procedimiento para la actualización del titular?<br>
        • ¿Cuándo es un hogar elegible?<br>
        • ¿Hogar sin abono o pendiente de abono?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box-red'>
        <b>Base de Conocimiento:</b><br>
        • Siglas y definiciones (EATO, MO, CSE, PHA, RIS, SITC, etc.)<br>
        • Procedimientos de Afiliación, actualización e información de pagaduría
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.header("📄 Documentos de Conocimiento")
    uploaded_file = st.file_uploader("Subir documento PDF", type=["pdf"])
    if uploaded_file is not None:
        if st.button("Procesar e Indexar"):
            with st.spinner("Guardando e indexando documento..."):
                doc_controller.upload_document(uploaded_file)
                st.success("Documento cargado e indexado exitosamente.")
                st.rerun()

    st.subheader("Archivos indexados:")
    docs = doc_controller.list_documents()
    if docs:
        for doc in docs:
            st.text(f"• {doc}")
    else:
        st.info("No hay documentos guardados.")

# 6. Renderizar Historial de Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "citations" in msg and msg["citations"]:
            with st.expander("Ver referencias y citas"):
                for cite in msg["citations"]:
                    source = get_cite_attr(cite, "source", "Documento")
                    page = get_cite_attr(cite, "page", "N/A")
                    content = get_cite_attr(cite, "content", "")
                    st.caption(f"**Origen:** {source} | **Página:** {page if page else 'N/A'}")
                    if content:
                        st.text(content)

# 7. Entrada de Chat Nativa (Siempre fija abajo)
prompt = st.chat_input("Escribe tu consulta aquí...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analizando consulta y consultando documentos..."):
            response = chat_controller.ask(prompt)
            st.write(response.answer)

            citations = getattr(response, "citations", []) or []

            if citations:
                with st.expander("Ver referencias y citas"):
                    for cite in citations:
                        source = get_cite_attr(cite, "source", "Documento")
                        page = get_cite_attr(cite, "page", "N/A")
                        content = get_cite_attr(cite, "content", "")
                        st.caption(f"**Origen:** {source} | **Página:** {page if page else 'N/A'}")
                        if content:
                            st.text(content)

            st.session_state.messages.append({
                "role": "assistant",
                "content": response.answer,
                "citations": citations
            })
            st.rerun()






