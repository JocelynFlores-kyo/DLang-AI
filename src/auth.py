# 权限管理
from pathlib import Path

class User:
    def __init__(self, name: str, department: str, rank: int):
        self.name = name
        self.department = department
        self.rank = rank

def query_with_permission(user, query, vector_db):
    # 构建过滤条件
    filter = {
        "$and": [
            {"department": {"$eq": user.department}},
            {"required_rank": {"$lte": user.rank}}
        ]
    }
    
    results = vector_db.similarity_search(
        query=query,
        filter=filter,
        k=5
    )
    return results

def check_permission(user: User, file_path: Path) -> bool:
    """检查用户是否有权访问该文件"""
    # 示例规则：
    # 1. 文件必须位于用户部门目录下
    # 2. 敏感文件需要更高权限
    if "confidential" in file_path.name:
        return user.rank >= 5
    return True