# Task Tracker 📝

A small Streamlit app for tracking tasks, priorities, time, and task status.

This project started as a console-based Python task tracker and was later rebuilt as a multi-page Streamlit app with CSV storage and a simple notebook-style interface.

## Features

- Add new tasks
- Edit existing tasks
- Delete tasks
- Track task status: `planned` / `done`
- Track task priority: `low` / `medium` / `high`
- Track estimated minutes
- Save tasks to `tasks.csv`
- Load tasks from CSV
- Basic protection against broken or incomplete CSV files
- Multi-page Streamlit layout:
  - Main dashboard
  - Completed Tasks
  - Scary Tasks
  - Task Dump

## Pages

### Main dashboard

Shows all tasks, total minutes, done minutes, planned minutes, and a quick summary.

### Completed Tasks

Shows completed tasks separately.

### Scary Tasks

A page for tasks that feel uncomfortable, annoying, or scary.  
Includes a small lottery feature that can randomly choose one scary task.

### Task Dump

A quick place for small planned tasks that take around 5–10 minutes.

## Tech stack

- Python
- Streamlit
- pandas
- CSV storage
- Custom CSS

## Project structure

```text
task_tracker/
│
├── app.py
├── task_utils.py
├── style.css
├── tasks.csv
├── requirements.txt
│
└── pages/
    ├── 1_Scary_Tasks.py
    ├── 2_Completed_Tasks.py
    └── 3_Task_Dump.py
```

## How to run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

## Future improvements

- Add filters by status and priority
- Improve the summary section
- Add download backup button
- Add tests for utility functions
- Add more polished UI for task cards
- Deploy to Streamlit Cloud

## Status

Work in progress.  
The app is functional locally and is being improved step by step.
