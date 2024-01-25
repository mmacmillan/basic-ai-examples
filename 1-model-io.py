#load all env vars from dotenv config
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from langchain.schema import HumanMessage
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate

modelName = "gpt-3.5-turbo-1106"
text = "what is the 2nd amendment of the constitution?"

#create a reference to the OpenAI llm; this accepts and returns a string
llm = OpenAI()

#the chat model sends messages with more context; returns a Message object
chatModel = ChatOpenAI(model_name=modelName)

#simply calling openai with a string promopt
print("sending message")
print(llm.invoke(text));

#sending using HumanMessage
print("\nsending using HumanMessage")
msg = HumanMessage(content=text)
print(chatModel.invoke([msg]))

#sending using a prompt template
print("\nsending using a PromptTemplate")
prompt = PromptTemplate.from_template("when was the {amendment} ratified?")
print(chatModel.invoke(prompt.format(amendment="5th")))


#sending using a chain
print("\nsending using chain")
template = """Question: {amendment}

Answer: when was the amendment the user is asking for created?"""
prompt = PromptTemplate(template=template, input_variables=["amendment"])
llmChain = LLMChain(prompt=prompt, llm=llm)
print(llmChain.invoke("4th amendment"))

#create a chain using pipe
chain = prompt | llm
print(chain.invoke({ "amendment": "6th amendment" }))

#create a chat prompt template
chatTemplate = ChatPromptTemplate.from_messages([
    ("system", "you are a helpful bot that explains things with kindness"),
    ("human", "what is the general summary of the 2nd amendment?")
])

res = chatModel.invoke(chatTemplate.format_messages())
print(res)
