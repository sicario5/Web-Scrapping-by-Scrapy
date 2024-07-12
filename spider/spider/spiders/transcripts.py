import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TranscriptsSpider(CrawlSpider):
    name = "transcripts"
    allowed_domains = ["subslikescript.com"]
    #start_urls = ["https://subslikescript.com/movies_letter-X"]
    custom_settings={
        'DOWNLOAD_DELAY':0.5, #sets a download delay of 0.5 seconds
    }

    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'


    # changing user agent so that the website we scrapy that don't know about us.
    def start_requests(self):
        yield scrapy.Request(url='https://subslikescript.com/movies_letter-X',headers={'user-agent':self.user_agent})

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//ul[@class="scripts-list"]/a')), callback="parse_item", follow=True , process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths=('//a[@rel="next"][1]')), process_request='set_user_agent'), # behave like pagination rule for next page
        )
    
    def set_user_agent(self,request,spider):
        request.headers['User-Agent']=self.user_agent
        return request

    def parse_item(self, response):
        article=response.xpath("//article[@class='main-article']")
        transcript_list=article.xpath("./div[@class='full-script']/text()").getall()
        transcript_string=' '.join(transcript_list)
        yield{
            'title':article.xpath("./h1/text()").get(),
            'plot':article.xpath("./p/text()").get(),
            'transcript':transcript_string, #sqllit3 only support string not list
            'url':response.url,
            #'user-agent':response.request.headers['User-Agent'],
        }




        