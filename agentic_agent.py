import os
from groq import Groq
from scraper import scrape_tripadvisor_search

# Initialize Groq client
api_key = "API_KEY"
llm_client = Groq(api_key=api_key)

# Groq Model Wrapper
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

llm = GroqModelWrapper(llm_client, "meta-llama/llama-4-scout-17b-16e-instruct")

# Chat memory
chat_memory = []

def run_agent(user_text, image_path=None, preferred_city=None):
    """
    Main agent function that combines LLM and scraping
    """
    # Add to memory
    chat_memory.append(user_text)
    if len(chat_memory) > 5:
        chat_memory.pop(0)

    # Build prompt
    prompt = f"""You are a restaurant recommendation assistant for Pakistan.

Recent conversation:
{chr(10).join(f"- {msg}" for msg in chat_memory)}

Current request: "{user_text}"
City: {preferred_city}

Task: Provide a brief, friendly recommendation (2-3 sentences) about what restaurants to look for based on the user's request. Be specific and helpful.

Do NOT list restaurants - just give guidance on what to look for."""

    print(f"\n🤖 Asking LLM for recommendations...")
    llm_output = llm(prompt)
    print(f"✅ LLM Response: {llm_output[:100]}...")

    # Scrape TripAdvisor
    print(f"\n🔍 Scraping TripAdvisor for: {user_text} in {preferred_city}")
    scraped_data = scrape_tripadvisor_search(user_text, preferred_city=preferred_city)

    return {
        "llm_output": llm_output,
        "scraped_data": scraped_data
    }
