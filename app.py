import streamlit as st
from main import answer_question

st.set_page_config(page_title="Reddit RAG Chatbot", page_icon="🤖")
st.title("🤖 Ask Reddit")
st.caption("Ask anything — I'll search Reddit and summarize what people say.")

# keep chat history in session
if "messages" not in st.session_state:
    st.session_state.messages = []

# display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# chat input
if question := st.chat_input("Ask anything..."):
    # show user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # get answer
    with st.chat_message("assistant"):
        with st.spinner("Searching Reddit..."):
            answer, sources = answer_question(question)
        st.markdown(answer)
        with st.expander("Sources"):
            for post in sources:
                st.markdown(f"- [{post['title']}]({post['url']})")

    st.session_state.messages.append({"role": "assistant", "content": answer})