import os
import openai 
import langchain 
from dotenv import find_dotenv, load_dotenv
from langchain.agents import AgentExecutor, AgentType, Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import tool 
from langchain.schema import SystemMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
import requests as re
import json
from todoist_api_python.api import TodoistAPI
from langchain.memory import ConversationBufferMemory

_ = load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']



llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo-0613')

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Your name is Echo, you are astraldev's personal assistant developed to help him with his day to day operations",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

@tool 
def get_crypto_updates(token: str) -> json:
    """
    returns the price of a particular cryptocurrency. 
    """

    url = 'https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=usd'.format(token)

    response = re.get(url)

    json_form = response.json()

    return json_form[token]['usd']

@tool
def add_todo(todo: str):
    """
    useful when user wants to add an item to their to do list 
    """

    api = TodoistAPI('c861b26a39eabe6b4c7f1295bf8ce4029eb630f9')

    try:
        task = api.add_task(content=todo, project_id='2325260660')
        #memory.save_context(task) 

        print('Task Added')

        return task

    except Exception as error:
        
        return error
    
    



tools = [
  get_crypto_updates, add_todo
]

memory = ConversationBufferMemory(memory_key="db")


llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])

system_message = SystemMessage(
    content= "Your name is Echo, you are astraldev's personal assistant developed to help him with his day to day operations"
)

echo_kwargs = {
    "system_message": system_message
}

""" echo = initialize_agent(
    tools, llm, agent=AgentType.OPENAI_MULTI_FUNCTIONS, verbose=True, agent_kwargs=echo_kwargs 
) """


echo = (
    {
        "input": lambda x: x['input'],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=echo, tools=tools, verbose=True, memory=memory)

agent_executor.invoke({"input": "what is the Task id for Code a game?"})