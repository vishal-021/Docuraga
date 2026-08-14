import asyncio
import requests

from ddgs import DDGS
from crawl4ai import AsyncWebCrawler


def search_web(queries, max_results=5):

    urls = set()

    with DDGS() as ddgs:
        for query in queries:
            results = ddgs.text(query, max_results=max_results)
            for result in results:
                urls.add(result["href"])

    return list(urls)


def is_pdf(url):

    try:

        response = requests.get(
            url,
            allow_redirects=True,
            timeout=10
        )

        content_type = response.headers.get("Content-Type", "")

        return "application/pdf" in content_type.lower()

    except:
        return False


async def crawl_page(crawler, url):
    if is_pdf(url):
        return {
            "url" : url,
            "pdf_links": [url]
        }
    else:

        result = await crawler.arun(url=url)

        pdf_links = []

        internal = result.links.get("internal", [])
        external = result.links.get("external", [])

        for link in internal + external:

            href = link.get("href")

            if href and is_pdf(href):
                pdf_links.append(href)
        metadata = result.metadata or {}

        return {
            "url": url,
            "title": metadata.get("title"),
            "description": metadata.get("description"),
            "markdown": result.markdown,
            "pdf_links": pdf_links
        }


async def GetFromNet(queries):

    urls = search_web(queries)
    pages = []
    print(f"Found {len(urls)} webpages\n")

    async with AsyncWebCrawler() as crawler:

        for url in urls:

            try:

                page = await crawl_page(crawler, url)
                pages.append(page)

            except Exception as e:
                print(f"Failed: {url}")
                print(e)
    return pages

def Run(queries):
    return asyncio.run(GetFromNet(queries))