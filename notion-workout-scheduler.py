"""Create a workout schedule in a Notion database.

Uses Notion API version 2025-09-03 (data sources) with notion-client 3.x.

Environment variables:
  NOTION_TOKEN           Personal access token, or an internal connection's API token
  NOTION_DATABASE_ID     ID of the database (from the database URL)
  NOTION_DATA_SOURCE_ID  (optional) ID of the data source to use.
                         Defaults to the first data source in the database.
"""
import os
from datetime import date, timedelta

from notion_client import Client
from notion_client.helpers import collect_paginated_api

NOTION_VERSION = "2025-09-03"

# Schedule details
START_DAYS_AGO = 21
END_DAYS_AFTER = 21
WEEKDAY_NAMES = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
DAYS_OF_WEEK = {
    "Monday": {"name": "DAY 1", "tag": ["chest", "triceps"]},
    "Tuesday": {"name": "DAY 2", "tag": ["back", "biceps"]},
    "Wednesday": {"name": "DAY 3", "tag": ["lower body", "shoulder"]},
    "Thursday": {"name": "DAY 1", "tag": ["chest", "triceps"]},
    "Friday": {"name": "DAY 2", "tag": ["back", "biceps"]},
    "Saturday": {"name": "DAY 3", "tag": ["lower body", "shoulder"]},
    # Sunday is a rest day.
}


def get_data_source_id(notion, database_id):
    """Return the data source to write to. A database can hold several data sources."""
    data_source_id = os.environ.get("NOTION_DATA_SOURCE_ID")
    if data_source_id:
        return data_source_id
    database = notion.databases.retrieve(database_id=database_id)
    return database["data_sources"][0]["id"]


def get_existing_dates(notion, data_source_id, start, end):
    """Return the dates that already have an event between start and end."""
    pages = collect_paginated_api(
        notion.data_sources.query,
        data_source_id=data_source_id,
        filter={
            "and": [
                {"property": "Date", "date": {"on_or_after": start.isoformat()}},
                {"property": "Date", "date": {"on_or_before": end.isoformat()}},
            ]
        },
    )
    dates = set()
    for page in pages:
        value = page["properties"]["Date"]["date"]
        if value:
            dates.add(value["start"][:10])  # "2026-10-05" or "2026-10-05T09:00:00.000+09:00"
    return dates


def main():
    notion = Client(auth=os.environ["NOTION_TOKEN"], notion_version=NOTION_VERSION)
    data_source_id = get_data_source_id(notion, os.environ["NOTION_DATABASE_ID"])

    today = date.today()
    start = today - timedelta(days=START_DAYS_AGO)
    end = today + timedelta(days=END_DAYS_AFTER)
    existing_dates = get_existing_dates(notion, data_source_id, start, end)

    for offset in range(-START_DAYS_AGO, END_DAYS_AFTER + 1):
        day = today + timedelta(days=offset)
        plan = DAYS_OF_WEEK.get(WEEKDAY_NAMES[day.weekday()])
        if plan is None:
            continue
        if day.isoformat() in existing_dates:
            print(f"Event already exists for {day}. Skipping.")
            continue

        notion.pages.create(
            parent={"type": "data_source_id", "data_source_id": data_source_id},
            properties={
                "Name": {"title": [{"text": {"content": plan["name"]}}]},
                "Date": {"date": {"start": day.isoformat()}},
                "Tag": {"multi_select": [{"name": tag} for tag in plan["tag"]]},
            },
        )
        print(f"Created event for {day} - {plan['name']} ({', '.join(plan['tag'])})")


if __name__ == "__main__":
    main()
