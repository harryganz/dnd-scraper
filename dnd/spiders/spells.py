# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SpellsSpider(CrawlSpider):
    name = 'spells'
    allowed_domains = ['5esrd.com']
    start_urls = ['http://5esrd.com/spellcasting/all-spells']

    rules = (
        Rule(LinkExtractor(allow=r'/spellcasting/all-spells/a/.+/$'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        item['url'] = response.url
        item['name'] = response.css('main[role="main"] section article h1::text').get()
        item['description'] = response.css('.article-content p.description::text').get()
        return item
