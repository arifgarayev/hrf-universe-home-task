import ast
import json

from sqlalchemy.dialects.postgresql import insert

from home_task.models import HireStatistics


class HireStatisticsInsert:
    def __init__(self, db_session):
        self.db_session = db_session

    def insert(self, stats: list[dict]):

        # no other way to do this
        # N + 1 upsert

        with self.db_session.begin_nested():
            for stat in stats:
                ctx = insert(HireStatistics.__table__).values(stat)

                upsert = ctx.on_conflict_do_update(
                    index_elements=[
                        "standard_job_id",
                        "country_code",
                    ],  # the two-column unique constraint
                    set_={
                        "minimum": ctx.excluded.minimum,
                        "average": ctx.excluded.average,
                        "maximum": ctx.excluded.maximum,
                        "n_of_postings": ctx.excluded.n_of_postings,
                        "threshold": ctx.excluded.threshold,
                    },
                )

                self.db_session.execute(upsert)
        return self.db_session
