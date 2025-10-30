# utils/opensearch_client.py
import requests
import json


def search_blogger_tips(query: str, top_k: int = 3) -> list:
    """
    调用阿里云 OpenSearch 检索最相关的博主建议
    """
    from config import OPENSEARCH_ENDPOINT, OPENSEARCH_APP_NAME, OPENSEARCH_ACCESS_KEY, OPENSEARCH_SECRET_KEY

    # 构造 OpenSearch 搜索请求
    # 注意：这里使用 OpenSearch 的标准 API 格式
    url = f"{OPENSEARCH_ENDPOINT}/v4/openapi/apps/{OPENSEARCH_APP_NAME}/search"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {OPENSEARCH_ACCESS_KEY}:{OPENSEARCH_SECRET_KEY}"
    }

    # 构建搜索查询
    payload = {
        "query": {
            "match": {
                "content": query  # 搜索 content 字段
            }
        },
        "fetch_fields": ["content", "title"],
        "size": top_k
    }

    try:
        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code == 200:
            results = resp.json().get("result", {}).get("items", [])
            return [item["fields"]["content"] for item in results]
        else:
            print(f"OpenSearch Error: {resp.status_code}, {resp.text}")
            return []
    except Exception as e:
        print(f"Request failed: {e}")
        return []