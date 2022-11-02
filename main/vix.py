import yfinance as yf
import datetime
import logging
from pylogrus import PyLogrus, TextFormatter



today = datetime.date.today()
today_string = str(today.year) + "-" + str(today.month) + "-" + str(today.day)
start_string = str(today.year - 10) + "-" + str(today.month) + "-" + str(today.day)

logging.setLoggerClass(PyLogrus)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = TextFormatter(datefmt='Z', colorize=True)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

# Creating Ticker Object
uvxy = yf.Ticker('UVXY')

# Downloading Historical Price Data
data = yf.download("UVXY", start=start_string, end=today_string)

# Creating the List of Prices
uvxy_prices = []
uvxy_dates = []
uvxy_historical_prices = dict()
for index, row in data.iterrows():
    date = (datetime.datetime(index.year, index.month, index.day)).strftime("%x")
    uvxy_historical_prices[date] = row['Close']
    uvxy_prices.append(row['Close'])
    uvxy_dates.append(date)


# *** DAILY AVERAGES ***
# Calculating the daily returns - All data points used

uvxy_historical_daily_returns = []
current = 1
previous = 1
index = 0
for date in uvxy_historical_prices:
    previous = current 
    current = uvxy_historical_prices[date]
    
    uvxy_historical_daily_returns.append(((current - previous)/previous)*100)

uvxy_historical_daily_returns.pop(0)

uvxy_daily_average = sum(uvxy_historical_daily_returns) / len(uvxy_historical_daily_returns)

uvxy_daily_average

# *** WEEKLY AVERAGES ***
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

uvxy_weekly_average = sum(uvxy_historical_weekly_returns) / len(uvxy_historical_weekly_returns)


# *** MONTHLY AVERAGES ***
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

uvxy_monthly_average = sum(uvxy_historical_monthly_returns) / len(uvxy_historical_monthly_returns)

# Next step is to get VIX data and calculate contango (the decay of the fund relative to the index it intends to mimic)

# Creating the VIX object
vix = yf.Ticker('^VIX')

# Downloading Historical Price Data
vix_data = yf.download("^VIX", start=start_string, end=today_string)

# Creating the List of Prices
vix_prices = []
vix_historical_prices = dict()
for index, row in vix_data.iterrows():
    date = (datetime.datetime(index.year, index.month, index.day)).strftime("%x")
    vix_historical_prices[date] = (row['Close'])
    vix_prices.append(row['Close'])

# *** DAILY AVERAGES ***
# Calculating the daily returns - All data points used
vix_historical_daily_returns = []
current = 1
previous = 1
for date in vix_historical_prices:
    previous = current 
    current = vix_historical_prices[date]
    
    vix_historical_daily_returns.append(((current - previous)/previous)*100)

vix_historical_daily_returns.pop(0)

vix_daily_average = sum(vix_historical_daily_returns) / len(vix_historical_daily_returns)

# *** WEEKLY AVERAGES ***
# Calculating the weekly returns - every 7 data points
vix_historical_weekly_returns = []
current = 1
previous = 1
index = 0
for date in vix_historical_prices.values():
    if index == 6:
        index = 0

        previous = current
        current = date

        vix_historical_weekly_returns.append(((current - previous)/previous)*100)
    else:
        index += 1

vix_historical_weekly_returns.pop(0)

vix_weekly_average = sum(vix_historical_weekly_returns) / len(vix_historical_weekly_returns)

# *** MONTHLY AVERAGES ***
# Calculating the monthly returns - checking for a change in month before adding another data point
vix_historical_monthly_returns = []
current = 1
previous = 1
last_month_used = ''
for date in vix_historical_prices:
    if last_month_used == date[:2]:
        continue
    else:
        last_month_used = date[:2]

        previous = current
        current = vix_historical_prices[date]

        vix_historical_monthly_returns.append(((current - previous)/ previous)*100)

vix_historical_monthly_returns.pop(0)

vix_monthly_average = sum(vix_historical_monthly_returns) / len(vix_historical_monthly_returns)

# *** CALCULATING CONTANGO ***
historical_daily_difference = []

if len(vix_prices) == len(uvxy_prices):
    daily_contango_returns = []
    weekly_contango_returns = []
    monthly_contango_returns = []
    logger.info("Contango Calculation Running")
    for index in range(1, len(vix_prices)):
        # Daily Contango
        uvxy_daily_change = (uvxy_prices[index] - uvxy_prices[index - 1])/uvxy_prices[index - 1]
        vix_daily_change = (vix_prices[index] - vix_prices[index - 1])/vix_prices[index - 1]

        daily_contango_returns.append(uvxy_daily_change - vix_daily_change)


        # Weekly Contango
        if index % 6 == 0:
            uvxy_weekly_change = (uvxy_prices[index] - uvxy_prices[index - 6])/uvxy_prices[index - 6]
            vix_weekly_change = (vix_prices[index] - vix_prices[index - 6])/vix_prices[index - 6]

            weekly_contango_returns.append(uvxy_weekly_change - vix_weekly_change)

        # Monnthly Contango
        if index % 30 == 0:
            uvxy_monthly_change = (uvxy_prices[index] - uvxy_prices[index - 30])/uvxy_prices[index - 30]
            vix_monthly_change = (vix_prices[index] - vix_prices[index - 30])/vix_prices[index - 30]

            monthly_contango_returns.append(uvxy_monthly_change - vix_monthly_change)

    daily_contango = sum(daily_contango_returns) / len(daily_contango_returns)
    weekly_contango = sum(weekly_contango_returns) / len(weekly_contango_returns)
    monthly_contango = sum(monthly_contango_returns) / len(monthly_contango_returns)

    logger.info("Contango Successfully Calculated")
else:
    logger.error("Cannot run contango calculation if UVXY and VIX have a different number of data points, check dates used to make sure they match")

# Calculating SMA and EMA of UVXY

# 1 Year Time Period
# 30 day SMA/EMA
time_period = 365
SMA_30_DAY = []
EMA_30_DAY = []
smoothing_30_day = 2
prices_used_30_day = []
dates_used_30_day = []
weighting_30_day = smoothing_30_day/(30 + 1)

for price in range(len(uvxy_prices) - time_period - 30, len(uvxy_prices)):
    prices_used_30_day.append(uvxy_prices[price])

first_run = True
# SMA & EMA
for price in range(len(prices_used_30_day) - time_period - 30, len(prices_used_30_day)):
    i = len(prices_used_30_day) - price
    if len(prices_used_30_day[i - 30: i]) == 0:
        continue
    else:
        dates_used_30_day.append(uvxy_dates[len(uvxy_dates) - i + 30 - 1])
        SMA_30_DAY.append(sum(prices_used_30_day[i - 30: i])/30)
        if first_run == True:
            EMA_30_DAY.append(sum(prices_used_30_day[i - 30: i])/30)
            first_run = False
        else:
            EMA_30_DAY.append( (EMA_30_DAY[-1] * (1 - weighting_30_day)) + (prices_used_30_day[i] * weighting_30_day) )

# 5 day SMA/EMA
time_period = 365
SMA_5_DAY = []
EMA_5_DAY = []
smoothing_5_day = 2
prices_used_5_day = []
dates_used_5_day = []
weighting_5_day = smoothing_5_day/(5 + 1)

for price in range(len(uvxy_prices) - time_period - 5, len(uvxy_prices)):
    prices_used_5_day.append(uvxy_prices[price])

first_run = True
# SMA & EMA
for price in range(len(prices_used_5_day) - time_period - 5, len(prices_used_5_day)):
    i = len(prices_used_5_day) - price
    if len(prices_used_5_day[i - 5: i]) == 0:
        continue
    else:
        dates_used_5_day.append(uvxy_dates[len(uvxy_dates) - i + 5 - 1])
        SMA_5_DAY.append(sum(prices_used_5_day[i - 5: i])/5)
        if first_run == True:
            EMA_5_DAY.append(sum(prices_used_5_day[i - 5: i])/5)
            first_run = False
        else:
            EMA_5_DAY.append( (EMA_5_DAY[-1] * (1 - weighting_5_day)) + (prices_used_5_day[i] * weighting_5_day) )


# 30 Day MACD
MACD_dates_30_Day = []
Buy_Sell_Toggle_30_Day = False
for x in range(0, len(SMA_30_DAY)):
    if SMA_30_DAY[x] > EMA_30_DAY[x]:
        if Buy_Sell_Toggle_30_Day == False:
            Buy_Sell_Toggle_30_Day = True
            logger.info('30 Day MACD BUY/SELL Triggered' + ' ' + str(x))
            MACD_dates_30_Day.append(dates_used_30_day[x])

    else:
        if Buy_Sell_Toggle_30_Day == True:
            Buy_Sell_Toggle_30_Day = False
            logger.info('30 Day MACD BUY/SELL Triggered' + ' ' + str(x))
            MACD_dates_30_Day.append(dates_used_30_day[x])

# 5 day MACD
MACD_dates_5_Day = []
Buy_Sell_Toggle_5_Day = False
for x in range(0, len(SMA_5_DAY)):
    if SMA_5_DAY[x] > EMA_5_DAY[x]:
        if Buy_Sell_Toggle_5_Day == False:
            Buy_Sell_Toggle_5_Day = True
            logger.info('5 Day MACD BUY/SELL Triggered' + ' ' + str(x))
            MACD_dates_5_Day.append(dates_used_5_day[x])

    else:
        if Buy_Sell_Toggle_5_Day == True:
            Buy_Sell_Toggle_5_Day = False
            logger.info('5 Day MACD BUY/SELL Triggered' + ' ' + str(x))
            MACD_dates_5_Day.append(dates_used_5_day[x]) 


# Data flow to main.py
def getContango():
    return [daily_contango, weekly_contango, monthly_contango]

def getUVXYAverages():
    return [uvxy_daily_average, uvxy_weekly_average, uvxy_monthly_average]

def getSMA():
    return SMA_5_DAY

def getEMA():
    return EMA_5_DAY

