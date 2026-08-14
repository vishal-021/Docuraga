import os
import requests
from urllib.parse import urlparse

def Download(pdf_links,path):
    os.makedirs(path, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for i, url in enumerate(pdf_links, start=1):
        try:
            response = requests.get(
                url,
                headers=headers,
                stream=True,
                timeout=30
            )

            response.raise_for_status()
            filename = os.path.basename(urlparse(response.url).path)

            if not filename.endswith(".pdf"):
                filename = f"document_{i}.pdf"

            filepath = os.path.join(path, filename)

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print(f"Downloaded: {filename}")

        except Exception as e:
            print(f"Failed: {url}")
            print(e)