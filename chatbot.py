from langchain import OpenAI
import os
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import sys


import time
import random

api_key = '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'
os.environ['OPENAI_API_KEY'] = api_key

OpenAI.api_key = api_key
llm = OpenAI(temperature=0.9)

loader = CSVLoader(file_path='products.csv')
documents = loader.load()

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever())

typing_speed = 175  # wpm


def slow_type(t):
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/typing_speed)
    time.sleep(1)
    print('')


os.system('clear')
os.system('clear')
slow_type("Hi! I am a chatbot that can answer simple questions about the products offered at JCrew.")
slow_type("I can provide information about product's name and price, and can give short descriptions about each product.")
slow_type("Ask me a question to get started, or type 'quit' to exit: ")
print()
prompt = input()

chat_history = []
while ("quit" not in prompt.lower()):
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=False)
    qa = ConversationalRetrievalChain.from_llm(
        llm, vectorstore.as_retriever(), memory=memory)
    result = qa({"question": prompt, "chat_history": chat_history})
    chat_history.append((prompt, result['answer']))

    slow_type(result['answer'])

    prompt = input()
slow_type("Goodbye! :)")
