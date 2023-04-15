
from langchain import OpenAI
import os
os.environ['OPENAI_API_KEY'] = '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'

OpenAI.api_key = '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'
llm = OpenAI(temperature=0.9)

text = "How far away is the moon"

print(llm(text))
