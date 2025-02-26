from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allow Flutter to access this API

# Replace with your Hugging Face API key
HUGGING_FACE_API_KEY = "your_hugging_face_api_key"
CODEBERT_URL = "https://api-inference.huggingface.co/models/microsoft/codebert-base"

headers = {
    "Authorization": f"Bearer {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}"
}

@app.route("/summarize", methods=["POST"])
def summarize_code():
    try:
        data = request.json
        code = data.get("code", "")

        if not code:
            return jsonify({"error": "No code provided"}), 400

        response = requests.post(CODEBERT_URL, headers=headers, json={"inputs": code})
        
        if response.status_code != 200:
            return jsonify({"error": "Error from Hugging Face API"}), 500

        summary = response.json()
        return jsonify({"summary": summary})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
