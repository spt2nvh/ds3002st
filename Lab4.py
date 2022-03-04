import sys
import requests

stock_arg = sys.argv[1]
stocks = stock_arg.split(',')
url = "https://yfapi.net/v6/finance/quote"
headers = {
    'x-api-key': "AjlcDa005ulssxOoyXKs2r65aAbYWRo9PSZQzv12"
    }
for stock in stocks:
    querystring = {"symbols": stock}
    response = requests.request("GET", url, headers=headers, params=querystring)

    stock_json = response.json()
    if (stock_json['quoteResponse']['result'] == []):
        print("Unable to find stock:", stock, "in yahoo finance api")
        continue
    name = stock_json['quoteResponse']['result'][0]['longName']
    value = stock_json['quoteResponse']['result'][0]['regularMarketPrice']
    print(str(name) + ": " + str(value))
    print("*************************")













