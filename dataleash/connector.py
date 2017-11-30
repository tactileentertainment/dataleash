from abc import ABCMeta, abstractmethod


class Connector():
    __metaclass__ = ABCMeta

    @abstractmethod
    def query(self, query):
        pass

    @abstractmethod
    def append_test_result(self, timestamp, test_name, passed, error):
        pass

    @abstractmethod
    def append_signal_metric(self, timestamp, signal_name, metric, value):
        pass

    @abstractmethod
    def get_signals(self, signal_names, min_timestamp, max_timestamp):
        pass

    @abstractmethod
    def clone(self):
        pass
