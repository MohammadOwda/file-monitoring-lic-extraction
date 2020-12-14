import requests
from datetime import datetime

API_ENDPOINT = ""

def sendPlate(self, data):
    requests.post(url = API_ENDPOINT, data = data) 