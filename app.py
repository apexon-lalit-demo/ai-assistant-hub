"""AI Assistant Hub â€” Simple AI-powered web application using AWS Bedrock (Claude)."""

import os
import json
import boto3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Bedrock client
REGION = os.environ.get("AWS_REGION", "us-east-1")
MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "us.amazon.nova-micro-v1:0")


def call_bedrock(system_prompt: str, user_message: str, max_tokens: int = 1000) -> str:
    """Call AWS Bedrock with a system prompt and user message."""
    try:
        bedrock = boto3.client("bedrock-runtime", region_name=REGION)
        response = bedrock.converse(
            modelId=MODEL_ID,
            system=[{"text": system_prompt}],
            messages=[{"role": "user", "content": [{"text": user_message}]}],
            inferenceConfig={"maxTokens": max_tokens, "temperature": 0.7},
        )
        return response["output"]["message"]["content"][0]["text"]
    except Exception as e:
        return f"Error: {str(e)}"


@app.route("/")
def index():
    """Home page with all AI tools."""
    return render_template("index.html")


@app.route("/api/summarize", methods=["POST"])
def summarize():
    """Summarize text."""
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    system = "You are a concise summarizer. Provide a clear, brief summary of the given text in 2-3 sentences."
    result = call_bedrock(system, f"Summarize this:\n\n{text}")
    return jsonify({"result": result})


@app.route("/api/explain-code", methods=["POST"])
def explain_code():
    """Explain code in plain English."""
    data = request.json
    code = data.get("code", "")
    language = data.get("language", "")
    if not code:
        return jsonify({"error": "No code provided"}), 400

    system = "You are a friendly code explainer. Explain the given code in simple, plain English. Be concise but thorough."
    prompt = f"Explain this {language} code:\n\n```{language}\n{code}\n```"
    result = call_bedrock(system, prompt)
    return jsonify({"result": result})


@app.route("/api/write-email", methods=["POST"])
def write_email():
    """Generate a professional email."""
    data = request.json
    topic = data.get("topic", "")
    tone = data.get("tone", "professional")
    recipient = data.get("recipient", "colleague")
    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    system = f"You are an email writing assistant. Write a {tone} email to a {recipient}. Include subject line, greeting, body, and sign-off."
    result = call_bedrock(system, f"Write an email about: {topic}")
    return jsonify({"result": result})


@app.route("/api/chat", methods=["POST"])
def chat():
    """Simple conversational AI."""
    data = request.json
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "No message provided"}), 400

    system = "You are a helpful, friendly AI assistant. Keep responses concise and useful."
    result = call_bedrock(system, message)
    return jsonify({"result": result})


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "ai-assistant-hub"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
