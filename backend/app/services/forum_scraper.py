"""
Forum Scraper Service for Used Car Checks

This module provides web scraping functionality to collect reliable information
about used cars from trusted car forums and expert websites.
"""
import asyncio
import logging
import re
from typing import Dict, List, Optional, Any
import aiohttp
from bs4 import BeautifulSoup
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of trusted sources for vehicle information
TRUSTED_SOURCES = [
    {
        "name": "CarComplaints",
        "url": "https://www.carcomplaints.com/[MAKE]/[MODEL]/[YEAR]/",
        "patterns": {
            "reliability_score": r"Reliability Index:\s*(\d+)",
            "common_issues": r"<h3 class=\"problem-title\">(.*?)</h3>",
            "severity": r"<li class=\"severity\">(.*?)</li>"
        }
    },
    {
        "name": "CarTalk",
        "url": "https://community.cartalk.com/search?q=[MAKE]%20[MODEL]%20[YEAR]%20reliability",
        "patterns": {
            "comments": r"<div class=\"post\">(.*?)</div>",
            "positive": r"(reliable|solid|recommend|good|excellent|great)",
            "negative": r"(problem|issue|faulty|avoid|breakdown|repair)"
        }
    },
    {
        "name": "AutoScout24",
        "url": "https://www.autoscout24.com/cars/[MAKE]/[MODEL]/fy-[YEAR]",
        "patterns": {
            "price_range": r"€([\d,]+)\s*-\s*€([\d,]+)",
            "market_value": r"Average market value:\s*€([\d,]+)",
            "mileage_stats": r"Average mileage:\s*([\d,]+)\s*km"
        }
    },
    {
        "name": "TÜV Report",
        "url": "https://www.tuv.com/content/dam/tuv-com/global/products-and-services/mobility/tuev-report-[YEAR]-en.pdf",
        "patterns": {
            "defect_rate": r"[MAKE]\s*[MODEL].*?defect rate:\s*([\d.]+)%"
        }
    },
    {
        "name": "AutoExpert",
        "url": "https://www.autoexpert.com/reviews/[MAKE]-[MODEL]-[YEAR]",
        "patterns": {
            "recommendation": r"<div class=\"recommendation\">(.*?)</div>",
            "pros": r"<h3>Pros</h3>.*?<ul>(.*?)</ul>",
            "cons": r"<h3>Cons</h3>.*?<ul>(.*?)</ul>"
        }
    }
]

# Regional price adjustment factors (for Eastern European market)
REGION_PRICE_FACTORS = {
    "Poland": 0.85,
    "Czech Republic": 0.88,
    "Slovakia": 0.82,
    "Hungary": 0.80,
    "Romania": 0.75,
    "Bulgaria": 0.72
}

# Vehicle mileage assessment thresholds (in km)
MILEAGE_THRESHOLDS = {
    "very_low": 50000,
    "low": 100000,
    "average": 150000,
    "high": 200000,
    "very_high": 250000
}

# Fallback data if scraping fails
FALLBACK_DATA = {
    "reliability_scores": {
        "Toyota": 92,
        "Honda": 90,
        "Mazda": 88,
        "Lexus": 94,
        "Subaru": 85,
        "Hyundai": 82,
        "Kia": 81,
        "Volkswagen": 78,
        "BMW": 75,
        "Mercedes-Benz": 77,
        "Audi": 74,
        "Ford": 76,
        "Chevrolet": 73,
        "Nissan": 79,
        "Volvo": 80
    },
    "common_issues": {
        "Toyota": ["Excessive oil consumption", "Water pump failure"],
        "Honda": ["Transmission issues", "AC compressor failure"],
        "Volkswagen": ["Timing chain issues", "DSG transmission problems", "Electrical issues"],
        "BMW": ["Oil leaks", "Cooling system issues", "Electrical problems"],
        "Ford": ["PowerShift transmission problems", "Spark plug failure"],
        "Mercedes-Benz": ["Airmatic suspension issues", "Electronic issues"]
    }
}

class ForumScraper:
    """Scrapes car forums and expert websites for used car information."""
    
    def __init__(self):
        self.session = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def fetch_page(self, url: str) -> Optional[str]:
        """Fetch HTML content from a URL."""
        try:
            async with self.session.get(url, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
                logger.warning(f"Failed to fetch {url}: HTTP {response.status}")
                return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None
    
    async def scrape_source(self, source: Dict[str, Any], make: str, model: str, year: int) -> Dict[str, Any]:
        """Scrape data from a specific source."""
        url = source["url"]
        url = url.replace("[MAKE]", make.lower()).replace("[MODEL]", model.lower()).replace("[YEAR]", str(year))
        
        result = {"source": source["name"], "url": url, "data": {}}
        
        html = await self.fetch_page(url)
        if not html:
            return result
        
        # Extract data using the patterns
        for key, pattern in source.get("patterns", {}).items():
            matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
            if matches:
                result["data"][key] = matches
        
        return result
    
    async def scrape_all_sources(self, make: str, model: str, year: int) -> List[Dict[str, Any]]:
        """Scrape data from all trusted sources."""
        tasks = [self.scrape_source(source, make, model, year) for source in TRUSTED_SOURCES]
        return await asyncio.gather(*tasks)
    
    def generate_reliability_score(self, scrape_results: List[Dict[str, Any]], make: str) -> Dict[str, Any]:
        """Generate reliability score from scrape results."""
        # Extract reliability scores from scrape results
        reliability_scores = []
        
        for result in scrape_results:
            if "reliability_score" in result.get("data", {}):
                try:
                    score = int(result["data"]["reliability_score"][0])
                    reliability_scores.append(score)
                except (ValueError, IndexError):
                    continue
        
        # Use fallback data if no scores were found
        if not reliability_scores and make in FALLBACK_DATA["reliability_scores"]:
            final_score = FALLBACK_DATA["reliability_scores"][make]
            source = "fallback database"
        else:
            # Average the scores or use a fallback
            final_score = int(sum(reliability_scores) / len(reliability_scores)) if reliability_scores else 75
            source = "aggregated data"
        
        # Determine rating based on score
        if final_score >= 90:
            rating = "Excellent"
        elif final_score >= 80:
            rating = "Good"
        elif final_score >= 70:
            rating = "Average"
        elif final_score >= 50:
            rating = "Below Average"
        else:
            rating = "Poor"
        
        return {
            "score": final_score,
            "rating": rating,
            "source": source
        }
    
    def extract_common_issues(self, scrape_results: List[Dict[str, Any]], make: str) -> List[Dict[str, Any]]:
        """Extract common issues from scrape results."""
        common_issues = []
        
        # Extract issues from scrape results
        for result in scrape_results:
            if "common_issues" in result.get("data", {}):
                for issue in result["data"]["common_issues"]:
                    # Clean up the issue text
                    issue_text = re.sub(r'<.*?>', '', issue).strip()
                    if issue_text:
                        severity = "Medium"  # Default severity
                        
                        # Look for severity indicators
                        if "severity" in result.get("data", {}):
                            severity_text = result["data"]["severity"][0] if result["data"]["severity"] else ""
                            if "critical" in severity_text.lower() or "severe" in severity_text.lower():
                                severity = "High"
                            elif "minor" in severity_text.lower() or "low" in severity_text.lower():
                                severity = "Low"
                        
                        common_issues.append({
                            "issue": issue_text,
                            "severity": severity,
                            "source": result["source"]
                        })
        
        # Use fallback data if no issues were found
        if not common_issues and make in FALLBACK_DATA["common_issues"]:
            for issue in FALLBACK_DATA["common_issues"][make]:
                common_issues.append({
                    "issue": issue,
                    "severity": "Medium",
                    "source": "fallback database"
                })
        
        return common_issues
    
    def evaluate_mileage(self, mileage: int, year: int) -> Dict[str, Any]:
        """Evaluate if mileage is appropriate for the vehicle's age."""
        current_year = 2025  # Update this regularly or use a dynamic approach
        age_years = current_year - year
        expected_mileage = age_years * 15000  # Average 15,000 km per year
        
        mileage_difference = mileage - expected_mileage
        mileage_difference_percent = (mileage_difference / expected_mileage) * 100 if expected_mileage > 0 else 0
        
        if mileage <= MILEAGE_THRESHOLDS["very_low"]:
            assessment = "Very Low"
            concern_level = "None"
            description = "Exceptionally low mileage for the vehicle's age, which is very positive."
        elif mileage <= MILEAGE_THRESHOLDS["low"]:
            assessment = "Low"
            concern_level = "None"
            description = "Below average mileage for the vehicle's age, which is positive."
        elif mileage <= MILEAGE_THRESHOLDS["average"]:
            assessment = "Average"
            concern_level = "Low"
            description = "Normal mileage for the vehicle's age."
        elif mileage <= MILEAGE_THRESHOLDS["high"]:
            assessment = "High"
            concern_level = "Medium"
            description = "Above average mileage for the vehicle's age. May require additional maintenance."
        elif mileage <= MILEAGE_THRESHOLDS["very_high"]:
            assessment = "Very High"
            concern_level = "High"
            description = "Significantly above average mileage. Likely to require major maintenance soon."
        else:
            assessment = "Extreme"
            concern_level = "Very High"
            description = "Extremely high mileage. Major components may be at the end of their lifespan."
        
        return {
            "assessment": assessment,
            "expected_annual": 15000,
            "expected_total": expected_mileage,
            "difference_percent": round(mileage_difference_percent, 1),
            "concern_level": concern_level,
            "description": description
        }
    
    def estimate_market_value(self, make: str, model: str, year: int, mileage: int, 
                             scrape_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Estimate the market value of the vehicle."""
        base_value = None
        price_ranges = []
        
        # Extract price ranges from scrape results
        for result in scrape_results:
            if "price_range" in result.get("data", {}):
                try:
                    min_price = int(result["data"]["price_range"][0].replace(',', ''))
                    max_price = int(result["data"]["price_range"][1].replace(',', ''))
                    price_ranges.append((min_price, max_price))
                except (ValueError, IndexError):
                    continue
            
            if "market_value" in result.get("data", {}):
                try:
                    value = int(result["data"]["market_value"][0].replace(',', ''))
                    if base_value is None or abs(base_value - value) < 2000:
                        base_value = value
                except (ValueError, IndexError):
                    continue
        
        # Calculate average min and max prices if available
        if price_ranges:
            avg_min = sum(pr[0] for pr in price_ranges) / len(price_ranges)
            avg_max = sum(pr[1] for pr in price_ranges) / len(price_ranges)
            
            # Set base value as the average if not already determined
            if base_value is None:
                base_value = (avg_min + avg_max) / 2
        
        # Use a simple valuation model if no value was found
        if base_value is None:
            age = 2025 - year
            # Basic model based on depreciation curves
            if make.lower() in ["toyota", "honda", "lexus"]:
                # Slower depreciation for reliable brands
                base_value = 30000 * (0.85 ** age)
            else:
                # Faster depreciation for other brands
                base_value = 30000 * (0.8 ** age)
        
        # Adjust for mileage
        expected_mileage = (2025 - year) * 15000
        mileage_factor = 1.0
        
        if mileage > expected_mileage:
            # Reduce value for high mileage
            excess_mileage = mileage - expected_mileage
            mileage_factor = max(0.7, 1.0 - (excess_mileage / 100000) * 0.1)
        elif mileage < expected_mileage:
            # Increase value for low mileage
            saved_mileage = expected_mileage - mileage
            mileage_factor = min(1.3, 1.0 + (saved_mileage / 100000) * 0.1)
        
        adjusted_value = base_value * mileage_factor
        
        # Apply regional adjustment for Eastern European market
        # Using average factor for simplicity
        regional_factor = sum(REGION_PRICE_FACTORS.values()) / len(REGION_PRICE_FACTORS)
        eastern_europe_value = adjusted_value * regional_factor
        
        return {
            "base_value": round(base_value),
            "adjusted_for_mileage": round(adjusted_value),
            "eastern_europe_value": round(eastern_europe_value),
            "regional_factors": REGION_PRICE_FACTORS,
            "regional_average_factor": round(regional_factor, 2)
        }
    
    def generate_recommendation(self, reliability_score: Dict[str, Any], common_issues: List[Dict[str, Any]], 
                               mileage_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a final recommendation based on all data with detailed explanations."""
        # Score components (max 100 points)
        reliability_points = reliability_score["score"]  # 0-100
        
        # Calculate issue_points (more issues and higher severity = lower points)
        issue_points = 100
        severity_weights = {"Low": 5, "Medium": 10, "High": 20}
        
        for issue in common_issues:
            severity = issue.get("severity", "Medium")
            weight = severity_weights.get(severity, 10)
            issue_points = max(0, issue_points - weight)
        
        # Calculate mileage_points
        mileage_concern = mileage_assessment["concern_level"]
        mileage_points = {
            "None": 100,
            "Low": 85,
            "Medium": 70,
            "High": 50,
            "Very High": 25
        }.get(mileage_concern, 50)
        
        # Calculate overall score (weighted average)
        overall_score = (reliability_points * 0.5) + (issue_points * 0.3) + (mileage_points * 0.2)
        overall_score = round(overall_score)
        
        # Generate recommendation based on overall score with detailed explanations
        if overall_score >= 85:
            recommendation = "Buy"
            confidence = "High"
            summary = "This vehicle is a strong buy based on its reliability history, low number of reported issues, and appropriate mileage."
            pros = [
                f"High reliability score of {reliability_points}/100 from forum reports",
                "Few or no significant issues reported by owners",
                f"Appropriate mileage for a {mileage_assessment['vehicle_age']}-year-old vehicle"
            ]
            cons = []
            
            # Add any minor cons if they exist
            if common_issues:
                cons.append("Some minor issues reported, but nothing critical")
            if mileage_concern != "None":
                cons.append("Slightly higher than average mileage, but still acceptable")
                
        elif overall_score >= 70:
            recommendation = "Buy with Inspection"
            confidence = "Medium"
            summary = "This vehicle is a reasonable buy, but should be inspected by a mechanic to check for potential issues."
            pros = [
                f"Above average reliability score of {reliability_points}/100",
                "Generally positive owner feedback"
            ]
            cons = []
            
            # Add specific cons based on issues and mileage
            if common_issues:
                issue_text = f"{len(common_issues)} known issues reported in forums"
                cons.append(issue_text)
            if mileage_concern in ["Medium", "High"]:
                cons.append(f"Higher than average mileage ({mileage_assessment['annual_average']} km/year)")
                
        elif overall_score >= 50:
            recommendation = "Caution"
            confidence = "Medium"
            summary = "Proceed with caution. This vehicle has some concerning factors that should be thoroughly investigated before purchase."
            pros = []
            
            # Add any pros if they exist
            if reliability_points > 60:
                pros.append("Some positive reliability aspects reported")
            if mileage_concern in ["None", "Low"]:
                pros.append("Mileage is within acceptable range")
                
            cons = [
                f"Mediocre reliability score of {reliability_points}/100 based on forum data"
            ]
            
            # Add specific cons for issues
            if common_issues:
                severe_issues = [issue for issue in common_issues if issue.get("severity") == "High"]
                if severe_issues:
                    cons.append(f"{len(severe_issues)} severe issues reported by owners")
                else:
                    cons.append(f"{len(common_issues)} notable issues reported in forums")
                    
            if mileage_concern in ["High", "Very High"]:
                cons.append(f"Concerning mileage ({mileage_assessment['annual_average']} km/year)")
                
        else:
            recommendation = "Avoid"
            confidence = "High"
            summary = "We recommend avoiding this vehicle due to significant reliability concerns and/or very high mileage."
            pros = []
            
            # Add any minor pros if they exist
            if mileage_concern in ["None", "Low"]:
                pros.append("Mileage is within acceptable range")
                
            cons = [
                f"Low reliability score of {reliability_points}/100 from forum data"
            ]
            
            # Add detailed cons
            if common_issues:
                severe_issues = [issue for issue in common_issues if issue.get("severity") == "High"]
                if severe_issues:
                    cons.append(f"{len(severe_issues)} severe issues commonly reported by owners")
                    # Add specific severe issues
                    for issue in severe_issues[:2]:  # Limit to top 2 severe issues
                        cons.append(f"Critical issue: {issue['issue']}")
                else:
                    cons.append(f"Multiple issues ({len(common_issues)}) reported across forums")
                    
            if mileage_concern in ["High", "Very High"]:
                cons.append(f"Excessive mileage ({mileage_assessment['annual_average']} km/year) suggesting heavy use")
        
        # Generate specific recommendations with more detail
        details = []
        
        # Add reliability details
        if reliability_score["score"] < 70:
            details.append({
                "type": "inspection",
                "priority": "high",
                "description": "Complete mechanical inspection required",
                "impact": "Low reliability scores indicate potential hidden problems that only a professional can identify"
            })
        
        # Add issue-specific details
        for issue in common_issues:
            priority = "high" if issue["severity"] == "High" else "medium" if issue["severity"] == "Medium" else "low"
            source = issue.get("source", "forum reports")
            details.append({
                "type": "issue",
                "priority": priority,
                "description": f"Check for {issue['issue']}",
                "impact": f"This is a known issue with this model according to {source}"
            })
        
        # Add mileage-specific details
        if mileage_assessment["concern_level"] in ["High", "Very High"]:
            details.append({
                "type": "maintenance",
                "priority": "high",
                "description": "Verify complete service history",
                "impact": f"High mileage ({mileage_assessment['annual_average']} km/year) requires proof of proper maintenance"
            })
            
            # Add specific component checks for high mileage vehicles
            details.append({
                "type": "inspection",
                "priority": "high",
                "description": "Inspect timing belt/chain and water pump",
                "impact": "These are critical wear items that often fail on high-mileage vehicles"
            })
        
        # Add market value context if mileage is unusual
        if mileage_assessment["concern_level"] in ["High", "Very High", "Low", "None"]:
            details.append({
                "type": "market",
                "priority": "low",
                "description": "Verify price reflects mileage condition",
                "impact": f"{mileage_assessment['concern_level']} mileage should be reflected in the asking price"
            })
        
        return {
            "recommendation": recommendation,
            "confidence": confidence,
            "overall_score": overall_score,
            "summary": summary,
            "pros": pros,
            "cons": cons,
            "details": details,
            "points_to_check": [f"Check for {issue['issue']}" for issue in common_issues if issue["severity"] in ["Medium", "High"]],
            "components": {
                "reliability": reliability_points,
                "issues": issue_points,
                "mileage": mileage_points
            },
            "forum_insights": f"Based on data from multiple forums, this {mileage_assessment['vehicle_age']}-year-old vehicle with {mileage_assessment['annual_average']} km/year has a reliability score of {reliability_points}/100 and {len(common_issues)} reported issues."
        }

async def scrape_vehicle_data(make: str, model: str, year: int, mileage: int) -> Dict[str, Any]:
    """Main function to scrape and analyze vehicle data."""
    async with ForumScraper() as scraper:
        try:
            # Scrape data from all sources
            scrape_results = await scraper.scrape_all_sources(make, model, year)
            
            # Generate reliability score
            reliability_score = scraper.generate_reliability_score(scrape_results, make)
            
            # Extract common issues
            common_issues = scraper.extract_common_issues(scrape_results, make)
            
            # Evaluate mileage
            mileage_assessment = scraper.evaluate_mileage(mileage, year)
            
            # Estimate market value
            market_value = scraper.estimate_market_value(make, model, year, mileage, scrape_results)
            
            # Generate final recommendation
            recommendation = scraper.generate_recommendation(reliability_score, common_issues, mileage_assessment)
            
            return {
                "vehicle_info": {
                    "make": make,
                    "model": model,
                    "year": year,
                    "mileage": mileage
                },
                "analysis": {
                    "reliability_score": reliability_score,
                    "common_issues": common_issues,
                    "mileage_assessment": mileage_assessment
                },
                "market_data": market_value,
                "recommendation": recommendation,
                "sources": [result["source"] for result in scrape_results if result.get("data")]
            }
        except Exception as e:
            logger.error(f"Error scraping vehicle data: {str(e)}")
            
            # Return fallback data
            return {
                "vehicle_info": {
                    "make": make,
                    "model": model,
                    "year": year,
                    "mileage": mileage
                },
                "analysis": {
                    "reliability_score": {
                        "score": FALLBACK_DATA["reliability_scores"].get(make, 70),
                        "rating": "Average",
                        "source": "fallback database (unable to scrape live data)"
                    },
                    "common_issues": [
                        {"issue": issue, "severity": "Medium", "source": "fallback database"}
                        for issue in FALLBACK_DATA["common_issues"].get(make, ["General wear and tear"])
                    ],
                    "mileage_assessment": scraper.evaluate_mileage(mileage, year)
                },
                "market_data": {
                    "base_value": 15000,
                    "adjusted_for_mileage": 13000,
                    "eastern_europe_value": 11000,
                    "note": "Fallback values - actual prices may vary significantly"
                },
                "recommendation": {
                    "recommendation": "Buy with Inspection",
                    "confidence": "Low",
                    "overall_score": 65,
                    "summary": "We're using fallback data due to an error retrieving live information. Always have a used vehicle inspected by a mechanic before purchase.",
                    "points_to_check": ["Have a mechanical inspection done by a trusted mechanic"]
                },
                "sources": ["fallback database"],
                "error": str(e)
            }
