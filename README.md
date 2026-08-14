# AI Intelligence Pipeline

An end-to-end AI intelligence pipeline that automatically discovers, extracts, and categorizes the latest AI research papers from arXiv. It features a robust Python/FastAPI backend and a premium glassmorphism dashboard built with modern HTML/CSS/JS.

## Features

- **Automated Data Ingestion:** Uses the official arXiv API to fetch the latest papers in `cs.AI`.
- **FastAPI Backend:** A lightweight, high-performance API that serves the data and caches results to avoid rate limiting.
- **AI Categorization (Simulated):** A modular `LLMOrchestrator` ready to be hooked up to an LLM (currently uses rule-based string matching).
- **Premium Frontend:** A highly polished, responsive web dashboard with live search, filtering, and micro-animations.

## Local Setup

### 1. Create a Virtual Environment

It is recommended to run the project in a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Run the Application

You can start the backend and frontend simultaneously using the provided run script:

```bash
python run.py
```

*Note: The server will start on `http://0.0.0.0:10000`. Open `http://localhost:10000` in your web browser to view the dashboard!*

## Deployment

This project is configured to be deployed on Render via the included `render.yaml` configuration file. It will automatically install dependencies and start the uvicorn server.
