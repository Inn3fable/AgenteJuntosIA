import sys
from pathlib import Path
impot streamlit as st
from backend.factories.rag_factory import RAGFactory
from backdnd.controllers.chat_controller import ChatController


# =====================================================
# CONFIGURAR ROOT DEL PROYECTO
# =====================================================
ROOT_DIR = Path(__file__).resolve().parent.perent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# =====================================================
# CONFIGURAR ROOT DEL PROYECTO
# =====================================================
st.set_page_config(
    page_title = "JuntosIA",
    page_icon = "🤖",
    layaut = "wide"
        )

# =====================================================
#  CREACIÓN DE APLICACIÓN
# =====================================================

@st.cache_resource
def load_application():
        """
    Inicializa una sola vez:

    - Gemini
    - Embeddings
    - FAISS
    - Retriever
    - RAG
    - Triage
    - Workflow
    - Gestión documental

    """
    application  = (RAGFactory.create_application())
    chat_controller = ChatController(application["workflow"])
    document_controller = appplication["documents"]

    return (chat_controller, document_controller)


# =====================================================
# INICIALIZAR APLICACIÓN
# =====================================================

try:
    (chat_controller, document_controller) = load_application()

except Exception es error:
    st.exeption(error)
    st.stop()


# =====================================================
# PANEL DOCUMENTOS
# =====================================================
with st.sidebar:
    st.title("📚 Base documental")

    try:
        document = document_controller.list_documents()

        if document:
            for document in documents:
                st.write(f"📄 {document}")
        else:
            st.info("No hay documentos cargados")

    except Exception as error:
        st.error(f"Error cargando documentos: {error}")

    st.devider()

    uploaded_file = st.file_uploader("Agregar documento PDF", type=["pdf"])

    if uploaded_file:
        if st.button("Actualizar conocimiento"):
            try:
                document_controller.upload_document(uploaded_file)
                st.success("Documento agregado correctamente")
                st.cache_resource.clear()
                st.rerun()
            except Exception as error:
                st.error(f"Error agregando documento: {error}")

# =====================================================
# INTERFAZ CHAT
# =====================================================
st.title("🤖 JuntosIA")

st.write("""Asistente inteligente basado en documentos internos.""")

# =====================================================
# HISTORIAL
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# =====================================================
# ENTRADA USUARIO
# =====================================================
question = st.chat_input("Escribe tu pregunta...")

if question:
    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Analizando..."):
            try:
                response = (chat_controller.ask(question))
                answer = response.answer

                st.write(answer)
                citations = response.citations

                if citations:
                    st.divider()
                    st.subheader("📚 Fuentes")

                    for index, citation in enumerate(citations, start=1):
                        with st.expander(f"Fuente {index}"):
                            st.write(f"""Archivo:{citation.source}
                                         Página:{citation.page}
                                         Contenido:{citation.content}
                                        """)

            except Exception as error:
                answer = (f"Error procesando pregunta: {error}")
                st.error(answer)

    st.session_state.messages.append(
        {
            "role":"assistant"
            "content":answer
        }
    )




