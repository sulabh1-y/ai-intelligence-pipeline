USE_LLM = False


class LLMOrchestrator:

    def clean_authors(self, authors_text):
        # fix spacing issues and split properly
        authors_text = authors_text.replace("',", ",").replace("  ", " ")
        return [a.strip() for a in authors_text.split(",")]


    def detect_category(self, text):
        text = text.lower()

        if "agent" in text or "multi-agent" in text:
            return "AI Agents"
        elif "vision" in text or "image" in text or "video" in text:
            return "Computer Vision"
        elif "language" in text or "llm" in text or "text" in text:
            return "NLP"
        elif "causal" in text or "reasoning" in text:
            return "AI Reasoning"
        elif "robot" in text:
            return "Robotics"
        else:
            return "General AI"


    def process_paper(self, paper):

        authors_list = self.clean_authors(paper["authors"])
        category = self.detect_category(paper["abstract"])

        return {
            "recordType": "RESEARCH_PAPER",
            "content": {
                "title": paper["title"],
                "authors": authors_list,
                "category": category,
                "summary": paper["abstract"]
            }
        }