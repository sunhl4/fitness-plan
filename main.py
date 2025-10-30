# main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import config
import utils.opensearch_client as opensearch
import utils.prompt_builder as prompter
import requests
import json

app = FastAPI()

# 挂载静态文件（前端页面）
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def get_form():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/generate")
async def generate_plan(request: Request):
    data = await request.json()

    # 提取用户输入
    user_info = {
        "age": data.get("age"),
        "gender": data.get("gender"),
        "height": data.get("height"),
        "weight": data.get("weight"),
        "goal": data.get("goal"),
        "experience": data.get("experience"),
        "time_per_week": data.get("time_per_week"),
        "preference": data.get("preference", "")
    }

    # 可调节权重（前端可加滑块）
    weight = float(data.get("weight", 0.7))  # 默认 0.7

    # 构造检索查询
    query = f"{user_info['age']}岁 {user_info['gender']} {user_info['goal']} {user_info['experience']}"

    # 从 OpenSearch 检索相关博主建议
    blogger_tips = opensearch.search_blogger_tips(query, top_k=3)

    # 使用我们优化的提示词构建函数
    prompt = prompter.build_fitness_prompt(user_info, blogger_tips, weight)

    # 调用通义千问 API（阿里百炼）
    headers = {
        "Authorization": f"Bearer {config.BALENG_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": config.QWEN_MODEL,
        "input": {
            "messages": [
                {"role": "user", "content": prompt}
            ]
        },
        "parameters": {
            "temperature": 0.8,
            "max_tokens": 1500
        }
    }

    try:
        resp = requests.post(config.BALENG_ENDPOINT, headers=headers, json=payload)
        if resp.status_code == 200:
            result = resp.json()
            ai_response = result["output"]["text"]
        else:
            ai_response = f"AI生成失败: {resp.status_code} {resp.text}"
    except Exception as e:
        ai_response = f"请求失败: {str(e)}"

    return {"plan": ai_response}



