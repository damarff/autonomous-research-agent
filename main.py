import sys
from agent import ResearchAgent

def main():
    print("🤖 Autonomous Web Research Agent Initialized...")
    agent = ResearchAgent()
    
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        # Default test URL if none provided
        target_url = "https://example.com"
        print(f"[*] No URL provided. Using default test URL: {target_url}")
        print("[*] Usage for next time: python main.py https://company-website.com")
        print("-" * 50)
        
    agent.run(target_url)

if __name__ == "__main__":
    main()
