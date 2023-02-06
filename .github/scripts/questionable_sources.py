import requests
import warnings
from bs4 import BeautifulSoup

url = 'https://mediabiasfactcheck.com/fake-news/'
texts = []

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    response = requests.get(url, verify=False)

soup = BeautifulSoup(response.text, 'html.parser')

for link in soup.find_all('a'):
    if "www." in link.text:
        texts.append(link.text.replace("www.", "").replace("https://", ""))

cleaned_texts = []
for text in texts:
    try:
        index_slash = text.index("/")
        cleaned_text = text[:index_slash]
    except ValueError:
        cleaned_text = text
    try:
        index_bracket = cleaned_text.index("(")
        cleaned_text = cleaned_text[index_bracket+1:]
    except ValueError:
        cleaned_texts.append(cleaned_text.strip())

with open("texts.txt", "w") as file:
    for text in cleaned_texts:
        file.write(text + "\n")
