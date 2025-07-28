"""
Web Scraper Module for Changi Airport RAG Chatbot
Scrapes content from Changi Airport and Jewel Changi Airport websites
"""

import requests
from bs4 import BeautifulSoup
import time
import logging
from typing import List, Dict, Set
from urllib.parse import urljoin, urlparse
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChangiAirportScraper:
    """Scraper for Changi Airport and Jewel Changi Airport websites"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.scraped_urls: Set[str] = set()
        self.content_data: List[Dict] = []
        
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\:\;\-\(\)]', '', text)
        return text
    
    def extract_text_from_element(self, element) -> str:
        """Extract clean text from a BeautifulSoup element"""
        if element is None:
            return ""
        
        # Remove script and style elements
        for script in element(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        text = element.get_text()
        return self.clean_text(text)
    
    def get_page_content(self, url: str) -> Dict:
        """Fetch and parse a single page"""
        try:
            logger.info(f"Scraping: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = ""
            title_tag = soup.find('title')
            if title_tag:
                title = self.clean_text(title_tag.get_text())
            
            # Extract main content
            content = ""
            
            # Try to find main content areas
            main_selectors = [
                'main',
                '.main-content',
                '.content',
                '#content',
                '.page-content',
                'article',
                '.article-content'
            ]
            
            for selector in main_selectors:
                main_element = soup.select_one(selector)
                if main_element:
                    content = self.extract_text_from_element(main_element)
                    break
            
            # If no main content found, extract from body
            if not content:
                body = soup.find('body')
                if body:
                    content = self.extract_text_from_element(body)
            
            return {
                'url': url,
                'title': title,
                'content': content,
                'source': 'changi_airport' if 'changiairport.com' in url else 'jewel_changi'
            }
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return {
                'url': url,
                'title': '',
                'content': '',
                'source': 'changi_airport' if 'changiairport.com' in url else 'jewel_changi',
                'error': str(e)
            }
    
    def find_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Find all relevant links on a page"""
        links = set()
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            # Only include links from the same domain
            if self.is_same_domain(base_url, full_url):
                # Filter out non-content links
                if not self.is_excluded_url(full_url):
                    links.add(full_url)
        
        return list(links)
    
    def is_same_domain(self, base_url: str, url: str) -> bool:
        """Check if URL is from the same domain"""
        base_domain = urlparse(base_url).netloc
        url_domain = urlparse(url).netloc
        return base_domain == url_domain
    
    def is_excluded_url(self, url: str) -> bool:
        """Check if URL should be excluded from scraping"""
        excluded_patterns = [
            '/search',
            '/login',
            '/register',
            '/cart',
            '/checkout',
            '/admin',
            '/api/',
            '.pdf',
            '.jpg',
            '.jpeg',
            '.png',
            '.gif',
            '.css',
            '.js',
            'mailto:',
            'tel:',
            '#'
        ]
        
        return any(pattern in url.lower() for pattern in excluded_patterns)
    
    def scrape_website(self, base_url: str, max_pages: int = 50) -> List[Dict]:
        """Scrape a website starting from base URL"""
        urls_to_scrape = [base_url]
        scraped_data = []
        
        while urls_to_scrape and len(scraped_data) < max_pages:
            current_url = urls_to_scrape.pop(0)
            
            if current_url in self.scraped_urls:
                continue
                
            self.scraped_urls.add(current_url)
            
            try:
                response = self.session.get(current_url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract content from current page
                page_data = self.get_page_content(current_url)
                if page_data['content']:  # Only add if content exists
                    scraped_data.append(page_data)
                
                # Find new links to scrape
                if len(scraped_data) < max_pages:
                    new_links = self.find_links(soup, current_url)
                    for link in new_links:
                        if link not in self.scraped_urls and link not in urls_to_scrape:
                            urls_to_scrape.append(link)
                
                # Be respectful with rate limiting
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error processing {current_url}: {str(e)}")
                continue
        
        return scraped_data
    
    def scrape_all_sites(self) -> List[Dict]:
        """Scrape both Changi Airport and Jewel Changi Airport websites"""
        all_data = []
        
        # Changi Airport main site
        logger.info("Starting to scrape Changi Airport website...")
        changi_data = self.scrape_website('https://www.changiairport.com')
        all_data.extend(changi_data)
        
        # Reset for next site
        self.scraped_urls.clear()
        
        # Jewel Changi Airport site
        logger.info("Starting to scrape Jewel Changi Airport website...")
        jewel_data = self.scrape_website('https://www.jewelchangiairport.com')
        all_data.extend(jewel_data)
        
        logger.info(f"Total pages scraped: {len(all_data)}")
        return all_data

def main():
    """Test the scraper"""
    scraper = ChangiAirportScraper()
    data = scraper.scrape_all_sites()
    
    print(f"Scraped {len(data)} pages")
    for item in data[:3]:  # Show first 3 items
        print(f"URL: {item['url']}")
        print(f"Title: {item['title']}")
        print(f"Content length: {len(item['content'])}")
        print(f"Source: {item['source']}")
        print("-" * 50)

if __name__ == "__main__":
    main() 