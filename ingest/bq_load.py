""" Module bq_load """
import logging

from google.cloud import bigquery

class BqLoad:  # pylint: disable=too-few-public-methods
    """ Manages load job """
    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(logging.INFO)

    def __init__(self, project_id: str):
        self._client = bigquery.Client(project_id)

    def load_csv(self, gsloc: str, dest_bq_tbl_fqdn: str) -> None:
        """
        Load csv data to predefined table in bigquery

        :param gsloc:
        :param dest_bq_tbl_fqdn:
        :return:
        :raise: RuntimeError
        """
        job_config = bigquery.LoadJobConfig(
            schema=None,
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            ignore_unknown_values=True,
            autodetect=False
        )

        loaded_job: bigquery.LoadJob = (
            self._client.load_table_from_uri(gsloc, dest_bq_tbl_fqdn, job_config=job_config))

        res: bigquery.job._AsyncJob = loaded_job.result()

        if res.error_result is not None:
            BqLoad.LOGGER.info("Something went wrong while loading csv. errs: %s", res.errors)
            raise RuntimeError()

        BqLoad.LOGGER.info(
            "%s rows inserted into %s",
            self._client.get_table(dest_bq_tbl_fqdn).num_rows, dest_bq_tbl_fqdn)
