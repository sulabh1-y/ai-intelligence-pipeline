import asyncio
import json
import csv
from src.crawler.base import BaseCrawler
from src.llm_engine.orchestrator import LLMOrchestrator
from bs4 import BeautifulSoup

class PapersScraper(BaseCrawler):

    async def scrape_papers(self, limit=20):
        url = f"http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=lastUpdatedDate&sortOrder=descending&max_results={limit}"
        xml_data = await self.fetch(url)

        if not xml_data:
            print("Failed to fetch from arXiv API")
            return []

        # Use xml parser for the arXiv API response
        soup = BeautifulSoup(xml_data, "xml")

        papers = []
        entries = soup.find_all("entry")

        for entry in entries:
            # Extract paper link (id in Atom feed is the URL)
            link_tag = entry.find("id")
            link = link_tag.text.strip() if link_tag else ""

            # Extract title
            title_tag = entry.find("title")
            title = title_tag.text.replace("\n", " ").strip() if title_tag else "No Title"

            # Extract authors
            authors_tags = entry.find_all("author")
            authors_list = [author.find("name").text.strip() for author in authors_tags if author.find("name")]
            authors = ", ".join(authors_list) if authors_list else "N/A"

            # Extract abstract/summary
            abstract_tag = entry.find("summary")
            abstract = abstract_tag.text.replace("\n", " ").strip() if abstract_tag else "N/A"

            papers.append({
                "title": title,
                "link": link,
                "authors": authors,
                "abstract": abstract
            })

        return papers

async def main():
    scraper = PapersScraper()
    papers = await scraper.scrape_papers(limit=5)

    llm = LLMOrchestrator()

    processed_data = []

    for p in papers:
        structured = llm.process_paper(p)
        processed_data.append(structured)

    # Save to CSV
    with open("outputs/papers.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["title", "link", "authors", "abstract"]
        )
        writer.writeheader()
        writer.writerows(papers)

    print("✅ Raw data saved to outputs/papers.csv")

    # Save structured JSON
    with open("outputs/papers.json", "w", encoding="utf-8") as f:
        json.dump(processed_data, f, indent=4)

    print("✅ Structured JSON saved to outputs/papers.json")

    # Print structured LLM output
    print("\n🔹 LLM Processed Output:")
    for item in processed_data:
        print("\n---")
        print(item)


if __name__ == "__main__":
    asyncio.run(main())