CREATE TABLE monthly_revenue_instant (
    date DATE NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    revenue INTEGER NOT NULL,
    last_year_revenue INTEGER,
    difference INTEGER,
    YoY FLOAT,
    cum_revenue INTEGER,
    cum_last_year INTEGER,
    cum_difference INTEGER,
    cum_YoY FLOAT,
    note VARCHAR
)