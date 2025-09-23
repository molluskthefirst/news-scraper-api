from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route("/scrape", methods=["GET"])
def scrape():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    soup = BeautifulSoup(r.text, "html.parser")

    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else None
    author = soup.find("meta", {"name": "author"})
    author = author["content"] if author else None
    paragraphs = [p.get_text(" ", strip=True) for p in soup.select("article p")]

    return jsonify({
        "url": url,
        "title": title,
        "author": author,
        "content": " ".join(paragraphs)
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
