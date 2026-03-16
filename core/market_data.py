import requests
import pandas as pd

class MarketDataFetcher:
    def __init__(self, binance_api_url, alpha_vantage_api_key):
        self.binance_api_url = binance_api_url
        self.alpha_vantage_api_key = alpha_vantage_api_key

    def fetch_binance_data(self, symbol):
        url = f'{self.binance_api_url}/api/v3/ticker/price?symbol={symbol}'
        response = requests.get(url)
        data = response.json()
        return {'symbol': data['symbol'], 'price': data['price'], 'exchange': 'Binance'}

    def fetch_alpha_vantage_data(self, symbol):
        url = f'https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol={symbol[:3]}&to_symbol={symbol[3:]}&interval=1min&apikey={self.alpha_vantage_api_key}'
        response = requests.get(url)
        data = response.json()
        latest_time = list(data['Time Series FX (1min)'].keys())[0]
        price = data['Time Series FX (1min)'][latest_time]['1. open']
        return {'symbol': symbol, 'price': price, 'exchange': 'Alpha Vantage'}

    def get_market_data(self, pairs):
        market_data = []
        for pair in pairs:
            if pair in ['XAUUSD', 'EURUSD', 'BTCUSD', 'ETHUSD']:
                if pair in ['XAUUSD', 'EURUSD']:
                    data = self.fetch_alpha_vantage_data(pair)
                else:
                    data = self.fetch_binance_data(pair)
                market_data.append(data)
        return pd.DataFrame(market_data)

# Example usage
if __name__ == '__main__':
    binance_api_url = 'https://api.binance.com'
    alpha_vantage_api_key = 'YOUR_ALPHA_VANTAGE_API_KEY'
    fetcher = MarketDataFetcher(binance_api_url, alpha_vantage_api_key)
    pairs = ['XAUUSD', 'EURUSD', 'BTCUSD', 'ETHUSD']
    market_data_df = fetcher.get_market_data(pairs)
    print(market_data_df)