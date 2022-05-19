import requests
from .models import Quote

url = "https://zenquotes.io/api/random/random.json"

def get_quote():
    """
    Function to consume http request and return a Quote class instance
    """
    response = requests.get(url).json()

    random_quote = Quote(response[0]["a"], response[0]["q"])
    return random_quote
