#!/usr/bin/env bash
# Note
# This script is equivalent to clicking download button with "Prezipped File" option enabled on BTS website.
# It's url is
# https://transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ&QO_fu146_anzr=

# constants
BTS="https://transtats.bts.gov/PREZIP"
BASEURL="${BTS}/On_Time_Reporting_Carrier_On_Time_Performance_1987_present"
ZIP_CONTENT_PREFIX="On_Time_Reporting_Carrier_On_Time_Performance_(1987_present)"
BQ_DATASET="dsongcp"
BQ_TABLE="flights_raw"

function download() {
  local year=$1
  local month_start=$2
  local month_end=$3

  for m in `seq $month_start $month_end` ; do
    year_mon=$(printf "%04d%02d" $year $m)
    curl -k -o tmp.zip "${BASEURL}_${year}_${m}.zip"
    unzip tmp.zip ${ZIP_CONTENT_PREFIX}_${year}_${m}.csv && \
      mv ${ZIP_CONTENT_PREFIX}_${year}_${m}.csv ${year_mon}.csv
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
  local project_id=$(gcloud config get core/project)
  local gs_data_in_place_dir="gs://${project_id}-ds/flights/raw"

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

  if [[ $start -gt $end ]]; then
    echo "Err: Start month bigger than end month. "
    exit 1
  fi

  echo "Downloading files for year: $year month from $start to $end."
  download $year $start $end

  # Upload to data-in-place
  echo "Uploading to google cloud storage"
  gsutil -m cp *.csv "$gs_data_in_place_dir/"

  # Load to bigquery
  for m in `seq $start $end`; do
    ym="$(printf "%04d%02d" $year $m)"
    csvfile="${gs_data_in_place_dir}/$ym.csv"

    echo "Loading to BQ csv: $csvfile"
    bq -project_id ${project_id} load \
      --source_format=CSV \
      --skip_leading_rows=1 \
      --ignore_unknown_values \
      --autodetect=false \
      "${project_id}:${BQ_DATASET}.${BQ_TABLE}\$$ym" $csvfile
  done
}

main "$@"