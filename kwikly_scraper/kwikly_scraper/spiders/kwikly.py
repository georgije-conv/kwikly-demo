import scrapy
from bs4 import BeautifulSoup


class KwiklySpider(scrapy.Spider):
    name = "kwikly"
    allowed_domains = ["joinkwikly.com"]
    start_urls = ["https://joinkwikly.com"]

    def parse(self, response):
        title = response.xpath("//title/text()").extract_first()
        soup = BeautifulSoup(response.body, 'html.parser')
        content = soup.find('main', attrs={"role": "main"}).get_text()

        yield {'Title': title,
               "Content": content}



"""
import scrapy
from bs4 import BeautifulSoup

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://www.example.com']

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')

        # Extract data using BeautifulSoup
        title = soup.find('h1').text
        content = soup.find('div', class_='content').get_text()

        # Convert to Markdown
        markdown_text = f"# {title}\n\n{content}"

        yield {'markdown': markdown_text}"""