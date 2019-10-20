# -*- coding: utf-8 -*-
import scrapy
from ..items import FarfetchItem

class FarfetchImagesSpider(scrapy.Spider):
    name = 'FarfetchImageSpider'
    allowed_domains = ['farfetch.com']
    start_urls = ['https://www.farfetch.com/eg/shopping/women/bags-purses-1/items.aspx?page=1&view=90']

    def parse(self, response):
    
        bag = FarfetchItem()
        bag["image_urls"] = response.xpath(".//meta[@itemprop='image']/@content").extract()

        return bag