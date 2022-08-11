from copy import deepcopy
from datetime import datetime
from typing import List, Optional


def update_agromanagement(agromanagement_raw, timed_events):
    agromanagement = deepcopy(agromanagement_raw)
    assert len(agromanagement) == 1
    campaign = agromanagement[0]
    for campaign_start_date, schedule in campaign.items():
        schedule['TimedEvents'] = timed_events
    return agromanagement


def add_irrigation_event(date: str, amount: float, timed_events: List) -> str:
    if timed_events is None:
        timed_events = [
            {
                'event_signal': 'irrigate',
                'name': 'Irrigation application table',
                'comment': 'All irrigation amounts in cm',
                'events_table': []
            }
        ]
    events = deepcopy(timed_events[0])
    events_table = events["events_table"]
    
    event_date = datetime.strptime(date, "%Y-%m-%d").date()
    events_table.append(
        {event_date: {'amount': amount, 'efficiency': 0.7}}
    )
    events["events_table"] = events_table
    return [events]

def get_timed_events(agromanagement) -> Optional[List]:
    assert len(agromanagement) == 1
    campaign = agromanagement[0]
    for campaign_start_date, schedule in campaign.items():
        events_cfg = schedule['TimedEvents']
    return events_cfg

def get_irrigation_events(campaign):
    event_cfgs = []

    for campaign_start_date, schedule in campaign.items():
        events_cfg = schedule['TimedEvents']
        irrigation_events = events_cfg[0]["events_table"]
        event_cfgs.extend(
            parse_irrigation_events(irrigation_events)
        )
    return event_cfgs

def parse_irrigation_events(events):
    event_cfgs = []
    
    for event in events:
        for date, irrigation_water_in_cm in event.items():
            event_cfgs.append((date, irrigation_water_in_cm))
    return event_cfgs


def get_crop_start_date(agromanagement):
    campaign = agromanagement[0]
    for campaign_start_date, schedule in campaign.items():
        break
    return schedule["CropCalendar"]["crop_start_date"]
