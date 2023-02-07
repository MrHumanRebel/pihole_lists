import requests
import os

with open("docs/urls.txt") as file:
    urls = [line.strip() for line in file]

parent_dir = "external"
if not os.path.exists(parent_dir):
    os.makedirs(parent_dir)

for url in urls:
    url = url.replace("https:", "")
    filename = f"{parent_dir}/{url.replace('/', '_')}"
    with open(filename, "w") as f:
        response = requests.get(url)
        f.write(response.text)
