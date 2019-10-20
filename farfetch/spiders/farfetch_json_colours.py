# -*- coding: utf-8 -*-
import scrapy
import json
import re

class FarfetchJsonColourSpider(scrapy.Spider):
    name = 'farfetch_json_colours'
    allowed_domains = ['farfetch.com']
    start_urls = [
        'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&colour=1&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&colour=7&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&colour=5&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&colour=13&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&colour=6&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&colour=3&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&colour=11&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&colour=12&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&colour=4&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&colour=16&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&colour=9&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&colour=15&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&colour=8&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&colour=14&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&colour=2&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971',
    'https://www.farfetch.com/eg/plpslice/listing-api/products-facets?view=180&colour=10&page=1&type=Shopping&gender=Women&pricetype=FullPrice&c-category=135971'
    ]
    
    def parse(self, response):

        data = json.loads(response.body)
        current_page = int(re.findall(r'page=(\d+)',response.url)[0])
        current_colour = re.findall(r'colour=(\d+)',response.url)[0]
        #colour_list = list(data.get('facetCount',[]).get('colour',[]).keys())
        #for colour in colour_list:
            #current_colour = re.findall(r'colour=(\d+)',response.url)[0]
        
        colour_labels = data.get('facetCount').get('colour').keys()
        colour_names = ["Black","Blue","Brown","Gold","Green","Grey","Metallic","Multicolour","Neutrals","Orange","Pink","Purple","Red","Silver","White","Yellow"]
        colour_dict = dict(zip(colour_labels,colour_names))
                
        for item in data.get('products',[]):
            yield {
                   'product_name': item.get('shortDescription').strip(),
                   'product_designer': item.get('brand',[]).get('name',[]).strip(),
                   'product_price': item.get('priceInfo', []).get('finalPrice',[]),
                   'product_stock': item.get('stockTotal',[]),
                   'product_colour': colour_dict.get(current_colour),
                   'page_debug': current_page
                }

            if data.get('totalPages',0) > current_page: 
                current_page += 1
                next_page = re.sub(r'page=(\d+)', 'page='+str(current_page), response.url)
                yield response.follow(next_page,callback=self.parse)

                #next_page = re.sub(r'colour=(\d+)', 'colour='+str(colour), response.url)
                #yield response.follow(next_page,callback=self.parse)