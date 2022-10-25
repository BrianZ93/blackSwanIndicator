from calendar import month
import yfinance as yf
import datetime

# Creating Ticker Object
uvxy = yf.Ticker('UVXY')

# Downloading Historical Price Data
data = yf.download("UVXY", start="2012-01-01", end="2022-10-23")

# Creating the List of Prices
uvxy_historical_prices = dict()
for index, row in data.iterrows():
    date = (datetime.datetime(index.year, index.month, index.day)).strftime("%x")
    uvxy_historical_prices[date] = row['Close']

# Calculating the daily returns - All data points used
uvxy_historical_daily_returns = []
current = 1
previous = 1
for date in uvxy_historical_prices:
    previous = current 
    current = uvxy_historical_prices[date]
    
    uvxy_historical_daily_returns.append(((current - previous)/previous)*100)

uvxy_historical_daily_returns.pop(0)

daily_average = sum(uvxy_historical_daily_returns) / len(uvxy_historical_daily_returns)

# Calculating the weekly returns - every 7 data points
uvxy_historical_weekly_returns = []
current = 1
previous = 1
index = 0
for date in uvxy_historical_prices.values():
    if index == 6:
        index = 0

        previous = current
        current = date

        uvxy_historical_weekly_returns.append(((current - previous)/previous)*100)
    else:
        index += 1

uvxy_historical_weekly_returns.pop(0)

weekly_average = sum(uvxy_historical_weekly_returns) / len(uvxy_historical_weekly_returns)



# Calculating the monthly returns - checking for a change in month before adding another data point
uvxy_historical_monthly_returns = []
current = 1
previous = 1
last_month_used = ''
for date in uvxy_historical_prices:
    if last_month_used == date[:2]:
        continue
    else:
        last_month_used = date[:2]

        previous = current
        current = uvxy_historical_prices[date]

        uvxy_historical_monthly_returns.append(((current - previous)/ previous)*100)

uvxy_historical_monthly_returns.pop(0)

monthly_average = sum(uvxy_historical_monthly_returns) / len(uvxy_historical_monthly_returns)

print("daily", daily_average)
print("weekly", weekly_average)
print("monthly", monthly_average)

# Next step is to get VIX data and calculate contango (the decay of the fund relative to the index it intends to mimic)








