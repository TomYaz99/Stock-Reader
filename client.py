from polygon import RESTClient
import config
import json
from typing import cast
from urllib3 import HTTPResponse
import pandas as pd
import plotly.graph_objects as go

class StockDataFetcher:
    def __init__(self, api_key, symbol):
        self.client = RESTClient(api_key)
        self.symbol = symbol

    def fetch_data(self, start_date, end_date):
        aggs = cast(
            HTTPResponse,
            self.client.get_aggs(
                self.symbol,
                1,
                "day",
                start_date,
                end_date,
                raw=True
            )
        )
        data = json.loads(aggs.data)
        return data.get('results', [])

    def process_data(self, data, value_type):
        value_list = [bar[value_type] for bar in data]
        date_list = [bar['t'] for bar in data]
        date_list = [pd.to_datetime(date, unit='ms', origin='unix').strftime('%Y-%m-%d') for date in date_list]
        return pd.DataFrame({
            "Date": date_list,
            value_type.capitalize(): value_list
        })

    def get_open_values(self, start_date, end_date):
        data = self.fetch_data(start_date, end_date)
        return self.process_data(data, 'o')

    def get_high_values(self, start_date, end_date):
        data = self.fetch_data(start_date, end_date)
        return self.process_data(data, 'h')

    def get_low_values(self, start_date, end_date):
        data = self.fetch_data(start_date, end_date)
        return self.process_data(data, 'l')

    def get_close_values(self, start_date, end_date):
        data = self.fetch_data(start_date, end_date)
        return self.process_data(data, 'c')


    def get_candlestick_graph(self, start_date, end_date):

        data = self.fetch_data(start_date, end_date)
        
        fig = go.Figure(data=[go.Candlestick(
            x=[pd.to_datetime(bar['t'], unit='ms', origin='unix').strftime('%Y-%m-%d') for bar in data],
            open=[bar['o'] for bar in data],
            high=[bar['h'] for bar in data],
            low=[bar['l'] for bar in data],
            close=[bar['c'] for bar in data]
        )])

        fig.update_layout(
            title=f'Candlestick Chart for {self.symbol} from {start_date} to {end_date}',
            xaxis_title='Date',
            yaxis_title='Price',
            xaxis_rangeslider_visible=False
        )
        fig.show()


# Usage example
fetcher = StockDataFetcher(config.API_KEY, 'AAPL')
fetcher.get_candlestick_graph("2023-01-01", "2023-03-01")


