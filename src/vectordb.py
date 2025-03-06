from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def store_in_vectordb(chunks):
    texts = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    
    vector_db = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas
    )
    return vector_db