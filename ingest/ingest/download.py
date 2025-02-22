""" Takes care of download"""
from urllib.request import urlopen

DOWNLOAD_URL_PREFIX = ("https://transtats.bts.gov/PREZIP/"
                       "On_Time_Reporting_Carrier_On_Time_Performance_1987_present")
ZIP_CONTENT_PREFIX= "On_Time_Reporting_Carrier_On_Time_Performance_(1987_present)"


class Download:  # pylint: disable=too-few-public-methods
    """ Downlaod class"""
    @staticmethod
    def download(year: str, month: str, destdir: str) -> str:
        """

        :param year:
        :param month:
        :param destdir:
        :return:
        """
        url = f"{DOWNLOAD_URL_PREFIX}/{ZIP_CONTENT_PREFIX}_{year}_{int(month)}.zip"
        filename = f"{destdir}/{ZIP_CONTENT_PREFIX}_{year}_{month}.zip"

        with open(filename, "wb") as fp:  # pylint: disable=invalid-name
            with urlopen(url) as r:  # pylint: disable=invalid-name
                fp.write(r.read())

        return filename
