import random
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

# Load models
embedder = SentenceTransformer('all-MiniLM-L6-v2')
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
grammar_corrector = pipeline("text2text-generation", model="prithivida/grammar_error_correcter_v1")

def generate_challenges(text):
    questions = [
        "What is the main goal of the paper?",
        "What method or approach is used?",
        "What are the key findings or results?",
        "What problem does the study address?",
        "What conclusions are drawn?"
    ]
    return random.sample(questions, 3)

def evaluate_answer(text, question, user_answer):
    # Grammar correct user's input before scoring
    corrected_user_answer = grammar_corrector(user_answer, max_length=150)[0]["generated_text"]

    # Get correct answer using QA model
    context = text[:5000] if len(text) > 5000 else text
    result = qa_pipeline(question=question, context=context)
    correct_answer = result['answer']

    # Semantic similarity scoring
    emb_user = embedder.encode(corrected_user_answer, convert_to_tensor=True)
    emb_correct = embedder.encode(correct_answer, convert_to_tensor=True)
    sim_score = util.pytorch_cos_sim(emb_user, emb_correct).item()

    # Scale to 0–5
    scaled_score = round(sim_score * 5)
    scaled_score = max(0, min(5, scaled_score))

    feedback = f"✅ Score: {scaled_score}/5 — "
    if scaled_score >= 4:
        feedback += "Excellent! Your answer is very relevant."
    elif scaled_score >= 2:
        feedback += "Partially correct. Try including more detail or phrasing closer to the document."
    else:
        feedback += "Not quite right. Try reviewing the document more carefully."

    feedback += f"\n\n📌 Expected answer: \"{correct_answer}\"\n✍️ Corrected Your Answer: \"{corrected_user_answer}\""
    return scaled_score, feedback
