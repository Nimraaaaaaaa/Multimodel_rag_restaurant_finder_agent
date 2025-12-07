import os
from groq import Groq
from scraper import scrape_tripadvisor_search

# Initialize Groq client
api_key = "Api_KEY"
llm_client = Groq(api_key=api_key)

# Tools
def tool_scrape(query):
    return scrape_tripadvisor_search(query)

# Wrapper for Groq — handles chat completions
class GroqModelWrapper:
    def __init__(self, client, model_id: str):
        self.client = client
        self.model_id = model_id

    def __call__(self, prompt: str):
        resp = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model_id
        )
        return resp.choices[0].message.content

# Use wrapper with your desired Groq model
llm = GroqModelWrapper(llm_client, "meta-llama/llama-4-scout-17b-16e-instruct")

# Short-term memory list (last 5 chats)
chat_memory = []

def run_agent(user_text, image_path=None):
    # Add current input to memory
    chat_memory.append(user_text)
    if len(chat_memory) > 5:
        chat_memory.pop(0)

    # Build prompt including recent chat history
    prompt = "Recent chats:\n"
    for msg in chat_memory:
        prompt += f"- {msg}\n"
    prompt += f"\nUser wants: {user_text}. Find best restaurants, use scraping if needed. Ignore all explanations. Only list restaurant names, addresses, and ratings. Do not mention Yelp or other platforms."

    # Run LLM directly instead of AGNO
    
    output = llm(prompt)

    # Optionally use scraping tool if needed
    if "scrape" in user_text.lower():
        output += "\n\nScrape result:\n" + tool_scrape(user_text)

    return output

