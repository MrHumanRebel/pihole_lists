import requests
from bs4 import BeautifulSoup

def jogserto_webaruhazak(base_url, file_name):
    texts = []

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a'):
        href = link.get("href")
        if href and href.startswith("http://www."):
            texts.append(href.replace("http://www.", "").replace("https://", ""))

    cleaned_texts = []
    for text in texts:
        try:
            index_slash = text.index("/")
            cleaned_text = text[:index_slash]
        except ValueError:
            cleaned_text = text
        try:
            index_bracket = cleaned_text.index("(")
            cleaned_texts.append(cleaned_text[:index_bracket].strip())
        except ValueError:
            cleaned_texts.append(cleaned_text.strip())

    with open(file_name, "w+") as file:
        for text in cleaned_texts:
            file.write(text + "\n")

def main():
    base_url = 'https://jogsertowebaruhazak.kormany.hu/'
    file_name = "custom/jogsertowebaruhazak.txt"
    
    print(f"Loading {file_name}...")
    jogserto_webaruhazak(base_url, file_name)

if __name__ == "__main__":
    main()
