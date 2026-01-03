# AI Personal Finance Agent

## Overview
This project is an AI-powered personal finance agent built to turn raw bank transactions into understandable insights through natural language.

Instead of static charts or dashboards, the agent allows you to **ask questions**, explore spending patterns, and receive automated monthly insights — while keeping full control over your financial data.

The project was built as a personal learning exercise at the intersection of **data analytics, automation, and AI agents**.

---

## What the Agent Does
- Reads bank transaction data (Excel)
- Cleans and prepares financial data
- Categorizes expenses automatically
- Answers questions in natural language
- Remembers context across conversations
- Generates monthly summaries and insights
- Runs locally (no third-party data sharing)

---

## Why This Project
Most banking apps and finance tools:
- Offer limited analytics
- Focus on charts, not understanding
- Require sharing sensitive financial data

This project explores a different approach:
**using an AI agent as an interface to financial data**, where data analysis is the foundation and AI provides reasoning and interaction.

---

## Project Architecture
- **Data Layer**: pandas-based data preparation & aggregation
- **Agent Layer**: LLM-powered reasoning and responses
- **Memory Layer**: Conversation context & session memory
- **Interface**: Streamlit-based chat UI

The agent is designed to sit *on top of* a traditional data analysis pipeline.

---

## Tech Stack
- Python
- pandas
- Streamlit
- LangChain
- OpenAI API
- Jupyter Notebook (for experimentation)

---

## Project Structure
```text
ai-personal-finance-agent/
├── app.py
├── agent/
│   ├── llm.py
│   ├── memory.py
│   ├── tools.py
│   └── prompts.py
├── data/
├── notebooks/
├── requirements.txt
└── README.md
