import psutil
import os
import spacy
from pyzotero import zotero
import PyPDF2
import json
import time

# Measure memory usage and time before the API call
process = psutil.Process(os.getpid())
memory_before = process.memory_info().rss / (1024 ** 2)  # in MB
start_time = time.time()  # Start time for the process

# API key and user details for Zotero
api_key = 'vnYz4zH1zJlasSJitJHtCbH2'  # Zotero API key
user_id = '14549093'  # Zotero user ID
library_type = 'user'  # 'user' or 'group'

# Initialize Zotero API client
zot = zotero.Zotero(user_id, library_type, api_key)
attachment_key = '8MHTI6RA'

# Define the path to check for the file near this script
pdf_file_path = os.path.join(os.path.dirname(__file__), 'Imports/chatbot_paper.pdf')

# Check if the file already exists
if not os.path.exists(pdf_file_path):
    print(f"{pdf_file_path} not found, downloading...")
    # Fetch the attachment file from Zotero
    attachment = zot.file(attachment_key)

    # Save the file locally
    with open(pdf_file_path, 'wb') as f:
        f.write(attachment)
    print(f"PDF has been downloaded as '{pdf_file_path}'.")
else:
    print(f"PDF file '{pdf_file_path}' already exists.")

# Open and read the content of the PDF
with open(pdf_file_path, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    number_of_pages = len(reader.pages)

    # Define lists of synonyms for 'Abstract' and 'Introduction' in multiple languages
    abstract_keywords = [
        "Abstract",          # English
        "Summary",           # English
        "Executive Summary",  # English
        "Résumé",             # French
        "Zusammenfassung",   # German
        "Resumen",           # Spanish
        "Sinopsis",          # Spanish
        "Prólogo",           # Spanish
        "Resum",             # Catalan
        "Abstracto",         # Portuguese
        "ملخص",               # Arabic
        "概要",               # Japanese (Gaiyō)
        "摘要",               # Chinese (Zhaiyao)
    ]
    introduction_keywords = [
        "Introduction",      # English, French
        "Motivation",        # English
        "Background",        # English
        "Rationale",         # English
        "Préface",           # French
        "Préambule",         # French
        "Einleitung",        # German
        "Introducción",      # Spanish
        "Introducció",       # Catalan
        "Introdução",        # Portuguese
        "مقدمة",              # Arabic
        "序論",                # Japanese (Joron)
        "引言",               # Chinese (Yǐnyán)
    ]

    # Extract text and find the Abstract
    found_abstract = False
    extracted_text = ""
    for page_num in range(number_of_pages):
        page = reader.pages[page_num]
        text = page.extract_text()

        # Split the text into lines for better control
        lines = text.split('\n')

        for line in lines:
            # Check for the start of the Abstract section
            if any(keyword in line for keyword in abstract_keywords):
                found_abstract = True
                extracted_text += line.strip() + " "  # Include the line with the keyword
                continue  # Move to the next line

            # If in the abstract, append the line
            if found_abstract:
                # Stop if we reach any of the Introduction section keywords
                if any(keyword in line for keyword in introduction_keywords):
                    found_abstract = False  # Stop capturing
                    break

                extracted_text += line.strip() + " "  # Append line to the result

    extracted_text = extracted_text.strip()
    print("Extracted Text:", extracted_text)

# Initialize SpaCy
nlp = spacy.load("en_core_web_sm")

# Process the extracted text with SpaCy
doc = nlp(extracted_text)

# Prepare the output structure
nlp_output = {
    "tokens": [],
    "entities": [],
    "sentences": [],
    "noun_chunks": []
}

# Process tokens and sentences
for sent in doc.sents:
    sentence = sent.text
    nlp_output["sentences"].append({"sentence": sentence, "tokens": []})

    for token in sent:
        nlp_output["tokens"].append({"token": token.text, "pos": token.pos_})
        nlp_output["sentences"][-1]["tokens"].append({
            "token": token.text,
            "pos": token.pos_,
            "dependency": token.dep_,
            "head": token.head.text
        })

# Process entities
for ent in doc.ents:
    nlp_output["entities"].append({"text": ent.text, "type": ent.label_})

# Process noun chunks
for chunk in doc.noun_chunks:
    nlp_output["noun_chunks"].append(chunk.text)

# Convert to JSON
json_output = json.dumps(nlp_output, indent=4)

# Get the desired filename from console input
filename = input("Enter the name for the output file (without extension): ")

# Create the full path for the JSON file
json_output_path = f"Exports/{filename}.json"

# Save JSON to a file
with open(json_output_path, "w") as json_file:
    json_file.write(json_output)

# Print or save the JSON output
print(f"JSON output saved to {json_output_path}")
print(json_output)

# Measure memory usage and time after the API call
memory_after = process.memory_info().rss / (1024 ** 2)  # in MB
end_time = time.time()  # End time for the process

# Calculate the time difference
response_time = end_time - start_time

# Print the results
print(f"Memory Usage Before: {memory_before} MB")
print(f"Memory Usage After: {memory_after} MB")
print(f"Memory Difference: {memory_after - memory_before} MB")
print(f"Response Time: {response_time} seconds")

# Visualizing the dependency graph (optional)
# from spacy import displacy
# displacy.serve(doc, style="dep")
