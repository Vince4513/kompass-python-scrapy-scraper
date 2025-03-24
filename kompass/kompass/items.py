# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KompassCompanyItem(scrapy.Item):
    # define the fields for your item here like:
    company_name = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
    products_services = scrapy.Field()
    exporter_status = scrapy.Field()
    phone_number = scrapy.Field()
    company_url = scrapy.Field()
# End class KompassCompanyItem