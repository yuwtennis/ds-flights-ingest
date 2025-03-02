""" Module extract """
import shutil
import zipfile
import gzip


class ZipExtract:  # pylint: disable=too-few-public-methods
    """ Handles extraction """

    @staticmethod
    def zip_to_gz_csv(filename: str, destdir: str) -> str:
        """

        :param filename:
        :param destdir:
        :return:
        """
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(path=destdir)
            csvfile = f'{destdir}/{zip_ref.namelist()[0]}'
            gzipped = f"{csvfile}.gz"

            with open(csvfile, 'rb') as ifp:
                with gzip.open(gzipped, 'wb') as ofp:
                    shutil.copyfileobj(ifp, ofp)

        return gzipped
