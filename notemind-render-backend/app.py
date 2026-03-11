from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import openai
import os

app = Flask(__name__)
CORS(app)

# 初始化百度ERNIE客户端
openai.api_key = os.environ.get("BAIDU_API_KEY", "90bf2944e8f1859e0191a1f9d9c0c16e58f0bb48")
openai.api_base = "https://aistudio.baidu.com/llm/lmapi/v3"

@app.route('/', methods=['POST', 'OPTIONS'])
def handle_request():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.json
        image_base64 = data.get('image', '')
        prompt = data.get('prompt', '请分析这张手写笔记，提取关键知识点')
        
        if not image_base64:
            return jsonify({"success": False, "error": "No image provided"}), 400
        
        # 调用ERNIE模型（旧版API语法）
        completion = openai.ChatCompletion.create(
            model="ernie-4.5-vl-28b-a3b-thinking",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                        }
                    ]
                }
            ]
        )
        
        response = completion.choices[0].message
        
        return jsonify({
            "success": True,
            "reasoning_content": getattr(response, 'reasoning_content', ''),
            "content": response.content
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
