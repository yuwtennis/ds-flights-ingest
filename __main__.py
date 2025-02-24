import logging
import argparse
import shutil
import tempfile

from ingest.app import App
from ingest.settings import RuntimeEnv

def arg_parser() -> argparse.Namespace:
    """

    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", type=str, required=True)
    parser.add_argument("--bucket", type=str, required=True)
    parser.add_argument("--year", type=str, required=False)
    parser.add_argument("--month", type=str, required=False)
    parser.add_argument("--dest_bq_tbl_fqdn", type=str, required=True)
    return parser.parse_args()

def main() -> None:
    """

    :return:
    """
    logging.basicConfig(level=logging.INFO)
    parser = arg_parser()

    try:
        App.run(
            RuntimeEnv(
                gc_project_id=parser.project_id,
                gcs_bucket=parser.bucket,
                bq_dest_tbl_fqdn=parser.dest_bq_tbl_fqdn,
                year=parser.year,
                month=parser.month
            )
        )

    except Exception as e:  # pylint: disable=invalid-name
        logging.error("Something went wrong!")

        # pylint: disable=fixme
        # TODO Structured logging
        raise RuntimeError() from e

if __name__ == "__main__":
    main()
