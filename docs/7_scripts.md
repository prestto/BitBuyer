# Scripts

- [Scripts](#scripts)
  - [Intro](#intro)
  - [Scheduling jobs on the cluster](#scheduling-jobs-on-the-cluster)
    - [Rebuild scripts](#rebuild-scripts)
    - [Run Coin Prices](#run-coin-prices)
    - [Run Update Current Prices](#run-update-current-prices)
    - [Run update Article Aggregates](#run-update-article-aggregates)
    - [Run a job manually (outside of cron)](#run-a-job-manually-outside-of-cron)
  - [Secrets](#secrets)

## Intro

We also have scripts that must necessarily be run by our project.  Current examples of these are:

- [coin prices](../scripts/coin_prices.py)
  - scraping of the current coin prices
- [update current prices](../scripts/update_current_prices.py)
  - update the current prices or coins in the table `current_prices`

These scripts are run using the docker file [here](../docker/Dockerfile-scripts).

All scripts are run in a python base image as a kubernetes [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/).  YAMLs can be found [here](../k8s/other/cronjobs/coin_prices.yml).

## Scheduling jobs on the cluster

To add a script and schedule it as a CronJob, we need to:

- Rebuild the `scripts` image with the new script
- schedule it on the prod cluster

### Rebuild scripts

```bash
# build Dockerfile
docker build -f docker/Dockerfile-scripts -t user632716/scripts:latest .

# push
docker push user632716/scripts:latest
```

### Run Coin Prices

To apply the job on the prod cluster:

```bash
kubectl --context kubernetes-admin@perso -n bitbuyer apply -f k8s/other/cronjobs/coin_prices.yml
```

### Run Update Current Prices

To apply the job on the prod cluster:

```bash
kubectl --context kubernetes-admin@perso -n bitbuyer apply -f k8s/other/cronjobs/update_current_prices.yml
```

### Run update Article Aggregates

To apply the job on the prod cluster:

```bash
kubectl --context kubernetes-admin@perso -n bitbuyer apply -f k8s/other/cronjobs/article_aggregates.yml
```

### Run a job manually (outside of cron)

```bash
kubectl --context kubernetes-admin@perso -n bitbuyer create job --from=cronjob/article-aggregates article-aggregates
```

## Secrets

We require a secret to run the `coin_prices.py` script.  This can be created using:

```bash
kubectl create --context kubernetes-admin@perso -n bitbuyer secret generic coin-api-key --from-literal=COIN_API_KEY=???
```
