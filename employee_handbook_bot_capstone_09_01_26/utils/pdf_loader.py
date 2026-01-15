from pypdf import PdfReader 

def load_pdf(file_path:str) -> str:
    reader=PdfReader(file_path)
    text=""

    for page in reader.pages:
        extracted_page=page.extract_text()
        if extracted_page:
            text+=extracted_page+" "

    return text.strip()