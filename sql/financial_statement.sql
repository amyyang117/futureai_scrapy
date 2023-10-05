CREATE TABLE financial_statement(
    reporting_period VARCHAR(10) NOT NULL
    ,symbol VARCHAR(10) NOT NULL
    ,cash_and_cash_equivalents FLOAT
    ,accounts_receivable_net FLOAT
    ,current_inventories FLOAT
    ,total_current_assets FLOAT
    ,property_plant_and_equipment FLOAT
    ,total_non_current_assets FLOAT
    ,total_assets FLOAT
    ,current_contract_liabilities FLOAT
    ,total_current_liabilities FLOAT
    ,total_non_current_liabilities FLOAT
    ,total_liabilities FLOAT
    ,total_share_capital FLOAT
    ,total_capital_surplus FLOAT
    ,total_operating_revenue FLOAT
    ,total_operating_costs FLOAT
    ,gross_profit_loss_from_operations FLOAT
    ,selling_expenses FLOAT
    ,administrative_expenses FLOAT
    ,research_and_development_expenses FLOAT
    ,net_operating_income_loss FLOAT
    ,total_interest_income FLOAT
    ,foreign_exchange_gains FLOAT
    ,foreign_exchange_losses FLOAT
    ,total_non_operating_income_and_expenses FLOAT
    ,profit_loss_from_continuing_operations_before_tax FLOAT
    ,profit_loss_from_continuing_operations FLOAT
    ,profit_loss FLOAT
    ,total_comprehensive_income FLOAT
    ,comprehensive_income_attributable_to_owners_of_parent FLOAT
    ,total_basic_earnings_per_share FLOAT
    ,profit_loss_before_tax FLOAT
    ,depreciation_expense FLOAT
    ,amortization_expense FLOAT
    ,net_cash_flows_from_used_in_operating_activities FLOAT
    ,net_cash_flows_from_used_in_investing_activities FLOAT
    ,net_cash_flows_from_used_in_financing_activities FLOAT
    ,net_increase_decrease_in_cash_and_cash_equivalents FLOAT

)
