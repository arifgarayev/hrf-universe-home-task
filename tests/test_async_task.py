import sys

sys.path.insert(0, "/Users/arifgarayev/hrf-universe-home-task/")
import json

from home_task.db import get_session
from home_task.selectors.selector import JobPostingSelector
from home_task.tasks.tasks import insert_hire_statistics
from home_task.transactions.insert import HireStatisticsInsert

db_session = get_session()

selector = JobPostingSelector(db_session)
insert = HireStatisticsInsert(db_session)


generator = selector.query(job_posting_threshold=0, is_batch=True)


selected_result = next(generator)

json_serialized = json.dumps(selected_result, default=str)

# print("JSON SERIALIZED", json_serialized, type(json_serialized))
# print("INSERTING STATS", json.loads(json_serialized), type(json.loads(json_serialized)))
insert_hire_statistics.delay(json_serialized)
