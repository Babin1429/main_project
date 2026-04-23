# ☆ JoestarIQ — AI Customer Support Chatbot



A production-grade AI-powered customer support chatbot that classifies queries, analyzes sentiment, and generates contextual responses using a full RAG (Retrieval Augmented Generation) pipeline — powered by Google Gemini 2.5 Flash.

---

##  What It Does

Every customer message goes through a **3-stage AI pipeline** automatically:

1. **Query Classification** — Identifies the type of query (Billing, Complaint, Technical Support, etc.)
2. **Sentiment Analysis** — Detects the emotional tone (Positive, Negative, Frustrated, Urgent, Neutral)
3. **Contextual Response Generation** — Generates a response conditioned on both the category and sentiment, grounded in a real FAQ knowledge base via RAG

---

##  Architecture

```
User Query
    ↓
[ Classification ]     → What type of query is this?
    ↓
[ Sentiment Analysis ] → How is the customer feeling?
    ↓
[ RAG Retrieval ]      → Find relevant FAQs from knowledge base (FAISS)
    ↓
[ Response Generation ]→ Gemini generates response using all context
    ↓
Streamlit UI
```







##  Requirements

```
streamlit
google-genai
sentence-transformers
faiss-cpu
numpy
toml
setuptools
```

---



##  Built By

**Babin Saravanan** — B.Tech AI & Data Science   ☆

 
