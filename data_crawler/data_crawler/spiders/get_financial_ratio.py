from typing import Any, Iterable, Optional
import scrapy
import pandas as pd
import datetime
import logging
from io import StringIO

from scrapy.http import Request
from ..items import UniformCrawlerItem, FundamentalCrawlerItem

class get_financial_ratio(scrapy.Spider):
    name = 'get_financial_ratio'
    allowed_domains = ['mops.twse.com.tw']

    market = ['sii', 'otc', 'rotc']

    def __init__(self, year, quarter, **kwargs):
        super(get_financial_ratio).__init__(**kwargs) 
        # transfer to cyear
        self.year = year
        self.cyear = int(year) - 1911
        self.quarter = quarter

    def start_requests(self):
        logging.debug("Starting requests...")
        markets = ['sii', 'otc', 'rotc']

        for market in markets:
            self.url = f'https://mops.twse.com.tw/mops/web/ajax_t163sb06?encodeURIComponent=1&step=1&firstin=1&off=1&isQuery=Y&TYPEK={market}&year={self.cyear}&season={self.quarter}'
            yield scrapy.Request(self.url, self.parse)

    def parse(self, response, **kwargs):
        dfs = pd.read_html(StringIO(response.text))
        df = dfs[0].iloc[1:,:]
        df.columns = ['code', 'name', 'revenue', 'gross_margin', 'operating_margin', 'ebt_margin', 'net_income_margin']
        # columns = ['公司代號','毛利率(%) (營業毛利)/ (營業收入)','營業利益率(%) (營業利益)/ (營業收入)', '稅前純益率(%) (稅前純益)/ (營業收入)', '稅後純益率(%) (稅後純益)/ (營業收入)']
        columns = ['code', 'gross_margin', 'operating_margin', 'ebt_margin', 'net_income_margin']
        df = df[columns]
        df = df[df['code']!='公司代號']

        value = df.to_dict('records')
        items = UniformCrawlerItem()
        items['date'] = f"{self.year}-Q{self.quarter}"
        items['parse_date'] = datetime.date.today()
        items['table'] = 'fundamental_features'
        items['status'] = 'success' if response.status == 200 else 'error'
        items['items'] = list()

        for data in value:
            val = FundamentalCrawlerItem()
            for k,v in data.items():
                val[k] = v
            items['items'].append(dict(val))
        
        yield dict(items)



    