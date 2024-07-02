import pandas as pd
import os

from pm4py.objects.conversion.log import converter as log_converter
import pm4py

class Parser():
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.data = None

    def process(self):
        for idx, file in enumerate(os.listdir(self.folder_path)):
            if idx == 0:
                self.data = pd.read_csv(self.folder_path + file, sep='\t')
            else:
                df = pd.read_csv(self.folder_path + file, sep='\t')
                self.data = pd.concat([self.data, df])

    def to_xes(self):
        data = self.data.copy()

        cols = ['', 'concept:name', 'lifecycle:transition', 'Event ID','time:timestamp','case:concept:name']
        data.columns = cols
        data['time:timestamp'] = pd.to_datetime(data['time:timestamp'])
        data['concept:name'] = data['concept:name'].astype(str)

        log = log_converter.apply(data, variant=log_converter.Variants.TO_EVENT_LOG)
        #dataframe = pm4py.format_dataframe(dataframe, case_id_column='case:concept:name', activity_column='lifecycle:transition', timestamp_column='time:timestamp')
        #log = pm4py.convert_to_event_log(dataframe)
        pm4py.write_xes(log, '1.xes', case_id_key='case:concept:name')

    def to_csv(self, path):
        self.data.to_csv(path)