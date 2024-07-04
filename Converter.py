from dataclasses import asdict
import pandas as pd
import pm4py

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
        event_list = []
        for event in model.events:
            event_dict = {
                'concept:name': event.activity,
                'time:timestamp': event.timestamp,
                'case:concept:name': event.call_id,
                'vru_line': event.vru_line,
                'customer_id': event.customer_id,
                'priority': event.priority,
                'type': event.type,
                'vru_time': event.vru_time,
                'q_time': event.q_time,
                'ser_time': event.ser_time,
                'server': event.server
            }
            event_list.append(event_dict)

        log = pm4py.format_dataframe(
            pm4py.convert_to_dataframe(event_list),
            case_id='case:concept:name',
            activity_key='concept:name',
            timestamp_key='time:timestamp'
        )

        pm4py.write_xes(log, path)
        print(f"XES file exported to {path}")
