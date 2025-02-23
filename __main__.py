import argparse
import logging

from ingest.app import App

def main():
    logging.basicConfig(level=logging.ERROR)
    parser = argparse.ArgumentParser()

    parser.add_argument("--project_id", type=str, required=True)
    parser.add_argument("--bucket", type=str, required=True)
    parser.add_argument("--year", type=str, required=True)
    parser.add_argument("--month", type=str, required=True)
    parser.add_argument("--dest_bq_tbl_fqdn", type=str, required=True)
    App.run(parser.parse_args())

if __name__ == "__main__":
    main()
