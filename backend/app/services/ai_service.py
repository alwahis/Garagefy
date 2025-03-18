import os
from typing import Dict, List, Optional
import httpx
from dotenv import load_dotenv
import json
import logging
import asyncio
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class CarDiagnosticAI:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            logger.warning("DeepSeek API key not found")
        self.api_url = "https://api.deepseek.com/v1/chat/completions"  # Updated URL
        self.manual_data = self._load_manual_data()
        self.available_brands = list(self.manual_data.keys())
        logger.info(f"Available car brands with manuals: {', '.join(self.available_brands)}")

    def _load_manual_data(self) -> Dict[str, Dict]:
        """Load manual data from JSON files."""
        manual_data = {}
        manuals_dir = os.path.join(os.path.dirname(__file__), "..", "data", "manuals")
        
        try:
            if not os.path.exists(manuals_dir):
                logger.warning(f"Manuals directory not found: {manuals_dir}")
                return {}
                
            for filename in os.listdir(manuals_dir):
                if filename.endswith('.json'):
                    brand = filename.split('.json')[0]
                    # Handle special case for toyota_manual.json
                    if brand == "toyota_manual":
                        brand = "toyota"
                    
                    filepath = os.path.join(manuals_dir, filename)
                    try:
                        with open(filepath, 'r') as f:
                            data = json.load(f)
                            # Only add if it's a properly formatted manual
                            if "brand" in data or "systems" in data:
                                manual_data[brand.lower()] = data
                                logger.info(f"Loaded manual for {brand}")
                            else:
                                logger.warning(f"Skipping {filename}: missing required fields")
                    except json.JSONDecodeError:
                        logger.error(f"Error parsing JSON in {filename}")
                    except Exception as e:
                        logger.error(f"Error loading {filename}: {str(e)}")
            
            return manual_data
        except Exception as e:
            logger.error(f"Error loading manual data: {str(e)}")
            return {}

    def _get_relevant_manual_info(self, car_brand: str, problem_description: str) -> Dict:
        """Get relevant information from service manuals."""
        car_brand = car_brand.lower()
        result = {
            "technical_info": [],
            "references": []
        }
        
        # Check if we have manual data for this brand
        if car_brand not in self.manual_data:
            logger.warning(f"No manual data available for {car_brand}. Available brands: {', '.join(self.available_brands)}")
            # Try to find the closest matching brand
            for brand in self.available_brands:
                if brand in car_brand or car_brand in brand:
                    logger.info(f"Using {brand} manual as a close match for {car_brand}")
                    car_brand = brand
                    break
            else:
                return result
            
        brand_data = self.manual_data[car_brand]
        
        # Extract references from the manual
        if "references" in brand_data:
            result["references"] = brand_data["references"]
        
        # Process systems data if available in the expected format
        if "systems" in brand_data:
            for system in brand_data["systems"]:
                system_name = system.get("system", "")
                
                # Check subsystems
                if "subsystems" in system:
                    for subsystem in system["subsystems"]:
                        subsystem_name = subsystem.get("name", "")
                        subsystem_data = subsystem.get("data", {})
                        
                        # Check if this subsystem is relevant to the problem description
                        relevance_score = self._calculate_relevance(subsystem_data, problem_description)
                        
                        if relevance_score > 0.3:  # Threshold for relevance
                            result["technical_info"].append({
                                "system": f"{system_name} - {subsystem_name}",
                                "data": subsystem_data,
                                "relevance_score": relevance_score  # Add the score for sorting
                            })
                            
                            # Add specific references from causes if available
                            if "causes" in subsystem_data:
                                for cause in subsystem_data["causes"]:
                                    if "reference" in cause and cause["reference"] not in result["references"]:
                                        result["references"].append(cause["reference"])
                            
                            # Add specific references from diagnostic steps if available
                            if "diagnostic_steps" in subsystem_data:
                                for step in subsystem_data["diagnostic_steps"]:
                                    if "reference" in step and step["reference"] not in result["references"]:
                                        result["references"].append(step["reference"])
            
            # Sort technical info by relevance score (highest first)
            result["technical_info"] = sorted(
                result["technical_info"], 
                key=lambda x: x.get("relevance_score", 0), 
                reverse=True
            )
            
            # Limit to top 3 most relevant systems to avoid overwhelming the prompt
            if len(result["technical_info"]) > 3:
                result["technical_info"] = result["technical_info"][:3]
                logger.info(f"Limited to top 3 most relevant systems for {car_brand}")
        
        return result
        
    def _calculate_relevance(self, subsystem_data: Dict, problem_description: str) -> float:
        """Calculate relevance score between subsystem data and problem description."""
        problem_lower = problem_description.lower()
        relevance_score = 0.0
        
        # Extract important keywords from the problem description
        keywords = set(re.findall(r'\b\w{4,}\b', problem_lower))
        
        # Check symptoms
        if "symptoms" in subsystem_data:
            for symptom in subsystem_data["symptoms"]:
                symptom_lower = symptom.lower()
                if symptom_lower in problem_lower:
                    relevance_score += 0.5
                    logger.debug(f"Exact symptom match: {symptom_lower}")
                else:
                    # Check for keyword matches
                    symptom_words = set(re.findall(r'\b\w{4,}\b', symptom_lower))
                    matches = keywords.intersection(symptom_words)
                    if matches:
                        relevance_score += 0.2 * len(matches) / len(symptom_words)
                        logger.debug(f"Keyword matches in symptom: {matches}")
        
        # Check causes
        if "causes" in subsystem_data:
            for cause in subsystem_data["causes"]:
                issue_lower = cause.get("issue", "").lower()
                if issue_lower in problem_lower:
                    relevance_score += 0.4
                    logger.debug(f"Exact cause match: {issue_lower}")
                else:
                    # Check for keyword matches
                    issue_words = set(re.findall(r'\b\w{4,}\b', issue_lower))
                    matches = keywords.intersection(issue_words)
                    if matches:
                        relevance_score += 0.15 * len(matches) / len(issue_words)
                        logger.debug(f"Keyword matches in cause: {matches}")
        
        # Check diagnostic steps for additional context
        if "diagnostic_steps" in subsystem_data:
            for step in subsystem_data["diagnostic_steps"]:
                action_lower = step.get("action", "").lower()
                action_words = set(re.findall(r'\b\w{4,}\b', action_lower))
                matches = keywords.intersection(action_words)
                if matches:
                    relevance_score += 0.1 * len(matches) / len(action_words)
                    logger.debug(f"Keyword matches in diagnostic step: {matches}")
        
        logger.debug(f"Relevance score: {relevance_score} for subsystem with keywords: {keywords}")
        return relevance_score

    def _construct_diagnostic_prompt(self, car_brand: str, problem_description: str, manual_info: Dict) -> str:
        """Construct a prompt for the AI model with technical documentation."""
        prompt = f"""As an expert automotive diagnostic AI assistant, analyze this car problem and provide a clear, actionable diagnosis:

Vehicle Information:
- Brand: {car_brand}
- Problem: {problem_description}

Based on the vehicle's service manual and technical documentation, provide:

1. SEVERITY ASSESSMENT
   - Assess if this is a HIGH, MEDIUM, or LOW severity issue
   - Explain why this severity level was chosen
   - Indicate if immediate action is required

2. PROBLEM ANALYSIS
   - Explain the likely root causes
   - List common symptoms associated with these causes
   - Note any potential complications if left unaddressed

3. DIAGNOSTIC STEPS
   - List specific steps to diagnose the issue
   - Include required tools and their specifications
   - Note any safety precautions

4. REPAIR RECOMMENDATIONS
   - Provide estimated repair costs
   - List parts that may need replacement
   - Indicate if professional service is required

5. SAFETY IMPLICATIONS
   - State any immediate safety concerns
   - Note if the vehicle is safe to drive
   - List any temporary precautions to take

6. TECHNICAL REFERENCES
   - Include specific references to service manual sections
   - Mention relevant Technical Service Bulletins (TSBs)
   - Cite manufacturer-specific diagnostic procedures

Format the response in clear sections with bullet points for easy reading. Include specific technical specifications and reference relevant service manual sections when available.

Technical Documentation from Service Manual:
"""

        # Add relevant technical information
        if manual_info.get("technical_info"):
            for info in manual_info["technical_info"]:
                system = info["system"]
                issue_data = info["data"]
                
                prompt += f"\n\nSystem: {system.upper()}\n"
                
                if "symptoms" in issue_data:
                    prompt += "\nDocumented Symptoms:\n"
                    for symptom in issue_data["symptoms"]:
                        prompt += f"- {symptom}\n"
                
                if "causes" in issue_data:
                    prompt += "\nKnown Causes:\n"
                    for cause in issue_data["causes"]:
                        prompt += f"- Issue: {cause['issue']}\n"
                        prompt += f"  Severity: {cause.get('severity', 'Unknown')}\n"
                        prompt += f"  Urgency: {cause.get('urgency', 'Unknown')}\n"
                        if "cost_range" in cause:
                            prompt += f"  Cost Range: ${cause['cost_range'].get('min', 0)}-${cause['cost_range'].get('max', 0)}\n"
                        if "reference" in cause:
                            prompt += f"  Reference: {cause['reference']}\n"
                
                if "diagnostic_steps" in issue_data:
                    prompt += "\nService Manual Diagnostic Steps:\n"
                    for step in issue_data["diagnostic_steps"]:
                        prompt += f"- {step['action']}\n"
                        if "tools_needed" in step:
                            prompt += f"  Tools needed: {', '.join(step['tools_needed'])}\n"
                        if "specifications" in step:
                            for key, value in step["specifications"].items():
                                prompt += f"  {key}: {value}\n"
                        if "reference" in step:
                            prompt += f"  Reference: {step['reference']}\n"

        # Add service manual references
        if manual_info.get("references"):
            prompt += "\nService Manual References:\n"
            for ref in manual_info["references"][:5]:  # Limit to 5 references
                prompt += f"- {ref}\n"

        return prompt

    async def get_diagnosis(self, car_brand: str, problem_description: str) -> str:
        """Get AI-powered diagnosis for car problems."""
        try:
            # Get relevant information from service manuals
            manual_info = self._get_relevant_manual_info(car_brand, problem_description)
            
            # Construct the prompt
            prompt = self._construct_diagnostic_prompt(car_brand, problem_description, manual_info)
            
            # Call DeepSeek API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "deepseek-chat",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7,
                        "max_tokens": 1000
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    diagnosis = result['choices'][0]['message']['content']
                    return diagnosis
                else:
                    logger.error(f"API error: {response.status_code} - {response.text}")
                    return "I apologize, but I encountered an error while analyzing your car's symptoms. Please try again or provide more detailed information about the problem."
                    
        except Exception as e:
            logger.error(f"Error getting diagnosis: {str(e)}")
            return "I apologize, but I encountered an error while analyzing your car's symptoms. Please try again or provide more detailed information about the problem."

    def _determine_severity(self, diagnosis: str, manual_info: Dict) -> str:
        """Determine severity level based on diagnosis content and manual data."""
        diagnosis_lower = diagnosis.lower()
        
        # Check for critical keywords
        critical_keywords = ['immediate', 'urgent', 'critical', 'dangerous', 'unsafe', 'severe']
        if any(keyword in diagnosis_lower for keyword in critical_keywords):
            return 'HIGH'
            
        # Check manual data
        if manual_info.get("technical_info"):
            for info in manual_info["technical_info"]:
                if "causes" in info["data"]:
                    for cause in info["data"]["causes"]:
                        severity = cause.get('severity', '').lower()
                        if severity == 'high':
                            return 'HIGH'
                        elif severity == 'medium':
                            return 'MEDIUM'
        
        # Default to MEDIUM if no clear indicators
        return 'MEDIUM'

    def _get_manual_based_diagnosis(self, car_brand: str, problem_description: str, manual_info: Dict) -> Dict:
        """Generate a diagnosis based on manual data and common automotive knowledge."""
        
        # Common diesel power loss issues for Mercedes
        common_diesel_issues = {
            "fuel_system": {
                "symptoms": ["power loss", "poor acceleration", "especially noticeable uphill"],
                "causes": [
                    {
                        "issue": "Clogged fuel filter",
                        "severity": "MEDIUM",
                        "urgency": "Should be addressed within 1-2 weeks",
                        "cost_range": {"min": 100, "max": 300}
                    },
                    {
                        "issue": "Faulty fuel pump",
                        "severity": "HIGH",
                        "urgency": "Requires immediate attention",
                        "cost_range": {"min": 800, "max": 1500}
                    },
                    {
                        "issue": "Blocked diesel particulate filter (DPF)",
                        "severity": "HIGH",
                        "urgency": "Requires immediate attention",
                        "cost_range": {"min": 600, "max": 2000}
                    }
                ],
                "diagnostic_steps": [
                    {
                        "action": "Check fuel pressure",
                        "tools_needed": ["Fuel pressure gauge"],
                        "specifications": {"Pressure": "2.5-3.0 bar at idle"}
                    },
                    {
                        "action": "Inspect fuel filter condition",
                        "tools_needed": ["Visual inspection"],
                        "specifications": {"Replace at": "Every 30,000 miles or if clogged"}
                    },
                    {
                        "action": "Check DPF status with diagnostic tool",
                        "tools_needed": ["OBD scanner"],
                        "specifications": {"Back pressure": "Less than 120 mbar at idle"}
                    }
                ]
            }
        }

        # If we don't have manual info, use common knowledge
        if not manual_info.get("technical_info"):
            manual_info["technical_info"] = [{
                "system": "Fuel System",
                "data": common_diesel_issues["fuel_system"]
            }]

        # Generate diagnosis
        diagnosis = "SEVERITY ASSESSMENT:\n"
        severity = "HIGH" if "uphill" in problem_description.lower() and "no power" in problem_description.lower() else "MEDIUM"
        diagnosis += f"- Level: {severity}\n"
        diagnosis += "- Immediate attention required due to safety concerns when driving uphill\n\n"

        diagnosis += "PROBLEM ANALYSIS:\n"
        diagnosis += "Based on your symptoms of power loss while going uphill in a Mercedes-Benz C-Class diesel:\n\n"

        diagnosis += "Likely causes (in order of probability):\n"
        for system_info in manual_info["technical_info"]:
            if "causes" in system_info["data"]:
                for cause in system_info["data"]["causes"]:
                    diagnosis += f"1. {cause['issue']}\n"
                    diagnosis += f"   - Severity: {cause['severity']}\n"
                    diagnosis += f"   - Urgency: {cause['urgency']}\n"
                    if "cost_range" in cause:
                        diagnosis += f"   - Estimated Cost: ${cause['cost_range']['min']}-${cause['cost_range']['max']}\n"
                    diagnosis += "\n"

        diagnosis += "\nDIAGNOSTIC STEPS:\n"
        for system_info in manual_info["technical_info"]:
            if "diagnostic_steps" in system_info["data"]:
                for step in system_info["data"]["diagnostic_steps"]:
                    diagnosis += f"1. {step['action']}\n"
                    if "tools_needed" in step:
                        diagnosis += f"   - Required tools: {', '.join(step['tools_needed'])}\n"
                    if "specifications" in step:
                        for key, value in step["specifications"].items():
                            diagnosis += f"   - {key}: {value}\n"
                    diagnosis += "\n"

        diagnosis += "\nSAFETY IMPLICATIONS:\n"
        diagnosis += "- Reduced power while driving uphill is a significant safety concern\n"
        diagnosis += "- The vehicle may be unsafe to drive in mountainous areas\n"
        diagnosis += "- If you must drive, avoid steep inclines until repaired\n"
        diagnosis += "- Consider having the vehicle towed to a repair facility\n"

        return {
            "diagnosis": {
                "analysis": diagnosis,
                "references": manual_info.get("references", [
                    "Mercedes-Benz C-Class W204 Service Manual - Fuel System",
                    "Mercedes-Benz Diesel Engine Diagnostic Guide"
                ])
            }
        }

# Initialize the AI service
car_diagnostic_ai = CarDiagnosticAI()
