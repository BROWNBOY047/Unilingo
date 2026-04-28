# 🎓 UniLingo — Multilingual University Support Bot

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Groq](https://img.shields.io/badge/LLM-Llama%203.3%2070B-orange)
![Gradio](https://img.shields.io/badge/UI-Gradio-yellow)
![HuggingFace](https://img.shields.io/badge/Deployed-HuggingFace%20Spaces-brightgreen)

A public AI-powered university support bot that automatically detects
the user's language and responds in the same language — powered by
Llama 3.3 70B via Groq API.

## 🌐 Live Demo
👉 **[Try UniLingo on Hugging Face Spaces](https://huggingface.co/spaces/BrownBoy47/unilingo)**

---

## 📸 Features

- 🌍 **Auto language detection** — detects 15+ languages automatically
- 💬 **Responds in user's language** — never switches mid-conversation
- 🧠 **Multi-turn memory** — remembers context across the conversation
- 🛡️ **Smart error handling** — guides users on vague inputs
- ⚡ **Fast responses** — powered by Groq's ultra-fast inference
- 🔄 **Reset button** — start fresh anytime

---

## 🎓 Topics Covered

| Topic | Examples |
|---|---|
| Study Techniques | Pomodoro, active recall, note-taking |
| Academic Writing | Essays, research papers, citations |
| University Applications | Personal statements, scholarships, visas |
| Exam Preparation | Revision strategies, stress management |
| Career Planning | CVs, cover letters, internships |
| International Students | Adapting abroad, language barriers |

---

## 🌍 Supported Languages

English • French • Spanish • Arabic • Urdu • German • Chinese
Hindi • Portuguese • Italian • Turkish • Russian • Japanese • Korean • Dutch

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM | Llama 3.3 70B via Groq API |
| Language Detection | LangDetect + LLM fallback |
| UI Framework | Gradio 6.13 |
| Deployment | Hugging Face Spaces |
| Language | Python 3.13 |

---

## 🚀 Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/BROWNBOY047/unilingo.git
cd unilingo
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set your Groq API key**
```bash
# Get free key at console.groq.com
export GROQ_API_KEY="your-key-here"
```

**4. Run the app**
```bash
python app.py
```

**5. Open in browser**
```
http://localhost:7860
```

---

## 🏗️ Project Architecture

```
User Message (any language)
        │
        ▼
┌─────────────────────┐
│  Language Detector  │  ← LangDetect + Groq LLM fallback
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  System Prompt      │  ← Rebuilt with detected language
│  Builder            │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Conversation       │  ← Full history passed every turn
│  Manager            │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Groq API           │  ← Llama 3.3 70B generates response
│  (Llama 3.3 70B)    │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Gradio UI          │  ← Clean chat interface
└─────────────────────┘
```

---

## 📁 Project Structure

```
unilingo/
├── app.py            ← Complete application (all logic + UI)
├── requirements.txt  ← Python dependencies
├── README.md         ← This file
└── .gitignore        ← Excludes secrets and cache files
```

---

## 🔮 Future Enhancements

- [ ] RAG integration for university-specific handbooks
- [ ] Voice input support
- [ ] More language support (Swahili, Thai, Vietnamese)
- [ ] User feedback rating system
- [ ] Analytics dashboard

---

## 👨‍💻 Author

**Muhammad Umer**
- Building expertise in AI/LLMs 
- This project is part of a 5-project LLM portfolio

---

## 📄 License

MIT License — free to use and modify
