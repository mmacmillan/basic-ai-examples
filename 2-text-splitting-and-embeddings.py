import os

# load all env vars from dotenv config
from dotenv import load_dotenv
load_dotenv()

# langchain imports for text splitting, embeddings, and the chroma vector db
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# load the bill of rights as a Document
loader = TextLoader('./bill-of-rights.txt')
docs = loader.load()

# use the splitter to chunk the text, if the chunk_size is too large, it will ignore the \n\n default
# separator, so we set the chunk size small to ensure it hits either new line, or 100 characters for small chunks
char_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)

# split the content up either by sentence or max chunk size
split_docs = char_splitter.split_documents(docs)
#for i in split_docs:
#    print(i.page_content +'\n')

# generate vectors for the chunked page content
embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L12-v2')

# generate embeddings manually from the split documents
# embed_documents expects an array of strings, not Documents (their text is in .page_content)
split_docs_content = [doc.page_content for doc in split_docs]
doc_vectors = embeddings.embed_documents(split_docs_content)

print('split documents')
print(split_docs)
print('vectors')
print(doc_vectors)