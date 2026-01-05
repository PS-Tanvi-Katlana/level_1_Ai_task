# 🕸️ Web2JSON Website - Local JSON Extractor (Ollama + Streamlit)

Turn any public website into perfect structured JSON - privately, locally, and with zero API keys.

This tool fetches a webpage, analyzes its HTML using a local LLM (Ollama), and returns clean JSON such as application/ld+json, OpenGraph metadata, product data, menu items, store hours, schema.org entities, and more.

It works entirely offline - ideal for developers, scrapers, automators, or AI pipelines.

### 🚀 Features
- ✨ 100% Local & Private - Powered by Ollama, no cloud API calls
- ⚡ Fast JSON Extraction - Llama3.2:3b optimized prompts
- 🌐 Smart URL Detection - Paste any sentence containing a URL
- 📄 Beautiful JSON Output - Interactive JSON viewer
- 🧠 Dual Mode - JSON extraction + normal chat
- 📦 Lightweight - Only 4 Python dependencies
- 🖼️ Optional Vision Model - llava:7b for JS-heavy websites

### 🧩 Tech Stack
| Component     | Tool | Description |
|---------------|------|-------------|
| LLM           | [Ollama](https://ollama.ai/) | Runs Llama3.2 local models |
| Text Model    | [llama3.2:3b](https://ollama.ai/models) | Fast, accurate HTML parsing |
| Vision Model  | [llava:7b](https://ollama.ai/models) | For React/Vue/SPA extraction |
| Frontend      | [Streamlit](https://streamlit.io/) | Clean UI + chat interface |
| HTTP Client   | [httpx](https://www.python-httpx.org/) | Fetches web pages |
| AI Client     | [OpenAI SDK](https://pypi.org/project/openai/) | Connects to Ollama’s OpenAI-compatible API |

### Installation
```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/JSONFinder_AI.git
cd JSONFinder_AI

# 2. Create and activate a virtual environment
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Ollama models (for LLM)
ollama pull llama3.2:3b

# 5. ▶️ Run the App
streamlit run JSONFinder_AI.py
```

### Example Output
```bash
{
"@context":"https://schema.org"
"@type":"WebPage"
"mainEntityOfPage":{
"@type":"WebPage"
"@id":"https://find.shell.com/ar/fuel/10129497-25-alvear-srl/en_US"
}
"url":"https://find.shell.com/ar/fuel/10129497-25-alvear-srl/en_US"
"datePublished":"2025-12-04"
"name":"Shell Fuel Station - Alvear SRL"
"description":""
"image":[
0:{
"@type":"ImageObject"
"url":"/error-pages/shell-pecten.svg"
}
]
"sameAs":[
0:"https://www.shell.com/motorist.html"
]
}
```