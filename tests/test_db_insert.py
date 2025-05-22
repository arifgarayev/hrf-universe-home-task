import sys
sys.path.insert(0, '/Users/arifgarayev/hrf-universe-home-task/')

from home_task.selectors.selector import JobPostingSelector
from home_task.transactions.insert import HireStatisticsInsert
from home_task.db import get_session


db_session_selector = get_session()
db_session_insert = get_session()
selector = JobPostingSelector(db_session_selector)
insert = HireStatisticsInsert(db_session_insert)

generator = selector.query(job_posting_threshold=0, is_batch=True)
selected_result = next(generator)
insert_result = insert.insert(selected_result)
print(insert_result)

