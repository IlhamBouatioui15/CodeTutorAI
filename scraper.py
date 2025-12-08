# scraper.py
import requests
from bs4 import BeautifulSoup
import json

LANGUAGES = {
    "Python": "https://www.geeksforgeeks.org/python-programming-language/",
    "Java": "https://www.geeksforgeeks.org/java/",
    "C": "https://www.geeksforgeeks.org/c-programming-language/",
    "C++": "https://www.geeksforgeeks.org/c-plus-plus/",
    "JavaScript": "https://www.geeksforgeeks.org/javascript/",
    "Go": "https://www.geeksforgeeks.org/go-programming-language/",
    "Ruby": "https://www.geeksforgeeks.org/ruby-programming-language/",
    "Rust": "https://www.geeksforgeeks.org/rust-programming-language/",
    "PHP": "https://www.geeksforgeeks.org/php/",
    "Swift": "https://www.geeksforgeeks.org/swift-programming-language/"
}

def scrape_geeksforgeeks():
    all_texts = []
    for lang, url in LANGUAGES.items():
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Erreur pour {lang}: {res.status_code}")
            continue
        soup = BeautifulSoup(res.text, "html.parser")
        paragraphs = [p.text for p in soup.find_all("p") if p.text.strip()]
        paragraphs = [f"[{lang}] {p}" for p in paragraphs]
        all_texts.extend(paragraphs)
    return all_texts

if __name__ == "__main__":
    all_texts = scrape_geeksforgeeks()
    # Sauvegarder dans un fichier JSON
    with open("geeks_texts.json", "w", encoding="utf-8") as f:
        json.dump(all_texts, f, ensure_ascii=False, indent=2)
    print("Scraping terminé et données sauvegardées dans geeks_texts.json")