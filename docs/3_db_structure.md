# Technical implications

The stack:

- Postgres DB
  - place to store prices
  - place to store tweets
  - sentiment analysis
- K3s
  - for dev
- Django
  - the backend
- Angular
  - the frontend

## Database Schema

```sql
drop table if exists twitter_users cascade;
drop table if exists tweets cascade;
drop table if exists coin_prices cascade;
drop table if exists tweet_sentiment cascade;
drop table if exists coins cascade;

create table twitter_users
(
    author integer PRIMARY KEY,
    name varchar(255),
    username varchar(255),
    description varchar(1023)
);

create table tweets
(
    id varchar(31),
    author_id integer,
    created_at TIMESTAMPTZ,
    text_ varchar(511),
    PRIMARY KEY(id),
    constraint fk_twitter_users
        foreign key(author_id)
            references twitter_users(author)
                on delete cascade
);

create table tweet_sentiment
(
    id serial,
    tweet_id varchar(31),
    verdict json,
    source varchar(63),
    version varchar(63),
    created_at timestamptz,
    constraint fk_tweet_id
        foreign key(tweet_id)
            references tweets(id)
                on delete cascade
);

create table coins
(
    id serial primary key,
    name varchar(31),
    abbreviation varchar(7),
    description varchar(511)
);

create table coin_prices
(
  id serial primary key,
  coin_id integer,
  rate_close double precision,
  rate_high double precision,
  rate_low double precision,
  rate_open double precision,
  time_close timestamptz,
  time_open timestamptz,
  time_period_end timestamptz,
  time_period_start timestamptz,
  constraint fk_coins
      foreign key(coin_id)
          references coins(id)
              on delete cascade
);

insert into twitter_users (author, name, username, description)
values (123, 'tom', 'usertom', 'champion')

insert into tweets (id, author_id, text_)
values ('1', 123, 'tweet1'), ('2', 123, 'tweet2')

insert into tweet_sentiment (tweet_id, verdict, source, version)
values 
('1', '{}', 'test', '1.1.1'),
('1', '{}', 'test', '1.1.2'),
('2', '{}', 'test', '1.1.1'),
('2', '{}', 'test', '1.1.2')

select *
from tweets

select *
from twitter_users

select *
from tweet_sentiment

select *
from twitter_users tu
  left join tweets tw on tw.author_id = tu.author 
```
