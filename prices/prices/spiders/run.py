from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .homedepot import HomedepotSpider
from .mapco import MapcoSpider
from .construrama import ConstruramaSpider

if __name__ == "__main__":
    # Start CrawlerProcess
    process = CrawlerProcess(get_project_settings())
    
    # Add spiders to the process
    for spider in [MapcoSpider,HomedepotSpider, ConstruramaSpider]:
        process.crawl(spider)
    
    # Start the crawling process
    process.start()