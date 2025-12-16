import os
import PyPDF2
from pyzotero import zotero

def get_pdf_file(user_id, library_type, api_key, attachment_key, file_name="chatbot_paper.pdf"):
    zot = zotero.Zotero(user_id, library_type, api_key)
    pdf_file_path = os.path.join(os.path.dirname(__file__), f"imports/{file_name}")

    if not os.path.exists(pdf_file_path):
        print(f"{pdf_file_path} not found, downloading...")
        attachment = zot.file(attachment_key)
        with open(pdf_file_path, 'wb') as f:
            f.write(attachment)
        print(f"PDF has been downloaded as '{pdf_file_path}'.")
    else:
        print(f"PDF file '{pdf_file_path}' already exists.")

    return pdf_file_path


def extract_abstract(pdf_file_path, abstract_keywords, introduction_keywords):
    reader = PyPDF2.PdfReader(open(pdf_file_path, 'rb'))
    extracted_text = ""
    found_abstract = False

    for page in reader.pages:
        text = page.extract_text()
        if not text:
            continue
        for line in text.split('\n'):
            if any(keyword in line for keyword in abstract_keywords):
                found_abstract = True
                extracted_text += line.strip() + " "
                continue
            if found_abstract:
                if any(keyword in line for keyword in introduction_keywords):
                    found_abstract = False
                    break
                extracted_text += line.strip() + " "

    return extracted_text.strip()