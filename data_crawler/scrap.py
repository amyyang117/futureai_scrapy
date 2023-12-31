import os
import pandas as pd
from io import StringIO

url = "https://storage.googleapis.com/symbol-config/tw_industry.json"


symbols = ["1215", "3293"]  # Add or import the list of symbols you want to scrape
year = 2023
quarter = 1

# Iterating over each symbol, year, and quarter
for symbol in symbols:
    
    cmd = f"scrapy crawl get_financial_statement -a symbol={symbol} -a year={year} -a quarter={quarter}"
    
    # Execute the command via the operating system
    os.system(cmd)
