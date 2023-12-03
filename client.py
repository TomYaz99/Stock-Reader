from polygon import RESTClient
import config
import json
from typing import cast
from urllib3 import HTTPResponse
client = RESTClient(config.API_KEY)

aggs = cast(
    HTTPResponse,
    client.get_aggs(
        'AAPL',
        1,
        "day",
        "2023-01-01",
        "2023-03-01",
        raw = True
    ),

)

data = json.loads(aggs.data)

print(data)






