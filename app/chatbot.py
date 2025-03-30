from dataloader import DataReader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import LlamaCpp
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from difflib import SequenceMatcher
from process_KGEmb import ClinicalKGEmbedding
import os
os.environ["OCR_AGENT"] = "tesseract"

def find_best_sentence(answer, source_docs):
    best_match = ""
    best_score = 0
    best_meta = {}

    for doc in source_docs:
        sentences = doc.page_content.split(". ")
        for sent in sentences:
            score = SequenceMatcher(None, sent.lower(), answer.lower()).ratio()
            if score > best_score:
                best_match = sent.strip()
                best_meta = doc.metadata
                best_score = score
    return best_match, best_meta, best_score

def shorten_sentence(text, max_words=30):
    words = text.split()
    return " ".join(words[:max_words]) + ("..." if len(words) > max_words else "")

pdf_path = "data/HER2_Paper.pdf"
processor = DataReader(chunk_size=1000, chunk_overlap=200)
chunks = processor.load_and_split(pdf_path)

print(f"Loaded {len(chunks)} chunks from the PDF.")
print(chunks[0].page_content)  # Example output


#!embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# Or better: use a clinical embedding like `Bio_ClinicalBERT`
#!embedding_model = HuggingFaceEmbeddings(model_name="emilyalsentzer/Bio_ClinicalBERT")
embedding_model = ClinicalKGEmbedding(
        mapping_csv_path="clinical_KGEmb/new_node_map_df.csv",
        embedding_pkl_path="clinical_KGEmb/full_h_embed_hms.pkl"
    )

# Build vector store
from langchain.vectorstores import FAISS
db = FAISS.from_documents(chunks, embedding_model)
retriever = db.as_retriever(search_kwargs={"k": 4})
print("Retriever:", retriever)

llm = LlamaCpp(
    #model_path="models/llama-2-7b.Q4_K_M.gguf",
    model_path="models/Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf",
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


query = "What is the role of HER2 in breast cancer?"
result = qa_chain.invoke(query)
# print('Result:', result['result'])

# print("\References:")
# for doc in result["source_documents"]:
#     print(f"- Page {doc.metadata.get('page', '?')} from {doc.metadata.get('source', 'unknown')}")

best_sentence, meta, score = find_best_sentence(result["result"], result["source_documents"])
short_snippet = shorten_sentence(best_sentence)

print("Answer:\n")
print(result["result"])

# print("\nSupporting Sentence (shortened):\n")
# print(f'"{short_snippet}" [Page {meta.get("page", "?")}] (Similarity: {score:.2f})')

print("\n Source Evidence from Paper:")
print('len of souce_doc', len(result["source_documents"]))
for i, doc in enumerate(result["source_documents"], start=1):
    page = doc.metadata.get("page", "?")
    snippet = doc.page_content[:400].strip()
    print(f'{i}. " {snippet}..."')
    print()
