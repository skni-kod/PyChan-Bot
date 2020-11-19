import requests
from bs4 import BeautifulSoup

def getDataFromAttachment(ctx):
    a = ctx.message.attachments[0]
    url = a.url
    file = requests.get(url)
    soup = BeautifulSoup(file.text, "html.parser")
    return soup