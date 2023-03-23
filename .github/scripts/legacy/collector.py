import requests
import os


def external_blocklist_collector():
    with open("urls.txt") as file:
        urls = [line.strip() for line in file]

    parent_dir = "external"
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    for url in urls:
        filename = f"{parent_dir}/{url.replace('/', '_')}"
        filename = filename.replace("https:__", "")
        print(filename)
        with open(filename, "w") as f:
            response = requests.get(url, verify=False)
            text = response.text.rstrip()
            f.write(text)
        with open(filename, "r") as f:
            lines = f.readlines()
        with open(filename, "w") as f:
            for line in lines:
                if not line.startswith("#") and "." in line:
                    line = line.replace("www.", "")
                    line = line.replace("https://", "")
                    line = line.replace("http://", "")
                    f.write(line)


def main():
    external_blocklist_collector()

main()