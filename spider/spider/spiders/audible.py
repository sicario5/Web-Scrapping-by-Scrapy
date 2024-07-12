from typing import Iterable
import scrapy


class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["www.audible.com"]
    #start_urls = ["https://www.audible.com/search/"]

# changing user agent so that the website we scrapy that don't know about us.
    def start_requests(self):
        yield scrapy.Request(url='https://www.audible.com/search/',callback=self.parse,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'})

    def parse(self, response):
        products_container=response.xpath('//div[@class="adbl-impression-container "]//li[contains(@class,"productListItem")]')
        

        for product in products_container:
            book_name=product.xpath('.//h3[contains(@class,"bc-heading")]/a/text()').get()
            author_name=product.xpath('.//li[contains(@class,"authorLabel")]/span/a/text()').getall() #because a book have more one author
            book_length=product.xpath('.//li[contains(@class,"runtimeLabel")]/span/text()').get()

            yield{
                'book_name':book_name,
                'author_name':author_name,
                'book_length':book_length,
                'user_agent':response.request.headers['User-Agent'],

            }
# getting pagination bar

        pagination=response.xpath('//ul[contains(@class,"pagingElements")]')
        next_page_url=pagination.xpath('.//span[contains(@class,"nextButton")]/a/@href').get()
        button_disabled=pagination.xpath('.//span[contains(@class,"nextButton")]/a/@aria-disabled').get()
# going to next_page_url

        if next_page_url and button_disabled==None:
            yield response.follow(url=next_page_url,callback=self.parse,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}) #better than selenium while loop

