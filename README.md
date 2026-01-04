# Ahmad Finance Assistant 💬💰

Ahmad Finance Assistant is a personal finance AI agent that allows you to **chat with your bank transactions** in a safe, transparent, and explainable way.

The project combines **data analytics** and **AI** while keeping a strict separation between:
- data processing (Python & pandas)
- language understanding and explanation (OpenAI API)

All financial calculations are done **locally**.  
The AI **never generates or guesses numbers**.

---

## 🚀 What This Project Does

- Loads bank transaction data from an Excel file
- Cleans and prepares transaction dates
- Automatically categorizes expenses using rule-based logic
- Answers natural-language questions such as:
  - *How much did I spend on groceries in May?*
  - *How much did I spend in November?*
- Asks follow-up questions if information is missing
- Keeps full chat history (conversation memory)
- Provides a friendly chat interface using Streamlit

---

## 🧠 Key Design Principles

### 1️⃣ Python Is the Source of Truth
- All calculations are done using pandas
- Filtering, grouping, and summing never rely on AI
- This guarantees accuracy and reproducibility

### 2️⃣ AI Is Used Only for Language
- Understanding user intent
- Handling vague or incomplete questions
- Explaining results in a human-friendly way
- AI never creates financial data

### 3️⃣ No Hallucinations by Design
The assistant is **technically prevented** from inventing:
- amounts
- categories
- months
- summaries

If data is missing, the assistant asks for clarification instead of guessing.

---

## 🗂️ Expense Categorization Strategy

Transaction categorization is handled through **explicit keyword-based rules**, for example:

- Grocery (EDEKA, REWE, LIDL, etc.)
- Bakery / Snacks
- Restaurants / Cafes
- Clothing
- Furniture / Home
- Electronics
- Online Shopping
- Transport
- Utilities
- Rent
- Banking & Fees
- Gifts & Flowers

This approach was chosen intentionally because it is:
- transparent
- explainable
- easy to extend
- easy to audit

The same category logic is used consistently across:
- data analysis notebooks
- the AI chat application

---

## 🏗️ Tech Stack

- Python
- pandas
- Streamlit
- OpenAI API (via `langchain-openai`)
- Excel (bank statement input)

---

## 📁 Project Structure
```text
ai-personal-finance-agent/
├── code.py
├── data/
├── notebooks/
├── requirements.txt
└── README.md
