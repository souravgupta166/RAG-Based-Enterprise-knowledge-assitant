from pathlib import Path
import fitz  # PyMuPDF
from docx import Document


def load_pdf(file_path: Path):
    text = ""

    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()

    return text


def load_docx(file_path: Path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs if p.text])


def load_txt(file_path: Path):
    return file_path.read_text(encoding="utf-8", errors="ignore")


def load_document(file_path: Path):
    ext = file_path.suffix.lower()

    if ext == ".pdf":
        return load_pdf(file_path)
    elif ext == ".docx":
        return load_docx(file_path)
    elif ext == ".txt":
        return load_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")