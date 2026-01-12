# cloud_llm.py
"""
Team B - Cloud LLM Integration
Handles Plan Mode chat using Cloud APIs (OpenAI/Anthropic).
"""
import os
from openai import OpenAI

# Initialize OpenAI client (requires OPENAI_API_KEY env var)
client = None
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        client = OpenAI(api_key=api_key)
except Exception as e:
    print(f"Warning: OpenAI client initialization failed: {e}")

def chat(prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Send prompt to Cloud LLM and get response.
    
    Args:
        prompt: User's message/query
        model: Model to use (default: gpt-4o-mini for cost efficiency)
    
    Returns:
        AI response string
    """
    # If no API key, return mock response
    if not client:
        return _mock_response(prompt)
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant integrated into the Frai AI Keyboard."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Cloud LLM error: {e}")
        return f"Error: {str(e)}"

def _mock_response(prompt: str) -> str:
    """Mock response when no API key is available"""
    return f"[Mock Response] You asked: '{prompt[:50]}...' (Set OPENAI_API_KEY to enable real responses)"
