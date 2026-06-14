# ⚖️ DebateBot — Multi-Agent AI Reasoning System

> **DebateBot** is an advanced multi-agent AI reasoning platform that takes any complex topic or decision, runs it through opposing advocate agents, and delivers a rigorous, objective final judgment. 
> Built for the **Microsoft Agents League Hackathon 2026 — Reasoning Agents Track**.
>
> **🔗 Live Demo:** [debatebot-adhipatya.streamlit.app](https://debatebot-adhipatya.streamlit.app/)

---

## 🤖 Multi-Agent Architecture & Flow
Instead of a single LLM prompt, DebateBot simulates a structured debate panel where agents are configured with specialized roles and optimal inference parameters (temperatures) to maximize reasoning depth:

```
                  ┌─────────────────────────────┐
                  │      User Input Topic       │
                  └──────────────┬──────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
      ┌───────────────────────┐       ┌───────────────────────┐
      │   Agent 1: FOR        │       │   Agent 2: AGAINST    │
      │   (Temp: 0.85)        │       │   (Temp: 0.85)        │
      │   Llama 3.3 70B       │       │   Llama 3.3 70B       │
      └───────────┬───────────┘       └───────────┬───────────┘
                 │                               │
                 └───────────────┬───────────────┘
                                 ▼
                      ┌───────────────────────┐
                      │    Agent 3: JUDGE     │
                      │    (Temp: 0.15)       │
                      │    Llama 3.3 70B      │
                      └───────────┬───────────┘
                                 ▼
                     ┌───────────────────────┐
                     │ Impartial Verdict     │
                     │ + Confidence Score    │
                     └───────────────────────┘
```

1. **Agent FOR (Creative & Persuasive):** Instantiated with `temperature=0.85` to generate 5 sharp, bold, evidence-backed arguments supporting the topic.
2. **Agent AGAINST (Creative & Critical):** Instantiated with `temperature=0.85` to formulate 5 distinct counter-arguments, citing statistics and real-world impact.
3. **Agent JUDGE (Analytical & Impartial):** Instantiated with a cool `temperature=0.15` to ensure consistent logic, identify blind spots missed by both sides, assign a confidence score, and deliver an objective verdict.

---

## ⚡ Tech Stack (100% Free)
| Layer | Tool / Model | Cost | Details |
|---|---|---|---|
| **LLM Inference** | Llama 3.3 70B / Llama 3.1 8B via Groq | **$0** | Lightning-fast inference (no token latency) |
| **Agent Framework** | LangChain | **$0** | Handles chains, templates, and multi-agent routing |
| **Frontend UI** | Streamlit | **$0** | Elegant, high-performance interactive interface |
| **Deployment** | Streamlit Cloud | **$0** | Live-hosted web app at [debatebot-adhipatya.streamlit.app](https://debatebot-adhipatya.streamlit.app/) |

---

## 🚀 Local Quickstart

### Prerequisites
- Python 3.10 or higher
- A free Groq API key (obtained from [console.groq.com](https://console.groq.com/) with no credit card required)

### Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone https://github.com/adhipatya3552/DebateBot.git
   cd DebateBot
   ```

2. **Create & Activate Virtual Environment**
   * **Windows**:
     ```powershell
     python -m venv venv
     venv\Scripts\activate
     ```
   * **macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Application**
   ```bash
   streamlit run app.py
   ```
   Open `http://localhost:8501` in your browser.

---

## 🏆 Hackathon Submission Checklist
- [x] Multi-agent reasoning pipeline showing reasoning and multi-step thinking (Reasoning track requirement)
- [x] Zero credit-card / paid subscriptions required (100% Free Stack)
- [x] Clean, responsive, glassmorphic layout styling with gradient branding
- [x] Downloadable debate results as Markdown records for B2B/academic auditing
- [x] Supporting README explaining the project structure and setup
