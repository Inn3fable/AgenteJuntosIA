import sys
from pathlib import Path

# 1. Agregar la raíz del proyecto al path de Python
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st

# 2. Configurar la página como la PRIMERA llamada de Streamlit
st.set_page_config(page_title="Asistente JuntosIA - RAG", layout="wide")

# 3. Importar los módulos del backend después de registrar la ruta raíz
from backend.factories.rag_factory import RAGFactory


# Inicialización diferida de la aplicación RAG
@st.cache_resource
def init_app():
    return RAGFactory.create_application()


app_components = init_app()
chat_controller = app_components["chat_controller"]
doc_controller = app_components["document_controller"]

st.title("🤖 Asistente de Consultas - Programa Juntos")

# Barra lateral para gestión de documentos
with st.sidebar:
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

# Estado de la conversación en Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "citations" in msg and msg["citations"]:
            with st.expander("Ver referencias y citas"):
                for cite in msg["citations"]:
                    st.caption(f"**Origen:** {cite.source} | **Página:** {cite.page if cite.page else 'N/A'}")
                    st.text(cite.content)

# Entrada de la pregunta del usuario
if prompt := st.chat_input("Escribe tu consulta aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analizando consulta y consultando documentos..."):
            response = chat_controller.ask(prompt)
            st.write(response.answer)

            if response.citations:
                with st.expander("Ver referencias y citas"):
                    for cite in response.citations:
                        st.caption(f"**Origen:** {cite.source} | **Página:** {cite.page if cite.page else 'N/A'}")
                        st.text(cite.content)

            st.session_state.messages.append({
                "role": "assistant",
                "content": response.answer,
                "citations": response.citations
            })