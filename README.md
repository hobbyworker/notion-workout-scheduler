# **Workout Schedule Automation with Notion API**

This Python code snippet demonstrates how to use the Notion API to automate the process of creating a workout schedule in a Notion database.

## **Prerequisites**

Before running this code snippet, you will need the following:

- A Notion account
- A Notion API key
- Python 3.x
- The Notion client library, which can be installed via pip:

```bash
pip install notion-client
```

## **Usage**

1. Clone this repository to your local machine.
2. Replace **`<API Key>`** and **`Database ID`** in the code with your Notion API key and database ID, respectively.
3. Modify the **`start_days_ago`**, **`end_days_after`**, and **`days_of_week`** variables to match your workout plan.
4. Run the code.

The code will automatically create a workout schedule for the specified date range and add new events to the Notion database based on the defined workout plan.

If you don't have a database set up in Notion for your workout schedule, follow these steps:

1. Create a new database in Notion.
2. Add the following properties to the database:
    - Name: Title
    - Date: Date
    - Tag: Multi-select

## **License**

This code snippet is licensed under the MIT License. See the **License** file for more information.
