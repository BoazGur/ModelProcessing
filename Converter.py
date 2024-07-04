from dataclasses import asdict
import pandas as pd
import pm4py
from pm4py.objects.log.obj import EventLog, Trace, Event

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
        log = EventLog()
        for event in model.events:
            trace = Trace()
            xes_event = Event()
            xes_event["concept:name"] = event.activity
            xes_event["time:timestamp"] = event.timestamp
            xes_event["case:concept:name"] = event.call_id
            xes_event["vru_line"] = event.vru_line
            xes_event["customer_id"] = event.customer_id
            xes_event["priority"] = event.priority
            xes_event["type"] = event.type
            xes_event["vru_time"] = event.vru_time
            xes_event["q_time"] = event.q_time
            xes_event["ser_time"] = event.ser_time
            xes_event["server"] = event.server
            trace.append(xes_event)
            log.append(trace)

        pm4py.write_xes(log, path)
        print(f"XES file exported to {path}")
