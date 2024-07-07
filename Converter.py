from dataclasses import asdict
import pandas as pd
import pm4py
from pm4py.objects.conversion.log import converter as log_converter


from ProcessModel import ProcessModel


class ConverterInterface():
    def convert(self, model: ProcessModel):
        ''' Convert and export file out of model '''
        pass


class CsvConverter(ConverterInterface):
    def convert(self, path, model: ProcessModel):
        df = pd.DataFrame.from_records(
            [asdict(event) for event in model.events])
        df.to_csv(path)


class XesConverter(ConverterInterface):
    def convert(self, path, model: ProcessModel):
        df = pd.DataFrame.from_records(
            [asdict(event) for event in model.events])

        df.columns = ['case:concept:name', 'time:timestamp', 'concept:name']
        df['time:timestamp'] = pd.to_datetime(df['time:timestamp'], yearfirst=True)
        df['concept:name'] = df['concept:name'].astype(str)

        df = pm4py.format_dataframe(df, case_id='case:concept:name',
                                    activity_key='concept:name', timestamp_key='time:timestamp')
        event_log = pm4py.convert_to_event_log(df)

        pm4py.write_xes(event_log, path)
        print(f"XES file exported to {path}")
