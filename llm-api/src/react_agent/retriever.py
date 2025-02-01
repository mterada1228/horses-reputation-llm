import os
import time

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from pinecone import ServerlessSpec, Pinecone as PineconeClient

def initialize_vector_store():
	pinecone_api_key = os.environ["PINECONE_API_KEY"]

	pc = PineconeClient(api_key=pinecone_api_key)

	index_name = os.environ["PINECONE_INDEX"]
	existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

	if index_name not in existing_indexes:
		pc.create_index(
				name=index_name,
				dimension=1536,
				metric="cosine",
				spec=ServerlessSpec(cloud="aws", region="us-east-1"),
		)
		while not pc.describe_index(index_name).status["ready"]:
			time.sleep(1)

	index = pc.Index(index_name)
	embedding = OpenAIEmbeddings()

	vector_store = PineconeVectorStore(index=index, embedding=embedding)

	return vector_store

def create_retriever():
	vector_store = initialize_vector_store()

	return vector_store.as_retriever()
