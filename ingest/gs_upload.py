""" Module gs_upload """
import logging

from google.cloud import storage  # type: ignore


class GsUpload:  # pylint: disable=too-few-public-methods
    """ Upload data to Google Storage """
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
        blob = storage.Blob(blobname, bucket)

        # Multipart upload natively supported in Blob class
        # https://github.com/googleapis/python-storage/blob/main/google/cloud/storage/blob.py#L2935
        blob.upload_from_filename(csvfile)
        gcslocation = f'gs://{bucket.name}/{blobname}'
        GsUpload.LOGGER.info("Uploaded %s ...", gcslocation)

        return gcslocation
