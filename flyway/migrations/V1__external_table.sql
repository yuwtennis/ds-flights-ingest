CREATE EXTERNAL TABLE `elite-caster-125113.dsongcp.flights_auto`
  OPTIONS (
    format = "CSV",
    uris = ['gs://elite-caster-125113-ds/flights/raw/201501.csv']
    );