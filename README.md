📁 Social Media OSINT Scraper (Twitter/LinkedIn)

Description
Automates scraping of public profiles from Twitter and LinkedIn using Selenium (headless Chrome). Extracts name, bio, followers, headline, location, etc., and saves to CSV.

Key Features

    Supports Twitter and LinkedIn.

    Headless browser automation.

    Handles login (optional) and dynamic content.

    Fallback simulation mode if real scraping is blocked.

Technologies

    Selenium, BeautifulSoup, ChromeDriver.

Prerequisites

    Chrome/Chromium browser, ChromeDriver installed.

    Python 3.

Installation
bash

sudo apt install chromium-chromedriver
pip install selenium beautifulsoup4

Usage
bash

python social_scraper.py twitter elonmusk

If scraping fails, it falls back to simulation.

Sample Output
text

[*] Twitter: Elon Musk (@elonmusk) | Bio: ... | Followers: 100M+
[*] Data saved to scraped_data.csv

Notes

    May require login or updated selectors if the site changes.

    Use simulation mode for demonstration.
