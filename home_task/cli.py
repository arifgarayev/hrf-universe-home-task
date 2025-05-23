from home_task.db import get_session
from home_task.models import HireStatistics
from home_task.selectors.selector import JobPostingSelector
from home_task.transactions.insert import HireStatisticsInsert


class CLI:

    def __init__(self, threshold):
        self.threshold = threshold
        self.session = get_session()
        self.jp_selector = JobPostingSelector(self.session)
        self.hire_statistics = HireStatisticsInsert(self.session)

    def start_flow(self):

        for value in self.jp_selector.query(
            job_posting_threshold=self.threshold, is_batch=True
        ):

            self.hire_statistics.insert(value)

        self.session.commit()
