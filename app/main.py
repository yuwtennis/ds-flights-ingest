""" Root module for Flask """
import logging
import traceback

from flask import Flask
from flask import request
from markupsafe import escape
from ingest.app import App
from ingest.settings import RuntimeEnv

app = Flask(__name__)

@app.route("/", methods=['POST'])
def ingest_flights() -> str:
    """ Function which will hook data loading process """
    try:
        json = request.get_json()

        year = escape(json['year']) if 'year' in json else None
        month = escape(json['month']) if 'month' in json else None
        bucket = escape(json['bucket'])
        project_id = escape(json['project_id'])
        dest_bq_tbl_fqdn = escape(json['dest_bq_tbl_fqdn'])

        App.run(
            RuntimeEnv(
                gc_project_id=project_id,
                gcs_bucket=bucket,
                year=year,
                month=month,
                bq_dest_tbl_fqdn=dest_bq_tbl_fqdn
        ))

        return "Success"

    # pylint: disable=broad-except
    # pylint: disable=invalid-name
    except Exception:
        logging.error('Try again later. err: %s', traceback.format_exc().splitlines())

        return "Error"
