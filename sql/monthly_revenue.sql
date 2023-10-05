CREATE TABLE monthly_revenue (
    date DATE NOT NULL,
    code VARCHAR(10) NOT NULL,
    revenue INTEGER NOT NULL,
    MoM FLOAT,
    YoY FLOAT,
    cum_revenue INTEGER NOT NULL,
    cum_YoY FLOAT,
    note VARCHAR
)