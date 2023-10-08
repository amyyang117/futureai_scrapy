

# 'https://mops.twse.com.tw/mops/web/ajax_t05st10_ifrs?TYPEK=sii&firstin=Y&co_id=2330&off=1&year=112&month=09&step=1'

import scrapy
import numpy as np
import pandas as pd
import datetime
import logging
import requests
from bs4 import BeautifulSoup
from io import StringIO
from ..items import UniformCrawlerItem , RevenueInstantCrawlerItem

class get_monthly_revenue_instant(scrapy.Spider):
    name = 'get_monthly_revenue_instant'
    allowed_domains = ['mops.twse.com.tw']
    

    # start_urls = ['https://mops.twse.com.tw/nas/t21/']
    markets = ['sii', 'otc','rotc']
    def __init__(self, *args, **kargs):
        super(get_monthly_revenue_instant, self).__init__(*args, **kargs)
        
        # # transfer to cyear
        # self.year = year
        # self.cyear = int(year) - 1911
        # self.month = month
        
    def start_requests(self):
        logging.debug('Get stock list..')
        r = requests.get('https://mops.twse.com.tw/mops/web/t51sb10?Stp=R1&TK=')
        soup = BeautifulSoup(r.text, 'html.parser')
        logging.debug("Starting requests...")
        for form in soup.find_all('form'):
            hidden_inputs = form.find_all('input', {'type': 'hidden'})
            # for hidden in hidden_inputs:
            #     print(f"Name: {hidden.get('name')}, Value: {hidden.get('value')}")
            if len(hidden_inputs) == 7: 
                params = "&".join(f"{input_tag.get('name')}={input_tag.get('value')}" for input_tag in hidden_inputs)
                for input in hidden_inputs:
                    if input.get('name') == 'co_id':
                        symbol = input.get('value')
                    
                # print(self.symbol)
                self.url = f'https://mops.twse.com.tw/mops/web/ajax_t05st10_ifrs?{params}'
                
                yield scrapy.Request(self.url, self.parse_stock, meta={'symbol': symbol})


    def parse_stock(self, response, **kwargs):
        val = RevenueInstantCrawlerItem()
        val['symbol'] = response.meta['symbol']
        # r = requests.get(url, 'html.parser')
        # df = pd.read_html(StringIO(r.text))
        columns = ['revenue', 'last_year_revenue', 'difference' ,'YoY', 'cum_revenue', 'cum_last_year', 'cum_difference', 'cum_YoY', 'note']
        dfs = pd.read_html(StringIO(response.text))
        df = dfs[1]
        if '營業收入淨額' in df.columns:
            value = df['營業收入淨額']
        else:
            df.replace(['-', '─'], np.nan, inplace=True)
            df.dropna(inplace=True)
            value = df.iloc[2:,:2][1]

        today = datetime.date.today()
        last_month = f"{today.year - 1}-12" if today.month == 1 else f"{today.year}-{today.month-1}"

        items = UniformCrawlerItem()
        items['date'] = pd.to_datetime(last_month)
        # items['date'] = datetime.datetime.today()
        items['parse_date'] = today
        items['table'] = 'monthly_revenue_instant'
        items['status'] = 'success' if response.status == 200 else 'error'
        items['items'] = list()

        
        for col, data in zip(columns, value):
            val[col] = data
    


        items['items'].append(val)
    
        yield dict(items)
        