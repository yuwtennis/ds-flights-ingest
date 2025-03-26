""" Root module for Flask """
import logging
import traceback

from flask import request, abort, Flask, jsonify
from markupsafe import escape
from ds_flights_ingest.app import App
from ds_flights_ingest.settings import RuntimeEnv

app = Flask(__name__)

@app.errorhandler(500)
def exception_handler(e):  # pylint: disable=invalid-name
    """ Exception handler"""
    return jsonify(error=str(e)), 500

@app.route("/", methods=['POST'])
def ingest_flights() -> str:
    """ Function which will hook data loading process """
    try:
        json = request.get_json()

        App.run(
            RuntimeEnv(
                gc_project_id=escape(json['project_id']),
                gcs_bucket=escape(json['bucket']),
                year=escape(json['year']) if 'year' in json else None,
                month=escape(json['month']) if 'month' in json else None,
                bq_dest_tbl_fqdn=escape(json['dest_bq_tbl_fqdn'])
        ))

        return "Success"

    # pylint: disable=broad-except
    # pylint: disable=invalid-name
    except Exception:
        logging.error('Try again later. err: %s', traceback.format_exc().splitlines())

        abort( 500, "Somthing went wrong" )
