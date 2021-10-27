# Scripts

- [Scripts](#scripts)
  - [Intro](#intro)
  - [Run Coin Prices](#run-coin-prices)
  - [Run Update Current Prices](#run-update-current-prices)
  - [Secrets](#secrets)

## Intro

We also have scripts that must necessarily be run by our project.  Current examples of these are:

- [coin prices](../scripts/coin_prices.py)
  - scraping of the current coin prices
- [update current prices](../scripts/update_current_prices.py)
  - update the current prices or coins in the table `current_prices`

These scripts are run using the docker file [here](../docker/Dockerfile-scripts).

All scripts are run in a python base image as a kubernetes [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/).  YAMLs can be found [here](../k8s/other/cronjobs/coin_prices.yml).

## Run Coin Prices

To apply the job on the prod cluster:

```bash
kubectl --context kubernetes-admin@perso -n bitbuyer apply -f k8s/other/cronjobs/coin_prices.yml
```

## Run Update Current Prices

To apply the job on the prod cluster:

```bash
kubectl --context kubernetes-admin@perso -n bitbuyer apply -f k8s/other/cronjobs/update_current_prices.yml
```

## Secrets

We require a secret to run the `coin_prices.py` script.  This can be created using:

```bash
kubectl create --context kubernetes-admin@perso -n bitbuyer secret generic coin-api-key --from-literal=COIN_API_KEY=???
```
