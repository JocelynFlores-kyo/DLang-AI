class User:
    def __init__(self, department, rank):
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