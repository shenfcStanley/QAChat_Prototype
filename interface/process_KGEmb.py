import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
from langchain.embeddings.base import Embeddings
from langchain.schema import Document

class ClinicalKGEmbedding(Embeddings):
    def __init__(self, mapping_csv_path, embedding_pkl_path):
        self.node_map = pd.read_csv(mapping_csv_path)
        self.embedding_matrix = pickle.load(open(embedding_pkl_path, "rb")).numpy()
        
        # fast name lookup
        self.name_to_idx = {
            row['node_name'].lower(): row['global_graph_index']
            for _, row in self.node_map.iterrows()
        }
        self.dim = self.embedding_matrix.shape[1]

    def _embed_text(self, text: str):
        text = text.lower()
        matched = [self.embedding_matrix[idx]
                   for name, idx in self.name_to_idx.items()
                   if name in text]

        if matched:
            avg_vec = np.mean(matched, axis=0)
        else:
            avg_vec = np.zeros(self.dim)

        return normalize(avg_vec.reshape(1, -1))[0]

    def embed_documents(self, texts):
        return [self._embed_text(doc.page_content if isinstance(doc, Document) else doc) for doc in texts]

    def embed_query(self, text):
        return self._embed_text(text)