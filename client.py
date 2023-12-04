from polygon import RESTClient
import config
import json
from typing import cast
from urllib3 import HTTPResponse
from plotly import graph_objects as graph
import pandas as pd
import numpy as np

client = RESTClient(config.API_KEY)

aggs = cast(
    HTTPResponse,
    client.get_aggs(
        'AAPL',
        1,
        "day",
        "2023-01-01",
        "2023-03-01",
        raw=True
    )
)
data = json.loads(aggs.data)
results = data.get('results', [])
close_list = [bar['c'] for bar in results]
open_list = [bar['o'] for bar in results]
high_list = [bar['h'] for bar in results]
low_list = [bar['l'] for bar in results]
date_list = [bar['t'] for bar in results]

date_list = [pd.to_datetime(date, unit='ms', origin='unix').strftime('%Y-%m-%d') for date in date_list]


df = pd.DataFrame({
    "Date": date_list,
    'Open': open_list,
    'High': high_list,
    'Low': low_list,
    'Close': close_list
})
pd.set_option('display.max_rows', None)
print(df)

