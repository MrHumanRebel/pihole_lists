import requests
import os


with open("docs/urls.txt") as file:
    urls = [line.strip() for line in file]


for i, url in enumerate(urls):
    filename = "external/" + f"{i+1}_{url.split('/')[-1]}"
    with open(filename, "w") as f:
        for url in urls:
            response = requests.get(url)
            with open(url.split("/")[-1], "w") as f:
                f.write(response.text)
