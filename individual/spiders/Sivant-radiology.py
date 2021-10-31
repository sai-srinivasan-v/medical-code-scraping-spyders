import scrapy


class CptSpider(scrapy.Spider):
    name = 'radio'
    allowed_domains = ['coder.aapc.com']
    # start_urls = ['https://coder.aapc.com/cpt-codes/?_ga=2.48652773.2140310105.1596085860-2128224574.1596085860']
    start_urls = ['https://coder.aapc.com/cpt-codes-range/2112']
    
    def parse(self,response):

        for cpt in response.xpath("//div[@class='sidebar-left']/div/div[2]/a"):
            link = cpt.xpath(".//@href").get()
            yield scrapy.Request(url=f"https://coder.aapc.com{link}", callback=self.parse_subtitle,meta={'name':cpt.xpath(".//text()").get()})

    def parse_subtitle(self,response):
        name = response.request.meta["name"]

        for cpt in response.xpath("//div[@class='sidebar-left']/div/div[2]/a"):
            link = cpt.xpath(".//@href").get()
            yield scrapy.Request(url=f"https://coder.aapc.com{link}", callback=self.parse_cpt_number,meta={'title':cpt.xpath(".//text()").get(),'name':name})

    def parse_cpt_number(self,response):
        title = response.request.meta["title"]
        name = response.request.meta["name"]

        for cpt in response.xpath("//div[@class='padtop-white']/a"):
            yield {
                "title":name,
                "sub_title":title,
                "number":cpt.xpath(".//text()").get()
            }

        next_page = response.xpath("//a[contains(text(),'>')]/@href").get()

        if next_page:
            yield scrapy.Request(url=f"https://coder.aapc.com{next_page}", callback=self.parse_cpt_number,meta={'title':title})
        
