import streamlit as st
import tempfile
from rag_agent import PDFAgent

st.set_page_config(page_title="PDF AI Agent (No OpenAI)")

st.title("Open-Source AI Agent - Chat with PDF")

if "agent" not in st.session_state:
    st.session_state.agent = PDFAgent()
    st.session_state.chain = None

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    try:
        st.session_state.agent.load_pdf(pdf_path)
        print('pdf loaded')
        st.session_state.chain = st.session_state.agent.create_agent()
        st.success("PDF indexed successfully")
    except Exception as e:
        st.error(str(e))

query = st.text_input("Ask a question")

if query and st.session_state.chain:
    try:
        response = st.session_state.chain.run(query)
        print('response',response)
        st.write("### Answer")
        st.write(response)
    except Exception as e:
        st.error(f"Query failed: {e}")
