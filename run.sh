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

function run_tag {
    if [[ $1 = "" ]]; then
        TAG="latest"
    else
        TAG=$1
    fi
    cecho "BL" "Building with tag: $TAG..."
    docker build --file docker/Dockerfile-bitbuyer --tag user632716/bitbuyer:$TAG .
    cecho "BL" "Built."
}

function run_push {
    cecho "BL" "Pushing user632716/bitbuyer:latest..."
    docker push user632716/bitbuyer:latest
    cecho "BL" "Pushed."
}

function run_migrate {
    cecho "BL" "Migrating..."
    kubectl exec deploy/bitbuyer-api -- python manage.py migrate
    kubectl exec deploy/bitbuyer-api -- python manage.py migrate coins
    cecho "BL" "Migrated."
}

function run_makemigrations {
    cecho "BL" "Making migrations..."
    kubectl exec deploy/bitbuyer-api -- python manage.py makemigrations common
    kubectl exec deploy/bitbuyer-api -- python manage.py makemigrations coins
    cecho "BL" "Migrations made."
}

function run_update_coins {
    cecho "BL" "Updating current prices..."
    pipenv run python ./scripts/update_current_prices.py
    cecho "BL" "Updated current prices."
}

function show_help {
    cecho "BL" "Help: $0 <ACTION>"
    cecho "BL" "Parameters :"
    cecho "BL" " - ACTION values :"
    cecho "BL" "   * dev                            - Run tilt up."
    cecho "BL" "   * seed                           - Run db seeding."
    cecho "BL" "   * reset                          - Run db reset."
    cecho "BL" "   * dump                           - Run db dump."
    cecho "BL" "   * scrape <table>                 - Scrape a data for a table."
    cecho "BL" "   *         coins                  - Scrape coins table."
    cecho "BL" "   *         coin_prices            - Scrape coin prices."
    cecho "BL" "   * tag <table>                    - Build & tag the docker image."
    cecho "BL" "   * push                           - Push user632716/bitbuyer:latest."
    cecho "BL" "   * migrate                        - Migrate the db."
    cecho "BL" "   * makemigrations                 - Make db migrations."
    cecho "BL" "   * update_coins                   - Update current coin prices."
}

if [[ "$1" == "" ]]; then
    cecho "No arguments provided."
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
tag)
    run_tag $2
    ;;
push)
    run_push
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
*)
    show_help
    ;;
esac
