""" Module settings"""
from typing import Optional
from pydantic import Field, BaseModel

class RuntimeEnv(BaseModel):
    """ Runtime variables """
    gc_project_id: str
    gcs_bucket: str
    year: Optional[str] = Field(default=None)
    month: Optional[str] = Field(default=None)
    bq_dest_tbl_fqdn: str
