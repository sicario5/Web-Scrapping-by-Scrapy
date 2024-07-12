import scrapy


class WorldometersSpider(scrapy.Spider):
    name = "worldometers"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country/"]

    def parse(self, response):
        title=response.xpath('//h1/text()').get()
        #countries=response.xpath('//td/a/text()').getall() # get all countries name
        countries=response.xpath('//td/a') # get all countries link list
        


        yield{
            'titles':title,
        }

        for country in countries:
            country_name=country.xpath('.//text()').get() # get name of couuntry
            country_link=country.xpath('.//@href').get() # get link of couuntry which is relative

         #   absolute_country_link=f'https://www.worldometers.info{country_link}'

            #yield{
                
            #    'country_name':country_name,
            #    'country_link':absolute_country_link,
            #}
            
            #absolute_country_link=response.urljoin(country_link)
            #yield scrapy.Request(url=absolute_country_link)

        #relative link
            yield response.follow(url=country_link, callback=self.prase_country,meta={'country':country_name})


    def prase_country(self, response):
        #response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr') #both are samw
        rows=response.xpath('(//table[contains(@class,"table")])[1]/tbody/tr')
        country=response.request.meta['country']

        for row in rows:
            year=row.xpath('.//td[1]/text()').get()
            population=row.xpath('.//td[2]/strong/text()').get()

            yield{
                'country':country,
                'year':year,
                'population':population,
            }




            
