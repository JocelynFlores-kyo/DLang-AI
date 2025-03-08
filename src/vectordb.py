# 向量数据库操作
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain.vectorstores import Chroma
from typing import List, Dict

class VectorDB:
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        self.embedding = HuggingFaceEmbeddings(model_name=embedding_model)
        self.db = Chroma(
            embedding_function=self.embedding,
            persist_directory="data/processed/chroma_db"
        )
    
    def ingest(self, chunks: List[Dict], collection: str):
        """存储文档块"""
        texts = [chunk["text"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        self.db.add_texts(
            texts=texts,
            metadatas=metadatas,
            collection_name=collection
        )
    
    def search(self, query: str, department: str, min_rank: int, k=5):
        """带权限的检索"""
        return self.db.similarity_search_with_relevance_scores(
            query=query,
            k=k,
            filter={
                "$and": [
                    {"department": department},
                    {"required_rank": {"$lte": min_rank}}
                ]
            }
        )