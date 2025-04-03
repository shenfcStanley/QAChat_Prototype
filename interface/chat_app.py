import streamlit as st
import os
from dataloader import DataReader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import LlamaCpp
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS
from difflib import SequenceMatcher
from process_KGEmb import ClinicalKGEmbedding

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


# UI

st.set_page_config(page_title="HER2 Clinical Chatbot", layout="wide")
st.title("🧬 HER2 Q&A Chatbot")

with st.sidebar:
    st.markdown("### Embedding Model")
    embed_choice = st.selectbox(
        "Choose embedding model:",
        [
            "MiniLM (general-purpose)",
            "Bio_ClinicalBERT (clinical-specific)",
            "ClinicalGraph (structured concept knowledge)"
        ]
    )

    st.markdown("---")
    st.markdown("---")

    st.markdown("### Author Info")
    st.markdown("""
**Name:** Feichen Shen  
**Email:** shenfeichen1102@gmail.com  
[LinkedIn](https://www.linkedin.com/in/feichen-shen-ph-d-famia-9336b895/)  
[GitHub](https://github.com/shenfcStanley/QAChat_Prototype/tree/main)
""")


@st.cache_resource
def load_chain(embed_choice):
    pdf_path = "../data/HER2_Paper.pdf"
    processor = DataReader(chunk_size=1000, chunk_overlap=200)
    chunks = processor.load_and_split(pdf_path)

    # Select embedding model
    if "Bio_ClinicalBERT" in embed_choice:
        embedding_model = HuggingFaceEmbeddings(model_name="emilyalsentzer/Bio_ClinicalBERT")
    elif "ClinicalGraph" in embed_choice:
        embedding_model = ClinicalKGEmbedding(
            mapping_csv_path="../clinical_KGEmb/new_node_map_df.csv",
            embedding_pkl_path="../clinical_KGEmb/full_h_embed_hms.pkl"
        )
    else:
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    db = FAISS.from_documents(chunks, embedding_model)
    retriever = db.as_retriever(search_kwargs={"k": 4})

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

    return qa_chain

qa_chain = load_chain(embed_choice)

query = st.text_input("💬 Ask a question about the HER2 paper:")

if query:
    with st.spinner("Thinking..."):
        result = qa_chain.invoke(query)
        best_sentence, meta, score = find_best_sentence(result["result"], result["source_documents"])
        short_snippet = shorten_sentence(best_sentence)

        st.markdown("### Answer")
        st.write(result["result"])

        st.markdown("### Source Evidence from the Paper")
        for i, doc in enumerate(result["source_documents"], start=1):
            snippet = doc.page_content.strip()[:400]
            st.markdown(f"**{i}. **")
            st.markdown(f'> "{snippet}..."')

