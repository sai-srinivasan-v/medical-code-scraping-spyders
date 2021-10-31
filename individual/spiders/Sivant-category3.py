import scrapy


class CptSpider(scrapy.Spider):
    name = 'category3'
    allowed_domains = ['coder.aapc.com']
    # start_urls = ['https://coder.aapc.com/cpt-codes/?_ga=2.48652773.2140310105.1596085860-2128224574.1596085860']
    start_urls = ['https://coder.aapc.com/cpt-codes-range/2962']
    
    def parse(self,response):

        for cpt in response.xpath("//div[@class='sidebar-left']/div/div[2]/a"):
            link = cpt.xpath(".//@href").get()
            yield scrapy.Request(url=f"https://coder.aapc.com{link}", callback=self.parse_cpt_number,meta={'title':cpt.xpath(".//text()").get()})

    def parse_cpt_number(self,response):
        title = response.request.meta["title"]

        for cpt in response.xpath("//div[@class='padtop-white']/a"):
            yield {
                "title":"Category III Codes",
                "sub_title":title,
                "number":cpt.xpath(".//text()").get()
            }

        next_page = response.xpath("//a[contains(text(),'>')]/@href").get()

        if next_page:
            yield scrapy.Request(url=f"https://coder.aapc.com{next_page}", callback=self.parse_cpt_number,meta={'title':title})
        

