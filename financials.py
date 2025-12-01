import pandas as pd
import yfinance as yf 
import numpy as np

my_tickers = pd.read_csv("data/input/constituents.csv")[:200]

tickers_list = my_tickers['Symbol'].tolist()
#convert 
tickers_list = [yf.Ticker(ticker) for ticker in tickers_list]

def company_data(tickers_list):
    row_data = []

    for ticker in tickers_list:

        try:
            info = ticker.info
            finance = ticker.financials
            balance = ticker.balance_sheet

            # Fetch last 3 years
            def last_three(df, metric):
                #most data for 2025 is not available
                allowed = {2024,2023,2022} 
                if df is None or metric not in df.index:
                    return[]
                
                #sort
                cols = sorted(df.columns, reverse=True)

                results = []
                for col in cols[:3]:
                    year = col.year
                    if year not in allowed:
                        continue
                    val = df.loc[metric, col]
                    results.append((year, val / 1e6 if val is not None else None))

                    if len(results) == 3:
                        break
                return results
            
            rev_yrs = last_three(finance, "Total Revenue")
            net_yrs = last_three(finance, "Net Income")
            assets_yrs = last_three(balance, "Total Assets")
                


            row ={
                "Ticker":info.get("symbol"),
                "Company name": info.get("shortName") or info.get("longName"),
                "Country":info.get("country"),
                "Industry":info.get("industry"),
                "Revenue unit": info.get("currency"),
                "Market Cap (millions)":info.get("marketCap")/ 1e6 if info.get("marketCap") is not None else None
            }

            for year, value in rev_yrs:
                row[f"Revenue_{year} (millions)"] = value

            for year, value in net_yrs:
                row[f"NetIncome_{year} (millions)"] = value

            for year, value in assets_yrs:
                row[f"TotalAssets_{year} (millions)"] = value

            row_data.append(row) 

        except Exception as e:
            print(f"error processing ticker{ticker}")
        
            row_data.append({
            "Ticker":info.get("symbol"),
            "Company name": None,
            "Country":None,
            "Industry":None,
            "Revenue unit":None,
            "Revenue_Y1 (millions)":None,"Revenue_Y2 (millions)": None, "Revenue_Y3 (millions)": None,
            "Net Income_Y1 (millions)": None,"NetIncome_Y2 (millions)": None, "NetIncome_Y3 (millions)": None,
            "Total Assets_Y1 (millions)": None, "TotalAssets_Y2 (millions)": None, "TotalAssets_Y3 (millions)": None,
            "Market Cap":None
        })

    my_data = pd.DataFrame(row_data)
    #round up for readabilityu
    numeric_cols = [c for c in my_data.columns if "millions" in c]
    my_data[numeric_cols] = my_data[numeric_cols].astype(float).round(2)


    return my_data

my_data = company_data(tickers_list)

#save file
my_data.to_csv("data/Case_study_output.csv", index=False)
print("Saved data to my_data.csv")


    