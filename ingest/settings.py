""" Module settings"""

from pydantic import BaseModel, model_validator

class RuntimeEnv(BaseModel):
    """ Runtime variables """
    gc_project_id: str
    gcs_bucket: str
    year: str | None = ...
    month: str | None = ...
    bq_dest_tbl_fqdn: str
