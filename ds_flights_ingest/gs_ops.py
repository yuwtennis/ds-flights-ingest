""" Module gs_ops """
import logging
import datetime
import os.path
from typing import Tuple

from google.cloud import storage  # type: ignore


class GsOps:  # pylint: disable=too-few-public-methods
    """ Operations related to Google Storage """
    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(logging.DEBUG)

    def __init__(self, project_id: str):
        self._client = storage.Client(project_id)

    def upload(self, csvfile: str, bucketname: str, blobname: str) -> str:
        """

        :param csvfile:
        :param bucketname:
        :param blobname:
        :return:
        """
        bucket: storage.Bucket = self._client.bucket(bucketname)
        blob: storage.Blob = storage.Blob(blobname, bucket)

        # Multipart upload natively supported in Blob class
        # https://github.com/googleapis/python-storage/blob/main/google/cloud/storage/blob.py#L2935
        blob.upload_from_filename(csvfile)
        gcslocation = f'gs://{bucket.name}/{blobname}'
        GsOps.LOGGER.info("Uploaded %s ...", gcslocation)

        return gcslocation

    def next_month(self, bucket_name: str, raw_flights_dir: str) -> Tuple[str, str]:
        """
        next_month will read the latest csv file in
        google storage and calculate the month-year of next month

        :param bucket_name:
        :param raw_flights_dir:
        :return:
        """
        bucket: storage.Bucket = self._client.get_bucket(bucket_name)
        blobs = list(bucket.list_blobs(prefix=raw_flights_dir))
        files = [blob.name for blob in blobs if 'csv' in blob.name]

        GsOps.LOGGER.info("Month years. Earliest: %s , Latest: %s", files[0] , files[-1])

        last_file: str = os.path.basename(files[-1])
        year: str = last_file[:4]
        month: str = last_file[4:6]

        # Middle of the month will be safe to count the next month from
        # pylint: disable=invalid-name
        dt = datetime.datetime(year=int(year), month=int(month), day=15)
        dt = dt + datetime.timedelta(30)

        return f"{dt:%Y}", f"{dt:%m}"
