# statista_case_study_financial_data_extraction
This project aims to extract financial data (KPIs)  alongside key metrics of S&amp;P 500 companies over the last three years.  

# Requirements 

import yfinance as yf

import pandas as pd

# Objective
Project aims to extract data from a public source. 4 KPIs are required to fulfill the necessary requirements. 

In my case: Net Income, Revenue, Market Capitalization and Total assets were among the data i extracted.

# Processing steps
- extract tickers from a data source - csv file downloaded from github
- Utilise yfinance
- Access metadata via ticker.info.
- Retrieve financial statements via: **ticker.financials and ticker.balance_sheet**
- A helper function extracts the most recent 3 years for a metric from a DataFrame.
- Adds the extracted metrics to a flat dictionary for easier analysis
- Collects all rows into a list.
- Converts the list into a pandas DataFrame.
- Round numeric types.
- Returns the final DataFrame.

# Error handling
If data retrieval for a ticker fails:
- The exception is logged to the console.
- The function inserts a row with **None** values for all financial metrics.

# Data Cleaning after extraction
- Empty rows droped.

# Output data
Features the following:
- Ticker symbol
- Company name
- Country
- Industry
- Currency for revenue
- Market capitalization (in millions)
- Total Revenue, Net Income, and Total Assets (in millions) for the last 3 years(2024,2023,2022)
     ## Returns a clean numeric-friendly DF with rounded values
