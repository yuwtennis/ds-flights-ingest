""" Module settings"""

from pydantic import BaseModel, Field

class RuntimeEnv(BaseModel):
    """ Runtime variables """
    gc_project_id: str
    gcs_bucket: str
    year: str | None = Field(...)
    month: str | None = Field(...)
    bq_dest_tbl_fqdn: str
