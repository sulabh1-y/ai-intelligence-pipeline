import asyncio
import json
import csv
from src.crawler.base import BaseCrawler
from src.llm_engine.orchestrator import LLMOrchestrator
from bs4 import BeautifulSoup


class PapersScraper(BaseCrawler):

    async def scrape_papers(self):
        url = "https://arxiv.org/list/cs.AI/recent"
        html = await self.fetch(url)

        if not html:
            print("Failed to fetch")
            return []

        soup = BeautifulSoup(html, "html.parser")

        papers = []

        entries = soup.find_all("dt")
        descriptions = soup.find_all("dd")

        for i in range(min(5, len(entries))):
            entry = entries[i]
            desc = descriptions[i]

            # Extract paper link
            link_tag = entry.find("a", title="Abstract")
            link = "https://arxiv.org" + link_tag["href"]

            # Extract title
            title_tag = desc.find("div", class_="list-title mathjax")
            title = title_tag.text.replace("Title:", "").strip()

            # Fetch paper detail page
            paper_html = await self.fetch(link)
            if not paper_html:
                continue

            paper_soup = BeautifulSoup(paper_html, "html.parser")

            # Extract authors
            authors_tag = paper_soup.find("div", class_="authors")
            authors = authors_tag.text.replace("Authors:", "").strip() if authors_tag else "N/A"

            # Extract abstract
            abstract_tag = paper_soup.find("blockquote", class_="abstract mathjax")
            abstract = abstract_tag.text.replace("Abstract:", "").strip() if abstract_tag else "N/A"

            papers.append({
                "title": title,
                "link": link,
                "authors": authors,
                "abstract": abstract
            })

        return papers


async def main():
    scraper = PapersScraper()
    papers = await scraper.scrape_papers()

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