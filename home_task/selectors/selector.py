from sqlalchemy import (Column, Float, Integer, String, and_, asc, func,
                        literal, or_, select, within_group)
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import percentile_cont

from home_task.models import HireStatistics, JobPosting
from home_task.selectors.constants import BATCH_SIZE, HireStatisticsView


class JobPostingSelector:

    coalesce_country = func.coalesce(JobPosting.country_code, literal("Global")).label(
        "country_code"
    )

    def __init__(self, db_session: Session):
        self.db_session: Session = db_session

    def _get_percentile_cte(self, min_percentile: float, max_percentile: float):
        return (
            select(
                JobPosting.standard_job_id,
                self.coalesce_country,
                percentile_cont(min_percentile)
                .within_group(asc(JobPosting.days_to_hire))
                .label("min_p10"),
                percentile_cont(max_percentile)
                .within_group(asc(JobPosting.days_to_hire))
                .label("max_p90"),
            )
            .where(JobPosting.days_to_hire.isnot(None))
            .group_by(JobPosting.standard_job_id, JobPosting.country_code)
            .cte("percentile_cte")
        )

    def _get_clean_jp_cte(self):
        return select(
            JobPosting.standard_job_id,
            self.coalesce_country,
            JobPosting.days_to_hire,
            JobPosting.title,
            JobPosting.id,
        ).cte("clean_job_postings")

    def _get_precalc_stats(self, job_posting_threshold: int):

        percentile_cte = self._get_percentile_cte(0.1, 0.9)
        clean_jp = self._get_clean_jp_cte()

        return (
            select(
                clean_jp.c.standard_job_id,
                clean_jp.c.country_code,
                literal(job_posting_threshold).label("threshold"),
                func.min(clean_jp.c.days_to_hire)
                .filter(
                    clean_jp.c.days_to_hire.between(
                        percentile_cte.c.min_p10, percentile_cte.c.max_p90
                    )
                )
                .label("minimum"),
                func.avg(clean_jp.c.days_to_hire)
                .filter(
                    clean_jp.c.days_to_hire.between(
                        percentile_cte.c.min_p10, percentile_cte.c.max_p90
                    )
                )
                .label("average"),
                func.max(clean_jp.c.days_to_hire)
                .filter(
                    clean_jp.c.days_to_hire.between(
                        percentile_cte.c.min_p10, percentile_cte.c.max_p90
                    )
                )
                .label("maximum"),
                func.count()
                .filter(
                    clean_jp.c.days_to_hire.between(
                        percentile_cte.c.min_p10, percentile_cte.c.max_p90
                    )
                )
                .label("n_of_postings"),
            )
            .select_from(clean_jp)
            .join(
                percentile_cte,
                and_(
                    clean_jp.c.standard_job_id == percentile_cte.c.standard_job_id,
                    clean_jp.c.country_code == percentile_cte.c.country_code,
                ),
            )
            .group_by(clean_jp.c.standard_job_id, clean_jp.c.country_code)
            .having(
                func.count().filter(
                    clean_jp.c.days_to_hire.between(
                        percentile_cte.c.min_p10, percentile_cte.c.max_p90
                    )
                )
                >= job_posting_threshold
            )
        )

    def query(self, job_posting_threshold: int = 5, is_batch: bool = False):
        stmt = self._get_precalc_stats(job_posting_threshold)
        # print(stmt)

        if not is_batch:
            result = self.db_session.execute(stmt).all()

            return result

        else:

            stream = stmt.execution_options(stream_results=True)
            result = self.db_session.execute(stream).mappings()

            while True:

                batch_res = result.fetchmany(BATCH_SIZE)

                if not batch_res:
                    break

                yield batch_res


"""
Native query - 


WITH percentile_cte AS (
    SELECT
        jp.standard_job_id,
        COALESCE(jp.country_code, 'Global') AS country_code,
        PERCENTILE_CONT(0.1)
            WITHIN GROUP (ORDER BY jp.days_to_hire ASC) AS min_p10,
        PERCENTILE_CONT(0.9)
            WITHIN GROUP (ORDER BY jp.days_to_hire ASC) AS max_p90
    FROM
        public.job_posting AS jp
    WHERE
        jp.days_to_hire IS NOT NULL
    GROUP BY
        jp.standard_job_id,
        jp.country_code
),

clean_jp AS (
    SELECT
        jp.standard_job_id,
        COALESCE(jp.country_code, 'Global') AS country_code,
        title,
        id,
        days_to_hire
        FROM job_posting AS jp
)

SELECT
    jp.standard_job_id,
    jp.country_code,
    MIN(jp.days_to_hire) FILTER (
        WHERE jp.days_to_hire BETWEEN c.min_p10 AND c.max_p90
    )   AS minimum,
    AVG(jp.days_to_hire) FILTER (
        WHERE jp.days_to_hire BETWEEN c.min_p10 AND c.max_p90
    )   AS average,
    MAX(jp.days_to_hire) FILTER (
        WHERE jp.days_to_hire BETWEEN c.min_p10 AND c.max_p90
    )   AS maximum,
    COUNT(*) FILTER (
        WHERE jp.days_to_hire BETWEEN c.min_p10 AND c.max_p90
    )   AS n_of_postings
FROM
    clean_jp AS jp
    JOIN percentile_cte AS c
      ON jp.standard_job_id = c.standard_job_id
     AND (
         jp.country_code = c.country_code
--          OR (jp.country_code IS NULL AND c.country_code IS NULL)
     )
GROUP BY
    jp.standard_job_id,
    jp.country_code
HAVING
    COUNT(*) FILTER (
        WHERE jp.days_to_hire BETWEEN c.min_p10 AND c.max_p90
    ) >= 1;


"""
