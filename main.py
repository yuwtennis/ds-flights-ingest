import logging

from flask import escape
from ingest.app import App
from ingest.gs_ops import GsOps
from ingest.settings import RuntimeEnv

app = Flask(__name__)

@app.route("/", methods=['POST'])
def ingest_flights(request):
    try:
        json = request.get_json()

        year = escape(json['year']) if 'year' in json else None
        month = escape(json['month']) if 'month' in json else None
        bucket = escape(json['month'])
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

    except Exception as e:
        logging.exception('Try again later')

