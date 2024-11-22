import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.spacy_embeddings import SpacyEmbeddings
from langchain_community.vectorstores import FAISS
from upload_s3 import upload_file_to_s3

embeddings = SpacyEmbeddings(model_name="en_core_web_sm")

def pdf_read(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    return chunks

def vector_store(text_chunks):
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_db")


def upload_pdf_and_process():
    with st.sidebar:
        pdf_doc = st.file_uploader("Upload your PDF", type=["pdf"])
        if pdf_doc and 'pdf_text' not in st.session_state:
            with st.spinner("Processing PDF..."):
                raw_text = pdf_read(pdf_doc)
                st.session_state['pdf_text'] = raw_text
                text_chunks = get_chunks(raw_text)
                vector_store(text_chunks)
                st.session_state['pdf_processed'] = True
                # st.success("PDF processed successfully!")
                status_code = upload_file_to_s3(pdf_doc, pdf_doc.name)
                
                if status_code == 204:
                    # pass
                    st.success("PDF processed and uploaded to S3 successfully!")
                else:
                    st.error("Failed to upload PDF to S3.")
                
                st.session_state['pdf_processed'] = True