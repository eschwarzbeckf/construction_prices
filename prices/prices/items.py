# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from itemloaders.processors import Join, MapCompose
from datetime import datetime

def remove_whitespace(value):
    return value.strip()

def clear_price(value):
    return value.replace('$','').replace(',','').strip()
    
class PricesItem(Item):
    webpage = Field(input_processor= MapCompose(remove_whitespace),output_processor=Join())
    name = Field(input_processor= MapCompose(remove_whitespace),output_processor=Join(),default='')
    manufacturer = Field(input_processor= MapCompose(remove_whitespace),output_processor=Join(),default='')
    short_description = Field(input_processor= MapCompose(remove_whitespace),output_processor=Join(),default='')
    price = Field(input_processor= MapCompose(clear_price,remove_whitespace),output_processor=Join(),default=0.0)
    date_scraped = Field(input_processor= MapCompose(remove_whitespace),output_processor=Join(),default=datetime.now().strftime("%Y-%m-%d"))
    city = Field(input_processor= MapCompose(remove_whitespace),output_processor=Join())
    state = Field(input_processor= MapCompose(remove_whitespace),output_processor=Join())
    store_name = Field(input_processor= MapCompose(remove_whitespace),output_processor=Join())
    store_address = Field(input_processor= MapCompose(remove_whitespace),output_processor=Join())
    product = Field(input_processor= MapCompose(remove_whitespace),output_processor=Join(),default='')

