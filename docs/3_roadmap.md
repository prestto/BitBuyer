# Roadmap

## Jumble

- setup tilt
- setup postgres database
  - dockerized postgres database
  - deployed on k3s
  - no seeded data
  - persistent, lifecycle independant from app
  - reset functionality
- create schema for prices
  - `coins` table
    - create table
    - determine list of coins to focus on
    - fill table
    - add seeding script
  - `coin_prices` table
    - create table
    - make dump to tsv script
    - add seeding script
- scrape prices
  - script to fill the table `coin_prices`
  - dockerize script
  - push image to dockerhub
- create schema for tweets
  - create `twitter_users` & `tweets` tables
  - make dump to tsv script
  - add seeding script
- scrape tweets
  - script to grab tweets / tweeters
- setup webserver hello world
- list view
- detail view
- api documentation (swagger)
