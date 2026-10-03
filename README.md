# **Workout Schedule Automation with Notion API**

This Python script uses the Notion API to create a workout schedule in a Notion database.

## **Blog posts**

- 2026 (current code): [Automating Workout Scheduling with Notion API (2026)](https://hobbyworker.me/en/dev/2026-10-06-automating-workout-scheduling-with-notion-api-2026/) (published on 2026-10-06)
- 2023 (code at the [`v2023`](https://github.com/hobbyworker/notion-workout-scheduler/tree/v2023) tag): [Automating Workout Scheduling with Notion API](https://hobbyworker.me/en/dev/2023-03-14-automating-workout-scheduling-with-notion-api/)

## **Versions**

| Tag | notion-client | Notion API version | Post |
|---|---|---|---|
| `v2026` | 3.1.0 | 2025-09-03 | 2026 |
| `v2023` | 2.0.0 | 2022-06-28 | 2023 |

Notion API version 2025-09-03 split databases into data sources. notion-client 2.6.0 and later follow it and no longer have `databases.query`, so the 2023 code only runs with the old version pinned at the `v2023` tag.

## **Prerequisites**

- A Notion account
- Python 3.11 or later
- A Notion database with these properties:
    - Name: Title
    - Date: Date
    - Tag: Multi-select
- A token, either of:
    - A [personal access token](https://www.notion.so/developers/tokens) with the Notion API capability. It uses your own permissions, so you don't need to share the database with anything.
    - An internal connection's API token. Share the database with the connection from the database's **•••** menu → **Add connections**.

## **Usage**

```bash
pip install -r requirements.txt

export NOTION_TOKEN="your-token"
export NOTION_DATABASE_ID="your-database-id"
# Optional: pick a data source when the database has more than one
# export NOTION_DATA_SOURCE_ID="your-data-source-id"

python notion-workout-scheduler.py
```

Edit **`START_DAYS_AGO`**, **`END_DAYS_AFTER`**, and **`DAYS_OF_WEEK`** in the script to match your workout plan. The script creates an event for each day in the range that has a plan and no event yet.

## **Testing**

Last checked on 2026-10-03 with Python 3.11 and 3.13 against a local mock of the Notion API (request paths, headers, request bodies, and pagination). It has not been run against a real Notion workspace yet.

## **License**

This code snippet is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
