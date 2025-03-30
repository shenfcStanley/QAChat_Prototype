from langchain_community.document_loaders import UnstructuredPDFLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DataReader:
    def __init__(self, chunk_size=500, chunk_overlap=100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load_and_split(self, pdf_path):
        """Load and split a PDF into text chunks."""
        loader = UnstructuredPDFLoader(pdf_path, strategy="hi_res")
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
 
        split_docs = splitter.split_documents(documents)
        print('doc', len(split_docs))
        for i in range(len(split_docs)):
            doc = split_docs[i]
            page = doc.metadata.get("page", "?")
            doc.page_content = f"{doc.page_content}"

        return split_docs