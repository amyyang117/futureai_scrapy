from typing import Any, Iterable, Optional
import scrapy
import pandas as pd
import datetime
import logging
from io import StringIO
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup

from scrapy.http import Request, Response
from ..items import UniformCrawlerItem 

class get_important_info(scrapy.Spider):
    name = 'get_important_info'
    allowed_domains = ['mops.twse.com.tw']

    # https://mops.twse.com.tw/mops/web/t05st02?step=0&newstuff=1&firstin=1&year=112&month=09&day=21
    def __init__(self, year, month, day, **kwargs):
        super(get_important_info, self).__init__(**kwargs)

        self.year = year
        self.cyear = int(year) - 1911
        self.month = month
        self.day = day

    def start_requests(self) -> Iterable[Request]:
        logging.debug('Starting requests...')
        self.url = f'https://mops.twse.com.tw/mops/web/t05st02?step=0&newstuff=1&firstin=1&year={self.cyear}&month={self.month}&day={self.day}'
        yield SplashRequest(self.url, self.parse, args={'wait': 0.5})
        # scrapy.Request(self.url, self.parse, args={'wait': 0.5})
        # return super().start_requests()
        
    def parse(self, response: Response, **kwargs: Any) -> Any:
        soup = BeautifulSoup(response.text, 'lxml')

        rows = response.css('table tr')  
        response.css('pre::text').getall()
        for row in rows:
            columns = row.css('td::text, th::text').getall()
            columns = [col.strip() for col in columns]
            if len(columns) >= 4:
                self.log(f'Row data: {columns}')

            # self.log(f'Row data: {columns}')

            # for data in columns:
            #     for row in rows:
            #         columns = row.css('td::text, th::text').getall()
            #         columns = [col.strip() for col in columns]
                    
                    
                        # items = UniformCrawlerItem()
                        # items['parse_date'] = datetime.date.today()
                        # # items['date'] = pd.to_datetime(f"{self.year}-{self.month}-{}")
                        # items['time'] = columns[1]
                        

                        # items['company_name'] = columns[2]
                        # items['announcement'] = columns[3]

                        
                        # items['table'] = 'important_info'
                        # items['items'] = list()
  
                        # yield items
                        # self.log(f'Row data: {columns}')

        # item = MyProjectItem()
        # item['row_data'] = columns

        return super().parse(response, **kwargs)