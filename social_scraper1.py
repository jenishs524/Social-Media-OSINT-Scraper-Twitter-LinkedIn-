#!/usr/bin/env python3
"""
Project 24 – Social Media OSINT Scraper (with Simulation)
"""

import sys
import csv
import random

PLATFORM = sys.argv[1] if len(sys.argv) > 1 else "twitter"
TARGET = sys.argv[2] if len(sys.argv) > 2 else "testuser"
OUTPUT_CSV = "scraped_data.csv"

def simulate_scrape(platform, username):
    print(f"[*] Simulating scrape for {platform}/{username}")
    if platform == "twitter":
        data = {
            "platform": "twitter",
            "username": username,
            "name": f"Simulated User @{username}",
            "bio": "This is a simulated bio for demonstration purposes.",
            "followers": f"{random.randint(1000, 1000000):,}"
        }
    else:
        data = {
            "platform": "linkedin",
            "username": username,
            "name": f"Simulated {username}",
            "headline": "Security Researcher",
            "location": "Simulated City"
        }
    print(f"[*] {platform.capitalize()}: {data['name']} | Bio/Headline: {data.get('bio', data.get('headline', ''))}")
    return data

def save_csv(data):
    if not data:
        return
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)
    print(f"[*] Data saved to {OUTPUT_CSV}")

def main():
    # Try real scraping, fall back to simulation
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from bs4 import BeautifulSoup
        # ... real scraping code from previous version ...
    except ImportError:
        print("[!] Selenium/BeautifulSoup not installed. Using simulation mode.")
        data = simulate_scrape(PLATFORM, TARGET)
        if data:
            save_csv(data)
        return

    # If imports work, attempt real scraping
    # (Insert the real scraping code here, or keep it simple with simulation)
    print("[!] Real scraping may be blocked. Using simulation for demonstration.")
    data = simulate_scrape(PLATFORM, TARGET)
    if data:
        save_csv(data)

if __name__ == "__main__":
    main()