import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def call_deepseek_api(prompt):
    """Call DeepSeek API for car diagnosis"""
    # This is a mock implementation
    # In a real app, this would make an API call to DeepSeek
    
    # Mock response based on common car issues
    response = (
        "Based on the symptoms described, here are the potential issues:\n\n"
        "1. The symptoms suggest a possible issue with the engine's sensors or electrical system.\n"
        "2. Recommend performing a diagnostic scan to identify specific error codes.\n"
        "3. Check all electrical connections and wiring for signs of wear or damage.\n"
        "4. Consider having a professional mechanic perform a thorough inspection.\n\n"
        "Important: This is an AI-generated diagnosis and should be verified by a qualified mechanic."
    )
    
    return response
