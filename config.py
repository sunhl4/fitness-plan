# config.py
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# OpenSearch 配置
OPENSEARCH_ENDPOINT = os.getenv("OPENSEARCH_ENDPOINT", "https://your-opensearch-endpoint")
OPENSEARCH_APP_NAME = os.getenv("OPENSEARCH_APP_NAME", "fitness-blogger-tips")
OPENSEARCH_ACCESS_KEY = os.getenv("OPENSEARCH_ACCESS_KEY")
OPENSEARCH_SECRET_KEY = os.getenv("OPENSEARCH_SECRET_KEY")

# 阿里百炼 API 配置
BALENG_API_KEY = os.getenv("BALENG_API_KEY")
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-max")  # 或 qwen-plus
BALENG_ENDPOINT = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"