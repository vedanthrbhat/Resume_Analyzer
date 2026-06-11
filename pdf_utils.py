import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader


def extract_text_from_uploaded_pdf(uploaded_file) -> str:
    """Save an uploaded PDF to a temp file and extract its text."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getvalue())
        temp_path = tmp.name

    try:
        loader = PyPDFLoader(temp_path)
        docs = loader.load()
        return "\n\n".join(doc.page_content for doc in docs)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
