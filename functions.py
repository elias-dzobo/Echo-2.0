from langchain.tools import tool
import requests as re 
from todoist_api_python.api import TodoistAPI


@tool 
def get_crypto_updates(token: str) -> str:
    """
    Useful for answering questions about the price of a particular cryptocurrency. if the cryptocurrency is unknown,
    do not assume, ask the user 
    """

    url = 'https://api.coingecko.com/api/v3/simple/price?ids={token}&vs_currencies=usd'

    response = re.request(url)

    token = response[token]


    return token['usd'] 

def add_todo(todo: str):
    """
    useful when user wants to add an item to their to do list 
    """

    api = TodoistAPI('c861b26a39eabe6b4c7f1295bf8ce4029eb630f9')

    try:
        task = api.add_task(content=todo, project_id='2325260660')
        print(task)

    except Exception as error:
        print(error)
    

if __name__ == '__main__':
    add_todo('Go to the gym')