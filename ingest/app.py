""" Module app """
import argparse
import logging
import tempfile
import shutil

from ingest.bq_load import BqLoad
from ingest.csv_download import CsvDownload
from ingest.zip_extract import ZipExtract
from ingest.gs_upload import GsUpload

GS_FLIGHTS_SUFFIX="flights/raw"

class App:  # pylint: disable=too-few-public-methods
    """ Orchestrates the whole workflow """
    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(logging.INFO)

    @staticmethod
    def run(args: argparse.Namespace):
        """

        :param args:
        :return:
        """
        workdir: str = tempfile.mkdtemp()
        try:
            App.LOGGER.info("Downloading csv file from BTS site.")
            dl_csv_path = CsvDownload.to_filesystem(args.year, args.month, workdir)

            App.LOGGER.info("ZipExtract csv and compress the file for upload.")
            gz_csv_path = ZipExtract.zip_to_gz_csv(dl_csv_path, workdir)

            App.LOGGER.info("Upload to gcs")
            gs_loc = f"{GS_FLIGHTS_SUFFIX}/{args.year}{args.month}.csv.gz"

            gs = GsUpload(args.project_id)  # pylint: disable=invalid-name
            gs.upload(gz_csv_path, args.bucket, gs_loc)

            App.LOGGER.info("Load to BQ")
            bq = BqLoad(args.project_id)  # pylint: disable=invalid-name
            bq.load_csv(f'gs://{args.bucket}/{gs_loc}', args.dest_bq_tbl_fqdn)

        except Exception as e:  # pylint: disable=invalid-name
            App.LOGGER.error("Something went wrong!")

            # pylint: disable=fixme
            # TODO Structured logging
            raise RuntimeError() from e
        finally:
            App.LOGGER.info("Cleaning up directories and files.")
            shutil.rmtree(workdir)
