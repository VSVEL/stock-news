import requests
from twilio.rest import Client
STOCK = "TSLA"
COMPANY_NAME = "Tesla"

account_sid = 'twilio sid'
account_auth = 'twilio auth token'

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_api = 'your stock api key'
stock_url = 'https://www.alphavantage.co/query'
stock_params = {
    'function' : 'TIME_SERIES_DAILY',
    'symbol' : STOCK,
    'apikey' : stock_api,
}
stock_response = requests.get(url=stock_url,params=stock_params)
stock_data = stock_response.json()
stock_daily_data = stock_data['Time Series (Daily)']
stock_daily_data_list = [value for (key,value) in stock_daily_data.items()]


yesterday_stock_data = stock_daily_data_list[0]
stock_closing_yesterday_price = float(yesterday_stock_data['4. close'])


day_before_yesterday_data = stock_daily_data_list[1]
stock_closing_day_before_yesterday_price = float(day_before_yesterday_data['4. close'])


diff_percentage = (stock_closing_yesterday_price-stock_closing_day_before_yesterday_price)/stock_closing_yesterday_price * 100

up_down = None
if diff_percentage > 0:
    up_down = '🔺'
else:
    up_down = '🔻'


# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
if abs(diff_percentage) > 0:
    news_api = 'your news api key'
    news_url = 'https://newsapi.org/v2/top-headlines'
    news_params = {
        'q': COMPANY_NAME,
        'language':'en',
        'apiKey': news_api
    }
    news_response = requests.get(url=news_url,params=news_params)
    news_data = news_response.json()
    news_articles = news_data['articles']
    three_articles = news_articles[:3]
    formatted_articles = []
    for article in three_articles:
        formatted_articles.append(f"{STOCK}:{up_down}{round(diff_percentage,3)}% \n\n Title:{article['title']} \n\n Description:{article['description']} \n\n To read more about click on:{article['url']}")


# STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.

    client = Client(account_sid, account_auth)

    for article in formatted_articles:
        message = client.messages \
            .create(
            body=article,
            from_='twilio number',
            to='your number'
        )


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

