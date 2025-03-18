import requests
import re
import random
from typing import List, Dict, Any, Optional
import hashlib
import time

class UsedCarChecker:
    def __init__(self):
        self.cache = {}
        self.cache_expiry = 3600 * 24  # 24 hours

    def _generate_cache_key(self, brand: str, model: str, year: int) -> str:
        """Generate a cache key based on car details."""
        key = f"{brand.lower()}_{model.lower()}_{year}"
        return hashlib.md5(key.encode()).hexdigest()

    def _is_cached_result_valid(self, cache_key: str) -> bool:
        """Check if a cached result is still valid."""
        if cache_key not in self.cache:
            return False
        
        cached_time = self.cache[cache_key].get('timestamp', 0)
        current_time = time.time()
        
        return current_time - cached_time < self.cache_expiry

    async def check_used_car(
        self, 
        brand: str, 
        model: str, 
        year: int, 
        mileage: int, 
        price: Optional[int] = 0,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Check if a used car is a good buy based on online resources and forums.
        
        Args:
            brand: Car brand (e.g., Toyota, BMW)
            model: Car model (e.g., Corolla, 3 Series)
            year: Manufacturing year
            mileage: Mileage in kilometers
            price: Price in euros
            description: Additional description of the car
            
        Returns:
            A dictionary containing the recommendation and analysis
        """
        # Check cache first
        cache_key = self._generate_cache_key(brand, model, year)
        if self._is_cached_result_valid(cache_key):
            cached_result = self.cache[cache_key]
            # Update with current car details
            cached_result['car_info']['mileage'] = mileage
            
            # Adjust recommendation based on mileage
            self._adjust_recommendation_for_specific_car(cached_result, mileage)
            
            return cached_result
            
        # Simulate API call to online forums and resources
        # In a real implementation, this would make actual API calls to Reddit, car forums, etc.
        result = self._simulate_online_research(brand, model, year, mileage, description)
        
        # Cache the result
        result['timestamp'] = time.time()
        self.cache[cache_key] = result
        
        return result
    
    def _adjust_recommendation_for_specific_car(self, result: Dict[str, Any], mileage: int) -> None:
        """Adjust the recommendation based on specific car details like mileage and price."""
        car_info = result['car_info']
        brand = car_info['brand']
        model = car_info['model']
        year = car_info['year']
        
        # Calculate expected mileage based on age
        car_age = 2025 - year  # Using current year 2025
        expected_mileage = car_age * 15000  # Average 15,000 km per year
        
        # Adjust score based on mileage comparison
        if mileage > expected_mileage * 1.5:
            result['score'] = max(1, result['score'] - 2)  # High mileage, reduce score
            result['issues'].append({
                'title': 'High Mileage',
                'description': f'The mileage ({mileage:,} km) is significantly higher than expected ({expected_mileage:,} km) for a {year} model.',
                'severity': 'warning'
            })
        elif mileage < expected_mileage * 0.7:
            result['score'] = min(10, result['score'] + 1)  # Low mileage, increase score
            
        # Update recommendation based on adjusted score
        if result['score'] >= 8:
            result['recommendation'] = 'Highly Recommended'
        elif result['score'] >= 6:
            result['recommendation'] = 'Recommended'
        elif result['score'] >= 4:
            result['recommendation'] = 'Consider with Caution'
        else:
            result['recommendation'] = 'Not Recommended'
            
        # Update summary
        result['summary'] = self._generate_summary(result['score'], brand, model, year, mileage)
    
    def _generate_summary(self, score: int, brand: str, model: str, year: int, mileage: int) -> str:
        """Generate a summary based on the score and car details."""
        if score >= 8:
            return f"This {year} {brand} {model} appears to be an excellent choice. The reported reliability is high for the mileage and condition."
        elif score >= 6:
            return f"The {year} {brand} {model} is generally a good choice. It has decent reliability ratings, though you should check for specific issues mentioned below."
        elif score >= 4:
            return f"This {year} {brand} {model} has mixed reviews. While it may be acceptable, be sure to have it inspected and consider the issues mentioned below."
        else:
            return f"We cannot recommend this {year} {brand} {model} based on our research. There are significant reported issues, and you may want to look for alternatives."
    
    def _simulate_online_research(
        self, 
        brand: str, 
        model: str, 
        year: int, 
        mileage: int, 
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Simulate researching online forums and resources.
        
        In a real implementation, this would make actual API calls to Reddit, car forums, etc.
        """
        # For demo purposes, we'll create simulated research results
        # This would be replaced with actual web scraping or API calls
        
        # Base reliability scores for some common brands (out of 10)
        brand_reliability = {
            'toyota': 9,
            'lexus': 9,
            'honda': 8,
            'mazda': 8,
            'subaru': 7,
            'kia': 7,
            'hyundai': 7,
            'ford': 6,
            'chevrolet': 6,
            'nissan': 6,
            'volkswagen': 6,
            'audi': 5,
            'bmw': 5,
            'mercedes': 5,
            'fiat': 4,
            'chrysler': 4,
            'land rover': 4,
            'jaguar': 4,
        }
        
        # Default score if brand not in our list
        base_score = brand_reliability.get(brand.lower(), 6)
        
        # Adjust score based on car age
        car_age = 2025 - year  # Using current year 2025
        if car_age <= 3:
            age_adjustment = 1  # Newer cars get a bonus
        elif car_age <= 7:
            age_adjustment = 0  # Medium age is neutral
        elif car_age <= 12:
            age_adjustment = -1  # Older cars get a penalty
        else:
            age_adjustment = -2  # Very old cars get a bigger penalty
            
        # Final score calculation
        score = max(1, min(10, base_score + age_adjustment))
        
        # Generate a recommendation based on the score
        recommendation = "Not Recommended"
        if score >= 8:
            recommendation = "Highly Recommended"
        elif score >= 6:
            recommendation = "Recommended"
        elif score >= 4:
            recommendation = "Consider with Caution"
            
        # Generate common issues based on the brand and age
        issues = self._generate_common_issues(brand, model, year, car_age)
        
        # Generate fictional sources that would be replaced with real ones
        sources = self._generate_sources(brand, model, year)
        
        # Compile the result
        result = {
            'car_info': {
                'brand': brand,
                'model': model,
                'year': year,
                'mileage': mileage
            },
            'score': score,
            'recommendation': recommendation,
            'summary': self._generate_summary(score, brand, model, year, mileage),
            'issues': issues,
            'sources': sources
        }
        
        return result
    
    def _generate_common_issues(self, brand: str, model: str, year: int, car_age: int) -> List[Dict[str, str]]:
        """Generate common issues for the car based on brand and age."""
        issues = []
        
        # Common issues by brand (would be replaced with real data from forums)
        brand_issues = {
            'toyota': [
                {'title': 'Water Pump Failure', 'description': 'Some models may experience water pump issues after 100,000 km.', 'severity': 'info'},
                {'title': 'Dashboard Cracks', 'description': 'Exposure to sun may cause dashboard cracking in older models.', 'severity': 'info'}
            ],
            'volkswagen': [
                {'title': 'Timing Chain Tensioner', 'description': 'Known issue in many VW engines that can lead to catastrophic engine failure.', 'severity': 'error'},
                {'title': 'DSG Transmission Issues', 'description': 'Some models have reported problems with the DSG automatic transmission.', 'severity': 'warning'}
            ],
            'bmw': [
                {'title': 'High Maintenance Costs', 'description': 'Parts and service can be significantly more expensive than average.', 'severity': 'warning'},
                {'title': 'Oil Leaks', 'description': 'Various gaskets and seals may develop leaks as the vehicle ages.', 'severity': 'warning'},
                {'title': 'Electrical Issues', 'description': 'Complex electronics may develop faults, especially in older models.', 'severity': 'warning'}
            ],
            'ford': [
                {'title': 'Transmission Problems', 'description': 'Some models have reported premature transmission failure.', 'severity': 'warning'},
                {'title': 'Rust Issues', 'description': 'Older models may develop rust in certain areas of the body.', 'severity': 'info'}
            ],
            'honda': [
                {'title': 'Air Conditioning Issues', 'description': 'Some models may need A/C compressor replacement.', 'severity': 'info'},
                {'title': 'Automatic Transmission', 'description': 'Some years had problems with automatic transmissions.', 'severity': 'warning'}
            ]
        }
        
        # Add brand-specific issues
        brand_specific = brand_issues.get(brand.lower(), [])
        issues.extend(brand_specific)
        
        # Add age-related issues
        if car_age > 10:
            issues.append({
                'title': 'Age-Related Wear',
                'description': f'At {car_age} years old, expect general wear on suspension components, bushings, and engine mounts.',
                'severity': 'warning'
            })
            
        if car_age > 15:
            issues.append({
                'title': 'Electronic Components',
                'description': 'Older vehicles may have failing electronic components including sensors and control modules.',
                'severity': 'warning'
            })
            
        # If no issues found, add a generic positive note
        if not issues:
            issues.append({
                'title': 'Generally Reliable',
                'description': f'No widespread issues reported for the {year} {brand} {model}.',
                'severity': 'success'
            })
            
        return issues
    
    def _generate_sources(self, brand: str, model: str, year: int) -> List[Dict[str, str]]:
        """Generate fictional sources that would be replaced with real ones."""
        sources = [
            {
                'title': f'r/whatcarshouldIbuy - {year} {brand} {model} Reliability Thread',
                'url': 'https://www.reddit.com/r/whatcarshouldIbuy/'
            },
            {
                'title': f'CarComplaints.com: {year} {brand} {model} Problems',
                'url': 'https://www.carcomplaints.com/'
            },
            {
                'title': f'Consumer Reports: {brand} {model} ({year}) Review',
                'url': 'https://www.consumerreports.org/'
            },
            {
                'title': f'Edmunds.com: {year} {brand} {model} Consumer Reviews',
                'url': 'https://www.edmunds.com/'
            }
        ]
        return sources


# Create a singleton instance
used_car_checker = UsedCarChecker()
