from pypdf import PdfReader
import re

def load_pdf(file_path:str) -> str:
    reader=PdfReader(file_path)
    text=""

    for page in reader.pages:
        extracted=page.extract_text()
        if extracted:
            text+=extracted+" "

    text=clean_pdf_text(text)
    return text

def clean_pdf_text(text:str) -> str:
    text=re.sub(r'\n+', ' ', text)
    text=re.sub(r'\s+', ' ', text)

    return text.strip()