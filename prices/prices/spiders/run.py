from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from prices.spiders.homedepot import HomedepotSpider
from prices.spiders.mapco import MapcoSpider
from prices.spiders.construrama import ConstruramaSpider
from azure.storage.blob import BlobClient 
from dotenv import load_dotenv
from datetime import datetime
import os
from azure.storage.blob import BlobServiceClient
load_dotenv()

def run_spiders(spiders:list) -> None:
    # Start CrawlerProcess
    process = CrawlerProcess(get_project_settings())

    # Add spiders to the process
    for spider in spiders:
        process.crawl(spider)

    # Start the crawling process
    process.start()

def upload_csv_to_azure(file,filename:str) -> None:
    url = os.getenv("BLOB_URL")
    token = os.getenv("BLOB_TOKEN")
    blob_client = BlobClient(account_url=url,credential=token,container_name='csvs',blob_name=f"csv/{filename}")
    blob_client.upload_blob(file)

def run_process():
    # Run the spiders
    run_spiders([MapcoSpider,HomedepotSpider, ConstruramaSpider])

    # Set file name
    filename = f"prices_{datetime.now().strftime('%Y-%m-%d')}.csv"
    print("Scraping completed")
    print("Start upload of file to azure")

    # Upload to azure
    try:
        with open(f'{filename}', 'rb') as file:
            upload_csv_to_azure(file,filename)
        
        # Remove file
        os.remove(f'{filename}')

        print("File uploaded to Azure")
    except Exception as e:
        print("\n\n Could not upload file \n\n","Due to Below Error:\n\n")
        print(e)

if __name__ == '__main__':
    print("Scraping Process Started")
    run_process()
    print("Scraping Process Ended")
