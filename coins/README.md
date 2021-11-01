# Coins

The Coins app deals with all aspects of getting prices for cryptos.

Currently the only data sources are:

- [coinAPI](https://www.coinapi.io/)
  - for all historical coin price data
  - populates tables:
    - CoinPrices
    - CurrentPrices
- [coin base](https://www.coinbase.com/)
  - for descriptions etc of coins
  - populates tables:
    - Coins
