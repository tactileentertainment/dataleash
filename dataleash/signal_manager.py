from datetime import datetime, timedelta
from croniter import croniter
from multiprocessing.dummy import Pool as ThreadPool
from itertools import compress


class SignalManager:
    def __init__(self, connector, signals):
        self.pool = ThreadPool(10)
        self.last_update = datetime.now() - timedelta(seconds=60)
        self.connector = connector
        self.signals = signals

    def __check_and_update_signal(self, timestamp, signal):
        connector = self.connector.clone()
        cron = croniter(signal['frequency'], timestamp - timedelta(minutes=1))
        if timestamp != cron.get_next(datetime):
            return False

        result = connector.query(signal['query'])

        for column in result:
            value = result[column][0] if len(result[column]) > 0 else 0
            connector.append_signal_metric(timestamp, signal['name'], column, value)
        return True

    def update_signals(self):
        start = datetime.now()
        if (start - self.last_update).seconds >= 60:
            timestamp = datetime.now().replace(second=0, microsecond=0)
            execution = self.pool.map(lambda signal: self.__check_and_update_signal(timestamp, signal), self.signals)
            updated_signals = list(set(map(lambda a: a['name'], list(compress(self.signals, execution)))))

            if len(updated_signals) > 0:
                self.last_update = start

            return updated_signals
        else:
            return []
