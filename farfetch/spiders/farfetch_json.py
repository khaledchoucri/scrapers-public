# -*- coding: utf-8 -*-
import scrapy
import json
import re

class FarfetchJsonSpider(scrapy.Spider):
    name = 'farfetch_json'
    allowed_domains = ['farfetch.com']
    start_urls = [
        'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?page=1&view=180&category=136311&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&category=137168&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&category=137188&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&category=137189&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&category=135999&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&category=136312&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&category=136314&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&category=136315&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&category=136015&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&category=137170&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&category=136035&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&category=136033&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971'
    ]
    
    def parse(self, response):

        data = json.loads(response.body)
        current_page = int(re.findall(r'page=(\d+)',response.url)[0])
        current_category = re.findall(r'category=(\d+)',response.url)[0]
        #colour_list = list(data.get('facetCount',[]).get('colour',[]).keys())
        #for colour in colour_list:
            #current_colour = re.findall(r'colour=(\d+)',response.url)[0]

        for item in data.get('products',[]):
            yield {
                   'product_name': item.get('shortDescription'),
                   'product_designer': item.get('brand',[]).get('name',[]),
                   'product_price': item.get('priceInfo', []).get('finalPrice',[]),
                   'product_stock': item.get('stockTotal',[]),
                   'product_category': current_category,
                   'page_debug': current_page
                }

            if data.get('totalPages',0) > current_page: 
                current_page += 1
                next_page = re.sub(r'page=(\d+)', 'page='+str(current_page), response.url)
                yield response.follow(next_page,callback=self.parse)

                #next_page = re.sub(r'colour=(\d+)', 'colour='+str(colour), response.url)
                #yield response.follow(next_page,callback=self.parse)