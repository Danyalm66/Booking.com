# -*- coding: utf-8 -*-
import scrapy


class BookSpider(scrapy.Spider):
    name = 'book'
    start_urls = ['https://www.booking.com/searchresults.en-gb.html?dest_id=-1506909;dest_type=city;iata=AKL;ss=Auckland%2C%2BAuckland%2BRegion%2C%2BNew%2BZealand']

    def parse(self, response):
        page_urls=response.xpath('//a[@class="hotel_name_link url"]/@href').getall()
        img_urls=response.xpath('//*[@class="hotel_image"]/@src').getall()
        for url in page_urls:
            abs_url=response.urljoin(url.strip())
            yield scrapy.Request(abs_url,callback=self.main_page,meta={'Image':img_urls[page_urls.index(url)]})

        next_page = response.xpath('//a[contains(@title, "Next page")]/@href').get()
        if next_page!=None:
            yield scrapy.Request(next_page)

    def main_page(self,response):
        data = {}
        data['Names'] = response.xpath('//*[@class="hp__hotel-name"]/text()')[1].get(default='').strip()
        data['Rating'] = response.xpath('//*[@class="bui-review-score__badge"]/text()').get(default='').strip()
        data['Reviews'] = response.xpath('//*[@class="bui-review-score__text"]/text()').get(default='').strip()
        data['Description'] = ' '.join(response.xpath('//*[@id="property_description_content"]/p/text()').getall())
        data['Location'] = response.xpath('//*[contains(@class,"hp_address_subtitle")]/text()').get(default='').strip()
        data['image'] = response.meta['Image']
        data['links'] = response.url
        data['Category']=response.xpath('//*[@class="hp__hotel-type-badge"]/text() | //span[contains(@class,"bui-badge")]/text()').get(default='').strip()
        yield data
