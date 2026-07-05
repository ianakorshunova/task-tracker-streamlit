from pathlib import Path

import pandas as pd

def load_css(file_name="style.css"):
    with open(file_name, "r", encoding="utf-8") as file:
        css = file.read()

    return f"<style>{css}</style>"

def delete_task_by_index(tasks, index):
    if 0 <= index < len(tasks):
        tasks.pop(index)

TASKS_FILE = Path("tasks.csv")

DEFAULT_TASKS = [
    {
        "title": "Python practice",
        "status": "done",
        "priority": "medium",
        "minutes": 30,
        "is_scary": False,
    },
    {
        "title": "SQL practice",
        "status": "planned",
        "priority": "high",
        "minutes": 45,
        "is_scary": False,
    },
    {
        "title": "Global3 AD",
        "status": "done",
        "priority": "high",
        "minutes": 120,
        "is_scary": False,
    },
    {
        "title": "Quizlet QA",
        "status": "planned",
        "priority": "low",
        "minutes": 15,
        "is_scary": False,
    },
    {
        "title": "Lu Ren scene",
        "status": "done",
        "priority": "medium",
        "minutes": 60,
        "is_scary": False,
    },
]

def load_tasks_from_file():
    required_columns = ["title", "status", "priority", "minutes", "is_scary"]

    if not TASKS_FILE.exists():
        return DEFAULT_TASKS.copy()

    try:
        df = pd.read_csv(TASKS_FILE)
    except pd.errors.EmptyDataError:
        return DEFAULT_TASKS.copy()

    # If the file exists but is broken or has wrong columns,
    # restore a safe structure instead of crashing the app.
    for column in required_columns:
        if column not in df.columns:
            if column == "title":
                df[column] = ""
            elif column == "status":
                df[column] = "planned"
            elif column == "priority":
                df[column] = "low"
            elif column == "minutes":
                df[column] = 0
            elif column == "is_scary":
                df[column] = False

    df = df[required_columns]

    # Clean broken / empty rows
    df["title"] = df["title"].fillna("").astype(str)
    df["status"] = df["status"].fillna("planned").astype(str)
    df["priority"] = df["priority"].fillna("low").astype(str)
    df["minutes"] = df["minutes"].fillna(0).astype(int)
    df["is_scary"] = df["is_scary"].fillna(False).astype(bool)

    # Remove rows without a real task title
    df = df[df["title"].str.strip() != ""]

    if len(df) == 0:
        return DEFAULT_TASKS.copy()

    return df.to_dict("records")

def save_tasks_to_file(tasks):
    required_columns = ["title", "status", "priority", "minutes", "is_scary"]

    df = pd.DataFrame(tasks)

    for column in required_columns:
        if column not in df.columns:
            if column == "title":
                df[column] = ""
            elif column == "status":
                df[column] = "planned"
            elif column == "priority":
                df[column] = "low"
            elif column == "minutes":
                df[column] = 0
            elif column == "is_scary":
                df[column] = False

    df = df[required_columns]

    df.to_csv(TASKS_FILE, index=False)


def analyze_tasks(tasks):
    done_tasks = []
    planned_tasks = []
    important_tasks = []
    scary_tasks = []

    total_minutes = 0
    done_minutes = 0
    planned_minutes = 0

    by_status = {}
    by_priority = {}

    for task in tasks:
        title = task["title"]
        status = task["status"]
        priority = task["priority"]
        minutes = task["minutes"]
        is_scary = task.get("is_scary", False)

        by_status[status] = by_status.get(status, 0) + 1
        by_priority[priority] = by_priority.get(priority, 0) + 1

        total_minutes += minutes

        if status == "done":
            done_tasks.append(title)
            done_minutes += minutes

        if status == "planned":
            planned_tasks.append(title)
            planned_minutes += minutes

        if priority == "high":
            important_tasks.append(title)

        if is_scary:
            scary_tasks.append(title)

    return {
        "done_tasks": done_tasks,
        "planned_tasks": planned_tasks,
        "important_tasks": important_tasks,
        "scary_tasks": scary_tasks,
        "total_minutes": total_minutes,
        "done_minutes": done_minutes,
        "planned_minutes": planned_minutes,
        "by_status": by_status,
        "by_priority": by_priority,
    }


def create_task(title, status, priority, minutes, is_scary=False):
    return {
        "title": title.strip(),
        "status": status,
        "priority": priority,
        "minutes": int(minutes),
        "is_scary": is_scary,
    }
