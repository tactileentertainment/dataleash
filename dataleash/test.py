from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta


class Test:
    __metaclass__ = ABCMeta

    def __init__(self, name, signals, min_timestamp=datetime.now() - timedelta(days=30), max_timestamp=datetime.now()):
        self.name = name
        self.signals = signals
        self.min_timestamp = min_timestamp
        self.max_timestamp = max_timestamp

    def run(self, connector, updated_signals):
        connector = connector.clone()
        if len(list(set(self.signals) & set(updated_signals))) > 0:
            timestamp = datetime.now()
            dataframe = connector.get_signals(self.signals, self.min_timestamp, self.max_timestamp)
            result, error = self._test(dataframe)
            connector.append_test_result(timestamp, self.name, result, error)

    @abstractmethod
    def _test(self, dataframe):
        return True, None
