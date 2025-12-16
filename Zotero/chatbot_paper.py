import os
from dotenv import load_dotenv
from pdf_utils import get_pdf_file, extract_abstract
from nlp_utils import process_text_with_spacy
from spacy import displacy

load_dotenv()

api_key = os.getenv('ZOTERO_API_KEY')
user_id = os.getenv('ZOTERO_USER_ID')
library_type = 'user'
attachment_key = os.getenv('ZOTERO_ATTACHMENT_KEY')

abstract_keywords = ["Abstract", "Summary", "Executive Summary", "Résumé", "Zusammenfassung", "Resumen", "Sinopsis", "Prólogo", "Resum", "Abstracto", "ملخص", "概要", "摘要"]
introduction_keywords = ["Introduction", "Motivation", "Background", "Rationale", "Préface", "Préambule", "Einleitung", "Introducción", "Introducció", "Introdução", "مقدمة", "序論", "引言"]

pdf_file_path = get_pdf_file(user_id, library_type, api_key, attachment_key)
extracted_text = extract_abstract(pdf_file_path, abstract_keywords, introduction_keywords)

print("Extracted Text:", extracted_text)

json_output, doc = process_text_with_spacy(extracted_text)

filename = input("Enter the name for the output file (without extension): ")
json_output_path = f"exports/{filename}.json"

with open(json_output_path, "w") as json_file:
    json_file.write(json_output)

print(f"JSON output saved to {json_output_path}")
print(json_output)

displacy.serve(doc, style="dep")