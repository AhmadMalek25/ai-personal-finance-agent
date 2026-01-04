# =========================================================
# Personal Finance Assistant – FINAL CORRECT VERSION
# =========================================================

import pandas as pd
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# ---------------------------------------------------------
# STREAMLIT SETUP
# ---------------------------------------------------------

st.set_page_config(page_title="Personal Finance Assistant")
st.title("💬 Personal Finance Assistant")

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = pd.read_excel("sample_data/transactions_sample.xlsx")

df["Buchungstag"] = pd.to_datetime(
    df["Buchungstag"],
    format="%d.%m.%y",
    errors="coerce"
)

df["Month"] = df["Buchungstag"].dt.to_period("M").astype(str)

# ---------------------------------------------------------
# CATEGORY RULES
# ---------------------------------------------------------

CATEGORY_RULES = {
    "EDEKA": "Grocery",
    "REWE": "Grocery",
    "LIDL": "Grocery",
    "PENNY": "Grocery",
    "KAUFLAND": "Grocery",
    "CINAR": "Grocery",
    "MARKAB": "Grocery",
    "ALQUDS": "Grocery",
    "PAYPAL": "PayPal / Online Payments",
    "AMAZON": "Amazon",
    "OTTO": "Online Shopping",
    "DB VERTRIEB": "Public Transport",
    "VODAFONE": "Internet / Phone",
    "PYUR": "Internet / Phone",
    "WBF": "Rent",
}

def categorize_transaction(row):
    text = row["Beguenstigter/Zahlungspflichtiger"]
    amount = row["Betrag"]

    if amount > 0:
        return "Income"

    if pd.isna(text):
        return "Bank / Internal"

    text_upper = text.upper()
    for keyword, category in CATEGORY_RULES.items():
        if keyword in text_upper:
            return category

    return "Other Expense"

df["Category"] = df.apply(categorize_transaction, axis=1)
VALID_CATEGORIES = sorted(df["Category"].unique().tolist())

# ---------------------------------------------------------
# FINANCE LOGIC (SOURCE OF TRUTH)
# ---------------------------------------------------------

def spending_by_category_and_month(category, month):
    return round(
        df[
            (df["Category"] == category) &
            (df["Month"] == month)
        ]["Betrag"].sum(),
        2
    )

def income_by_month(month):
    return round(
        df[
            (df["Category"] == "Income") &
            (df["Month"] == month)
        ]["Betrag"].sum(),
        2
    )

# ---------------------------------------------------------
# LLM – INTENT ONLY (SAFE)
# ---------------------------------------------------------

llm = ChatOpenAI(temperature=0)

def detect_intent(text):
    response = llm.invoke(
        [
            HumanMessage(
                content=f"""
Classify intent. Reply with ONE word only:

- spending
- income
- greeting
- other

Question:
{text}
"""
            )
        ]
    )
    return response.content.strip().lower()

# ---------------------------------------------------------
# EXTRACTORS (ROBUST, NO AI)
# ---------------------------------------------------------

MONTH_MAP = {
    "january": "01", "february": "02", "march": "03",
    "april": "04", "may": "05", "june": "06",
    "july": "07", "august": "08", "september": "09",
    "october": "10", "november": "11", "december": "12"
}

def extract_month(text):
    text = text.lower()
    for name, num in MONTH_MAP.items():
        if name in text:
            return f"2025-{num}"
    return None

def extract_category(text):
    text = text.lower()

    for cat in VALID_CATEGORIES:
        base = cat.lower()

        # exact
        if base in text:
            return cat

        # grocery -> groceries
        if base.endswith("y") and base[:-1] + "ies" in text:
            return cat

        # simple plural
        if base + "s" in text:
            return cat

    return None

# ---------------------------------------------------------
# SESSION STATE (REAL CHAT MEMORY)
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending" not in st.session_state:
    st.session_state.pending = None

if "welcome_shown" not in st.session_state:
    welcome = (
        "Hello Ahmad 👋\n\n"
        "I’m your personal finance assistant.\n\n"
        "Ask me anything about your spending whenever you’re ready."
    )
    st.session_state.messages.append(
        {"role": "assistant", "content": welcome}
    )
    st.session_state.welcome_shown = True


# ---------------------------------------------------------
# DISPLAY FULL CHAT HISTORY
# ---------------------------------------------------------

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------

user_input = st.chat_input("Ask a finance question")

if user_input:
    # ---------------------------------------------
    # Store + render user message
    # ---------------------------------------------
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    st.chat_message("user").write(user_input)

    # ---------------------------------------------
    # FOLLOW-UP RESPONSE
    # ---------------------------------------------
    if st.session_state.pending:
        category = extract_category(user_input)
        month = st.session_state.pending["month"]

        if category:
            amount = spending_by_category_and_month(category, month)
            reply = (
                f"Alright Ahmad 😊\n\n"
                f"In **{month}**, you spent **€{abs(amount):,.2f}** on **{category}**.\n\n"
                "If you want to check something else, just ask 👍"
            )
            st.session_state.pending = None
        else:
            reply = (
                "I still need the category 😊\n"
                "For example: Grocery, Rent, Amazon, Transport."
            )

    # ---------------------------------------------
    # NEW QUESTION
    # ---------------------------------------------
    else:
        intent = detect_intent(user_input)
        month = extract_month(user_input)
        category = extract_category(user_input)

        # -------- GREETING --------
        if intent == "greeting":
            reply = (
                "Hi Ahmad 👋\n\n"
                "How can I help you today?"
            )

        # -------- INCOME --------
        elif intent == "income":
            if month:
                amount = income_by_month(month)
                reply = (
                    f"Alright Ahmad 😊\n\n"
                    f"In **{month}**, you earned **€{amount:,.2f}**.\n\n"
                    "Would you like to check another month?"
                )
            else:
                reply = (
                    "Sure 😊\n\n"
                    "Which month are you asking about?\n"
                    "For example: March, May, November."
                )

        # -------- SPENDING --------
        elif intent == "spending":
            if month and category:
                amount = spending_by_category_and_month(category, month)
                reply = (
                    f"Alright Ahmad 😊\n\n"
                    f"In **{month}**, you spent **€{abs(amount):,.2f}** on **{category}**.\n\n"
                    "Would you like to check another month or category?"
                )

            elif month and not category:
                st.session_state.pending = {"month": month}
                reply = (
                    "Got it 👍\n\n"
                    "Which category are you asking about?\n"
                    "For example: Grocery, Rent, Amazon, Transport."
                )

            else:
                reply = (
                    "Sure 😊\n\n"
                    "Which month are you asking about?\n"
                    "For example: May, November, December 2025."
                )

        # -------- FALLBACK --------
        else:
            reply = (
                "I didn’t fully understand that yet 🤔\n\n"
                "You can ask about your spending or income.\n"
                "For example: *groceries in May* or *income in March*."
            )

    # ---------------------------------------------
    # Store + render assistant reply
    # ---------------------------------------------
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
    st.chat_message("assistant").write(reply)
