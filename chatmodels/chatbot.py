from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage,SystemMessage, HumanMessage

model= ChatMistralAI(model ="mistral-small-2506",temperature=0.9)

messages=[
  SystemMessage(content="you are a funny AI agent")
]
print("---------welcome type 0 to exit the apllication -------------")
while True:
  prompt=input("You : ")
  messages.append((HumanMessage(content=prompt)))
  if prompt=="0":
    break
  response=model.invoke(messages)
  messages.append(AIMessage(content=response.content))
  print("Bot:" ,response.content)
  
print(messages)     