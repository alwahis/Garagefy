import aiohttp
import asyncio
import json
import logging
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from typing import List, Dict, Optional
import random
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EditusGarageScraper:
    def __init__(self):
        self.base_url = "https://www.editus.lu"
        self.search_url = f"{self.base_url}/fr/categories/garage-automobile"
        self.user_agent = UserAgent()
        self.session = None
        self.scraped_garages = []

    async def _get_headers(self) -> Dict[str, str]:
        """Get randomized headers to avoid detection"""
        return {
            "User-Agent": self.user_agent.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }

    async def _init_session(self):
        """Initialize aiohttp session with proxy support"""
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def _close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
            self.session = None

    async def _fetch_page(self, url: str, retries: int = 3) -> Optional[str]:
        """Fetch page content with retries and delay"""
        await self._init_session()
        
        for attempt in range(retries):
            try:
                # Random delay between requests
                await asyncio.sleep(random.uniform(2, 5))
                
                async with self.session.get(
                    url,
                    headers=await self._get_headers(),
                    timeout=30
                ) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        logger.error(f"Failed to fetch {url}, status: {response.status}")
                        
                    if response.status == 403:
                        # If blocked, wait longer
                        await asyncio.sleep(random.uniform(10, 20))
                        
            except Exception as e:
                logger.error(f"Error fetching {url}: {str(e)}")
                
            if attempt < retries - 1:
                await asyncio.sleep(random.uniform(5, 10))
                
        return None

    def _parse_garage_details(self, html: str) -> List[Dict]:
        """Parse garage details from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        garages = []
        
        # Find all garage listings
        listings = soup.find_all('div', class_='business-listing')
        
        for listing in listings:
            try:
                name = listing.find('h2', class_='business-name').text.strip()
                address = listing.find('div', class_='address').text.strip()
                phone = listing.find('div', class_='phone').text.strip()
                
                # Extract services
                services_div = listing.find('div', class_='services')
                services = [s.strip() for s in services_div.text.split(',')] if services_div else []
                
                # Extract coordinates
                map_div = listing.find('div', class_='map-container')
                latitude = float(map_div['data-lat']) if map_div and 'data-lat' in map_div.attrs else None
                longitude = float(map_div['data-lng']) if map_div and 'data-lng' in map_div.attrs else None
                
                # Extract URL
                url_tag = listing.find('a', class_='business-link')
                url = self.base_url + url_tag['href'] if url_tag else None
                
                garage = {
                    'name': name,
                    'address': address,
                    'phone': phone,
                    'services': services,
                    'latitude': latitude,
                    'longitude': longitude,
                    'url': url
                }
                
                garages.append(garage)
                
            except Exception as e:
                logger.error(f"Error parsing garage listing: {str(e)}")
                continue
                
        return garages

    async def scrape_garages(self, max_pages: int = 5) -> List[Dict]:
        """Scrape garage information from multiple pages"""
        try:
            for page in range(1, max_pages + 1):
                logger.info(f"Scraping page {page}")
                url = f"{self.search_url}?page={page}"
                
                html = await self._fetch_page(url)
                if not html:
                    break
                    
                page_garages = self._parse_garage_details(html)
                if not page_garages:
                    break
                    
                self.scraped_garages.extend(page_garages)
                
                # Save progress after each page
                self.save_to_json()
                
            return self.scraped_garages
            
        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}")
            return []
            
        finally:
            await self._close_session()

    def save_to_json(self, filename: str = "scraped_garages.json"):
        """Save scraped garages to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.scraped_garages, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(self.scraped_garages)} garages to {filename}")
        except Exception as e:
            logger.error(f"Error saving to JSON: {str(e)}")

    @staticmethod
    def load_from_json(filename: str = "scraped_garages.json") -> List[Dict]:
        """Load scraped garages from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading from JSON: {str(e)}")
            return []

async def main():
    scraper = EditusGarageScraper()
    garages = await scraper.scrape_garages()
    scraper.save_to_json()

if __name__ == "__main__":
    asyncio.run(main())
