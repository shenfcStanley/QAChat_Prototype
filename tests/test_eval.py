from dataloader import DataReader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import LlamaCpp
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from difflib import SequenceMatcher
from process_KGEmb import ClinicalKGEmbedding
import os
import time
import csv
from datetime import datetime

os.environ["OCR_AGENT"] = "tesseract"

def find_best_sentence_and_all_context(answer, source_docs):
    best_match = ""
    best_score = 0
    best_meta = {}
    all_context = []

    for doc in source_docs:
        snippet = doc.page_content.strip()
        all_context.append(f"{snippet}")

        sentences = doc.page_content.split(". ")
        for sent in sentences:
            score = SequenceMatcher(None, sent.lower(), answer.lower()).ratio()
            if score > best_score:
                best_match = sent.strip()
                best_meta = doc.metadata
                best_score = score

    # Join snippets to form the whole context
    combined_context = ";;".join(all_context)

    return best_match, best_meta, best_score, combined_context

def shorten_sentence(text, max_words=200):
    words = text.split()
    return " ".join(words[:max_words]) + ("..." if len(words) > max_words else "")

pdf_path = "../data/HER2_Paper.pdf"
processor = DataReader(chunk_size=1000, chunk_overlap=200)
chunks = processor.load_and_split(pdf_path)

print(f"Loaded {len(chunks)} chunks from the PDF.")
print(chunks[0].page_content)  # Example output

# uncomment the following code to use MiniLM
## embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# uncomment the following code to use Bio_ClinicalBERT
## embedding_model = HuggingFaceEmbeddings(model_name="emilyalsentzer/Bio_ClinicalBERT")

## Use pre-trained Clinical Knowledge Embeddings
embedding_model = ClinicalKGEmbedding(
        mapping_csv_path="../clinical_KGEmb/new_node_map_df.csv",
        embedding_pkl_path="../clinical_KGEmb/full_h_embed_hms.pkl"
    )

# vector db
from langchain.vectorstores import FAISS
db = FAISS.from_documents(chunks, embedding_model)
retriever = db.as_retriever(search_kwargs={"k": 2})
print("Retriever:", retriever)

llm = LlamaCpp(
    model_path="../models/Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf",
    n_ctx=2048,
    temperature=0.1,
    max_tokens=512
)

custom_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant answering questions about HER2 from a scientific paper.
Use the provided context to answer the question. 
Include the exact sentence used in your answer in brackets.
Context:
{context}

Question: {question}
Answer:"""
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": custom_prompt},
    return_source_documents=True
)

with open('testdata/queries.txt', 'r', encoding='utf-8') as file:
    queries = [line.strip() for line in file]

# output evaluation file
output_path = "eval_results.csv"
fieldnames = ["query", "answer", "context", "response_time_sec"]

with open(output_path, mode="w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for query in queries:
        start_time = time.time()
        result = qa_chain.invoke(query)
        elapsed = time.time() - start_time
        answer = result["result"]
        best_sentence, meta, score, combined_context = find_best_sentence_and_all_context(answer, result["source_documents"])
        short_snippet = shorten_sentence(combined_context)

        writer.writerow({
            "query": query,
            "answer": answer,
            "context": short_snippet,
            "response_time_sec": round(elapsed, 2)
        })

print(f"\n Saved results to: {output_path}")
