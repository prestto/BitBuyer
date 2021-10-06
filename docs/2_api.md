# Private api

The api used by the front to talk to the back.

Exchange format:

| URL              | METHOD | response                                                                                                                  | params      |
| ---------------- | ------ | ------------------------------------------------------------------------------------------------------------------------- | ----------- |
| coins/           | GET    | {‘name’:’’,‘abbreviation’:’’,‘current_sentiment’:’’,‘price’:[{‘date’: ‘’, ‘value’: 1.29}, …], ‘price_change_today’: 0.29} |             |
| coins/<coin>     | GET    | {‘name’: ‘’, ‘abbreviation’: ‘’, ‘about’: ‘’}                                                                             |             |
| prices/<coin>    | GET    | {‘current_price’: ‘’, ‘change_period’: 2.79, ‘period’: ‘’, ‘historic’: [{‘date’: ‘’, price: ‘’}, …]}                      | period<week, month, all> |
| sentiment/<coin> | GET    | {‘current_sentiment’: ‘’, ‘change_period’: -1, ‘period’: ‘’, ‘historic’: [{‘date’: ‘’, price: ‘’}, …]}                    | period<week, month, all> |
