""" Module app """
import logging
import shutil
import tempfile

from ingest.bq_ops import BqOps
from ingest.csv_download import CsvDownload
from ingest.settings import RuntimeEnv
from ingest.zip_extract import ZipExtract
from ingest.gs_ops import GsOps

GS_FLIGHTS_SUFFIX="flights/raw"

class App:  # pylint: disable=too-few-public-methods
    """ Orchestrates the whole workflow """
    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(logging.INFO)

    @staticmethod
    def run(settings: RuntimeEnv) -> None:
        """

        :param settings: Runtime environment settings
        :return:
        """

        workdir: str = tempfile.mkdtemp()

        try:
            year = settings.year
            month = settings.month
            gs = GsOps(settings.gc_project_id)  # pylint: disable=invalid-name

            if year is None or month is None:
                year, month = gs.next_month(settings.gcs_bucket, GS_FLIGHTS_SUFFIX)

            App.LOGGER.info("Downloading csv file from BTS site.")
            dl_csv_path = CsvDownload.to_filesystem(year, month, workdir)

            App.LOGGER.info("ZipExtract csv and compress the file for upload.")
            gz_csv_path = ZipExtract.zip_to_gz_csv(dl_csv_path, workdir)

            App.LOGGER.info("Upload to gcs")
            gs_loc = f"{GS_FLIGHTS_SUFFIX}/{year}{month}.csv.gz"
            gs.upload(gz_csv_path, settings.gcs_bucket, gs_loc)

            App.LOGGER.info("Load to BQ")
            bq = BqOps(settings.gc_project_id)  # pylint: disable=invalid-name
            bq.load_csv(f'gs://{settings.gcs_bucket}/{gs_loc}', settings.bq_dest_tbl_fqdn)
        finally:
            logging.info("Cleaning up directories and files.")
            shutil.rmtree(workdir)
