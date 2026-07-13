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

        client = Groq(api_key=api_key)
        
 
        system_instruction = "You are a backend classification module. You must respond with exactly ONE word from these choices: Low, Medium, High. Do not include any punctuation, spaces, or explanations."
        
        user_prompt = f"Task Title: {title}\nTask Description: {description}"
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0,
            max_tokens=5,
            timeout=2.5     
        )
        

        result = completion.choices[0].message.content.strip().replace(".", "").capitalize()
        
        print(f"🤖 AI RAW RESPONSE: '{result}'")  
        
        if result in ['Low', 'Medium', 'High']:
            return result
            
        print(f"⚠️ DEBUG: AI returned invalid option '{result}', defaulting to Medium.")
        return "Medium"  
        
    except Exception as e:
        print(f"❌ Groq AI Engine Error: {e}")
        return "Medium"