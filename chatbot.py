from langchain import OpenAI
import os
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain

os.environ['OPENAI_API_KEY'] = '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'

OpenAI.api_key = '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'
llm = OpenAI(temperature=0.9)

loader = CSVLoader(file_path='products.csv')
documents = loader.load()

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever())

query = "what is the most expensive pair of pants that jcrew offers"
chat_history = []
result = qa({"question": query, "chat_history": chat_history})
print(result["answer"])

# conversation = ConversationChain(llm=llm)

# text_splitter = CharacterTextSplitter(
#     separator=", Document",
#     chunk_size=2000,
#     chunk_overlap=0,
# )
# texts = text_splitter.create_documents(documents)
# text = "How far away is the moon"

# print(llm(text))
