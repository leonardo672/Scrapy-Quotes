import scrapy
from ..items import QuotesScraperItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        items = QuotesScraperItem()
        all_div_class_quote = response.css('div.quote')

        # Extract quotes from the current page
        for quote in all_div_class_quote:
            text = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()
            tags = quote.css('div.tags a.tag::text').getall()

            items['Text'] = text
            items['Author'] = author
            items['Tags'] = tags

            yield items

        # Find the next page link and follow it if it exists
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
