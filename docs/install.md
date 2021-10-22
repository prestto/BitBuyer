# Install

This doc is separated into 2 parts, [Dev dependencies](#dev-dependencies) and [Additional dev tools](#additional-dev-tools).  Note that if you just want to run the project in local **you only need the dev dependencies**.

## Contents

- [Install](#install)
  - [Contents](#contents)
  - [Dev dependencies](#dev-dependencies)
    - [Minikube](#minikube)
    - [Kubectl](#kubectl)
    - [Tilt](#tilt)
    - [Docker](#docker)
  - [Additional dev tools](#additional-dev-tools)
    - [Pipenv](#pipenv)
    - [K9s](#k9s)
    - [Angular](#angular)
    - [Python](#python)
    - [Node](#node)

## Dev dependencies

The following dependencies are required to run the project in local:

- [minikube](https://minikube.sigs.k8s.io/docs/start/)
- [Kubectl](https://v1-18.docs.kubernetes.io/docs/tasks/tools/install-kubectl/)
- [Tilt](https://tilt.dev/)
- [Docker](https://www.docker.com/)

### Minikube

The official [install doc](https://minikube.sigs.k8s.io/docs/start/) can be found [here](https://minikube.sigs.k8s.io/docs/start/).

OVH uses k8s `v1.20.2`, thus we need to mimic this in dev.

```bash
# install
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# start
minikube start --kubernetes-version=v1.20.2
```

### Kubectl

The official [install doc](https://v1-18.docs.kubernetes.io/docs/tasks/tools/install-kubectl/) can be found [here](https://v1-18.docs.kubernetes.io/docs/tasks/tools/install-kubectl/).

```bash
# Install version: 
curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.20.11/bin/linux/amd64/kubectl

# make ezxecutable
chmod +x ./kubectl

# move to bin
sudo mv ./kubectl /usr/local/bin/kubectl

# test
kubectl version --client
```

### Tilt

The official [install doc](https://docs.tilt.dev/install.html#linux) can be found [here](https://docs.tilt.dev/install.html#linux).

```bash
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
```

### Docker

The official [install doc](https://docs.docker.com/engine/install/ubuntu/) can be found [here](https://docs.docker.com/engine/install/ubuntu/).

```bash
# uninstall preexisting
sudo apt remove -y docker docker-engine docker.io docker-compose golang-docker-credential-helpers containerd runc
sudo apt autoremove -y
sudo rm -rf ~/.docker

# install dependancies
sudo apt install -y apt-transport-https ca-certificates curl gnupg gnupg-agent software-properties-common lsb-release

# install docker-ce
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
```

## Additional dev tools

The following tools are useful to install locally.

**They are not necessary to run the project**

### Pipenv

- [pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today)

```bash
pip3 install --user pipenv
```

### K9s

- [k9s (bonus)](https://k9scli.io/topics/install/)

```bash
curl -sS https://webinstall.dev/k9s | bash
```

### Angular

- [angular](https://angular.io/guide/setup-local#install-the-angular-cli)

```bash
npm install -g @angular/cli
```

### Python

- [python 3.10](https://github.com/deadsnakes/python3.10)

```bash
sudo add-apt-repository --yes ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.10 python3.10-dev python3.10-distutils libpq-dev
```

### Node

- [Node 14](https://github.com/nodesource/distributions/blob/master/README.md#debinstall)

```bash
# Nodejs 14 using Ubuntu (src: https://github.com/nodesource/distributions/blob/master/README.md#debinstall)
curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt-get install -y nodejs build-essential gcc g++ make

## To install the Yarn package manager, run:
curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | gpg --dearmor | sudo tee /usr/share/keyrings/yarnkey.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/yarnkey.gpg] https://dl.yarnpkg.com/debian stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt-get update && sudo apt-get install yarn
```
