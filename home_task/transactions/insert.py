from home_task.models import HireStatistics


class HireStatisticsInsert:
    def __init__(self, db_session):
        self.db_session = db_session

    def insert(self, stats: list[dict]):
        
        stats_model = [HireStatistics(**s) for s in stats]
        self.db_session.bulk_save_objects(stats_model)
        # trans = self.db_session.get_transaction()
        # if trans:
        #     print(trans.origin)

        # print(self.db_session.in_transaction())
        # # self.db_session.add_all(stats_model)
        # print(self.db_session.in_transaction())
        # return stats_model
    
