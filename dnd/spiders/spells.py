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

    items_regex = r':\s(.*)$'

    def parse_item(self, response):
        item = {}
        item['url'] = response.url
        item['name'] = response.xpath('//main[@role="main"]/section/article/h1//text()').get()
        item['level'] = response.xpath('//div[@class="article-content"]/p[1]//text()').get()
        spell_paragraph = response.xpath('//div[@class="article-content"]/p[2]//text()').re(self.items_regex)
        if len(spell_paragraph) > 0:
            item['casting-time'] = spell_paragraph[0]
        if len(spell_paragraph) > 1:
            item['range'] = spell_paragraph[1]
        if len(spell_paragraph) > 2:
            item['components'] = spell_paragraph[2]
        if len(spell_paragraph) > 3:
            item['duration'] = spell_paragraph[3]
        item['description'] = "".join(response.xpath('//div[@class="article-content"]/p[3]//text()').getall()) 
        item['higher-levels'] = "".join(response.xpath('//div[@class="article-content"]/p[4]//text()').getall())

        return item
