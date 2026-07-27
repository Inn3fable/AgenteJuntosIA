from backend.adapters.document_adapter import DocumentAdapter
from backend.models.document import Document

doc = Document(
    id="1",
    content="Hola mundo",
    source="manual.pdf",
    page=2,
    metadata={
        "categoria": "manual"
    }
)

langchain_doc = DocumentAdapter.to_langchain(doc)

print(langchain_doc.page_content)
print(langchain_doc.metadata)

domain_doc = DocumentAdapter.to_domain(langchain_doc)

print(domain_doc)