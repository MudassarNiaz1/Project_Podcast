
# load_pdf.py
from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path: str) :
    loader = PyPDFLoader(file_path)
    data = loader.load()
    return " ".join([doc.page_content for doc in data])


# split_text.py
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text(text: str, chunk_size=500, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_text(text)
