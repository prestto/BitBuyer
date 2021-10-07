# API Snippets

Minimal working snippets for API calls.

- [API Snippets](#api-snippets)
  - [CoinPriceAPI](#coinpriceapi)
  - [Twitter API](#twitter-api)

## CoinPriceAPI

- [Bit coin prices](https://www.coinapi.io/)
  - 100 requests per day, but time series info available upto 100000

```python
import requests
import json
from pprint import pprint
import os
frrom sys import exit

asset_id_base='BTC'
asset_id_quote='USD'
period="1HRS"
time_start="2016-01-01T00:00:00"
time_end="2017-08-09T14:31:18.3150000Z"
limit=100000

url = f'https://rest.coinapi.io/v1/exchangerate/{asset_id_base}/{asset_id_quote}/history?period_id={period}&time_start={time_start}&time_end={time_end}&limit={limit}'

COIN_API_KEY=os.environ.get('COIN_API_KEY', None)

if not COIN_API_KEY:
    print('No API key found in .env)
    exit(1)

headers = {
    'X-CoinAPI-Key' : COIN_API_KEY
}
response = requests.get(url, headers=headers)
response_dict = json.loads(response.text)
pprint(response_dict[0])
```

Response:

```json
{
    "rate_close": 430.83162967280316,
    "rate_high": 432.0797235201113,
    "rate_low": 430.1742451974526,
    "rate_open": 432.03987993229157,
    "time_close": "2016-01-01T00:59:00.0000000Z",
    "time_open": "2016-01-01T00:09:00.0000000Z",
    "time_period_end": "2016-01-01T01:00:00.0000000Z",
    "time_period_start": "2016-01-01T00:00:00.0000000Z"
}
```

## Twitter API

- [Twitter API](https://developer.twitter.com/en)
  - [Search Tweets Endpoint](https://developer.twitter.com/en/docs/twitter-api/tweets/search/quick-start/recent-search)
  - [User Tweets Endpoint](https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-tweets)

```python
import requests
import os
import json
from datetime import datetime, timedelta, timezone

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN", None)

search_url = "https://api.twitter.com/2/tweets/search/recent"

start_datetime = datetime.now(timezone.utc) - timedelta(minutes=60)
end_datetime = datetime.now(timezone.utc) - timedelta(minutes=30)

def format_dt(dt: datetime) -> str:
    return dt.isoformat()

# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {
    'query': '#cryptocurrency OR #crypto',
    'max_results': 10,
    'tweet.fields': 'created_at',
    'expansions': 'author_id',
    'user.fields': 'description',
    'start_time': format_dt(start_datetime),
    'end_time': format_dt(end_datetimit API requires to help prevent CSRF. Modhashes can be obtained via the /api/me.json call or in response data of listing endpoints.

The preferred way to send a modhash is to include an X-Modhash custom HTTP header with your requests.

Modhashes are not required when authenticated with OAuth.
fullnamese)
}

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

json_response = connect_to_endpoint(search_url, query_params)
print(json.dumps(json_response, indent=4, sort_keys=True))
```