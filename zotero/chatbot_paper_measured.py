import os, time, psutil
from dotenv import load_dotenv
from pdf_utils import get_pdf_file, extract_abstract
from nlp_utils import process_text_with_spacy

load_dotenv()

process = psutil.Process(os.getpid())
memory_before = process.memory_info().rss / (1024 ** 2)
start_time = time.time()

api_key = os.getenv('ZOTERO_API_KEY')
user_id = os.getenv('ZOTERO_USER_ID')
library_type = 'user'
attachment_key = os.getenv('ZOTERO_ATTACHMENT_KEY')

abstract_keywords = ["Abstract", "Summary", "Executive Summary", "Résumé", "Zusammenfassung", "Resumen", "Sinopsis", "Prólogo", "Resum", "Abstracto", "ملخص", "概要", "摘要"]
introduction_keywords = ["Introduction", "Motivation", "Background", "Rationale", "Préface", "Préambule", "Einleitung", "Introducción", "Introducció", "Introdução", "مقدمة", "序論", "引言"]

pdf_file_path = get_pdf_file(user_id, library_type, api_key, attachment_key)
extracted_text = extract_abstract(pdf_file_path, abstract_keywords, introduction_keywords)

json_output, doc = process_text_with_spacy(extracted_text)

filename = input("Enter the name for the output file (without extension): ")
json_output_path = f"exports/{filename}.json"

with open(json_output_path, "w") as json_file:
    json_file.write(json_output)

memory_after = process.memory_info().rss / (1024 ** 2)
end_time = time.time()

print(f"Memory Usage Before: {memory_before:.2f} MB")
print(f"Memory Usage After: {memory_after:.2f} MB")
print(f"Memory Difference: {memory_after - memory_before:.2f} MB")
print(f"Response Time: {end_time - start_time:.2f} seconds")