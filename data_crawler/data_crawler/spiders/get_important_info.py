from typing import Any, Iterable, Optional
import scrapy
import pandas as pd
import datetime
import logging
from io import StringIO
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup

from scrapy.http import Request, Response
from ..items import UniformCrawlerItem, InfoCrawlerItem

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
     

    def parse(self, response: Response, **kwargs: Any) -> Any:
        if not response.xpath("//tr[@class='odd' or @class='even']"):
            self.log(f"No data found in {response.url}", level=logging.WARNING)
            return

        for row_i, row in enumerate(response.xpath("//tr[@class='odd' or @class='even']")):
            values = {}
            columns = ['name', 'symbol', 'issue_date', 'issue_time', 'subject', 'a', 'b', 'happen_date', 'content', 'c']
            for col_i, col in enumerate(columns):
                value_num = f'h{str(col_i + row_i * 10).zfill(2)}'
                value = row.xpath(f".//input[@name='{value_num}']/@value").get()
                if value:
                    values[col] = value.strip()
            
            items = UniformCrawlerItem()
            items['date'] = pd.to_datetime(f"{self.year}-{self.month}-{self.day}")
            items['parse_date'] = datetime.date.today()
            items['table'] = 'important_info'
            items['status'] = 'success' if response.status == 200 else 'error'
            items['items'] = list()
            
            val = InfoCrawlerItem()
            for k, v in values.items():
                if k == 'issue_time':
                    v = v.zfill(6)
                val[k] = v
            items['items'].append(dict(val))
            yield dict(items)

        # return super().parse(response, **kwargs)