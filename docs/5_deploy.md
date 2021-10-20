# Deploy

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
