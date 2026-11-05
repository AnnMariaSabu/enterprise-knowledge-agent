import streamlit as st

import config
from agent import run_agent
from ingest import run_ingest
from permissions import ROLES
from rag import rewrite_question


def show_steps(searches, understood_as):
    if searches:
        with st.expander("How I found this"):
            if understood_as:
                st.write("🧠 Understood as: " + understood_as)
            for query in searches:
                st.write("🔍 " + query)


def show_sources(passages):
    if passages:
        with st.expander("Sources"):
            for passage in passages:
                st.markdown(f"**📄 {passage['source']}**")
                st.caption(passage["text"])


st.title("Acme Policy Assistant")
st.write("Ask me anything about Acme Corp's HR, IT and travel policies.")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    role = st.selectbox("Your role", ROLES)
    if st.session_state.get("role") != role:
        st.session_state.role = role
        st.session_state.messages = []

    if st.button("🆕 New chat"):
        st.session_state.messages = []
        st.rerun()

    st.header("Add a document")
    department = st.selectbox("Department", ["hr", "it", "travel"])
    uploaded = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])

    if uploaded is not None and st.button("Upload and add"):
        save_path = config.DOCS_DIR / department / uploaded.name
        save_path.write_bytes(uploaded.getvalue())
        with st.spinner("Adding the document..."):
            run_ingest()
        st.success(f"Added {uploaded.name}. You can ask about it now!")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        show_steps(message.get("searches"), message.get("understood_as"))
        show_sources(message.get("passages"))

question = st.chat_input("Ask a question...")

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking and searching..."):
            full_question = rewrite_question(question, st.session_state.messages)
            result = run_agent(full_question, role)

        understood_as = full_question if full_question != question else None

        st.write(result["answer"])
        show_steps(result["searches"], understood_as)
        show_sources(result["passages"])

    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "searches": result["searches"],
        "understood_as": understood_as,
        "passages": result["passages"],
    })