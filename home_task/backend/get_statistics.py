from typing import Optional
from fastapi import Path, Query
from pydantic import BaseModel
from typing import Annotated, Literal
from home_task.models import HireStatistics
from home_task.db import get_session
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from dataclasses import asdict
from fastapi import APIRouter

router = APIRouter()

class Input(BaseModel):
    standard_job_id: str
    country_code: Optional[str] = 'Global'


class Output(BaseModel):
    standard_job_id: str
    country_code: str
    minimum: int
    average: int
    maximum: int
    n_of_postings: int
    threshold: int


@router.get("/hire_stats")
async def hire_stats(
    standard_job_id: str = Query(..., description="Normalized job UUID"),
    country_code: Optional[str] = Query('Global', description="Country code"),
):

    db_session = get_session()
    
    return asdict(db_session.query(HireStatistics).where(
            HireStatistics.standard_job_id == standard_job_id,
            HireStatistics.country_code == country_code
        ).first())
    
    