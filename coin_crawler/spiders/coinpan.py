# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from coin_crawler.items import CoinCrawlerItem


class CoinpanItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    context_out = Join(' ')


class CoinpanSpider(CrawlSpider):
    name = 'coinpan'
    allowed_domains = ['coinpan.com']
    start_urls = ['https://coinpan.com/']
    
    item_fields = {
        'title': '//div[@class="read_header"]/h1/a/text()',
        'nick_name': '//*[contains(@class, "author")]/text()',
        # 렌더링
        'level': '//img[contains(@class, "level")]/@alt',
        'recommend': '//*[text()[contains(., "추천")]]/span/b/text()',
        'non_recommend': '//*[text()[contains(., "비추천")]]/span/b/text()',
        'uploaded_time': '//span[@class="number"]/text()',
        'context': '//*[contains(@class, "xe_content")]/p/text()',
        'view_count': '//a[text()[contains(., "조회")]]/span/b/text()',
    }
    
    rules = (
        Rule(LinkExtractor(allow=('free/*',)), callback='parse_item', follow=True),
    )
    
    def parse_item(self, response):
        loader = CoinpanItemLoader(item=CoinCrawlerItem(), response=response)
        
        for field, xpath in self.item_fields.items():
            loader.add_xpath(field, xpath)
        return loader.load_item()
