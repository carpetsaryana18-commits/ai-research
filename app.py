
import streamlit as st
from utils.summarizer import generate_summary
from utils.qa import answer_question
from utils.challenge import generate_challenges, evaluate_answer
from utils.parser import parse_document
from utils.recommender import recommend_papers
import database
import hashlib

# Initialize the database
database.init_db()

st.set_page_config(page_title="Smart Research Assistant", layout="wide")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = database.get_user(username)
        if user and user[2] == password:
            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.session_state.username = user[1]
            st.session_state.role = user[3]
            st.rerun()
        else:
            st.error("Invalid username or password")

def main_app():
    st.sidebar.title(f"Welcome, {st.session_state.username}")
    st.sidebar.write(f"Role: {st.session_state.role}")

    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.title("📚 Smart Assistant for Research Summarization")

    def reset_state():
        for key in [
            "document_text", "summary", "challenge_questions", "qa_button",
            "qa_history", "last_answer", "last_justification", "last_snippet", "polish"
        ]:
            if key in st.session_state:
                del st.session_state[key]

    uploaded_files = st.file_uploader(
        "Upload research papers (PDF or TXT)",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        on_change=reset_state
    )

    if uploaded_files:
        if "document_text" not in st.session_state:
            with st.spinner("Reading and analyzing documents..."):
                full_text = []
                for uploaded_file in uploaded_files:
                    full_text.append(parse_document(uploaded_file))
                st.session_state.document_text = "\n\n---\n\n".join(full_text)
            st.success("✅ Documents uploaded and processed successfully.")

        if "document_text" in st.session_state and st.session_state.document_text:
            tabs_list = ["📘 Summary", "❓ Ask Anything", "🧠 Challenge Me", "🔗 Recommend Similar Papers"]
            if st.session_state.role == 'admin':
                tabs_list.append("🔒 Admin Panel")
            
            tabs = st.tabs(tabs_list)

            # --- Tab 1: Summary ---
            with tabs[0]:
                with st.expander("🔎 Auto Summary", expanded=True):
                    if "polish" not in st.session_state:
                        st.session_state.polish = True

                    new_polish = st.checkbox(
                        "Polish grammar (may be slower)",
                        value=st.session_state.polish
                    )

                    if new_polish != st.session_state.polish or "summary" not in st.session_state:
                        st.session_state.polish = new_polish
                        with st.spinner("Generating summary..."):
                            st.session_state.summary = generate_summary(
                                st.session_state.document_text,
                                polish=st.session_state.polish
                            )

                    st.write(st.session_state.summary)

            # --- Tab 2: Ask Anything ---
            with tabs[1]:
                if "qa_history" not in st.session_state:
                    st.session_state.qa_history = []

                question = st.text_input("Type your question:")

                if question and st.button("Find Answer"):
                    database.log_activity(st.session_state.user_id, 'ask_question', question)
                    with st.spinner("🔍 Finding the answer..."):
                        answer, justification, snippet = answer_question(
                            st.session_state.document_text,
                            question,
                            st.session_state.qa_history
                        )
                        st.session_state.last_answer = answer
                        st.session_state.last_justification = justification
                        st.session_state.last_snippet = snippet
                        st.session_state.qa_history.append((question, answer))

                if "last_answer" in st.session_state:
                    st.markdown("**Answer:** " + st.session_state.last_answer)
                    st.markdown("**Justification:** " + st.session_state.last_justification)
                    st.markdown("**📌 Supporting Snippet:**")
                    st.code(st.session_state.last_snippet, language="markdown")

            # --- Tab 3: Challenge Me ---
            with tabs[2]:
                if "challenge_questions" not in st.session_state:
                    with st.spinner("⚙️ Generating questions..."):
                        st.session_state.challenge_questions = generate_challenges(
                            st.session_state.document_text
                        )

                st.info("Answer the following 3 logic-based questions:")

                for i, q in enumerate(st.session_state.challenge_questions):
                    st.markdown(f"**Q{i+1}:** {q}")
                    user_answer = st.text_input(
                        f"Your Answer to Q{i+1}", key=f"user_answer_{i}"
                    )

                    if user_answer and st.button(f"Evaluate Q{i+1}", key=f"eval_btn_{i}"):
                        with st.spinner("🧠 Evaluating your response..."):
                            score, feedback = evaluate_answer(
                                st.session_state.document_text,
                                q,
                                user_answer
                            )
                            st.session_state[f"feedback_{i}"] = feedback

                    if f"feedback_{i}" in st.session_state:
                        st.markdown(f"**Feedback:** {st.session_state[f'feedback_{i}']}")

            # --- Tab 4: Recommend Similar Papers ---
            with tabs[3]:
                st.subheader("Discover Similar Research")
                if st.button("Find Recommendations"):
                    query_text = st.session_state.document_text[:500]
                    database.log_activity(st.session_state.user_id, 'recommend_papers', query_text)
                    with st.spinner("Searching for similar papers..."):
                        recommendations = recommend_papers(query_text)
                        st.session_state.recommendations = recommendations

                if "recommendations" in st.session_state:
                    if st.session_state.recommendations:
                        for paper in st.session_state.recommendations:
                            st.markdown(f"- **[{paper['title']}]({paper['url']})** by {', '.join(paper['authors'])}")
                    else:
                        st.warning("Could not find any recommendations.")

            # --- Admin Panel ---
            if st.session_state.role == 'admin':
                with tabs[4]:
                    st.subheader("User Activity")
                    activity = database.get_user_activity()
                    for username, activity_type, query in activity:
                        st.write(f"**User:** {username}, **Activity:** {activity_type}, **Query:** {query}")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    main_app()
else:
    login_page()
