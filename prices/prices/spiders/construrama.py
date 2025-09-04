import scrapy
from prices.items import PricesItem
from scrapy.loader import ItemLoader
from datetime import datetime
from time import sleep

stores = {
    "Sonora":{
        "Hermosillo":{
            "locationCityId":"ChIJ5a7femiEzoYR-X-I6ZVTPbM:Hermosillo&%Son.&%Mexico:29.0729673:-110.9559192:83079",
            'stores':['knmateriales','san-benito']
        },
        "Obregon":{
            "locationCityId":"ChIJwQ5tmvEVyIYRdaBl00jka60:Ciudad%Obregon&%Son.&%Mexico:27.4827729:-109.930367:85160",
            "stores":["walhouse","knmateriales"]
        },
        "Guaymas":{
            "locationCityId":"ChIJ7x3QuPQVyYYRhPkF6AJU2ZY:Guaymas&%Son.&%Mexico:27.9110633:-110.9090678:85465",
            "stores":["knmateriales","ferreteriaindustrialsancarlos"]
        },
        "Nogales":{
            "locationCityId":"ChIJm-hjlLhO0YYR1UnTOdrKLcc:Nogales&%Son.&%Mexico:31.3011855:-110.9381047:94723",
            "stores":["marego","ferroacero","promexma-orizaba"]
        }
    },
    "Baja California":{
        "Tijuana":{
            "locationCityId":"ChIJ03tYJgI52YARViTmpK9LchQ:Tijuana&%Baja%California&%Mexico:32.5331957:-117.0192784:22010",
            "stores":["ferremaster","tijuana","lagloriasantafe","lomas"]
        },
        "Mexicali":{
            "locationCityId":"ChIJ0913qAxw14ARmvXN5aAzANQ:Mexicali&%B.C.&%Mexico:32.6245389:-115.4522623:21280",
            "stores":["promexma-mexicali"]
        },
        "Rosarito":{
            "locationCityId":"ChIJG87Ocj8x2YARR9J4jRzGDno:Rosarito&%B.C.&%Mexico:32.3661011:-117.0617553:22703",
            "stores":["ferrepacifico","ferremaster","lagloriasantafe"]
        },
        "Ensenada":{
            "locationCityId":"ChIJ9blUH_CO2IARUaZ2thuYYPM:Ensenada&%B.C.&%Mexico:31.8557021:-116.6057392:22880",
            "stores":["materialesalvarez","ferrepacifico"]
            }
    },
    "Baja California Sur":{
        "La Paz":{
            "locationCityId":"ChIJVxDa9d7Sr4YRtqPxwOjSdUg:La%Paz&%B.C.S.&%Mexico:24.1426408:-110.3127531:23079",
            "stores":["risol-cardenas"]
        },
        "Los Cabos":{
            "locationCityId":"ChIJoQjlifNKr4YRaLiiwWLfpEs:Los%Cabos&%B.C.S.&%Mexico:22.8948129:-109.9152149:23469",
            "stores":["hymca","aycdeloscabos","materialeszr"]
        }
    },
    "Sinaloa":{
        "Culiacan":{
            "locationCityId":"ChIJg1vdK6_QvIYR-Co2zF3c0_g:Culiacan&%Sin.&%Mexico:24.8090649:-107.3940117:80000",
            "stores":["culiacan"]
        },
        "Los Mochis":{
            "locationCityId":"ChIJw-o1tkIvuoYRCIgyUkfDJLY:Los%Mochis&%Sin.&%Mexico:25.7904657:-108.985882:81200",
            "stores":["losmochis"]
        },
        "Mazatlan":{
            "locationCityId":"ChIJwTcYaEFTn4YRsnI88arEpGI:Mazatlan&%Sin.&%Mexico:23.2494148:-106.4111425:82158",
            "stores":["mazatlan"]
        },
        "Guasave":{
            "locationCityId":"ChIJczjs56O_u4YR2V5OIG49B0U:Guasave&%Sin.&%Mexico:25.5666987:-108.4673051:81040",
            "stores":["guasave"]
        }
    },
    "Jalisco":{
        "Guadalajara":{
            "locationCityId":"ChIJm9MvtYyxKIQRUFeGvwKTPdY:Guadalajara&%Jal.&%Mexico:20.6751707:-103.3473385:44100",
            "stores":["guadalajara"]
        }
    }
}

from scrapy.shell import inspect_response

class ConstruramaSpider(scrapy.Spider):
    name = "construrama"
    allowed_domains = ["www.construrama.com"]
    start_urls = ["https://www.construrama.com/"]

    def parse(self, response):
        for state in stores.keys():
            for city in stores[state].keys():
                for store in stores[state][city]['stores']:
                    info = {
                        'city':city,
                        'state':state,
                        'store':store,
                        'locationCityId':stores[state][city]['locationCityId']
                    }
                    yield scrapy.Request(
                        url=f"https://www.construrama.com/{store}/catalogo/materiales-de-construccion/c/006",
                        callback=self.parse_with_cookies,
                        cookies={'locationCityId':stores[state][city]['locationCityId']},
                        cb_kwargs=info
                    )
    
    def parse_with_cookies(self, response,**kwargs):
        manufacturers = response.xpath("//ul[@id='isGrid']//span[@slot='brand']/text()").getall()
        names = response.xpath("//ul[@id='isGrid']//span[@slot='title']/text()").getall()
        short_descriptions = response.xpath("//ul[@id='isGrid']//div[@slot='description']/text()").getall()
        prices = response.xpath("//ul[@id='isGrid']//cma-card/@currentprice").getall()
        prices = [price.strip().replace('$','').replace(',','') for price in prices]

        # inspect_response(response,self)
        
        for name,manufacturer,short_description,price in zip(names,manufacturers,short_descriptions,prices):
            item = ItemLoader(item=PricesItem())
            item.add_value("webpage","Construrama")
            item.add_value("name", name)
            item.add_value("manufacturer", manufacturer)
            item.add_value("short_description", short_description)
            item.add_value("price", price.replace("$","").strip())
            item.add_value("date_scraped", datetime.now().strftime("%Y-%m-%d"))
            item.add_value("city", kwargs['city'])
            item.add_value("state", kwargs['state'])
            item.add_value("store_address", '')
            item.add_value("store_name", kwargs['store'])
            yield item.load_item()

        next_page = response.xpath("//li[@class='pagination-next']/a/@href").get()
        next_page = response.urljoin(next_page)
        if next_page:
            response.follow(next_page, callback=self.parse_with_cookies, cb_kwargs=kwargs)