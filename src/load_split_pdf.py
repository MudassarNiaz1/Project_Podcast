from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
def pdfloader(file_path):
    loader = PyPDFLoader(file_path)
    extracted_data=loader.load()
    return extracted_data

def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 20)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks
















# # load_pdf.py
# from langchain_community.document_loaders import PyPDFLoader

# def load_pdf(file_path) :
#     loader = PyPDFLoader(file_path)
#     data = loader.load()
#     return " ".join([doc.page_content for doc in data])


# # split_text.py
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# def split_text(text: str, chunk_size=500, chunk_overlap=200):
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#     return text_splitter.split_text(text)

