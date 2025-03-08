# 文本分块器
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

def chunk_documents(docs: List[dict]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    
    chunks = []
    for doc in docs:
        # 修正点：使用字典键访问
        texts = text_splitter.split_text(doc["text"])  # 原错误行
        for text in texts:
            chunks.append({
                "text": text,
                "metadata": {
                    "source": doc["metadata"]["source"],  # 确保嵌套结构
                    "page": doc["metadata"]["page"],
                    "bbox": ";".join(f"{x:.4f}" for x in doc["metadata"].get("bbox", []))
                }
            })
    return chunks

def format_result(chunk):
    return {
        "text": chunk.text,
        "metadata": {
            "bbox": chunk.metadata.get("bbox", []),
            "pageNo": chunk.metadata["page"],
            "originalFile": chunk.metadata["source"]
        }
    }

# 处理跨页文本示例
def merge_crosspage_chunks(chunks):
    merged = []
    current = None
    for chunk in chunks:
        if current and current["page"]+1 == chunk["page"]:
            current["text"] += "\n" + chunk["text"]
            current["metadata"]["end_page"] = chunk["page"]
        else:
            if current: merged.append(current)
            current = chunk
    return merged