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
    cecho "BL" "Scraping..."
    pipenv run python ./scripts/coin_names.py
    cecho "BL" "Scrape complete."
}

function show_help {
    cecho "BL" "Help: $0 <ACTION>"
    cecho "BL" "Parameters :"
    cecho "BL" " - ACTION values :"
    cecho "BL" "   * dev                            - Run tilt up."
    cecho "BL" "   * seed                           - Run db seeding."
    cecho "BL" "   * reset                          - Run db reset."
    cecho "BL" "   * dump                           - Run db dump."
    cecho "BL" "   * scrape                         - Scrape coins page."
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
    run_scrape
    ;;
*)
    show_help
    ;;
esac
