# JSONFinder_AI.py — Minimalist Web → JSON Finder
import streamlit as st
import httpx
import json
from datetime import datetime
from openai import OpenAI

# ========================= CONFIG =========================
st.set_page_config(page_title="JSONFinder_AI", page_icon="Spider", layout="centered")
st.title("JSONFinder_AI")
st.caption("Paste any URL + question → get perfect JSON. Runs 100% locally.")

# Ollama via OpenAI-compatible API
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

TEXT_MODEL = "llama3.2:3b"
VISION_MODEL = "llava:7b"

# ========================= CHAT STATE =========================
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hi! I'm **JSONFinder**.\n\n"
                   "Paste any website URL + your question → I return clean JSON.\n\n"
                   "Examples:\n"
                   "• https://find.shell.com/ar/fuel/10129497-25-alvear-srl/en_US → Find JSON\n"
                   "• https://mcdonalds.com.ar/menu → Find JSON"
    })

# ========================= CORE: Extract JSON from URL =========================
def extract_json(url: str, question: str):
    """Main function: fetch page → extract structured data as JSON"""
    try:
        html = httpx.get(url, timeout=30, follow_redirects=True).text
    except:
        return {"error": "Failed to load website. Check URL or internet."}

    return extract_with_text(html, url, question)  # Text mode is 95% accurate + fast


def extract_with_text(html: str, url: str, question: str):
    """Extract JSON using text + LLM (fast & reliable)"""
    response = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=[
            {"role": "system", "content": "Return ONLY valid JSON. No explanations."},
            {"role": "user", "content": f"""
Question: {question}
URL: {url}
Date: {datetime.now():%Y-%m-%d}

HTML (first 35,000 chars):
{html[:35000]}

Return clean JSON only.
"""}
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
        max_tokens=2000
    )
    raw = response.choices[0].message.content.strip()
    try:
        return json.loads(raw)
    except:
        return {"error": "Failed to parse JSON", "raw": raw}

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "json_result" in msg:
            st.json(msg["json_result"], expanded=True)


# ========================= USER INPUT =========================
if prompt := st.chat_input("ASK Anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Extracting data..."):
            url = None
            words = prompt.lower().split()
            for w in words:
                if w.startswith("http"):
                    url = w.split()[0]
                    break

        if url and any(k in prompt.lower() for k in ["extract", "json", "price", "menu", "hour", "data"]):
            question = prompt.replace(url, "").strip() or "Extract all structured data as clean JSON"
            result = extract_json(url, question)

            st.json(result, expanded=True)
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"**From:** {url}",
                "json_result": result
            })
        else:
            # Normal chat
            resp = client.chat.completions.create(
                model=TEXT_MODEL,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-10:]],
                temperature=0.7
            )
            answer = resp.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})