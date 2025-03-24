import scrapy

from kompass.items import KompassCompanyItem


class KompassCompanyProfileSpider(scrapy.Spider):
    name = "kompass_company_profile"
    allowed_domains = ["fr.kompass.com", "proxy.scrapeops.io", "proxy.scrapeops.io/v1"]
    start_urls = ["https://fr.kompass.com/searchCompanies?text=LALLEMAND&searchType=COMPANYNAME"]

    custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.jsonl': { 'format': 'jsonlines',}}
    }

    def start_requests(self):
        """Allow to add proxy on first url we are going on otherwise we might be blocked"""
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)
    # End def start_requests

    def parse(self, response):
        companies = response.css('div[id="resultatDivId"]')
        print("*************** TEST ****************")
        print(companies)

        # Loop on each company to retrieve some data
        for company in companies:
            yield self.parse_profile(company)

        # Go trough all pages
        next_page = response.css('li.next a ::attr(href)').get() # /searchCompanies/scroll?tab=cmp&pageNbre=2

        if next_page is not None:
            next_page_url = 'https://fr.kompass.com/' + next_page
            yield scrapy.Request(url=next_page_url, callback=self.parse)
    # End def parse

    def parse_profile(self, response):
        kompass_company = KompassCompanyItem()

        ## Company name
        try:
            kompass_company['company_name'] = response.css("h1::text").get()
        except Exception as e:
            print("--> company_name", e)
            kompass_company['company_name'] = ''

        ## Company location
        try:
            kompass_company['location'] = response.css("span[itemprop='addressLocality']::text").get()
        except Exception as e:
            print("--> location", e)
            kompass_company['location'] = ''

        ## Company description
        try:
            kompass_company['description'] = response.css("div#summaryContent p::text").get()
        except Exception as e:
            print("--> description", e)
            kompass_company['description'] = ''

        ## Company products_services
        try:
            kompass_company['products_services'] = response.css(".main-activity__activities li::text").getall()
        except Exception as e:
            print("--> products_services", e)
            kompass_company['products_services'] = ''

        ## Company exporter_status
        try:
            kompass_company['exporter_status'] = response.xpath("//dt[contains(text(), 'Exporter')]/following-sibling::dd/text()").get()
        except Exception as e:
            print("--> exporter_status", e)
            kompass_company['exporter_status'] = ''

        ## Company phone_number
        try:
            kompass_company['phone_number'] = response.css("a.phone span::text").get()
        except Exception as e:
            print("--> phone_number", e)
            kompass_company['phone_number'] = ''
        
        ## company_url
        try:
            kompass_company['company_url'] = response.css("a.company-link::attr(href)").get()
        except Exception as e:
            print("--> company_url", e)
            kompass_company['company_url'] = ''      
        
        yield kompass_company
    # End def parse_profile
# End class KompassCompanyProfileSpider