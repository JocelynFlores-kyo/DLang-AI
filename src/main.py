# src/main.py
import os
from pathlib import Path
from typing import List, Dict, Any

# 导入自定义模块
from document_loader import load_document
from chunker import chunk_documents
from vectordb import VectorDB
from auth import User, check_permission

def init_system():
    """系统初始化"""
    # 创建必要目录
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    
    # 初始化向量数据库
    vector_db = VectorDB(embedding_model="all-MiniLM-L6-v2")
    return vector_db

def process_documents(user: User, vector_db: VectorDB):
    """
    文档处理全流程
    :param user: 用户对象（包含权限信息）
    :param vector_db: 向量数据库实例
    """
    # 1. 扫描文档目录
    doc_dir = Path("data/raw/") / user.department
    print(f"[DEBUG] 正在访问目录: {doc_dir.absolute()}")
    if not doc_dir.exists():
        raise FileNotFoundError(f"部门 {user.department} 无文档目录")
    
    # 2. 加载并过滤文档
    all_docs = []
    for file_path in doc_dir.glob("**/*"):
        if file_path.suffix.lower() in [".pdf", ".docx"]:
            if check_permission(user, file_path):
                # 这里是关键修改点：加载文档内容
                print(f"正在处理: {file_path.name}")  # 正确访问文件名
                docs = load_document(str(file_path))  # 返回文档字典列表
                all_docs.extend(docs)  # 添加文档内容而非文件路径

    # 调试输出
    print(f"\n成功加载 {len(all_docs)} 个文本块")
    if len(all_docs) > 0:
        # 从第一个块的元数据获取文件名
        sample_source = all_docs[0]["metadata"]["source"]
    print(f"示例文件: {Path(sample_source).name}")
    if len(all_docs) > 0:
        print("类型:", type(all_docs[0]))  # 应该输出 <class 'dict'>
        print("内容键:", all_docs[0].keys())  # 应该输出 dict_keys(['text', 'metadata'])
    else:
        print("没有加载到任何文档内容")

    if not all_docs:
        raise FileNotFoundError(f"目录 {doc_dir} 内无有效文档")
    
    # 3. 文本分块
    chunks = chunk_documents(all_docs)
    
    # 4. 存储到向量数据库
    vector_db.ingest(chunks, user.department)

def query_engine(user: User, vector_db: VectorDB):
    """交互式查询引擎"""
    print(f"欢迎 {user.name}（{user.department} {user.rank} 级）")
    while True:
        try:
            question = input("\n请输入问题（输入 q 退出）: ").strip()
            if question.lower() == 'q':
                break
                
            # 执行检索
            results = vector_db.search(
                query=question,
                department=user.department,
                min_rank=user.rank
            )
            
            # 处理结果
            if not results:
                print("未找到相关文档")
                continue
                
            for i, result in enumerate(results[:3]):  # 显示前3个结果
                print(f"\n结果 {i+1}:")
                print(f"- 来源文件: {result['metadata']['source']}")
                print(f"- 页码: {result['metadata']['page']}")
                print(f"- 可信度: {result['score']:.2f}")
                print(f"- 内容:\n{result['text'][:500]}...")  # 限制预览长度
                
                # 显示回溯信息
                if 'bbox' in result['metadata']:
                    bbox = [float(x) for x in result['metadata']['bbox'].split(';')]
                    print(f"- 原文位置: {bbox}")
                
        except Exception as e:
            print(f"查询出错: {str(e)}")

if __name__ == "__main__":
    # 初始化系统
    db = init_system()
    
    # 模拟用户登录（实际应替换为你的认证系统）
    test_user = User(
        name="张三",
        department="技术部门",
        rank=3
    )
    
    # 文档处理流程
    print("正在初始化文档库...")
    process_documents(test_user, db)
    
    # 启动查询
    print("\n文档库就绪")
    query_engine(test_user, db)