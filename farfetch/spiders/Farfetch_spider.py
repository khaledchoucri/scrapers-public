# -*- coding: utf-8 -*-
import scrapy
import csv
import os
from ..items import FarfetchItem

class FarfetchSpiderSpider(scrapy.Spider):
    name = 'Farfetch_spider'
    allowed_domains = ['farfetch.com']
    start_urls = ['https://www.farfetch.com/eg/shopping/women/bags-purses-1/items.aspx?page=1&view=90']

    def parse(self, response):
        """Function to parse Farfetch bags page"""

        bag = FarfetchItem()

        XPATH_PRODUCT_DESIGNER = ".//h3[@data-test = 'productDesignerName']/text()"
        XPATH_PRODUCT_NAME=".//p[@data-test='productDescription']/text()"
        XPATH_PRODUCT_PRICE=".//span[@data-test = 'price']/text()"

        productinfo = response.xpath("//div[@data-test='information']")
        
        raw_product_designer = productinfo.xpath(XPATH_PRODUCT_DESIGNER).extract()
        raw_product_name = productinfo.xpath(XPATH_PRODUCT_NAME).extract()
        raw_product_price = productinfo.xpath(XPATH_PRODUCT_PRICE).extract()

        #bag["image_urls"] = response.xpath(".//meta[@itemprop='image']/@content").extract() 
        #bag["image_name"]
        bag["product_designer"] = ''.join(raw_product_designer).strip() if raw_product_designer else None
        bag["product_name"] = ''.join(raw_product_name).strip() if raw_product_name else None
        bag["product_price"] = ''.join(raw_product_price).strip() if raw_product_price else None
        #productinfo = response.xpath("//div[@data-test='information']")
        #for productinfo in productinfo:
        
            # XPATH_PRODUCT_DESIGNER = ".//h3[@data-test = 'productDesignerName']/text()"
            # XPATH_PRODUCT_NAME=".//p[@data-test='productDescription']/text()"
            # XPATH_PRODUCT_PRICE=".//h3[@data-test = 'productDesignerName']/text()"

            # raw_product_designer = productinfo.xpath(XPATH_PRODUCT_DESIGNER).extract()
            # raw_product_name = productinfo.xpath(XPATH_PRODUCT_NAME).extract()
            # raw_product_price = productinfo.xpath(XPATH_PRODUCT_PRICE).extract()
            
            # product_designer = ''.join(raw_product_designer).strip() if raw_product_designer else None
            # product_name = ''.join(raw_product_name).strip() if raw_product_name else None
            # product_price = ''.join(raw_product_price).strip() if raw_product_price else None

            # yield {
            #     'product_designer': product_designer,
            #     'product_name': product_name,
            #     'product_price': product_price
            # } 
            
        nextpage = response.xpath("//link[@rel='next']/@href").extract_first()

        if nextpage is not None:
            yield response.follow(nextpage,callback=self.parse)