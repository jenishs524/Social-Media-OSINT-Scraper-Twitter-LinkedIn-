#!/usr/bin/env python3
"""
Project 24 – Social Media OSINT Scraper (Fixed)
Scrapes public Twitter/LinkedIn profiles using Selenium.
"""

import sys
import time
import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

# ---------- CONFIG ----------
PLATFORM = sys.argv[1] if len(sys.argv) > 1 else "twitter"
TARGET = sys.argv[2] if len(sys.argv) > 2 else "testuser"
OUTPUT_CSV = "scraped_data.csv"

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,720")
    # Prevent detection
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def scrape_twitter(username):
    url = f"https://twitter.com/{username}"
    driver = init_driver()
    try:
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Try multiple selectors
        name = "N/A"
        bio = "N/A"
        followers = "N/A"
        
        # Try to get name from various possible elements
        name_elements = soup.find_all('span', {'class': 'css-901oao'})
        if name_elements and len(name_elements) > 0:
            name = name_elements[0].text.strip()
        
        # Try to get bio
        bio_elements = soup.find_all('span', {'data-testid': 'UserDescription'})
        if bio_elements:
            bio = bio_elements[0].text.strip()
        
        # Try to get followers
        for link in soup.find_all('a'):
            if '/followers' in link.get('href', ''):
                followers = link.text.strip()
                break
        
        if name == "N/A" and "not found" in soup.text.lower():
            print(f"[!] Twitter profile {username} not found or requires login.")
            return None
            
        print(f"[*] Twitter: {name} | Bio: {bio[:50]}... | Followers: {followers}")
        return {"platform": "twitter", "username": username, "name": name, "bio": bio, "followers": followers}
    except Exception as e:
        print(f"[!] Error scraping Twitter: {e}")
        return None
    finally:
        driver.quit()

def scrape_linkedin(username):
    url = f"https://www.linkedin.com/in/{username}"
    driver = init_driver()
    try:
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        name = soup.find("h1").text.strip() if soup.find("h1") else "N/A"
        headline = "N/A"
        location = "N/A"
        
        headline_elem = soup.find("div", {"class": "text-body-medium"})
        if headline_elem:
            headline = headline_elem.text.strip()
        location_elem = soup.find("span", {"class": "text-body-small"})
        if location_elem:
            location = location_elem.text.strip()
        
        print(f"[*] LinkedIn: {name} | Headline: {headline} | Location: {location}")
        return {"platform": "linkedin", "username": username, "name": name, "headline": headline, "location": location}
    except Exception as e:
        print(f"[!] Error scraping LinkedIn: {e}")
        return None
    finally:
        driver.quit()

def save_csv(data):
    if not data:
        return
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)
    print(f"[*] Data saved to {OUTPUT_CSV}")

def main():
    if PLATFORM == "twitter":
        result = scrape_twitter(TARGET)
    elif PLATFORM == "linkedin":
        result = scrape_linkedin(TARGET)
    else:
        print("Usage: python social_scraper.py <platform> <username>")
        print("Example: python social_scraper.py twitter elonmusk")
        sys.exit(1)

    if result:
        save_csv(result)
    else:
        print("[!] No data scraped.")

if __name__ == "__main__":
    main()