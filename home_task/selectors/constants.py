from dataclasses import dataclass

BATCH_SIZE = 2


@dataclass
class HireStatisticsView:
    standard_job_id: str
    country_code: str
    minimum: float
    average: float
    maximum: float
    n_of_postings: int
