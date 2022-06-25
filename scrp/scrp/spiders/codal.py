import json

import scrapy
from ..items import CodalItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class CodalSpider(scrapy.Spider):
    name = 'codal'
    allowed_domains = ['codal.ir']
    start_urls = [
        'https://codal.ir/Reports/Decision.aspx?LetterSerial=ozOMdvEayKqFMgL6tT6%2BWw%3D%3D&rt=0&let=6&ct=0&ft=-1']

    def parse(self, response):

        property_loader = ItemLoader(item=CodalItem(), response=response)
        property_loader.default_output_processor = TakeFirst()
        property_loader.add_xpath("company", '//*[@id="ctl00_txbCompanyName"]/text()')
        property_loader.add_xpath("symbol", '//*[@id="ctl00_txbSymbol"]/text()')
        spec_data = response.xpath('//script[contains(., "datasource")]/text()').re_first('var datasource = (.*);')
        my_data = json.loads(spec_data)['sheets'][0]['tables'][0]['cells']
        my_dict, m_val, m_val2, row_code = {}, {}, {}, ''

        # I know the following code is not good :( but I am improving it
        header = next(d['value'] for d in my_data if
                      d['cellGroupName'] == 'Header' and d['rowCode'] == 2 and d['rowSequence'] == 2)
        for d in my_data:
            if d['value'] and d['isVisible'] and d['cellGroupName'] == 'Body':
                if d['cssClass'] == 'dynamic_desc' and d['columnCode'] == 1:
                    m_val = {}
                    my_dict[d['value']] = m_val
                elif d['columnCode'] == 1:
                    m_val2 = {}
                    m_val[d['value']] = m_val2
                    row_code = d['rowCode']
                elif d['columnCode'] == 2 and row_code == d['rowCode']:
                    m_val2[header] = d['value']
        property_loader.add_value("explanation", my_dict)
        yield property_loader.load_item()
