import scrapy
import json
from prices.items import PricesItem
from scrapy.loader import ItemLoader
from datetime import datetime

stores = {
    "Sonora":{
        "Hermosillo":{
            "Hermosillo":{
                "address":"Blvd. Solidaridad #990 Sur,  Col. Proyecto Río Sonora,   Hermosillo, C.P.  83280 ",
                "storeid":8720
            },
            "Hermosillo Pitic":{
                "address":"Blvd. Juan Bautista Escalante #17,  Fracc. Los Angeles,   Hermosillo, C.P.  83106 ",
                "storeid":1335
            }
        },
        "Guaymas":{
            "Guaymas":{
                "address":"Av. García López #15 Carretera Internacional esq. Blvd. Camino Altular,  Col. Linda Vista,   Guaymas, C.P.  85456",
                "storeid":8654
                }
        },
        "Nogales":{
            "Nogales":{
                "address":"Blvd. Luis Donaldo Colosio 2750 entre Blvd. el Greco y Av. Alejandra,  Col. El Greco,   Nogales, C.P.  84065 ",
                "storeid":8651
            }
        },
        "Obregon":{
            "Obregon":{
                "address":"Calle Lago Superior #1065 Nte.,  Fracc. Comercial Zona Norte,   Ciudad Obregón, C.P.  85010 ",
                "storeid":8759
            }
        }
    },
    "Baja California Sur":{
        "La Paz":{
            "La Paz":{
                "address":"Blvd. Agustín Olachea esq. Libramiento,  Col. El Zacatal,  La Paz, C.P.  23090 ",
                "storeid":8628
            },
            "Los Cabos":{
                "address":"Carretera Transpeninsular Benito Juárez Km 6.5,  Col. Cabo Bello,  Los Cabos, C.P.  23410 ",
                "storeid":8766
            }
        }
    },
    "Baja California":{
        "Ensenada":{
            "Ensenada":{
                "address":"Lote 194, Manzana 054, Av. Pedro Loyola #673 esq. Calle Hierro,  Col. Carlos Pacheco,  Ensenada, C.P.  22897",
                "storeid":8775
            }
        },
        "Mexicali":{
            "Mexicali":{
                "address":"Blvd. Benito Juárez #2398,  Col. Sánchez Taboada,  Mexicali, C.P.  21370",
                "storeid":8705
            },
            "Mexicali":{
                "address":"Calz. Venustiano Carranza,  No. 876,  Col. Rivera,  Mexicali, C.P.  21259 ",
                "storeid":1325
            },
        },
        "Rosarito":{
            "Rosarito":{
                "address":"Blvd. Benito Juárez #300 Lote 000, Manzana 030,  Col. Reforma,  Playas de Rosarito, C.P.  22710 ",
                "storeid":8082
            }
        },
        "Tijuana":{
            "Tijuana 2000":{
                "address":"Corredor Tijuana-Rosarito #2000 esq. Lázaro Cárdenas,  Manzana 819,  Tijuana, C.P.  22205",
                "storeid":8854
            },
            "TIJUANA SANTA FE":{
                "address":"El Rosario #7402,  Col Valparaiso Residencial,  Tijuana, C.P.  22663 ",
                "storeid":4038
            },
            "TIJUANA SOLER":{
                "address":"Braulio Maldonado 680,  Fraccionamiento El Soler,  Tijuana, C.P.  22530 ",
                "storeid":1168
            },
            "Tijuana Via Rapida":{
                "address":"Vía Rápida Pte. esq. Lázaro Cárdenas,  Col. Los Santos Del. La Mesa,  Tijuana, C.P.  22430 ",
                "storeid":8706
            }

        }
    },
    "Sinaloa":{
        "Culiacan":{
            "Culiacán Tres Ríos":{
                "address":"Blvd. Rotarismo #1430 Nte.,   Fracc. Lago Tres Ríos esq. con Blvd. Isidro Salas,   Culiacán, C.P.  80020",
                "storeid":8664
            },
            "Culiacán Zapata":{
                "address":"Blvd. Emiliano Zapata #2546 Pte.,   Col. El Vallado,   Culiacán, C.P.  80110",
                "storeid":8708
            },
        },
        "Guasave":{
            "Guasave":{
                "address":"Calle 20 de Noviembre,   Sector Mega Proyector Sur,   Guasave, C.P.  81000",
                "storeid":8682
            }
        },
        "Mazatlan":{
            "Mazatlan":{
                "address":"Av. Rafael Buelna #600,  Col. Alameda,   Mazatlán, C.P.  82123 ",
                "storeid":8784
            }
        },
        "Los Mochis":{
            "Los Mochis":{
                "address":"Blvd. Antonio Rosales #1280 Sur,   Centro,   Mochis, C.P.  81271",
                "storeid":8771
            }
        }
    },
    "Jalisco":{
        "Zapopan":{
            "Zapopan":{
                "address":"Av. Manuel Clouthier y Av. Patria Plaza Cordilleras,   Col. El Borrego,   Zapopan, C.P.  45045",
                "storeid":8742
            },
            "Zapopan Acueducto":{
                "address":"Av. Acueducto #6050 Unidad Privativa Dos,   Lomas del Bosque Plaza Acueducto,   Zapopan, C.P.  45110 ",
                "storeid":8772
            }
        },
        "Guadalajara":{
            "GDL SANTA ANITA":{
                "address":"Av. López Mateos #7700,  Col. Santa Anita,   Guadalajara, C.P.  45640",
                "storeid":1176
            },
            "Independencia":{
                "address":"Periférico Norte #40 esq. Calzada Independencia,   Col. Lomas del Paraíso,   Guadalajara, C.P.  44250",
                "storeid":8659
            },
            "Lázaro Cárdenas":{
                "address":"Calz. Lázaro Cárdenas #2297,   Col. Las Torres,   Guadalajara, C.P.  44920 ",
                "storeid":1328
            },
            "Oblatos":{
                "address":"Av. José María Iglesias #3150 y Calle Cairo,   Col. Lomas de San Eugenio,   Guadalajara, C.P.  44700",
                "storeid":8643
            }
        },
        "Puerto Vallarta":{
            "Las Juntas":{
                "address":"Carretera Tepic-Vallarta #5348,   Col. Las Juntas,   Puerto Vallarta, C.P.  48291 ",
                "storeid":8785
            }
        },
        "Tlaquepaque":{
            "ITESO":{
                "address":"Av. Camino al Iteso #8952,   Col. Nueva Santa María,   Tlaquepaque, C.P.  45530",
                "storeid":8727
            },
            "Tlaquepaque":{
                "address":"Gral. Marcelino García Barragán #1455 esq. con Hator,   Col. San Pedro,   Tlaquepaque, C.P.  44360 ",
                "storeid":8636
            }
        }
    }
}

class HomedepotSpider(scrapy.Spider):
    name = "homedepot"
    allowed_domains = ["www.homedepot.com.mx"]
    start_urls = ["https://www.homedepot.com.mx/"]
    limit = 100

    def parse(self, response):
        for state in stores.keys():
            for city in stores[state].keys():
                for store in stores[state][city].keys():
                    storeid = stores[state][city][store]["storeid"]
                    offset = 0
                    address = stores[state][city][store]["address"]
                    url = f"https://www.homedepot.com.mx/search/resources/api/v2/products?storeId=10351&categoryId=10503&limit={self.limit}&offset={offset}&contractId=4000000000000000003&currency=MXN&langId=-5&marketId=70&stLocId=12516&physicalStoreId={storeid}&profileName=HCL_V2_findProductsByCategoryWithPriceRangeSequenceTest&orderBy=5"

                    info = dict(state=state, city=city, store=store, storeid=storeid, limit=self.limit,address=address, offset=offset,url=url)
                    yield scrapy.Request(url, callback=self.parse_page, cb_kwargs=info)
    
    def parse_page(self, response, **kwargs):
        payload = json.loads(response.body)
        state,city,store,storeid,limit,address,offset,url = kwargs.values()
        if 'contents' in payload:
            for product in payload["contents"]:
                if product.get("name") == "YESO CONSTRUCCIÓN 40 Kg":
                    product["manufacturer"]="YESERA MONTERREY"
                
                if product.get("name") == "MOCUZARI":
                    product["manufacturer"]="YINSA"

                item = ItemLoader(item=PricesItem())
                item.add_value("webpage", "Home Depot")
                item.add_value("name", product.get("name","NA"))
                item.add_value("manufacturer", product.get("manufacturer","NA"))
                item.add_value("short_description", product.get("shortDescription","NA"))
                item.add_value("price", product["price"][1]["value"])
                item.add_value("date_scraped", datetime.now().strftime("%Y-%m-%d"))
                item.add_value("city", kwargs['city'])
                item.add_value("state", kwargs['state'])
                item.add_value("store_address", kwargs["address"])
                item.add_value("store_name", kwargs['store'])
                yield item.load_item()
            offset += limit
            url = f'https://www.homedepot.com.mx/search/resources/api/v2/products?storeId=10351&categoryId=10503&limit={limit}&offset={offset}&contractId=4000000000000000003&currency=MXN&langId=-5&marketId=70&stLocId=12516&physicalStoreId={storeid}&profileName=HCL_V2_findProductsByCategoryWithPriceRangeSequenceTest&orderBy=5'
            info = dict(state=state, city=city, store=store, storeid=storeid, limit=limit,address=address, offset=offset,url=url)
            yield scrapy.Request(url, callback=self.parse_page, cb_kwargs=info)
        else:
            print("NO CONTENT")



