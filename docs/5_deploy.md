# Deploy

- [Deploy](#deploy)
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
