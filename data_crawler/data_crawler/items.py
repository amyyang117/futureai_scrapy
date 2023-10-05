# items
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UniformCrawlerItem(scrapy.Item):
    date = scrapy.Field()
    parse_date = scrapy.Field()
    status = scrapy.Field()
    table = scrapy.Field()
    items = scrapy.Field()

    def keys(self):
        return ['date', 'parse_date', 'status', 'table', 'items']

class RevenueCrawlerItem(scrapy.Item):
    code = scrapy.Field()
    revenue = scrapy.Field()
    mom = scrapy.Field()
    yoy = scrapy.Field()
    cum_revenue = scrapy.Field()
    cum_yoy = scrapy.Field()
    note = scrapy.Field()


class InfoCrawlerItem(scrapy.Item):
    code = scrapy.Field()

class FundamentalCrawlerItem(scrapy.Item):
    code = scrapy.Field()
    gross_margin = scrapy.Field()
    operating_margin = scrapy.Field()
    ebt_margin = scrapy.Field()
    net_income_margin = scrapy.Field()

class FinancialStatementCrawlerItem(scrapy.Item):
    symbol = scrapy.Field()
    cash_and_cash_equivalents = scrapy.Field()
    accounts_receivable_net = scrapy.Field()
    current_inventories = scrapy.Field()
    total_current_assets = scrapy.Field()
    property_plant_and_equipment = scrapy.Field()
    total_non_current_assets = scrapy.Field()
    total_assets = scrapy.Field()
    current_contract_liabilities = scrapy.Field()
    total_current_liabilities = scrapy.Field()
    total_non_current_liabilities = scrapy.Field()
    total_liabilities = scrapy.Field()
    total_share_capital = scrapy.Field()
    total_capital_surplus = scrapy.Field()
    total_operating_revenue = scrapy.Field()
    total_operating_costs = scrapy.Field()
    gross_profit_loss_from_operations = scrapy.Field()
    selling_expenses = scrapy.Field()
    administrative_expenses = scrapy.Field()
    research_and_development_expenses = scrapy.Field()
    net_operating_income_loss = scrapy.Field()
    total_interest_income = scrapy.Field()
    foreign_exchange_gains = scrapy.Field()
    foreign_exchange_losses = scrapy.Field()
    total_non_operating_income_and_expenses = scrapy.Field()
    profit_loss_from_continuing_operations_before_tax = scrapy.Field()
    profit_loss_from_continuing_operations = scrapy.Field()
    profit_loss = scrapy.Field()
    total_comprehensive_income = scrapy.Field()
    comprehensive_income_attributable_to_owners_of_parent = scrapy.Field()
    total_basic_earnings_per_share = scrapy.Field()
    profit_loss_before_tax = scrapy.Field()
    depreciation_expense = scrapy.Field()
    amortization_expense = scrapy.Field()
    net_cash_flows_from_used_in_operating_activities = scrapy.Field()
    net_cash_flows_from_used_in_investing_activities = scrapy.Field()
    net_cash_flows_from_used_in_financing_activities = scrapy.Field()
    net_increase_decrease_in_cash_and_cash_equivalents = scrapy.Field()
