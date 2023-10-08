import re
import scrapy
import pandas as pd
import logging
import datetime
from io import StringIO
from ..items import UniformCrawlerItem, FinancialStatementCrawlerItem

class get_financial_statement(scrapy.Spider):
    name = 'get_financial_statement'
    allowed_domains = ['mops.twse.com.tw']

    def __init__(self, symbol, year, quarter, *args, **kargs):
        super(get_financial_statement, self).__init__(*args, **kargs)
        self.symbol = symbol
        self.year = year
        self.quarter = quarter

    def start_requests(self):
        logging.debug("Starting requests...")
        self.url = f'https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID={self.symbol}&SYEAR={self.year}&SSEASON={self.quarter}&REPORT_ID=C'
        yield scrapy.Request(self.url, self.parse_stock)

    def parse_stock(self, response, **kwargs):
        try:
            dfs = pd.read_html(StringIO(response.text))
            df_concat = pd.DataFrame()
            for i in range(3):
                df = dfs[i].iloc[:, 1:3].copy()
                df.columns = df.columns.droplevel(0)
                df.columns = ['accounting', 'number']
                df['accounting'] = df['accounting'].str.replace(r'\(|\)|\（|\）', '', regex=True)
                df.insert(0, 'symbol', self.symbol)
                df.insert(0, 'accounting_title', df['accounting'].apply(lambda x: self.split_cn_en(x)[-1]).str.replace('-', '_').str.replace(' ', '_').str.lower())
                df['accounting_title'] = df['accounting_title'].str.replace(' ', '_')
                df = df.dropna()
                df_concat = pd.concat([df_concat, df])

            df_concat['number'] = df_concat['number'].apply(self.convert_to_number_format)
            df_data = pd.pivot_table(df_concat, values='number', index=['symbol'], columns='accounting_title', aggfunc='max')
            value = df_data.reset_index().to_dict('records')
        
            items = UniformCrawlerItem()
            items['date'] = f"{self.year}-Q{self.quarter}"
            items['parse_date'] = datetime.date.today()
            items['table'] = 'financial_statement'
            items['status'] = 'success' if response.status == 200 else 'error'
            items['items'] = list()

            for data in value:
                val = FinancialStatementCrawlerItem()
                for k,v in data.items():
                    if k in FinancialStatementCrawlerItem.fields:  # Check if k is a field defined in FinancialStatementCrawlerItem
                        val[k] = v
                items['items'].append(dict(val))
            
            yield dict(items)
            
        except Exception as e:
            logging.error(f"Error while parsing response for symbol {self.symbol}, year {self.year}, quarter {self.quarter}: {e}")
        

    def split_cn_en(self, s):
        if '年' in s and '月' in s and '日' in s:
            if "至" in s:
                cn_pattern = r"[\u4e00-\u9fa5]+年[\u4e00-\u9fa5]+月[\u4e00-\u9fa5]+日至[\u4e00-\u9fa5]+年[\u4e00-\u9fa5]+月[\u4e00-\u9fa5]+日"
                en_pattern = r"\d{4}/\d{1,2}/\d{1,2}To\d{4}/\d{1,2}/\d{1,2}"
            else:
                cn_pattern = r"[\u4e00-\u9fa5]+年[\u4e00-\u9fa5]+月[\u4e00-\u9fa5]+日"
                en_pattern = r"\d{4}/\d{1,2}/\d{1,2}"
        else:
            cn_pattern = r"[\u4e00-\u9fa5]"
            en_pattern = r"[A-Za-z\s\-]+"
        
        cn_match = re.search(cn_pattern, s)
        en_match = re.search(en_pattern, s)

        results = []
        if cn_match:
            results.append(cn_match.group().strip())
        if en_match:
            results.append(en_match.group().strip())
        
        return results if results else [""]


    def convert_to_number_format(self, s):
        if isinstance(s, str):
            if s.startswith('(') and s.endswith(')'):
                s = s[1:-1] 
                s = s.replace(',', '') 
                return -float(s)  # Convert to negative float
            else:
                s = s.replace(',', '')  # Remove commas for non-negative numbers
                return pd.to_numeric(s, errors='coerce')  # Convert to numeric, handle errors as you wish
        return s  