# AI-Powered Analysis from Diverse Research Systems for Efficient Data Management and Evaluation

This project, developed for my bachelor thesis, explores the integration of artificial intelligence (AI) in research systems to improve data management and evaluation processes. It leverages large language models (LLMs) and natural language processing (NLP) techniques to enhance the extraction, transformation, analysis and integration of research data, facilitating efficient and scalable workflows.

## Table of Contents

- [Overview](#overview)
- [Technologies](#technologies)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [License](#License)

## Overview

The core goal of this project is to implement an AI-powered system that automates and optimizes metadata transformation and analysis across different research platforms. By leveraging NLP tools such as the spaCy module in Python and LLMs such as **Qwen2.5-1.5B-Instruct** and combining them with imperative programming techniques, the system can import research data from different platforms such as PyRAT, RSpace and Zotero then convert it into a unified structured JSON format for easier interpretation and further analysis in the interdisciplinary fields of scientific research.

- Automate metadata cleaning and conversion processes for datasets across multiple research systems.
- Integrate large language models for more accurate and context-aware data transformation.
- Improve the efficiency of managing and analyzing complex and unstructured datasets in research.
- Showcase the practical benefits of AI in data-driven research workflows.

## Technologies

- **Python**: The primary programming language used for implementation, including various libraries such as `bs4`, `requests`, `PyPDF2`, `typing`, `json`, and `pyzotero`.
- **Qwen2.5-1.5B-Instruct (LLM)**: A state-of-the-art language model fine-tuned for instruction-following tasks like data transformation and cleaning.
- **Hugging Face Transformers**: Provides access to powerful pretrained models like Qwen2.5-1.5B-Instruct.
- **Chainlit**: A framework for building and interacting with chatbots and conversational interfaces.
- **CUDA**: For GPU support, ensuring that the model runs efficiently.
- **spaCy**: A fast and efficient NLP library used for text processing tasks like tokenization, named entity recognition, and dependency parsing.

## Features

- **HTML to JSON Conversion**: The system can convert HTML code (e.g., experimental protocols) into structured JSON for easier manipulation and analysis.
- **Flexible Data Processing**: Supports various input formats and can be adapted to handle different research data types.
- **Scalable Model**: Uses the latest Qwen2.5 LLM, providing long-context support and multilingual capabilities, ideal for research environments with diverse datasets.
- **LDH Integration**: Processed metadata can be integrated to an NFDI4Health database, with full compatibility via Local Data Hub (ldh-deployment).

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/digital-medicine/ba-25-alakrach-code.git
   cd ba-25-alakrach-code
    ```
2. **Install Requirements**:
   Please ensure you have Python 3.9.10+ installed. Install dependencies with:
    ```bash
    pip install -r requirements.txt
    ```

### Usage
1. **Running PyRAT, RSpace, and Zotero Data Management**:
   To use tools such as PyRAT, RSpace, and Zotero, simply execute their respective .py scripts directly:
    ```bash
    python animals.py
    python cages.py     # same process for the other endpoints
    python SJHP3_ELISA.py
    python chatbot_paper.py
    ```
2. **Running the LLM Model**:
   For LLM-based metadata processing, use run_model.ipynb to initialize the model:
    1. Open run_model.ipynb and run the cells to launch the Docker image. (Docker must be installed on the system)
    2. Access the model interface by navigating to http://localhost:8501 in your browser.
3. **Integrating Research Data into NFDI4Health's LDH**:
   To integrate the transformed metadata into the NFDI4Health Local Data Hub (LDH), run ldh-deployment/start.sh.

### License
   The LDH component used in this project, including all code and documentation is property of the NFDI4Health group, and its usage here serves only as a research tool in this thesis. It operates under the MIT License (Copyright © 2022 Institute for Medical Informatics, Statistics and Epidemiology, University of Leipzig).
   For more details on the LDH, please refer to the other README.md within the ldh-deployment directory. Other platforms and libraries are also used in this project and are subject to their respective licenses. Please consult the documentation provided with each library for further licensing details.