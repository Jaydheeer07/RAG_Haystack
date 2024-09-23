import streamlit as st
import os
from dotenv import load_dotenv
from backend.components.document_store import initialize_document_store
from backend.components.ingestion import create_ingestion_pipeline, ingest_document
from backend.components.retrieval import create_retrieval_pipeline, query_documents


load_dotenv()

st.set_page_config(page_title="RAG Chat App", layout="wide")

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'document_store' not in st.session_state:
    st.session_state.document_store = None

if 'ingestion_pipeline' not in st.session_state:
    st.session_state.ingestion_pipeline = None

if 'retrieval_pipeline' not in st.session_state:
    st.session_state.retrieval_pipeline = None

# Sidebar for configuration
st.sidebar.title("Configuration")

# OpenAI API Key input
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key

# Document upload
uploaded_file = st.sidebar.file_uploader("Upload a PDF document", type="pdf")
if uploaded_file is not None:
    with st.spinner("Processing document..."):
        # Save the uploaded file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Initialize document store and pipelines if not already done
        if st.session_state.document_store is None:
            st.session_state.document_store = initialize_document_store()
            st.session_state.ingestion_pipeline = create_ingestion_pipeline(st.session_state.document_store)
            st.session_state.retrieval_pipeline = create_retrieval_pipeline(st.session_state.document_store)
        
        # Ingest the document
        ingest_document(st.session_state.ingestion_pipeline, "temp.pdf")
        
        # Remove the temporary file
        os.remove("temp.pdf")
    
    st.sidebar.success("Document processed successfully!")

# Main chat interface
st.title("Chat with Your Documents")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for new question
if question := st.chat_input("Ask a question about your documents"):
    # Add user question to chat history
    st.session_state.chat_history.append({"role": "user", "content": question})
    
    # Display user question
    with st.chat_message("user"):
        st.markdown(question)
    
    # Generate and display answer
    if st.session_state.retrieval_pipeline:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = query_documents(st.session_state.retrieval_pipeline, question)
                st.markdown(answer)
        
        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
    else:
        st.error("Please upload a document first.")

# Run the Streamlit app
if __name__ == "__main__":
    st.write("Welcome to the RAG Chat App!")
