from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

# Load models
embedder = SentenceTransformer("all-MiniLM-L6-v2")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def chunk_text(text, max_len=500):
    sentences = text.split(". ")
    chunks, chunk = [], ""
    for sent in sentences:
        if len(chunk) + len(sent) < max_len:
            chunk += sent + ". "
        else:
            chunks.append(chunk.strip())
            chunk = sent + ". "
    if chunk:
        chunks.append(chunk.strip())
    return chunks

def answer_question(text, question, history=[]):
    chunks = chunk_text(text)

    # Prepend history memory
    memory_context = " ".join([f"Q: {q} A: {a}" for q, a in history[-3:]])
    full_question = memory_context + " Q: " + question if history else question

    # 💡 Smart pre-filtering based on question intent
    keywords = ["faculty", "teacher", "grading", "workload", "automation", "staff"]
    relevant_chunks = [c for c in chunks if any(k in c.lower() for k in keywords)]

    # If relevant chunks are found, prioritize them
    if relevant_chunks:
        chunks = relevant_chunks + chunks

    # Embed question and chunks
    q_embed = embedder.encode(full_question, convert_to_tensor=True)
    chunk_embeds = embedder.encode(chunks, convert_to_tensor=True)

    # Top 3 matching chunks
    sims = util.pytorch_cos_sim(q_embed, chunk_embeds)[0]
    top_indices = sims.topk(3).indices.tolist()
    top_chunks = [chunks[i] for i in top_indices]
    combined = " ".join(top_chunks)

    # Generate detailed answer
    answer = summarizer(combined, max_length=150, min_length=50, do_sample=False)[0]["summary_text"]

    # Return justification and raw matched paragraph
    justification = f"Supported by paragraph {top_indices[0] + 1} (match score: {sims[top_indices[0]]:.2f})"
    snippet = chunks[top_indices[0]]

    return answer, justification, snippet
