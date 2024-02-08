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

### Setup .env config
Rename .env-rename-me to .env.  If you're running the examples using OpenAI, make sure to add your api key to the .env file (replace the key thats already there).


### Setup ChromaDB
When using [ChromaDB](https://docs.trychroma.com/usage-guide) as a vector store, you have several options: run it in a container locally, or run it in a container in a cloud provider...running ChromaDB is required for the chroma client to connect (either using the ChromaDB library directly), or via [LangChain](https://js.langchain.com/docs/integrations/vectorstores/chroma#setup).  To run the container:

```
docker run -d -p 8000:8000 chromadb/chroma
```

### Setup OpenSearch
When using [OpenSearch](https://opensearch.org/) as a vector store and/or documnt index, for supporting semantic/neural search, k-nn indexes, and all the great functionality OpenSearch offers for the RAG/Semantic Search stack...you will need to initialize your cluster for neural search, configure a model for creating embeddings, and setup an ingestion pipeline to generate vectors when adding documents, etc.  It is well documented in the [neural search tutorial](https://opensearch.org/docs/2.11/search-plugins/neural-search-tutorial/) on the open search site, but I have put together a Postman collection to perform all the tasks necessary in order, including creating an index that supports neural search and some test queries.  In `opensearch-initialize-neural-search-for-cluster.json` there is a collection of tasks to perform from 0-14 in order.

You can run this against a cluster, or a single-node OpenSearch (development) instance.  To get up and running quickly, it is recommended to run OpenSearch in a docker container in a "single-node" configuration.  It is documented on the [Installing OpenSearch](https://opensearch.org/docs/latest/install-and-configure/install-opensearch/docker/) page, but to run a single-node config, the command is:

```
docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" opensearchproject/opensearch:2.11.1
```

Note: the default security is `Basic Auth` with admin:admin as the username/password.

