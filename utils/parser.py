import pdfplumber
import re

def parse_document(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        with pdfplumber.open(uploaded_file) as pdf:
            raw_text = " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
    else:
        raw_text = uploaded_file.read().decode("utf-8")

    # Clean up malformed characters (e.g., (cid:415), \n, etc.)
    cleaned_text = re.sub(r"\(cid:\d+\)", "", raw_text)
    cleaned_text = re.sub(r"[^\x00-\x7F]+", " ", cleaned_text)  # remove non-ascii
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)  # normalize spacing

    return cleaned_text.strip()
