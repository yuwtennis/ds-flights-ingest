""" Module download """
import ssl
from urllib.request import urlopen

DOWNLOAD_URL_PREFIX = ("https://transtats.bts.gov/PREZIP/"
                       "On_Time_Reporting_Carrier_On_Time_Performance_1987_present")


class CsvDownload:  # pylint: disable=too-few-public-methods
    """ Downlaod class"""
    @staticmethod
    def to_filesystem(year: str, month: str, destdir: str) -> str:
        """

        :param year:
        :param month:
        :param destdir:
        :return:
        """
        url = f"{DOWNLOAD_URL_PREFIX}_{year}_{int(month)}.zip"
        filename = f"{destdir}/{year}_{month}.zip"
        ctx = ssl.SSLContext()
        ctx.verify_mode = ssl.CERT_NONE

        with open(filename, "wb") as fp:  # pylint: disable=invalid-name
            with urlopen(url, context=ctx) as r:  # pylint: disable=invalid-name
                fp.write(r.read())

        return filename
