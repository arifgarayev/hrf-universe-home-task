import sys
sys.path.insert(0, '/Users/arifgarayev/hrf-universe-home-task/')

from home_task.selectors.selector import JobPostingSelector
from home_task.models import HireStatistics
from home_task.db import get_session


db_session_selector = get_session()
selector = JobPostingSelector(db_session_selector)

generator = selector.query(job_posting_threshold=0, is_batch=True)

# print(HireStatistics(**next(generator)[0]))
