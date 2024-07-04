from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class Event():
    vru_line: str
    call_id: str
    customer_id: str
    priority: int
    type: str
    timestamp: datetime
    vru_time: int
    q_time: int
    activity: str
    ser_time: int
    server: str


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
            return None
        
        if values == self.headers:
            return None

        event_dict = dict(zip(self.headers, values))

        date = datetime.strptime(event_dict['date'], '%y%m%d').date()
        time = datetime.strptime(event_dict['vru_entry'], '%H:%M:%S').time()
        timestamp = datetime.combine(date, time)

        if event_dict['outcome'] == 'AGENT':
            activity = 'Call Handled'
        elif event_dict['outcome'] == 'HANG':
            activity = 'Call Abandoned'
        elif event_dict['outcome'] == 'PHANTOM':
            activity = 'Call Ignored'

        return Event(
            vru_line=event_dict['vru+line'],
            call_id=event_dict['call_id'],
            customer_id=event_dict['customer_id'],
            priority=int(event_dict['priority']),
            type=event_dict['type'],
            timestamp=timestamp,
            vru_time=int(event_dict['vru_time']),
            q_time=int(event_dict['q_time']),
            activity=activity,
            ser_time=int(event_dict['ser_time']),
            server=event_dict['server']
        )

    def add_event(self, event):
        self.model.events.append(event)
    
    def get_model(self):
        return self.model