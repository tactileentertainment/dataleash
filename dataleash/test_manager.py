from multiprocessing.dummy import Pool as ThreadPool


class TestManager:
    def __init__(self, connector, tests):
        self.connector = connector
        self.pool = ThreadPool(10)
        self.tests = tests

    def run_tests(self, updated_signals):
        self.pool.map(lambda test: test.run(self.connector, updated_signals), self.tests)
