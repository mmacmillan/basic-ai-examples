# Basic AI Examples

This is a collection of basic samples that progressively add more complexity.  Most of the samples use LangChain.  The goal is to progressively cover topics from simple model io, to splitting text and creating embeddings, to interacting with a vector store and doing semantic search, to building out custom RAG (Retrieval Augmented Generation) using a variety of combinations of embedding libraries, vector stores, and LLMs.

## Before running any of the examples...

#### Install the dependencies:

Python
```
pip install langchain
pip install langchain-openai
pip install sentence_transformers
pip install chromadb
```

Javascript
```
npm install
```

### Setup ChromaDB
When using [ChromaDB](https://docs.trychroma.com/usage-guide) as a vector store, you have several options: run it in a container locally, or run it in a container in a cloud provider...running ChromaDB is required for the chroma client to connect (either using the ChromaDB library directly), or via [LangChain](https://js.langchain.com/docs/integrations/vectorstores/chroma#setup).  To run the container:

```
docker run -d -p 8000:8000 chromadb/chroma
```


### Setup .env config
Rename .env-rename-me to .env.  If you're running the examples using OpenAI, make sure to add your api key to the .env file (replace the key thats already there).


