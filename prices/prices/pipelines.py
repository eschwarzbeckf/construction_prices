# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
from datetime import datetime
import os
import re

class PricesPipeline:
    def __init__(self):
        self.file_path = f'prices_{datetime.now().strftime("%Y-%m-%d")}.csv' # Define your desired CSV file name
        self.file = None
        self.writer = None
        self.header_written = False


    def open_spider(self, spider):
        # Check if file exists to determine if header needs to be written
        self.header_written = os.path.exists(self.file_path)

        # Open the file in append mode ('a')
        self.file = open(self.file_path, 'a', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)

    def close_spider(self, spider):
        if self.file:
            self.file.close()

    def process_item(self, item, spider):
        if not self.header_written:
            # Write header if it hasn't been written yet
            self.writer.writerow(item.fields.keys())
            self.header_written = True

        # Write the item data
        self.writer.writerow([item.get(field, '') for field in item.fields.keys()])

        return item

class ProductPipeline:
    def __init__(self):
        pass
    def process_item(self,item,spider):
        # estuco, mortero, yeso, adhesivo
        estuco = re.compile(r'\bestuco\b', re.IGNORECASE)
        morter= re.compile(r'\bmortero\b', re.IGNORECASE)
        yeso = re.compile(r'\byeso\b', re.IGNORECASE)
        adhesivo = re.compile(r'\badhesivo\b', re.IGNORECASE)
        for pattern, product in [(estuco, 'Estuco'), (morter, 'Mortero'), (yeso, 'Yeso'), (adhesivo, 'Adhesivo')]:
            if pattern.search(item['name']):
                item['product'] = product
                break
        return item
    

