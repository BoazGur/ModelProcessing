from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class Event():
    case_id: str
    timestamp: datetime
    activity: str


@dataclass
class ProcessModel():
    events: List[Event] = field(default_factory=list)
    headers: List[str] = field(default_factory=list)


class ProcessModelParser():

    def __init__(self):
        self.headers = None
        self.model = ProcessModel()

    def parse_headers(self, header_line):
        self.headers = header_line.strip().split('\t')
        self.model.headers = self.headers

    def parse_line(self, line):
        if not self.headers:
            raise Exception('Headers must be parsed first')
        
        values = line.strip().split('\t')
        if len(values) != len(self.headers):
            return None, None, None, None
        
        if values == self.headers:
            return None, None, None, None

        event_dict = dict(zip(self.headers, values))

        date = datetime.strptime(event_dict['date'], '%y%m%d').date()

        time = datetime.strptime(event_dict['vru_entry'], '%H:%M:%S').time()
        timestamp_priority = datetime.combine(date, time)

        time = datetime.strptime(event_dict['vru_entry'], '%H:%M:%S').time()
        timestamp_type = datetime.combine(date, time)

        time = datetime.strptime(event_dict['vru_exit'], '%H:%M:%S').time()
        timestamp_outcome = datetime.combine(date, time)

        if event_dict['ser_start'] == '00:00:00':
            time = datetime.strptime('23:59:59', '%H:%M:%S').time()
        else:
            time = datetime.strptime(event_dict['ser_start'], '%H:%M:%S').time()

        timestamp_server = datetime.combine(date, time)

        server_activity = 'SERVER' if event_dict['server'] != 'NO_SERVER' else 'NO_SERVER'

        event_priority = Event(
            case_id=event_dict['call_id'],
            timestamp=timestamp_priority,
            activity=event_dict['priority']
        )

        event_type = Event(
            case_id=event_dict['call_id'],
            timestamp=timestamp_type,
            activity=event_dict['type']
        )

        event_outcome = Event(
            case_id=event_dict['call_id'],
            timestamp=timestamp_outcome,
            activity=event_dict['outcome']
        )

        event_server = Event(
            case_id=event_dict['call_id'],
            timestamp=timestamp_server,
            activity=server_activity
        )

        if event_outcome.activity == 'HANG':
            event_server = None
        
        time = datetime.strptime('00:00:00', '%H:%M:%S').time()
        if timestamp_server == datetime.combine(date, time):
            event_server = None

        if (event_outcome is not None) and ((event_outcome.timestamp < event_priority.timestamp) or (event_outcome.timestamp < event_type.timestamp)):
            return None, None, None, None

        if (event_server is not None) and ((event_server.timestamp < event_priority.timestamp) or (event_server.timestamp < event_type.timestamp) or (event_server.timestamp < event_outcome.timestamp)):
            return None, None, None, None

        return event_priority, event_type, event_outcome, event_server

    def add_event(self, event):
        self.model.events.append(event)
    
    def get_model(self):
        return self.model