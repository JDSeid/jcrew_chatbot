from langchain import OpenAI
import os
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
import sys
import time
import random

os.environ['OPENAI_API_KEY'] = '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'

OpenAI.api_key = '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'
llm = OpenAI(temperature=0.9)

loader = CSVLoader(file_path='products.csv')
documents = loader.load()
print(type(documents[0]))

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever())

# query = "what is the most expensive pair of pants that jcrew offers"
# chat_history = []
# result = qa({"question": query, "chat_history": chat_history})
# print(result)


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

    result = qa({"question": prompt, "chat_history": chat_history})
    chat_history.append((prompt, result['answer']))

    slow_type(result['answer'])

    prompt = input()
slow_type("Goodbye! :)")
