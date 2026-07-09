import os
from google import genai
from google.genai import types

def analyze_task_priority(title, description):
    """
    Leverages Google's Gemini LLM to semantically analyze the task
    context and return an accurate priority tag.
    """
    # 1. Grab your API key safely from environment variables
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Fallback to safe default if you haven't set up the key yet
    if not api_key:
        return "Medium"
        
    try:
        # 2. Initialize the official Gemini client
        client = genai.Client(api_key=api_key)
        
        # 3. Create a strict prompt instructing the AI how to behave
        prompt = f"""
        You are an AI backend module for a project management tool.
        Analyze the following task and categorize its priority strictly as 'Low', 'Medium', or 'High'.
        Consider factors like systemic urgency, blockages, or routine maintenance.
        
        Task Title: {title}
        Task Description: {description}
        
        Respond with exactly ONE word from these options: Low, Medium, High. Do not include punctuation or explanations.
        """
        
        # 4. Generate content using the lightweight, fast gemini-2.5-flash model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        # 5. Clean up the response text
        result = response.text.strip()
        
        if result in ['Low', 'Medium', 'High']:
            return result
            
        return "Medium" # Fallback if the AI gives an unexpected response
        
    except Exception as e:
        print(f"AI Engine Error: {e}")
        return "Medium" # Fallback if the network request fails