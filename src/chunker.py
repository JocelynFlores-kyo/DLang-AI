from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_documents(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        add_start_index=True
    )
    
    chunks = []
    for doc in docs:
        texts = text_splitter.split_text(doc.text)
        for text in texts:
            chunks.append({
                "text": text,
                "metadata": {
                    "source": doc.metadata["source"],
                    "page": doc.metadata["page"],
                    "bbox": doc.metadata.get("bbox", [])
                }
            })
    return chunks