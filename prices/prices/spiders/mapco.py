import scrapy
from prices.items import PricesItem
from scrapy.loader import ItemLoader
from datetime import datetime


class MapcoSpider(scrapy.Spider):
    name = "mapco"
    allowed_domains = ["mapco.com.mx"]
    start_urls = ["https://mapco.com.mx/collections/construccion"]

    def parse(self, response):
        names = response.xpath("//a[contains(@class,'product-item__title')]/text()").getall()
        names = [name for name in names if name.strip()]
        manufacturers = response.xpath("//a[contains(@class,'product-item__vendor')]/text()").getall()
        manufacturers = [manufacturer for manufacturer in manufacturers if manufacturer.strip()]
        prices = response.xpath("//span[@class='price']/text()").getall()
        prices = [price for price in prices if price.strip()]
        prices = [price.split("$")[1].strip() for price in prices]

        for name, manufacturer, price in zip(names, manufacturers, prices):
            item = ItemLoader(item=PricesItem())
            item.add_value("webpage","Mapco")
            item.add_value("name", name)
            item.add_value("manufacturer", manufacturer)
            item.add_value("short_description", '')
            item.add_value("price", price)
            item.add_value("date_scraped", datetime.now().strftime("%Y-%m-%d"))
            item.add_value("city", 'Navojoa')
            item.add_value("state", 'Sonora')
            item.add_value("store_address", '')
            item.add_value("store_name", 'Navojoa')

            yield item.load_item()
        
        next_page = response.xpath("//a[contains(@class,'pagination__next')]/@href").get()
        next_page = response.urljoin(next_page)
        if next_page:
            yield response.follow(next_page, callback=self.parse)