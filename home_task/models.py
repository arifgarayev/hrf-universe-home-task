import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        Table, UniqueConstraint, func)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry

mapper_registry = registry()


class Model: ...


@mapper_registry.mapped
@dataclass
class StandardJobFamily(Model):
    __table__ = Table(
        "standard_job_family",
        mapper_registry.metadata,
        Column("id", String, nullable=False, primary_key=True),
        Column("name", String, nullable=False),
        schema="public",
    )

    id: str
    name: str


@mapper_registry.mapped
@dataclass
class StandardJob(Model):
    __table__ = Table(
        "standard_job",
        mapper_registry.metadata,
        Column("id", String, nullable=False, primary_key=True),
        Column("name", String, nullable=False),
        Column("standard_job_family_id", String, nullable=False),
        schema="public",
    )

    id: str
    name: str
    standard_job_family_id: str


@mapper_registry.mapped
@dataclass
class JobPosting(Model):
    __table__ = Table(
        "job_posting",
        mapper_registry.metadata,
        Column("id", String, nullable=False, primary_key=True),
        Column("title", String, nullable=False),
        Column("standard_job_id", String, nullable=False),
        Column("country_code", String, nullable=True),
        Column("days_to_hire", Integer, nullable=True),
        schema="public",
    )

    id: str
    title: str
    standard_job_id: str
    country_code: Optional[str] = None
    days_to_hire: Optional[int] = None


@mapper_registry.mapped
@dataclass
class HireStatistics(Model):
    __table__ = Table(
        "hire_statistics",
        mapper_registry.metadata,
        Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        Column(
            "created_at",
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
        Column(
            "standard_job_id",
            String,
            ForeignKey("public.standard_job.id"),
            nullable=False,
        ),
        Column("country_code", String, nullable=True),
        Column("minimum", Float, nullable=False),
        Column("maximum", Float, nullable=False),
        Column("average", Float, nullable=False),
        Column("n_of_postings", Integer, nullable=False),
        Column(
            "updated_at",
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        ),
        Column("threshold", Integer, nullable=True, server_default="5"),
        UniqueConstraint(
            "standard_job_id", "country_code", name="uq_hire_statistics_stdjob_country"
        ),
        schema="public",
    )

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    standard_job_id: str  # required
    minimum: float
    maximum: float
    average: float
    n_of_postings: int
    threshold: int
    country_code: Optional[str] = None  # if None -> meaning global
