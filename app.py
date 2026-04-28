import os
import gradio as gr
from groq import Groq
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

client     = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL_NAME = "llama-3.3-70b-versatile"

LANGUAGE_MAP = {
    "en": "English",    "fr": "French",     "es": "Spanish",
    "ar": "Arabic",     "ur": "Urdu",       "de": "German",
    "zh-cn": "Chinese", "zh-tw": "Chinese", "hi": "Hindi",
    "pt": "Portuguese", "it": "Italian",    "tr": "Turkish",
    "ru": "Russian",    "ja": "Japanese",   "ko": "Korean",
    "nl": "Dutch",      "pl": "Polish",     "fa": "Persian",
}
SUPPORTED_LANGS = sorted(set(LANGUAGE_MAP.values()))


def detect_language(text):
    try:
        if len(text.strip()) < 8:
            return "English"
        code = detect(text.strip())
        has_non_latin = any(ord(c) > 127 for c in text)
        if has_non_latin and code == "en":
            raise ValueError("wrong")
        return LANGUAGE_MAP.get(code, "English")
    except Exception:
        try:
            resp = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": f"What language is this? Reply with ONE word from: {', '.join(SUPPORTED_LANGS)}. Text: {text}"}],
                max_tokens=5, temperature=0
            )
            name = resp.choices[0].message.content.strip()
            if name in SUPPORTED_LANGS:
                return name
        except Exception:
            pass
        return "English"


def build_prompt(lang):
    return f"""You are UniLingo, a friendly multilingual university support assistant.
CRITICAL: Student writes in {lang}. Reply ONLY in {lang}. Never switch languages.
Max 3 sentences or 3 bullet points per reply.
Only answer about: study tips, assignments, university applications, exam prep, careers, international student life.
For anything else say in {lang}: "I only cover academic topics — ask me anything about your studies!"
End every reply with a short follow-up question in {lang}."""


def is_too_short(text):
    cleaned = text.strip()
    return len(cleaned) < 10 or len(cleaned.split()) <= 1


SHORT_REPLY = """👋 Hi! Please ask a full question so I can help you properly.

For example:
• "How do I write a research paper?"
• "What are the best study techniques?"
• "How can I apply for a scholarship?"
• "كيف أتقدم للجامعة؟" (Arabic)
• "مجھے امتحان کی تیاری کیسے کرنی چاہیے؟" (Urdu)

What would you like help with? 😊"""


def chat(user_message, chat_history):
    # chat_history is a list of {"role": ..., "content": ...} dicts in Gradio 6
    if chat_history is None:
        chat_history = []

    if not user_message or not user_message.strip():
        return "", chat_history

    # Short message — guide user, no API call
    if is_too_short(user_message):
        chat_history = chat_history + [
            {"role": "user",      "content": user_message},
            {"role": "assistant", "content": SHORT_REPLY}
        ]
        return "", chat_history

    # Detect language
    try:
        lang_name = detect_language(user_message)
    except Exception:
        lang_name = "English"

    # Build API messages — system + history + new message
    api_messages = [{"role": "system", "content": build_prompt(lang_name)}]

    for msg in chat_history:
        if isinstance(msg, dict) and msg.get("role") in ("user", "assistant"):
            api_messages.append({
                "role":    msg["role"],
                "content": msg["content"]
            })

    api_messages.append({"role": "user", "content": user_message})

    # Token limit protection
    if len(api_messages) > 21:
        api_messages = api_messages[:1] + api_messages[-20:]

    # Call Groq
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=api_messages,
            max_tokens=300,
            temperature=0.7
        )
        bot_reply = response.choices[0].message.content.strip()
    except Exception:
        bot_reply = "⚠️ Connection issue. Please try again in a moment."

    # Append in Gradio 6.13 dict format
    chat_history = chat_history + [
        {"role": "user",      "content": user_message},
        {"role": "assistant", "content": bot_reply}
    ]
    return "", chat_history


def reset():
    return []


# ── UI ────────────────────────────────────────────────────────
with gr.Blocks(title="UniLingo") as demo:

    gr.Markdown("""
    # 🎓 UniLingo — Multilingual University Support Bot
    Ask anything about studying, exams, university applications, or student life — **in any language!**
    """)

    # Gradio 6.13 requires dict format — NO type parameter needed
    # The Chatbot auto-detects format from the data we return
    chatbot = gr.Chatbot(
        value=[],
        height=460,
        show_label=False,
        render_markdown=True
    )

    with gr.Row():
        msg = gr.Textbox(
            placeholder="Type your question in any language...",
            scale=5,
            show_label=False,
            container=False
        )
        send_btn = gr.Button("Send ➤", scale=1, variant="primary")

    reset_btn = gr.Button("🔄 Reset Conversation", variant="secondary")

    gr.Markdown("""
    **📚 Topics:** Study techniques • Essay writing • University applications • Exam prep • Career advice • International student support

    **🌍 Languages:** English • French • Spanish • Arabic • Urdu • German • Chinese • Hindi • Portuguese • Italian • Turkish • Russian • Japanese • Korean • Dutch

    ---
    *Built with Groq (Llama 3.3 70B) • Hugging Face Spaces • by Muhammad Umer*
    """)

    msg.submit(fn=chat,  inputs=[msg, chatbot], outputs=[msg, chatbot])
    send_btn.click(fn=chat,  inputs=[msg, chatbot], outputs=[msg, chatbot])
    reset_btn.click(fn=reset, inputs=None, outputs=[chatbot])

demo.launch()
