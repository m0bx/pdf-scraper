import requests
from bs4 import BeautifulSoup

def scrape_links(url):
    # Make request to URL and get page content
    response = requests.get(url)
    content = response.content

    # Parse page content using BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Find all links on the page
    links = soup.find_all('a')

    # Create list of links that end with ".pdf"
    pdf_links = []
    for link in links:
        href = link.get('href')
        if href is not None and href.startswith('http') and href.endswith('.pdf'):
            pdf_links.append(href)

    # Return list of PDF links
    return pdf_links
