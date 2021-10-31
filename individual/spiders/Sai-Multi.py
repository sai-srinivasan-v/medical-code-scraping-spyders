import scrapy


class CptSpider(scrapy.Spider):
    name = 'cpt'
    allowed_domains = ['coder.aapc.com']
    # start_urls = ['https://coder.aapc.com/cpt-codes/?_ga=2.48652773.2140310105.1596085860-2128224574.1596085860']
    start_urls = ['https://coder.aapc.com/cpt-codes-range/61590']
    
    def parse(self,response):
        for cpt in response.xpath("//div[@class='padtop-white']/a"):
            yield {
                "title":" Multianalyte Assay",
                "sub_title":'',
                "number":cpt.xpath(".//text()").get()
            }

        next_page = response.xpath("//a[contains(text(),'>')]/@href").get()

        if next_page:
            yield scrapy.Request(url=f"https://coder.aapc.com{next_page}", callback=self.parse)
