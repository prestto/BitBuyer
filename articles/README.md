# Articles

Articles refers to news stories about one or more crypto currences.

The project is mainly concerned with twitter stories at present.

The articles can be broken down into 2 sections:

- aggregated article numbers
- article sentiment analysis

## Aggregated Article Numbers

Hourly totals of articles from sources.

### Aggregated Models

Database tables to store aggregates:

- `article_aggregates`
  - counts of articles published within a timeframe of 1hr.
  - columns:
    - start_time
    - end_time
    - total
- `platforms`
  - lookup table with platforms on which articles are published ie. twitter, bbc...
  - columns:
    - id
    - platform
    - impact

## Article Sentiment Analysis

Sentiment analysis on articles from a subsection of sources.

### Article Models

- `article_source`
  - the account publishing the article
  - columns:
    - id
    - tag
    - platform
