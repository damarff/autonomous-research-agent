import os
import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Define the expected JSON structure using Pydantic (Strict Schema)
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
        
        # Initialize Google GenAI client
        self.client = genai.Client(api_key=self.api_key)

    def scrape_website(self, url: str) -> str:
        """Navigates to the URL using Playwright and extracts readable text."""
        print(f"[*] Agent is navigating to {url}...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Go to the website, wait until the network is idle
            try:
                page.goto(url, wait_until="networkidle", timeout=15000)
            except Exception as e:
                print(f"[!] Warning during navigation: {e}")
                
            html_content = page.content()
            browser.close()
            
        # Parse HTML to clean text
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Remove scripts, styles, and empty tags
        for script in soup(["script", "style", "nav", "footer"]):
            script.extract()
            
        text = soup.get_text(separator="\n")
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = "\n".join(chunk for chunk in chunks if chunk)
        
        print("[+] Website successfully scraped and cleaned.")
        return clean_text

    def analyze_company(self, website_text: str) -> str:
        """Uses Gemini LLM to analyze the scraped text and generate a B2B Lead Report."""
        print("[*] Agent is analyzing the company profile using LLM...")
        
        # Truncate text if it's too long (Gemini 1.5 flash has 1M context, but let's be safe)
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
            
            # Save to file
            domain = url.split("//")[-1].split("/")[0]
            with open(f"{domain}_report.json", "w", encoding="utf-8") as f:
                f.write(report)
            print(f"[+] Saved report to {domain}_report.json")
            
        except Exception as e:
            print(f"[!] Error executing Agent: {e}")
