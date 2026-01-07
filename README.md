---
title: AI Research Assistant
emoji: 🚀
colorFrom: blue
colorTo: blue
sdk: streamlit
sdk_version: 1.25.0
app_file: app.py
pinned: false
---




# 🔮 Smart Assistant for Research Summarization

An AI-powered assistant that helps researchers, students, and educators quickly understand and interact with academic documents. Built entirely on **free open-source models**, this app extracts summaries, answers deep questions, evaluates answers, and explains its reasoning. Designed with an intuitive Streamlit interface.

---

## 🔁 What It Does

- 📄 **Upload a PDF/TXT research paper**
- 📝 **Auto Summary**: Generates a rich abstract with optional grammar polishing
- ❓ **Ask Anything**: Answer any question from the document using semantic search + context memory
- 🧠 **Challenge Me**: Auto-generated logic questions to test comprehension
- ✅ **Evaluate Answers**: Gives feedback and scoring based on meaning match
- 🧠 **Memory-Enabled**: Handles follow-up questions with retained context
- 🔍 **Answer Highlighting**: Shows exactly which paragraph supports each answer

---

## 🚀 Features Overview

| Feature                        | Description                                                                 |
|------------------------------- |---------------------------------------------------------------------------- |
| 📂 Document Upload            | Upload `.pdf` or `.txt` files                                              |
| 📝 Grammar-Polished Summaries | Toggle to clean and enhance auto summaries                                 |
| 🧠 Ask Anything Mode          | Extracts context-aware answers from anywhere in the doc                    |
| 🔎 Semantic Search Ranking    | Uses sentence transformers to rank relevant chunks                         |
| 📖 Justification & Snippet    | Shows paragraph number and exact source snippet                            |
| 💬 Context Memory             | Supports intelligent follow-up questions                                   |
| 🧠 Challenge Generator        | Generates 3 logic-based questions from the uploaded doc                    |
| ✅ Answer Evaluator           | Compares user input vs doc and gives smart feedback                        |

---

## 🛠️ Tech Stack

- `Python 3.9+`
- `Streamlit`
- `Transformers`
- `Sentence-Transformers`
- `pdfplumber`

---

## 🏠 Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/amanrss/smart-assistant-genai.git
cd smart-assistant-genai
```

### 2. Set up virtual environment (Windows)
```bash
python -m venv venv
venv\Scripts\activate
```
*For Linux/macOS:* `source venv/bin/activate`

### 3. Install requirements
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

---
## 📸 Screenshots 

UPLOAD

<img width="962" height="450" alt="Upload" src="https://github.com/user-attachments/assets/e23a6200-cbae-42ca-9b47-9f03e75067eb" />


<br><br>

SUMMARY

<img width="945" height="444" alt="Summary" src="https://github.com/user-attachments/assets/701aa419-e623-49db-9f89-b54f752edfad" />



<br><br>
Ask Anything

<img width="941" height="425" alt="AskAnything" src="https://github.com/user-attachments/assets/1010d315-f09f-480f-8437-5f5211e874d6" />



<br><br>
CHALLENGE ME

<img width="956" height="449" alt="ChallengeMe" src="https://github.com/user-attachments/assets/696d364b-8004-4995-8a7e-2cb9b336477a" />


---

## 📂 Folder Structure

```
smart-assistant-genai/
├── app.py
├── README.md
├── requirements.txt
└── utils/
    ├── parser.py
    ├── summarizer.py
    ├── qa.py
    └── challenge.py
```

---
 👤 Author

Meerum