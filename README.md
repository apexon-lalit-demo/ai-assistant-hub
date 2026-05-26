# AI Assistant Hub

A simple AI-powered web application with 4 tools, powered by AWS Bedrock.

## Features

1. **Text Summarizer** â€” Paste any text, get a concise 2-3 sentence summary
2. **Code Explainer** â€” Paste code in any language, get plain English explanation
3. **Email Writer** â€” Provide topic and tone, get a professional email draft
4. **AI Chat** â€” General-purpose conversational AI

## Tech Stack

- Python / Flask
- AWS Bedrock (Claude / Nova)
- Gunicorn (production server)
- Docker

## Run Locally

```bash
pip install -r requirements.txt
export AWS_REGION=us-east-1
python app.py
```

Open http://localhost:8000

## Docker

```bash
docker build -t ai-assistant-hub .
docker run -p 8000:8000 -e AWS_REGION=us-east-1 ai-assistant-hub
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| AWS_REGION | us-east-1 | AWS region for Bedrock |
| BEDROCK_MODEL_ID | us.amazon.nova-micro-v1:0 | Bedrock model to use |
