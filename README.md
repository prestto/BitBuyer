# BitBuyer

## Intro

Predict buy or sell on bitcoins.

The price of bitcoin is notoriously volatile.  This is because it has no inherent value, it's price is based almost exclusively on speculation.  How can you accurately predict the value of such an asset?  The short answer is that's almost impossible.  As so much of the price is speculative though, we can suppose that the decision to buy and sell is impacted by news, and online word of mouth.  This is compounded by the fact that bitcoin is held by private individuals, as opposed to companies.

Lets look at news outlets then, specifically twitter.  We've taken 16M tweets and used Natural Language Processing techniques determine the sentiment of the tweet (positive, negative or passive) and used them as a predictor to buy, sell, or hodl.

## Install

Bitbuyer is tested on an ubuntu system.  The following dependencies are required:

- [python 3.10](https://github.com/deadsnakes/python3.10)

```bash
sudo add-apt-repository --yes ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.10 python3.10-dev python3.10-distutils libpq-dev
```

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

- [pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today)

```bash
pip3 install --user pipenv
```

- [Docker](https://docs.docker.com/engine/install/ubuntu/)

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

- [K3d](https://k3d.io/v4.4.8/#install-script)
- [DiskPressure issue](https://github.com/tilt-dev/tilt/issues/1076)

```bash
# install
curl -s https://raw.githubusercontent.com/rancher/k3d/main/install.sh | bash

# launch cluster: tilt-test-cluster
k3d cluster create bitbuyer-cluster --k3s-server-arg '--kubelet-arg=eviction-hard=imagefs.available<1%,nodefs.available<1%' \
    --k3s-server-arg '--kubelet-arg=eviction-minimum-reclaim=imagefs.available=1%,nodefs.available=1%'
```

- [Tilt](https://docs.tilt.dev/install.html#linux)

```bash
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
```

- [k9s (bonus)](https://k9scli.io/topics/install/)

```bash
curl -sS https://webinstall.dev/k9s | bash
```

- [angular](https://angular.io/guide/setup-local#install-the-angular-cli)

```bash
npm install -g @angular/cli
```

## Dev

Dev is handled in tilt.

To run a dev server:

```bash
# launch tilt
./run.sh dev

# open tilt GUI
xdg-open http://localhost:10350
```

## Deployment

The bitbuyer app is deployed at [bitbuyer.tom-preston.co.uk](https://bitbuyer.tom-preston.co.uk).

Ingress is handled in the [ingress repo](https://github.com/prestto/ingress).
