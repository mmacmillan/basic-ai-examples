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
model = HuggingFaceEmbeddings(model_name='all-MiniLM-L12-v2')

# create a chroma instance from the set of documents; pass the embedding function so it generates vectors for us
db = Chroma.from_documents(split_docs, model)

# perform a semantic search on the query provided, finding the most relevant documents
print('quering for documents related to the 2nd amendment')
results = db.similarity_search('which amendment discusses the right to bear arms')

print(results)