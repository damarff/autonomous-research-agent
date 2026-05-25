import os
import json
import requests
from bs4 import BeautifulSoup
from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class LeadReport(BaseModel):
    company_name: str
    main_business: str
    target_audience: str
    key_products_or_services: list[str]
    pain_points_we_can_solve: list[str]
    suggested_cold_email_subject: str

class ResearchAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set. Please add it to your .env file.")
        self.client = genai.Client(api_key=self.api_key)

    def scrape_website(self, url: str) -> str:
        print(f"[*] Agent is navigating to {url}...")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            html_content = response.text
        except Exception as e:
            print(f"[!] Warning during navigation: {e}")
            html_content = "<html><body>Failed to load</body></html>"
            
        soup = BeautifulSoup(html_content, "html.parser")
        for script in soup(["script", "style", "nav", "footer"]):
            script.extract()
            
        text = soup.get_text(separator="\n")
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = "\n".join(chunk for chunk in chunks if chunk)
        
        print("[+] Website successfully scraped and cleaned.")
        return clean_text

    def analyze_company(self, website_text: str) -> str:
        print("[*] Agent is analyzing the company profile using LLM...")
        if len(website_text) > 50000:
            website_text = website_text[:50000]
            
        prompt = f"""
        You are an elite B2B Sales Development Representative (SDR) and Research Agent.
        I have scraped the landing page of a company. 
        Your task is to analyze the text and extract key business intelligence to help me write a highly personalized cold email.
        
        Answer ONLY using the provided JSON schema. If information is missing, infer logically or write "Unknown".
        
        COMPANY WEBSITE TEXT:
        {website_text}
        """
        
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=LeadReport,
                temperature=0.2
            ),
        )
        return response.text

    def run(self, url: str):
        try:
            text = self.scrape_website(url)
            report = self.analyze_company(text)
            
            print("\n" + "="*50)
            print("🚀 LEAD GENERATION REPORT (JSON)")
            print("="*50)
            print(report)
            print("="*50 + "\n")
            
            domain = url.split("//")[-1].split("/")[0]
            with open(f"{domain}_report.json", "w", encoding="utf-8") as f:
                f.write(report)
            print(f"[+] Saved report to {domain}_report.json")
            
        except Exception as e:
            print(f"[!] Error executing Agent: {e}")
