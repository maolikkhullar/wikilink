from langchain_google_genai import GoogleGenerativeAI
import os

class LLM:
    def __init__(self):
        self.llm = GoogleGenerativeAI(google_api_key=os.environ['API_KEY'],model="gemini-1.5-pro")

    def get_categories(self, article_text):
        prompt_template = """
                        You are an expert in categorizing Wikipedia articles. Your task is to assign relevant categories to the provided Wikipedia article, strictly based on its content, following Wikipedia's category naming conventions. The categories must be specific, accurate, and directly reflect the article’s main topics, subjects, and themes. Do not infer or generate categories unrelated to the given text.

                        Steps:
                        1. Read the entire article carefully and focus only on its content.
                        2. Identify the primary topics, subjects, and themes present in the article.
                        3. Assign categories that are hierarchical and as specific as possible (e.g., "20th-century German scientists" instead of just "Scientists").
                        4. Use existing Wikipedia category names or follow their standard naming conventions (e.g., proper capitalization, no extraneous prefixes like "Category:").
                        5. Output only the category names, one per line, without any prefixes, labels, or additional text.

                        Article:

                        {article_text}

                        Categories:
                        """

        prompt = prompt_template.format(article_text=article_text)

        response = self.llm(prompt)

        categories = response.strip().split('\n')
        return categories
    

