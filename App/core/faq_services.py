# App/core/faq_services.py

from google import genai
import streamlit as st
import time
import toml
import os
from App.core.prompts import CLASSIFY_PROMPT, SENTIMENT_PROMPT, RESPONSE_PROMPT
from App.core.retrivel import retrieve

# ── Setup Gemini client ────────────────────────────────────────────────────
def _get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        secrets = toml.load(".streamlit/secrets.toml")
        return secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=_get_api_key())


def _run_prompt(prompt, retries=3):
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1.5)
            else:
                raise RuntimeError(f"Gemini API failed: {e}")


def process_query(user_query):

    # Step 1 — Classify
    category = _run_prompt(CLASSIFY_PROMPT.format(query=user_query))
    if category not in ["Billing", "Technical Support", "General Inquiry",
                         "Complaint", "Feedback", "Refund Request", "Account Issue"]:
        category = "General Inquiry"

    # Step 2 — Sentiment
    sentiment = _run_prompt(SENTIMENT_PROMPT.format(query=user_query))
    if sentiment not in ["Positive", "Negative", "Neutral", "Frustrated", "Urgent"]:
        sentiment = "Neutral"

    # Step 3 — Retrieve relevant FAQs from knowledge base
    relevant_faqs = retrieve(user_query)
    faq_context = "\n".join(
        [f"Q: {f['question']}\nA: {f['answer']}" for f in relevant_faqs]
    )

    # Step 4 — Generate response using context
    reply = _run_prompt(
        RESPONSE_PROMPT.format(
            query=user_query,
            category=category,
            sentiment=sentiment,
            context=faq_context
        )
    )

    return {
        "category":  category,
        "sentiment": sentiment,
        "response":  reply
    }