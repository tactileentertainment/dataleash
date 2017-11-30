from .signal_manager import SignalManager
from .test_manager import TestManager
from time import sleep


class DataLeash:
    def __init__(self, connector, signals, tests):
        self.connector = connector
        self.signals = signals
        self.tests = tests

        self.signal_manager = SignalManager(connector, signals)
        self.test_manager = TestManager(connector, tests)

    def run(self, interval=1):
        while True:
            updated_signals = self.signal_manager.update_signals()
            self.test_manager.run_tests(updated_signals)
            sleep(interval)
