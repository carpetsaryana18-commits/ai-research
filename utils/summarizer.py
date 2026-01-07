from transformers import pipeline
import re
import streamlit as st

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
grammar_corrector = pipeline("text2text-generation", model="prithivida/grammar_error_correcter_v1")

def clean_text(text):
    text = re.sub(r"\(cid:\d+\)", "", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    text = re.sub(r"\s+", " ", text)
    text = text.replace("Senment", "Sentiment")
    text = text.replace("Collecon", "Collection")
    return text.strip()

@st.cache_data(show_spinner=False)
def generate_summary(text, polish=True):
    text = clean_text(text)
    
    # Break into 2-3 chunks (avoid overload)
    chunk_size = 1000
    chunks = [text[i:i+chunk_size] for i in range(0, min(len(text), 3000), chunk_size)]

    partial_summaries = []
    for chunk in chunks:
        s = summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]
        partial_summaries.append(s)

    combined_summary = " ".join(partial_summaries)

    # Optionally run one more layer of summarization
    final_summary = summarizer(combined_summary, max_length=150, min_length=40, do_sample=False)[0]["summary_text"]

    if polish:
        polished = grammar_corrector(final_summary, max_length=160)[0]["generated_text"]
        return polished
    else:
        return final_summary
