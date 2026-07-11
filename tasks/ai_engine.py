import os
from groq import Groq

def analyze_task_priority(title, description):
    """
    Leverages Meta's Llama 3 model via Groq Cloud to semantically 
    analyze task details and assign an automated priority tier.
    """
    # 1. Grab your Groq API key safely from environment variables
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        print("⚠️ DEBUG: GROQ_API_KEY is missing from environment variables!")
        return "Medium"
        
    try:
        # 2. Initialize the official Groq client
        client = Groq(api_key=api_key)
        
        # 3. Formulate a system message + user prompt to force strict output
        system_instruction = "You are a backend classification module. You must respond with exactly ONE word from these choices: Low, Medium, High. Do not include any punctuation, spaces, or explanations."
        
        user_prompt = f"Task Title: {title}\nTask Description: {description}"
        
        # 4. Trigger the chat completion using a rock-solid model ID
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Blazing fast and highly precise for classification
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0,  # 0.0 minimizes creativity and forces strict rule-following
            max_tokens=5      # Keeps token limits tiny
        )
        
        # 5. Extract and aggressively sanitize the output text
        # .replace(".", "") strips out rogue accidental periods
        result = completion.choices[0].message.content.strip().replace(".", "").capitalize()
        
        print(f"🤖 AI RAW RESPONSE: '{result}'")  # Look at your VS Code terminal for this!
        
        if result in ['Low', 'Medium', 'High']:
            return result
            
        print(f"⚠️ DEBUG: AI returned invalid option '{result}', defaulting to Medium.")
        return "Medium"  
        
    except Exception as e:
        print(f"❌ Groq AI Engine Error: {e}")
        return "Medium"