# Roadmap

- [Roadmap](#roadmap)
  - [Setup dev env](#setup-dev-env)
  - [Add API List view](#add-api-list-view)
  - [coin prices](#coin-prices)
  - [frontend](#frontend)
  - [deploy](#deploy)
  - [automate scraping](#automate-scraping)
  - [detail view](#detail-view)
  - [display aggregated tweets](#display-aggregated-tweets)
  - [store individual tweets for sentiment analysis](#store-individual-tweets-for-sentiment-analysis)
  - [sentiment analysis on tweets](#sentiment-analysis-on-tweets)
  - [data analysis on coins](#data-analysis-on-coins)
  - [homepage](#homepage)

## Setup dev env

Set up a local development environment in which we'll deploy the app.  We should deploy an ephemeral database, with a table structure as outlined in the [technical implications](./1_technical_implications.md).  This should allow us to recreate the database from scratch, and reset it, ready to store data from our scripts.

As we're developping in k8s, we'll need a techno to act as a volume for develoment, allowing live reloading: Tilt.

## Add API List view

We can now scrape data or a list of coins.  this can be done from any of the existing websites.  Take the top 100 (with API limits we won't be able to scrape much more than this anyway).

Deploy a django REST server in dev, and integrate this into Tilt.

Scripts can be run to populate the db independantly of django.

## coin prices

The next data to collect is from CoinAPI.  Create a script that stores daily coin prices in the db.

Create an endpoint in django with a list view to display minimal data about the coins (name, abbreviation etc.)

## frontend

Add angular to the project.  First port of call is to create a front end for the list view that we just created in the [coin prices](#coin-prices) feature

## deploy

Time to make the project public.  Create a k8s cluster on OVH.  Site should be deployed on [bitbuyer.tom-preston.co.uk](https://bitbuyer.tom-preston.co.uk).

## automate scraping

The scripts that we created for making api calls should now be automated.  We had to wait until we had a production db in place(which we made in the [deploy](#deploy) feature.

## detail view

We have enough data for a detail view.  Create that now.

## display aggregated tweets

Scrape the data for total tweets per coin, store this in the db.

This can be displayed in the front end as per the wireframes.

## store individual tweets for sentiment analysis

create a script to query the sentiment analysis api/model.  Store the result in the database, we can use this in combination with the tweet volume info.

## sentiment analysis on tweets

run sentiment analysis on the tweets, labaling them positive, negative, neutral.  store this in the db

## data analysis on coins

Run data analysis on the best known coins.  Clearly there will be a lot of heterogeneity between the coins behaviours, so stick to the best known, as they should be in theory the most likely to follow twitter news.

## homepage

If we've gotten this far, the site deserves a landing page.
