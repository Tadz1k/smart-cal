# -*- coding: utf-8 -*-

from Google_Integration import Google_Integration
from Models.Event import Event
from datetime import datetime, timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta

INTEGRATION = Google_Integration()


def parse_datetime(datetime_str):
    #check if datetime_str is in format dd.mm.yyyy hh:mm
    if len(datetime_str) == 16:
        return datetime.strptime(datetime_str, "%d.%m.%Y %H:%M")
    return None

def get_events():
    events_list = []
    for item in INTEGRATION.get_events():
        #check if event has key 'location'
        if "location" in item:
            location = item["location"]
        else:
            location = ""
        e = Event(item["summary"], item['start'], item['end'], location)
        events_list.append(e)
    return events_list

def add_event(event):
    INTEGRATION.add_event(event)
    
def parse_event(event):
    name = event.name

    # Parsowanie daty i czasu z formatu ISO 8601
    start_datetime = parser.parse(event.start_time['dateTime'])
    end_datetime = parser.parse(event.end_time['dateTime'])

    # Odejmowanie 1 miesiąca
    start_datetime -= relativedelta(months=1)
    end_datetime -= relativedelta(months=1)

    # Formatowanie daty i godziny
    start_date = start_datetime.strftime("%Y-%m-%d")
    start_time = start_datetime.strftime("%H:%M")
    end_date = end_datetime.strftime("%Y-%m-%d")
    end_time = end_datetime.strftime("%H:%M")

    location = event.location
    if 'http' in location:
        location = 'online'
    return {'Date': start_date, 'Title': f'{start_time} {name}, {location}'}
    
