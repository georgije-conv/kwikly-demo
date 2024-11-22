# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os


class KwiklyScraperPipeline:
    def process_item(self, item, spider):
        return item


class MarkdownPipeline:
    def process_item(self, item, spider):
        # Create a directory for output if it doesn't exist
        output_dir = "output_markdown"
        os.makedirs(output_dir, exist_ok=True)

        # Generate a filename based on the URL
        filename = os.path.join(output_dir, f"{item['title']}.md".replace("/", "_").replace("\\", "_"))

        # Write content to a Markdown file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {item['title']}\n\n")
            f.write(f"URL: {item['url']}\n\n")
            f.write(item['text'])

        return item
