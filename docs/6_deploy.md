# Deploy

- [Deploy](#deploy)
  - [TLS certificate](#tls-certificate)
  - [Run deploy](#run-deploy)
    - [create secrets](#create-secrets)
    - [run kustomize](#run-kustomize)
  - [Deploying angular in prod](#deploying-angular-in-prod)
    - [Dev](#dev)
    - [Prod](#prod)

There are a few stages for deployment:

- create secrets on server
- create pv
- variabalize pv
- create kustomize overlay
- update run.sh
- go

## TLS certificate

We only use a TLS cert in prod.

Install cert-manager:

```bash
# https://cert-manager.io/docs/installation/
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.5.3/cert-manager.yaml
```

The first stage is to get a cert.  We do this using [cert-manager](https://cert-manager.io/), which uses [let's encrypt](https://letsencrypt.org/) as a CA.  Following the guide [here](https://medium.com/flant-com/cert-manager-lets-encrypt-ssl-certs-for-kubernetes-7642e463bbce), we just need to:

```bash
kubectl --context kubernetes-admin@perso -n bitbuyer apply -f k8s/other/cert.yml
```

This will create the secret used in tls here: `kubectl get --context kubernetes-admin@perso -n bitbuyer secret tls-secret`

## Run deploy

### create secrets

You first need to create two secrets: `postgres-auth` & `django-secret-key`, this can be done by applying :

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-auth
type: Opaque
stringData:
  POSTGRES_USER: super-secret
  POSTGRES_PASSWORD: super-secret
---
apiVersion: v1
kind: Secret
metadata:
  name: django-secret-key
type: Opaque
stringData:
  SECRET_KEY: super-secret
```

Then applying the yaml using :

```bash
kubectl --context kubernetes-admin@perso -n bitbuyer apply -f k8s/secrets.prod.yml
```

### run kustomize

Apply the kustomize yamls :

```bash
kubectl --context kubernetes-admin@perso -n bitbuyer apply -k ./k8s/overlays/prod/
```

## Deploying angular in prod

We run a dev server when developing in tilt, but this isn't the one for prod.

In prod we should:

- build the project (builds the project in `dist/`)
- load the dist folder into an nginx image to deploy

This has some important implications in the difference between dev and prod environments.

### Dev

The dev environment will not really be touched, we will deploy a **pod with a node image** with a container running `ng serve`.

### Prod

In prod we will need to build, then deploy.

This implies that we will need different tage for the dockerhub image repo:

- dev
  - will be a node image
  - will contain all code
  - runs using `npm run start` which runs `ng serve --host 0.0.0.0 --disable-host-check --port 8080 --live-reload --watch`
- latest
  - will be an nginx image
  - contain only a fraction of the code (from `./dist`)
  - runs using `npm run build` which runs `ng build --configuration production`
