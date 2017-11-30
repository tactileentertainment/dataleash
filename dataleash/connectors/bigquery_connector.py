from dataleash.connector import Connector
from pandas_bigquery import Bigquery
from datetime import datetime
import pandas as pd
import os


class BigqueryConnector(Connector):
    def __init__(self, project_id=os.getenv('BIGQUERY_PROJECT'),
                 private_key_path=os.getenv('BIGQUERY_KEY_PATH'),
                 dataset='dataleash',
                 signals_table='signals',
                 tests_table='tests'):
        super().__init__()
        self.bigquery = Bigquery(project_id, private_key_path)
        self.project_id = project_id
        self.private_key_path = private_key_path
        self.dataset = dataset
        self.signals_table = signals_table
        self.tests_table = tests_table

        try:
            self.bigquery.datasets.insert(dataset)
        except:
            pass

        try:
            self.bigquery.tables.insert(dataset, signals_table, schema={
                "fields": [{"name": "estimationTime", "type": "TIMESTAMP"},
                           {"name": "signal", "type": "STRING"},
                           {"name": "metric", "type": "STRING"},
                           {"name": "value", "type": "FLOAT"}]
            }, body={'timePartitioning': {'type': 'DAY'}})
        except:
            pass

        try:
            self.bigquery.datasets.insert(dataset)
        except:
            pass

        try:
            self.bigquery.tables.insert(dataset, tests_table, schema={
                "fields": [{"name": "estimationTime", "type": "TIMESTAMP"},
                           {"name": "test", "type": "STRING"},
                           {"name": "pass", "type": "BOOLEAN"},
                           {"name": "error", "type": "STRING"}]
            }, body={'timePartitioning': {'type': 'DAY'}})
        except:
            pass

    def query(self, query):
        return self.bigquery.query(query, strict=False)

    def append_test_result(self, timestamp, test_name, passed, error):
        dataframe = pd.DataFrame(
            {'estimationTime': [timestamp],
             'test': [test_name],
             'pass': [passed],
             'error': [error]})
        return self.bigquery.upload(dataframe,
                                    f"{self.dataset}.{self.tests_table}${datetime.now().strftime('%Y%m%d')}",
                                    if_exists='append')

    def append_signal_metric(self, timestamp, signal_name, metric, value):
        dataframe = pd.DataFrame(
            {'estimationTime': [timestamp],
             'signal': [signal_name],
             'metric': [metric],
             'value': [float(value)]})
        return self.bigquery.upload(dataframe,
                                    f"{self.dataset}.{self.signals_table}${datetime.now().strftime('%Y%m%d')}",
                                    if_exists='append')

    def get_signals(self, signal_names, min_timestamp, max_timestamp):
        signals_string = ",".join(list(map(lambda signal: f"'{signal}'", signal_names)))
        query = f"""select * from {self.dataset}.{self.signals_table}
                                where 
                                signal in ({signals_string}) 
                                and _partitionTime between '{max_timestamp.strftime('%Y-%m-%d')}' 
                                and '{max_timestamp.strftime('%Y-%m-%d')}'"""
        return self.query(query)

    def clone(self):
        return BigqueryConnector(self.project_id, self.private_key_path, self.dataset, self.signals_table,
                                 self.tests_table)
