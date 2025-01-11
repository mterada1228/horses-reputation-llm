import logging
import os
import sys
import time
import requests

from dotenv import load_dotenv

from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_pinecone import PineconeVectorStore

from pinecone import ServerlessSpec, Pinecone as PineconeClient

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

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
def initialize_selenium_driver():
	service = Service()
	options = webdriver.ChromeOptions()
	options.add_argument("--headless=new")
	driver = webdriver.Chrome(service=service, options=options)

	return driver

def urls_from_netkeiba_news(start_page=1, end_page=1):
	urls = []

	driver = initialize_selenium_driver()

	for page_num in range(start_page, end_page + 1):
		logger.info(f"scrape from https://news.netkeiba.com/?pid=news_backnumber&page={page_num}")

		driver.get(f"https://news.netkeiba.com/?pid=news_backnumber&page={page_num}")

		html = driver.page_source
		bsObj = BeautifulSoup(html, "html.parser")

		articles_div = bsObj.find("div", id="news-view-default")
		articles_a = articles_div.find_all("a", class_="ArticleLink")

		logger.info(f"find {len(articles_a)} articles")

		for a in articles_a:
			urls.append(a.get("href"))

		time.sleep(1)

	return urls

def text_from_netkeiba_news(url):
	logger.info(f"scrape from {url}")

	r = requests.get(url)
	r.encoding = r.apparent_encoding

	bsObj = BeautifulSoup(r.text, "html.parser")
	body = bsObj.find("div", class_="NewsArticle_Body")

	return r.url, body.text

# テキストデータを Pinecone に保存
if __name__ == "__main__":
	urls = urls_from_netkeiba_news(start_page=int(sys.argv[1]), end_page=int(sys.argv[2]))

	for url in urls:
		id_prefix, raw_text = text_from_netkeiba_news(url)

		logger.info("Loaded %d documents", len(raw_text))

		text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=30)
		texts = text_splitter.split_text(raw_text)
		
		logger.info("Split %d documents", len(texts))

		ids = [f"{id_prefix}_{i}" for i in range(len(texts))]

		vectorstore = initialize_vector_store()
		vectorstore.add_texts(ids=ids, texts=texts)

		time.sleep(1)