# QAChat_Prototype

## Description
This is the take-home case study/real world problem exercise finished by **Feichen Shen**.  
In this task, a Q/A chatbot prototype was built to address diverse questions related to a specific research paper. The work also clearly presented comprehensive evaluations/testing/KPI definition and detailed how clinical network embeddings can be incorporated.

## Overall Workflow

The overall workflow is designed based on the Retrieval-Augmented Generation (RAG) architecture:
1. Query Submission
2. Knowledge (e.g., research paper) Ingestion and Indexing
3. Semantic search
4. Contextual Prompt Design
5. Post-processing and Response Generation

<img src="imgs/workflow.png" alt="Chatbot Illustration" width="700"/>

## Installation Instructions  

git clone https://github.com/shenfcStanley/QAChat_Prototype.git  
cd QAChat_Prototype  
pip install -r requirements.txt  

In order to use OCR for PDF parsing, you need to install tesseract here: https://tesseract-ocr.github.io/tessdoc/Installation.html. After installation, you need to add the tesseract path to the system environment

In this task, the open-source LLM model "Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf" is used, you need to download the model from the huggingface hub to the models folder, using huggingface-cli: <pre> ```huggingface-cli download NousResearch/Nous-Hermes-2-Mistral-7B-DPO-GGUF Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf --local-dir models --local-dir-use-symlinks False``` </pre>

## How to Run the Code

1. To run the code, go to app, and then <pre> ```python chatbot.py``` </pre>  
Three embeddings can be used: 
- 1). general embeddings from all-MiniLM-L6-v2;
- 2). clinical embeddings from Bio_ClinicalBERT;
- 3). clinical knowledge embeddings from the research paper. The embeddings data and knowledge graph are downloaded and saved in the clinical_KGEmb folder (ref: https://github.com/mims-harvard/Clinical-knowledge-embeddings/tree/main)

2. To run the Streamlit UI, go to interface, and then <pre>```streamlit run streamlit_app.py```<pre>


