from langchain.tools import tool
import requests as re 



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