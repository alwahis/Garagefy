from typing import Dict, List, Tuple
import os
from dotenv import load_dotenv
import requests
import json
from data import SERVICE_MANUALS
from repair_costs import estimate_repair_cost, format_cost_estimate

load_dotenv()

class CarDiagnosticSystem:
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
        
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        print("DeepSeek API initialized successfully!")

    def generate_response(self, prompt: str, max_length: int = 500) -> str:
        try:
            # Using DeepSeek chat API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Use a faster model with lower temperature and max tokens for quicker responses
            data = {
                "model": "deepseek-chat",  # Using the standard model for faster responses
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert automotive diagnostic system. Provide concise, accurate diagnoses."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.5,  # Lower temperature for more deterministic responses
                "max_tokens": max_length,
                "top_p": 0.9  # Slightly more focused sampling
            }
            
            # Set a shorter timeout for faster user experience
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            response_data = response.json()
            if not response_data.get('choices') or not response_data['choices'][0].get('message', {}).get('content'):
                raise Exception("Empty response from DeepSeek API")
            
            return response_data['choices'][0]['message']['content'].strip()
            
        except Exception as e:
            print(f"Error in generate_response: {str(e)}")
            # Provide a fallback response if the API call fails
            if "timeout" in str(e).lower():
                return "The diagnostic system is experiencing high demand. Please try again in a moment. In the meantime, check if the issue is related to common problems like battery, fuel system, or electrical connections."
            raise Exception(f"Failed to generate response: {str(e)}")

    def get_repair_category(self, symptoms: str, car_brand: str) -> str:
        """Determine the repair category based on symptoms."""
        symptoms_lower = symptoms.lower()
        categories = SERVICE_MANUALS.get(car_brand, {}).get("repair_categories", {})
        
        for category, info in categories.items():
            for symptom in info["symptoms"]:
                if symptom.lower() in symptoms_lower:
                    return category
        return "general"

    def get_severity(self, symptoms: str, car_brand: str, category: str) -> str:
        """Determine the severity of the issue based on symptoms."""
        symptoms_lower = symptoms.lower()
        severity_info = SERVICE_MANUALS.get(car_brand, {}).get("repair_categories", {}).get(category, {}).get("severity", {})
        
        for severity, symptoms_list in severity_info.items():
            for symptom in symptoms_list:
                if symptom.lower() in symptoms_lower:
                    return severity
        return "unknown"

    def format_prompt(self, symptoms: str, car_brand: str, car_model: str, year: int) -> str:
        # Get the service manual reference
        manual_ref = SERVICE_MANUALS.get(car_brand, {}).get("manual_refs", {}).get(car_model, "")
        if manual_ref:
            manual_ref = manual_ref.format(year=year)
        
        # Get repair category and severity
        category = self.get_repair_category(symptoms, car_brand)
        severity = self.get_severity(symptoms, car_brand, category)
        
        # Get relevant symptoms and repair info
        repair_info = SERVICE_MANUALS.get(car_brand, {}).get("repair_categories", {}).get(category, {})
        common_symptoms = repair_info.get("symptoms", [])
        severity_symptoms = repair_info.get("severity", {}).get(severity, [])
        
        return f"""You are an expert automotive diagnostic system. A customer has reported an issue with their {year} {car_brand} {car_model}.

CUSTOMER COMPLAINT:
{symptoms}

VEHICLE INFORMATION:
- Make: {car_brand}
- Model: {car_model}
- Year: {year}
- Service Manual: {manual_ref}

DIAGNOSTIC CONTEXT:
- Common issues in this category: {', '.join(common_symptoms)}
- Known severity indicators: {', '.join(severity_symptoms)}

Based on your expertise and the service manual, provide a diagnostic report in the following format. DO NOT use the example text - generate a NEW, SPECIFIC diagnosis for this exact issue.

Required sections:
1. DIAGNOSIS: Explain the most likely cause of the problem and potential consequences
2. SEVERITY: Rate as High/Medium/Low and explain why
3. REPAIR STEPS: List 2-3 specific steps to address the issue
4. MANUAL REFERENCE: Cite the relevant section from {manual_ref}

Example format (DO NOT USE THIS CONTENT - GENERATE NEW CONTENT FOR THE ACTUAL ISSUE):
---
DIAGNOSIS: The transmission fluid leak from the front seal indicates deterioration of the main transmission seal. This can lead to low fluid levels and potential transmission damage.

SEVERITY: Medium - While not immediately dangerous, continued driving will worsen the leak and could lead to transmission failure.

REPAIR STEPS:
1. Schedule service appointment within next 7 days
2. Check transmission fluid level daily until repair
3. Avoid long trips or heavy traffic until repaired

MANUAL REFERENCE: Section 7-2.1 Transmission, Subsection: Main Seal Replacement
---

Now, provide your diagnosis for the current issue. Remember to be specific to this vehicle and symptom:"""

    def diagnose_issue(self, symptoms: str, car_brand: str, car_model: str, year: int, audio_path: str = None) -> Dict:
        try:
            # Add note about audio file if provided
            audio_note = ""
            if audio_path:
                audio_note = "\n\nNote: The user has also provided an audio recording describing the symptoms."
            
            prompt = self.format_prompt(symptoms, car_brand, car_model, year) + audio_note
            response = self.generate_response(prompt)
            
            # Parse the response into sections
            sections = {}
            current_section = None
            current_text = []
            
            for line in response.split('\n'):
                line = line.strip()
                if not line or line.startswith('---'):
                    continue
                    
                if line.startswith('DIAGNOSIS:'):
                    current_section = 'diagnosis'
                    current_text = [line.replace('DIAGNOSIS:', '').strip()]
                elif line.startswith('SEVERITY:'):
                    if current_section:
                        sections[current_section] = '\n'.join(current_text).strip()
                    current_section = 'severity'
                    current_text = [line.replace('SEVERITY:', '').strip()]
                elif line.startswith('REPAIR STEPS:'):
                    if current_section:
                        sections[current_section] = '\n'.join(current_text).strip()
                    current_section = 'steps'
                    current_text = []
                elif line.startswith('MANUAL REFERENCE:'):
                    if current_section:
                        sections[current_section] = '\n'.join(current_text).strip()
                    current_section = 'manual_ref'
                    current_text = [line.replace('MANUAL REFERENCE:', '').strip()]
                elif line and current_section:
                    # For repair steps, clean up numbering
                    if current_section == 'steps' and (line[0].isdigit() or line[0] in ['•', '-']):
                        line = line.lstrip('0123456789.- ').strip()
                    current_text.append(line)
            
            if current_section:
                sections[current_section] = '\n'.join(current_text).strip()
            
            # Extract severity level from severity text
            severity_text = sections.get('severity', '').lower()
            if 'high' in severity_text:
                severity = 'high'
            elif 'medium' in severity_text:
                severity = 'medium'
            elif 'low' in severity_text:
                severity = 'low'
            else:
                severity = 'unknown'
            
            # Get repair category
            category = self.get_repair_category(symptoms, car_brand)
            
            # Estimate repair costs
            try:
                year_int = int(year) if isinstance(year, str) else year
                cost_estimate = estimate_repair_cost(category, severity, car_brand, year_int)
                cost_estimate_text = format_cost_estimate(cost_estimate)
            except Exception as e:
                print(f"Error estimating repair costs: {str(e)}")
                cost_estimate = {}
                cost_estimate_text = "Cost estimation unavailable"
            
            result = {
                "diagnosis": sections.get('diagnosis', 'No diagnosis available'),
                "severity": severity,
                "severity_details": sections.get('severity', ''),
                "recommendations": [step.strip() for step in sections.get('steps', '').split('\n') if step.strip()],
                "manual_ref": sections.get('manual_ref', ''),
                "category": category,
                "cost_estimate": cost_estimate,
                "cost_estimate_text": cost_estimate_text
            }
            
            # Add audio path info if provided
            if audio_path:
                result["audio_path"] = audio_path
                
            return result
        except Exception as e:
            print(f"Error in diagnose_issue: {str(e)}")
            raise Exception(f"Error during diagnosis: {str(e)}")

    def validate_car_info(self, car_brand: str, car_model: str, year: int) -> Tuple[bool, str]:
        """Validate car information against our database."""
        if car_brand not in SERVICE_MANUALS:
            return False, f"Unsupported car brand: {car_brand}"
        
        if car_model not in SERVICE_MANUALS[car_brand]["manual_refs"]:
            return False, f"Unsupported model for {car_brand}: {car_model}"
        
        return True, "Valid"

    def diagnose(self, symptoms: str, car_brand: str, car_model: str, year: str) -> str:
        try:
            prompt = f"""Please analyze this car issue:

            Vehicle Information:
            - Make: {car_brand}
            - Model: {car_model}
            - Year: {year}

            Reported Symptoms:
            {symptoms}

            Please provide a detailed analysis including:
            1. Most likely diagnosis based on the symptoms
            2. Recommended repair steps
            3. Estimated repair cost range
            4. Safety implications if not addressed
            5. Relevant service manual references if available

            Format your response in a clear, structured way."""

            return self.generate_response(prompt)
        except Exception as e:
            raise Exception(f"Diagnosis failed: {str(e)}")
