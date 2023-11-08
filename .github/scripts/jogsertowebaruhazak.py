import requests

def extract_urls_from_server_response(base_url, page_start, page_end, file_name):
    texts = []

    for page in range(page_start, page_end + 1):
        url = f"{base_url}&page={page}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            urls = [entry['url'] for entry in data['content']]
            texts.extend(urls)

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
    base_url = 'https://jogsertowebaruhazak.kormany.hu/api/ios/search?page=40&size=10'
    page_start = 1
    page_end = 45  # Adjust the page range as needed
    file_name = "custom/jogsertowebaruhazak.txt"

    print(f"Loading {file_name}...")
    extract_urls_from_server_response(base_url, page_start, page_end, file_name)

if __name__ == "__main__":
    main()
