import requests
import xmltodict
from bs4 import BeautifulSoup
import csv
import time
import json
import certifi
from langchain import OpenAI
import os
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
import sys
import time
import random
from langchain.docstore.document import Document

os.environ['OPENAI_API_KEY'] = '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'

OpenAI.api_key = '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'
llm = OpenAI(temperature=0.9)


url = 'https://www.jcrew.com/p/womens/categories/clothing/blazers/lady-jacket/odette-sweater-lady-jacket-in-cotton-blend-boucleacute/BR789?display=standard&fit=Classic&color_name=kelly-green&colorProductCode=BR789'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
script = soup.find('script', id="__NEXT_DATA__").getText()


def scriptToDoc(script, url):
    script = "Document(pagecontent='" + script + \
        "' metadata={'source': " + url + "'}"


documents = [scriptToDoc(script, url)]
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever())

query = "tell me about a product that jcrew offers"
chat_history = []
result = qa({"question": query, "chat_history": chat_history})
print(result)
