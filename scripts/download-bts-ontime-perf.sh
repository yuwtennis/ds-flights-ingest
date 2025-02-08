#!/usr/bin/env bash

# constants
BTS="https://transtats.bts.gov/PREZIP"
BASEURL="${BTS}/On_Time_Reporting_Carrier_On_Time_Performance_1987_present"

function run() {
  local year=$1
  local month_start=$2
  local month_end=$3

  for m in `seq $month_start $month_end` ; do
    echo "${BASEURL}_${year}_${m}.zip"
    curl -k -o tmp.zip "${BASEURL}_${year}_${m}.zip"
    unzip tmp.zip On_Time_Reporting_Carrier_On_Time_Performance_\(1987_present\)_${year}_${m}.csv && \
      mv On_Time_Reporting_Carrier_On_Time_Performance_\(1987_present\)_${year}_${m}.csv ${year}_${m}.csv
    rm -v tmp.zip
  done
}

function help() {
  echo "Usage: $0 [-h] [-y year] [-s start of the month] [-e end of the month]"
  exit 0
}

function main() {
  local year=$(date "+%Y")
  local start=1
  local end=12

  while getopts ":y:s:e:h" opt; do
    case $opt in
      y)
        year=$OPTARG
        ;;
      s)
        start=$OPTARG
        ;;
      e)
        end=$OPTARG
        ;;
      h)
        help
        ;;
      \?)
        help
        ;;
    esac
  done

  run $year $start $end
}

main "$@"