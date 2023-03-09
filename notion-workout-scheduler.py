#-*- coding: utf-8 -*-

import os
import pprint
from datetime import datetime, timedelta
from notion_client import Client

# authenticate to Notion API
notion = Client(auth="<API Key>")

# set up database details
database_id = "Database ID"

# set up schedule details
start_days_ago = 21
end_days_after = 21
days_of_week = {
    "Monday": {"name": "DAY 1", "tag": ["chest", "triceps"]},
    "Tuesday": {"name": "DAY 2", "tag": ["back", "biceps"]},
    "Wednesday": {"name": "DAY 3", "tag": ["lower body", "shoulder"]},
    "Thursday": {"name": "DAY 1", "tag": ["chest", "triceps"]},
    "Friday": {"name": "DAY 2", "tag": ["back", "biceps"]},
    "Saturday": {"name": "DAY 3", "tag": ["lower body", "shoulder"]},
}

# get today's date
today = datetime.now().strftime("%Y-%m-%d")

# get start and end dates for schedule
start_date = (datetime.now() - timedelta(days=start_days_ago)).strftime("%Y-%m-%d")
end_date = (datetime.now() + timedelta(days=end_days_after)).strftime("%Y-%m-%d")

# query the database for existing events within the schedule date range
existing_events = notion.databases.query(
    **{
        "database_id": database_id,
        "filter": {
            "and": [
                {"property": "Date", "date": {"on_or_after": start_date}},
                {"property": "Date", "date": {"on_or_before": end_date}},
            ]
        },
    }
).get("results")

# create new events for each day of the week within the schedule date range
for date in (datetime.now() + timedelta(days=n) for n in range(-start_days_ago, end_days_after + 1)):
    # skip Sundays
    if date.strftime("%A") == "Sunday":
        continue

    # check if event already exists on this date
    if any(event.get("properties").get("Date").get("date").get("start") == date.strftime("%Y-%m-%d") for event in existing_events):
        print(f"Event already exists for {date.strftime('%Y-%m-%d')}. Skipping.")
        continue

    # create new event for this date
    day_of_week = date.strftime("%A")
    event_name = days_of_week[day_of_week]["name"]
    event_tag = days_of_week[day_of_week]["tag"]
    new_event = {
        "Name": {"title": [{"text": {"content": event_name}}]},
        "Date": {"date": {"start": date.strftime("%Y-%m-%d")}},
        "Tag": {"multi_select": [{"name": tag} for tag in event_tag]},
    }
    notion.pages.create(parent={"database_id": database_id}, properties=new_event)
    print(f"Created event for {date.strftime('%Y-%m-%d')} - {event_name} ({', '.join(event_tag)})")

