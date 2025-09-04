# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from itemloaders.processors import Join
from datetime import datetime

class PricesItem(Item):
    webpage = Field(output_processor=Join())
    name = Field(output_processor=Join(),default='')
    manufacturer = Field(output_processor=Join(),default='')
    short_description = Field(output_processor=Join(),default='')
    price = Field(output_processor=Join(),default='')
    date_scraped = Field(output_processor=Join(),default=datetime.now().strftime("%Y-%m-%d"))
    city = Field(output_processor=Join())
    state = Field(output_processor=Join())
    store_name = Field(output_processor=Join())
    store_address = Field(output_processor=Join())
