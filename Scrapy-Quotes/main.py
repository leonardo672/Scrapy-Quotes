import scrapy
import asyncio
from twisted.internet import asyncioreactor



class QuotesSpider(scrapy.Spider):
    name = "quotes"  # Название паука
    start_urls = [
        'http://quotes.toscrape.com/page/1/',  # Начальная страница для парсинга
    ]
    # Disable signal handling by setting handle_signals=False
  #  asyncioreactor.install(asyncio.get_event_loop(), handle_signals=False)
    def parse(self, response):
        # Парсинг цитат
        for quote in response.css("div.quote"):
            yield {
                'text': quote.css("span.text::text").get(),
                'author': quote.css("small.author::text").get(),
                'tags': quote.css("div.tags a.tag::text").getall(),
            }

        # Переход на следующую страницу, если она существует
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
