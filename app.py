import streamlit as st

from rag import answer


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

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        show_sources(message.get("passages"))

question = st.chat_input("Ask a question...")

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the policies..."):
            result = answer(question)
        st.write(result["answer"])
        show_sources(result["passages"])

    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.messages.append(
        {"role": "assistant", "content": result["answer"], "passages": result["passages"]}
    )