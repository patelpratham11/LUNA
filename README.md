# LUNA — Localized Unified Neural Assistant

**LUNA** (Localized Unified Neural Assistant) is a personal, offline-first AI assistant inspired by J.A.R.V.I.S., built to serve as a natural language interface to both real-world APIs and my own personal knowledge base. It leverages LangChain to orchestrate a local LLM (Phi-3 Mini) and integrates various modular tools to handle tasks ranging from calendar management to personalized information retrieval.

LUNA is designed to be fast, private, and highly extensible — running entirely on local hardware without relying on external cloud-based AI services.

---

## 🧠 Core Capabilities

### 🔗 Local LLM Integration
- Runs on **Phi-3 Mini**, a small, fast, and efficient language model.
- Orchestrated via **LangChain**, enabling tool-use, memory, and agentic reasoning.

### 📅 Agent Tools
- **Google Calendar Agent** — Fetch upcoming events, create new entries, and manage schedules via natural language.
- **Weather Agent** — Retrieves weather forecasts using an integrated weather API.
- **General LLM Agent** — Handles open-ended queries, conversation, and utility tasks.

### 📚 RAG with Personal Knowledge Base
- Connects to a **ChromaDB vector store** built from my **Obsidian Vault**.
- Supports **retrieval-augmented generation**, enabling LUNA to answer questions grounded in my own notes, files, and documentation.

### 🖥️ Local & Secure
- Entirely self-contained and offline-first.
- No external API calls required for inference, ensuring full **data privacy** and **autonomy**.

---

## 🌟 Why LUNA?

I built LUNA to bring together the power of local LLMs with practical daily tools and a contextual understanding of my own digital world. It’s a flexible framework that acts as both a smart assistant and a knowledge companion — with complete control and no data leakage.

---

*Note: This project is personal and not intended for public deployment or replication.*
