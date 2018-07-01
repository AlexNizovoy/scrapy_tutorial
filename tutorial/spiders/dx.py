# -*- coding: utf-8 -*-
import scrapy


class DxSpider(scrapy.Spider):
    name = 'dx'
    allowed_domains = ['dx.com']

    def start_requests(self):
        url = 'http://dx.com/'
        search = getattr(self, 's', None)
        if search:
            url = url + 's/' + search.replace(' ', '+')
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for product in response.css('#c_list'):
            yield {
                'category': product.css('.cate a::text').extract_first(),
                'title': product.css('.title a::attr(title)').extract_first(),
                'price': product.css('.price::text').extract_first(),
                'url': product.css('.title a::attr(href)').extract_first(),
            }

        next_url = response.css('div.pagelist_bt a.next')
        if next_url:
            yield response.follow(next_url[0], self.parse)
