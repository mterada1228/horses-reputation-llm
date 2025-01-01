import logging
import os
import sys
import time
import requests

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec, Pinecone as PineconeClient
from bs4 import BeautifulSoup

load_dotenv()

# ロガーの設定
logging.basicConfig(
  format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Pinecone の設定
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

# スクレイピングでデータを得る
def data_from_scraping():
	r = requests.get("https://news.netkeiba.com/?pid=news_view&no=284559")
	r.encoding = r.apparent_encoding

	print(r.content)

# テキストデータを Pinecone に保存
if __name__ == "__main__":
	data_from_scraping()

	# file_path = sys.argv[1]
	# loader = TextLoader(file_path)
	# raw_docs = loader.load()

	# logger.info("Loaded %d documents", len(raw_docs))

	# text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=30)
	# docs = text_splitter.split_documents(raw_docs)
	
	# logger.info("Split %d documents", len(docs))

	# vectorstore = initialize_vector_store()
	# vectorstore.add_documents(docs)
