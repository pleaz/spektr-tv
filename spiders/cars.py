# -*- coding: utf-8 -*-
from car.items import CarItem
import scrapy


class CarSpider(scrapy.Spider):
    name = 'cars'
    allowed_domains = ['www.spektr-tv.ru']
    start_urls = ['https://www.spektr-tv.ru/complect.php']

    def parse(self, response):
        prods = response.xpath('//div[@class="media-heading"]/a/@href').extract()
        for prod in prods:
            yield scrapy.Request(
                prod,
                callback=self.parse_url
            )
        next_page = response.xpath('//div[@class="next"]/parent::a/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request('https://www.spektr-tv.ru/'+next_page)

    @staticmethod
    def parse_url(response):
        title = response.xpath('//h1[@class="title-page"]/text()').extract_first()
        model = response.xpath('//meta[@itemprop="model"]/@content').extract_first()
        s = response.xpath('//span[@class="or_price price"]/text()').extract_first()
        ss = filter(lambda x: x.isdigit(), s)
        price = "".join(ss)
        desc = response.xpath('//div[@class="span7 offset1"]/*[not(self::div[@class="buy"]) and not(self::div[@class="row"]) and not(self::div[@class="clearfix"])]').extract()
        description = "".join(desc)
        manufacturer = response.xpath('//meta[@itemprop="manufacturer"]/@content').extract_first()
        image = response.xpath('//meta[@itemprop="image"]/@content').extract_first()
        category = response.xpath('//span[@typeof="v:Breadcrumb" and position() = (last()-1)]/a/@alt').extract_first()

        item = CarItem()
        item['model'] = model
        item['title'] = title
        item['price'] = price
        item['description'] = description
        item['manufacturer'] = manufacturer
        item['image'] = image
        item['category'] = category
        yield item
