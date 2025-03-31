# QAChat_Prototype

## Description
This is the take-home case study/real world problem exercise finished by **Feichen Shen**.  

In this task, a Q/A chatbot prototype was built to address diverse questions related to a specific research paper. The work also clearly presented comprehensive evaluations/testing/KPI definition and detailed how clinical network embeddings can be incorporated.

## Overall Workflow

The overall workflow is designed based on the Retrieval-Augmented Generation (RAG) architecture:
1. Query Submission
2. Knowledge (e.g., research paper) Ingestion and Indexing with Three Models
   - MiniLM for general purpose
   - Bio_ClinicalBERT for clinical purpose
   - Clinical_KGEmb for leveraging medical ontologies and clinical knowledge.  
     **Note:** incorporating the clinical knowledge embeddings research into the prototype  
     **Reference:** [Clinical-knowledge-embeddings GitHub Repository](https://github.com/mims-harvard/Clinical-knowledge-embeddings)

4. Semantic search
5. Contextual Prompt Design
6. Post-processing and Response Generation. Evidence from articles will be provided as reference resources

<img src="imgs/workflow.png" alt="Chatbot Illustration" width="550"/>

## Lessons Learned from the Clinical Knowledge Embeddings Work
**Reference:** [Clinical-knowledge-embeddings GitHub Repository](https://github.com/mims-harvard/Clinical-knowledge-embeddings)  
**Paper:** [Clinical-knowledge-embeddings Paper](https://www.medrxiv.org/content/10.1101/2024.12.03.24318322v2)

1. Three Takeaways from the Research
   - 1
   - 2
   - 3
2. Why it is important to Humana
3. How to incorporate it into the prototype (please refer to step 2 in the workflow and the codes)
## Installation Instructions  

<pre>
git clone https://github.com/shenfcStanley/QAChat_Prototype.git
cd QAChat_Prototype
pip install -r requirements.txt
</pre>

In order to use OCR for PDF parsing, you need to install tesseract here: https://tesseract-ocr.github.io/tessdoc/Installation.html. After installation, you need to add the tesseract path to the system environment

In this task, the open-source LLM model "Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf" is used, you need to download the model from the huggingface hub to the models folder, using huggingface-cli: <pre> ```huggingface-cli download NousResearch/Nous-Hermes-2-Mistral-7B-DPO-GGUF Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf --local-dir models --local-dir-use-symlinks False```</pre>

## How to Run the Codes

#### 1. To run the code locally, navigate to the `app` directory:
<pre>python chatbot.py</pre>
Three embeddings can be used: 
- a). general embeddings from all-MiniLM-L6-v2;
- b). clinical embeddings from Bio_ClinicalBERT;
- c). clinical knowledge embeddings from the research paper. The embeddings data and knowledge graph are downloaded and saved in the clinical_KGEmb folder (ref: https://github.com/mims-harvard/Clinical-knowledge-embeddings/tree/main)
#### 2. To run the Streamlit UI, go to the `interface` folder:
<pre>streamlit run chat_app.py</pre>
<img src="imgs/webapp.png" alt="Chatbot UI" width="550"/>  

#### 3. The `test_eval.py` script in the `tests` directory is used to generate answers for 16 tested queries `queries.txt` stored under `tests/testdata`.  
`Zephyr-7B-Beta` was utilized as a third-party language model for query/data augmentation and `ChatGPT-4o` was used for automated result scoring. Prompts for query augmentation and auto scoring is under `tests\prompts`

## Assumptions
See [Assumption.md](Assumption.md) for full details.

## Comprehensive Evaluation

Although I used three models to generate the initial embeddings, here I assume the Clinical-Knowledge-Embeddings yield the optimal performance overall based on the initial check, and showcase the evaluation on all 16 queries using this model to assess response accuracy, quality, evidence grounding, and response time

#### Business Metrics
- Mean response time (sec): 50.47 
- Mean LLM-based score (1-5): 4.25
- Mean Human-level score (1-5): 4.19
- Correlation between LLM scorer and human scorer: 0.91
- Acceptable Answer Rate (Human Score ≥ 4): 81.2%
- Acceptable Answer Rate (LLM ≥ 4): 87.5%



#### Example QA Pairs
| Question | Answer | Context | LLM-based Score | Human-level Score |
|----------|--------|--------------|----------|----------|
| What is HER2? | A protein... | HER2 is a protein... | 5 | 5 |
| How does HER2 ampli... |   HER2 amplification... | Picornavirions have relative ... | 4 | 3 |

See [Evaluation.md](Evaluation.md) for full details.


