import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import html2text


class KwiklyCrawlerSpider(CrawlSpider):
    name = "kwikly_crawler"
    allowed_domains = ["joinkwikly.com"]
    start_urls = ["https://joinkwikly.com"]

        # Define rules for following links
    rules = (
        Rule(
            LinkExtractor(
                allow_domains=allowed_domains,
                deny=( # Add patterns you want to exclude
                    r'swarm-pages/'
                )
            ),
            callback='parse_page',
            follow=True
        ),
    )

    def __init__(self, *args, **kwargs):
        super(KwiklyCrawlerSpider, self).__init__(*args, **kwargs)
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
        self.html_converter.ignore_tables = False
        self.html_converter.body_width = 0  # Don't wrap text

    # def parse_page(self, response):
    #     title = response.xpath("//title/text()").extract_first()
    #     page_content = response.xpath('//main[@id="content"]//text()').extract()
    #     content = {
    #         "title": title.strip() if title else "No Title",
    #         "url": response.url,
    #         "text": "\n\n".join([text.strip() for text in page_content if text.strip()])
    #     }
    #     yield content

    def parse_page(self, response):
        # Parse the URL to create directory structure
        parsed_url = urlparse(response.url)
        path_parts = parsed_url.path.strip('/').split('/')

        # Create filename from URL
        if path_parts[-1] == '':
            # the home page should have a blank path_parts ending.
            filename = 'index.md'
        else:
            filename = path_parts[-1] + '.md'

        # Create directory path
        dir_path = os.path.join('output', *path_parts[:-1])
        os.makedirs(dir_path, exist_ok=True)

        # Get the main content
        soup = BeautifulSoup(response.body, 'lxml')

        # Remove unwanted elements (customize as needed)
        for element in soup.select('nav, footer, header, script, style'):
            element.decompose()

        # Extract main content (customize selectors based on website structure)
        main_content = soup.select_one('main, article, .content, #content, body')

        # Extract main content (customize selectors based on website structure)
        main_content = soup.select_one('main, article, .content, #content, body')
        
        if main_content:
            content = main_content
        else:
            content = soup.body

        markdown_content = self.html_converter.handle(str(content))
        markdown_content = markdown_content.replace('Skip to the content', '')
        markdown_content = markdown_content.replace('Skip to content', '')
        # Remove empty lines at the start of the content
        markdown_content = '\n'.join(line for line in markdown_content.split('\n') if line.strip()).strip()

        # Create metadata section
        metadata = f"""---
url: {response.url}
title: {soup.title.string if soup.title else 'Untitled'}
date_scraped: {response.headers.get('Date', b'').decode('utf-8')}
---
"""

        # Combine metadata and content
        full_content = metadata + markdown_content

        # Save to file
        file_path = os.path.join(dir_path, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_content)

        yield {
            'url': response.url,
            'file_path': file_path,
            'title': soup.title.string if soup.title else 'Untitled'
        }