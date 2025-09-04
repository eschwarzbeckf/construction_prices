from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .homedepot import HomedepotSpider
from .mapco import MapcoSpider
from .construrama import ConstruramaSpider

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    for spider in [HomedepotSpider, MapcoSpider, ConstruramaSpider]:
        process.crawl(spider)
    
    process.start()