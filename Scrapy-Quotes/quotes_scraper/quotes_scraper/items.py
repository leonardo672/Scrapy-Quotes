# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotesScraperItem(scrapy.Item):
        Text = scrapy.Field()
        Author = scrapy.Field()
        Tags = scrapy.Field()

