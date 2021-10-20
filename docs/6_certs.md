# Cert-manager / Let's encrypt

We only use a TLS cert in prod.

Install cert-manager:

```bash
# https://cert-manager.io/docs/installation/
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.5.3/cert-manager.yaml
```

The first stage is to get a cert.  We do this using [cert-manager](https://cert-manager.io/), which uses [let's encrypt](https://letsencrypt.org/) as a CA.  Following the guide [here](https://medium.com/flant-com/cert-manager-lets-encrypt-ssl-certs-for-kubernetes-7642e463bbce), we just need to:

```bash
kubectl --context kubernetes-admin@perso -n bitbuyer apply -f certs/cert.yml
```

This will create the secret used in tls here: `kubectl get --context kubernetes-admin@perso -n bitbuyer secret tls-secret`
