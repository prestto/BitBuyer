#!/bin/bash
cecho() {
    LB='\033[1;36m' # Light Blue
    LG='\033[1;32m' # Light Green
    YE='\033[1;33m' # Yellow

    # print normally if no second arg added
    if [[ $2 == "" ]]; then
        echo $1
        return
    fi

    case $1 in
    BL)
        printf "$LB%s\033[0m\n" "$2" # Light Cyan
        ;;
    GR)
        printf "$LG%s\033[0m\n" "$2" # Light green
        ;;
    YE)
        printf "$YE%s\033[0m\n" "$2" # Light green
        ;;
    normal | *)
        echo $2 # Light Purple
        ;;
    esac
}

function run_dev {
    cecho "BL" "Tilting..."
    tilt up
}

function run_seed {
    cecho "BL" "Seeding..."
    pipenv run python ./scripts/seed.py
    cecho "BL" "Seeding complete."
}

function run_reset {
    cecho "BL" "Resetting..."
    pipenv run python ./scripts/reset.py
    cecho "BL" "Reset complete."
}

function run_dump {
    cecho "BL" "Dumping..."
    pipenv run python ./scripts/dump.py
    cecho "BL" "Dump complete."
}

function run_scrape {

    if [[ "$1" = "" ]]; then
        TABLE="coins"
    else
        TABLE=$1
    fi

    cecho "BL" "Scraping $TABLE..."
    pipenv run python ./scripts/$TABLE.py
    cecho "BL" "Scrape complete."
}

function run_build {
    TAG="latest"
    if [[ $1 = "" ]]; then
        ENV="dev"
    else
        ENV=$1
    fi
    cecho "BL" "Building: user632716/bitbuyer:$TAG..."
    docker build --file docker/Dockerfile-bitbuyer --tag user632716/bitbuyer:$TAG .

    # check the value is recognized, otherwise error quit
    if [[ $ENV != "dev" ]] && [[ $ENV != "prod" ]]; then
        cecho "YE" "$ENV was is not a recognized value, try 'dev' or 'prod'"
        cecho "YE" "Exiting process"
        exit 1
    fi

    # set the dockerfile to use
    if [[ $ENV = "dev" ]]; then
        # dev
        DOCKERFILE=docker/Dockerfile-bitbuyer-front
        cecho "BL" "Building: docker build --file docker/Dockerfile-bitbuyer-front --tag user632716/bitbuyer-front:$ENV ."
        docker build --file docker/Dockerfile-bitbuyer-front --tag user632716/bitbuyer-front:$ENV .
    else
        # prod
        cecho "BL" "Building: docker build --file docker/Dockerfile-bitbuyer-front-prod --tag user632716/bitbuyer-front:$ENV ."
        docker build --file docker/Dockerfile-bitbuyer-front-prod --tag user632716/bitbuyer-front:$ENV .
    fi

    cecho "BL" "Built."
}

function run_push {
    cecho "BL" "Pushing user632716/bitbuyer:latest..."
    docker push user632716/bitbuyer:latest

    # default to latest
    if [[ $1 = "" ]]; then
        TAG="dev"
    else
        TAG=$1
    fi

    if [[ $TAG != "dev" ]] && [[ $TAG != "prod" ]]; then
        cecho "YE" "$TAG only tags 'dev' or 'prod' are accepted"
        cecho "YE" "Exiting process"
        exit 1
    fi

    if [[ $TAG = "dev" ]]; then
        # dev
        cecho "BL" "Pushing user632716/bitbuyer-front:dev..."
        docker push user632716/bitbuyer-front:dev
    else
        # prod
        cecho "BL" "Pushing user632716/bitbuyer-front:prod..."
        docker push user632716/bitbuyer-front:prod
    fi

    cecho "BL" "Pushed."
}

function run_rollout {
    # default to latest
    if [[ $1 = "" ]]; then
        ENV="dev"
    else
        ENV=$1
    fi

    if [[ $ENV != "dev" ]] && [[ $ENV != "prod" ]]; then
        cecho "YE" "$ENV only tags 'dev' or 'prod' are accepted"
        cecho "YE" "Exiting process"
        exit 1
    fi

    # match the cluster
    if [[ $ENV = "dev" ]]; then
        CLUSTER='minikube'
    fi

    if [[ $ENV = "prod" ]]; then
        CLUSTER='kubernetes-admin@perso'
    fi

    cecho "BL" "Rolling out bitbuyer-api ${CLUSTER}"
    kubectl --context ${CLUSTER} rollout restart -n bitbuyer deploy/bitbuyer-api
    cecho "BL" "Rolling out bitbuyer-front ${CLUSTER}"
    kubectl --context ${CLUSTER} rollout restart -n bitbuyer deploy/bitbuyer-front
}

function run_migrate {
    cecho "BL" "Migrating..."
    kubectl exec -n bitbuyer deploy/bitbuyer-api -- python manage.py migrate
    kubectl exec -n bitbuyer deploy/bitbuyer-api -- python manage.py migrate coins
    cecho "BL" "Migrated."
}

function run_makemigrations {
    cecho "BL" "Making migrations..."
    kubectl exec -n bitbuyer deploy/bitbuyer-api -- python manage.py makemigrations common
    kubectl exec -n bitbuyer deploy/bitbuyer-api -- python manage.py makemigrations coins
    cecho "BL" "Migrations made."
}

function run_deploy {
    # set the default option as dev
    if [[ $1 = "" ]]; then
        ENV="dev"
    else
        ENV=$1
    fi

    # check the value is recognized, otherwise error quit
    if [[ $ENV != "dev" ]] && [[ $ENV != "prod" ]]; then
        cecho "YE" "$ENV was is not a recognized value, try 'dev' or 'prod'"
        cecho "YE" "Exiting process"
        exit 1
    fi

    # match the cluster
    if [[ $ENV = "dev" ]]; then
        CLUSTER='minikube'
    fi

    if [[ $ENV = "prod" ]]; then
        CLUSTER='kubernetes-admin@perso'
    fi

    cecho "BL" "Deploying to cluster: $CLUSTER (mode: $ENV)..."
    kubectl --context ${CLUSTER} -n bitbuyer apply -k ./k8s/overlays/${ENV}/

    run_rollout $ENV
}

function run_update_coins {
    cecho "BL" "Updating current prices..."
    pipenv run python ./scripts/update_current_prices.py
    cecho "BL" "Updated current prices."
}

function run_reset_mini {
    cecho "BL" "Resetting minikube"
    minikube delete

    run_start_mini
}

function run_start_mini {
    cecho "BL" "Starting Minikube."
    minikube start --kubernetes-version=v1.20.2

    cecho "BL" "Enabling ingress."
    minikube addons enable ingress

    CLUSTER_IP=docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' minikube
    cecho "BL" "Cluster running with IP: $CLUSTER_IP"

    cecho "BL" "Run the following to launch cluster in dev mode:"
    cecho "BL" "./run.sh dev"
}

function run_forward_postgres {
    cecho "BL" "Setting up port forward to postgres-db"
    kubectl --context kubernetes-admin@perso port-forward -n bitbuyer svc/postgres-internal 5432:5432
}

function show_help {
    cecho "BL" "Help: $0 <ACTION>"
    cecho "BL" "Parameters :"
    cecho "BL" " - ACTION values :"
    cecho "BL" "   * dev                            - Run tilt up."
    cecho "BL" " "
    cecho "BL" " - Minikube:"
    cecho "BL" "   * start_mini                     - Start minikube."
    cecho "BL" "   * reset_mini                     - Reset and restart minikube."
    cecho "BL" " "
    cecho "BL" " - K8s Deployment:"
    cecho "BL" "   * build <env>                    - Build & tag the docker image (default env=dev)."
    cecho "BL" "   *     dev                        - Build & tag images, front will be tagged for dev."
    cecho "BL" "   *     prod                       - Build & tag images, front will be tagged for prod."
    cecho "BL" "   * push <env>                     - Push user632716/bitbuyer:latest."
    cecho "BL" "   *     dev                        - Push front and back images, front only with dev."
    cecho "BL" "   *     prod                       - Push front and back images, front only with prod."
    cecho "BL" "   * deploy <env>                   - Deploy to cluster (default env=dev)."
    cecho "BL" "   *     dev                        - Deploy to cluster: minikube."
    cecho "BL" "   *     prod                       - Deploy to cluster: kubernetes-admin@perso."
    cecho "BL" "   * rollout <env>                  - Redeploy on k8s using dockerhub image (included in deploy)."
    cecho "BL" "   *     dev                        - Rollout dev"
    cecho "BL" "   *     prod                       - Rollout prod."
    cecho "BL" " "
    cecho "BL" " - K8s Other:"
    cecho "BL" "   * forward_postgres               - Set up post forward to postgres on cluster kubernetes-admin@perso"
    cecho "BL" " "
    cecho "BL" " - Postgres:"
    cecho "BL" "   * seed                           - Run db seeding."
    cecho "BL" "   * reset                          - Run db reset."
    cecho "BL" "   * dump                           - Run db dump."
    cecho "BL" "   * migrate                        - Migrate the db."
    cecho "BL" "   * makemigrations                 - Make db migrations."
    cecho "BL" " "
    cecho "BL" " - Scripts:"
    cecho "BL" "   * scrape <table>                 - Scrape a data for a table."
    cecho "BL" "   *         coins                  - Scrape coins table."
    cecho "BL" "   *         coin_prices            - Scrape coin prices."
    cecho "BL" "   * update_coins                   - Update current coin prices."
}

if [[ "$1" == "" ]]; then
    cecho "YE" "No arguments provided."
    show_help
    exit 1
fi

case "$1" in
dev)
    run_dev
    ;;
seed)
    run_seed
    ;;
reset)
    run_reset
    ;;
dump)
    run_dump
    ;;
scrape)
    run_scrape $2
    ;;
build)
    run_build $2
    ;;
push)
    run_push $2
    ;;
rollout)
    run_rollout $2
    ;;
migrate)
    run_migrate
    ;;
makemigrations)
    run_makemigrations
    ;;
update_coins)
    run_update_coins
    ;;
start_mini)
    run_start_mini
    ;;
reset_mini)
    run_reset_mini
    ;;
deploy)
    run_deploy $2
    ;;
forward_postgres)
    run_forward_postgres
    ;;
*)
    show_help
    ;;
esac
