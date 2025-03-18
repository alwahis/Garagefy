from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import random

def setup_driver():
    """Set up Chrome driver with additional options"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    
    # Add random user agent
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def extract_garage_info(element):
    """Extract information from a garage element"""
    try:
        # Initialize dictionary with empty values
        garage_info = {
            'name': '',
            'address': '',
            'phone': '',
            'email': '',
            'website': '',
            'opening_hours': '',
            'services': '',
            'rating': '',
            'reviews_count': ''
        }
        
        # Extract information using try-except for each field
        try:
            garage_info['name'] = element.find_element(By.CSS_SELECTOR, 'h2.title, .company-name').text.strip()
        except NoSuchElementException:
            try:
                garage_info['name'] = element.find_element(By.CSS_SELECTOR, '.business-name').text.strip()
            except NoSuchElementException:
                pass
            
        try:
            garage_info['address'] = element.find_element(By.CSS_SELECTOR, '.address, .location').text.strip()
        except NoSuchElementException:
            pass
            
        try:
            garage_info['phone'] = element.find_element(By.CSS_SELECTOR, '.phone, .telephone').text.strip()
        except NoSuchElementException:
            try:
                phone_elem = element.find_element(By.CSS_SELECTOR, 'a[href^="tel:"]')
                garage_info['phone'] = phone_elem.get_attribute('href').replace('tel:', '')
            except NoSuchElementException:
                pass
            
        try:
            garage_info['email'] = element.find_element(By.CSS_SELECTOR, '.email, a[href^="mailto:"]').text.strip()
        except NoSuchElementException:
            try:
                email_elem = element.find_element(By.CSS_SELECTOR, 'a[href^="mailto:"]')
                garage_info['email'] = email_elem.get_attribute('href').replace('mailto:', '')
            except NoSuchElementException:
                pass
            
        try:
            website_elem = element.find_element(By.CSS_SELECTOR, '.website a, a[href^="http"]')
            garage_info['website'] = website_elem.get_attribute('href')
        except NoSuchElementException:
            pass
            
        try:
            garage_info['opening_hours'] = element.find_element(By.CSS_SELECTOR, '.opening-hours, .hours').text.strip()
        except NoSuchElementException:
            pass
            
        try:
            garage_info['services'] = element.find_element(By.CSS_SELECTOR, '.services, .business-categories').text.strip()
        except NoSuchElementException:
            pass
            
        try:
            garage_info['rating'] = element.find_element(By.CSS_SELECTOR, '.rating, .stars').text.strip()
        except NoSuchElementException:
            pass
            
        try:
            garage_info['reviews_count'] = element.find_element(By.CSS_SELECTOR, '.reviews-count, .review-count').text.strip()
        except NoSuchElementException:
            pass
        
        return garage_info
    except Exception as e:
        print(f"Error extracting garage info: {e}")
        return None

def scrape_garages(url):
    """Scrape garage information from the website"""
    driver = setup_driver()
    garages_data = []
    
    try:
        print(f"Accessing URL: {url}")
        driver.get(url)
        
        # Add a random delay to simulate human behavior
        time.sleep(random.uniform(2, 4))
        
        # Wait for the page to load
        wait = WebDriverWait(driver, 20)  # Increased timeout
        print("Waiting for results to load...")
        
        # Try different selectors for garage elements
        selectors = [
            '.result-item',
            '.business-listing',
            '.company-card',
            'article',
            '.search-result-item'
        ]
        
        garage_elements = []
        for selector in selectors:
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                garage_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if garage_elements:
                    print(f"Found elements using selector: {selector}")
                    break
            except TimeoutException:
                continue
        
        if not garage_elements:
            print("No garage elements found with any selector")
            # Save page source for debugging
            with open('page_source.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print("Saved page source to page_source.html for debugging")
            return []
        
        print(f"Found {len(garage_elements)} garage elements")
        
        # Extract information from each garage
        for element in garage_elements:
            # Scroll element into view
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(random.uniform(0.5, 1))  # Random delay between extractions
            
            garage_info = extract_garage_info(element)
            if garage_info:
                garages_data.append(garage_info)
                print(f"Extracted info for garage: {garage_info['name']}")
        
        return garages_data
    except TimeoutException:
        print("Timeout waiting for page to load")
        # Save page source for debugging
        with open('page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("Saved page source to page_source.html for debugging")
        return []
    except Exception as e:
        print(f"Error during scraping: {e}")
        return []
    finally:
        driver.quit()

def save_to_csv(data, filename='luxembourg_garages.csv'):
    """Save the scraped data to a CSV file"""
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Successfully saved {len(data)} garage entries to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def save_to_json(data, filename='luxembourg_garages.json'):
    """Save the scraped data to a JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully saved {len(data)} garage entries to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

def main():
    url = 'https://www.editus.lu/en/results/vehicle-maintenance/garage-1101r'
    print("Starting garage data scraping...")
    
    garages_data = scrape_garages(url)
    
    if garages_data:
        print(f"\nSuccessfully scraped {len(garages_data)} garages")
        # Save in both CSV and JSON formats
        save_to_csv(garages_data)
        save_to_json(garages_data)
        
        # Print first garage as example
        print("\nExample of scraped data (first garage):")
        print(json.dumps(garages_data[0], indent=2))
    else:
        print("No garage data was scraped")

if __name__ == "__main__":
    main()
