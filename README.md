# Task Tracker 📝

A small Streamlit app for tracking tasks, priorities, time, and task status.

This project started as a console-based Python task tracker and was later rebuilt as a multi-page Streamlit app with authentication, PostgreSQL storage, and a soft notebook-style interface.

## Live demo

Open the demo app on Streamlit:  
[Live Demo]((https://task-tracker-demo.streamlit.app/))

Demo Mode uses a shared demo workspace. You can add, edit, delete, and reset demo tasks.

## Data privacy note

The demo app is public and uses a shared demo workspace. Data entered in Demo Mode is not private and may be visible to other users.

Please use only test/demo tasks in the public version. Do not enter personal, sensitive, or confidential information.

For private use, run the app locally with your own Streamlit secrets and database connection.

## Features

- User login and registration
- Per-user task storage
- Demo Mode with automatic demo login
- Reset demo data button
- Add new tasks
- Edit existing tasks
- Delete tasks
- Track task status: planned / done
- Track task priority: low / medium / high
- Track estimated minutes
- Mark tasks as scary
- Random scary task picker
- Completed tasks page
- Task dump page for quick small tasks
- Multi-page Streamlit layout
- Custom CSS styling
- PostgreSQL database storage via Neon

## Pages

### Main dashboard

Shows all tasks, total minutes, done minutes, planned minutes, and a quick summary.

### Completed Tasks

Shows completed tasks separately, with summary stats for completed minutes and completed scary tasks.

### Scary Tasks

A page for tasks that feel uncomfortable, annoying, or scary.  
Includes a small lottery feature that can randomly choose one scary task.

### Task Dump

A quick place for small planned tasks that take around 5–10 minutes.

## Tech stack

- Python
- Streamlit
- pandas
- PostgreSQL
- Neon
- psycopg
- bcrypt
- Custom CSS

## Project structure

```text
task_tracker/
│
├── app.py
├── demo_app.py
├── task_app.py
├── auth.py
├── database.py
├── task_utils.py
├── style.css
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

Create a local Streamlit secrets file:

```bash
.streamlit/secrets.toml
```

Example owner mode:

```bash
APP_MODE = "owner"
DATABASE_URL = "your-postgresql-connection-string"
```

Run the owner app:

```bash
streamlit run app.py
```

Run the demo entrypoint:

```bash
streamlit run demo_app.py
```

## Demo mode

Demo mode automatically logs visitors into a shared demo_user workspace.

```bash
APP_MODE = "demo"
```
The demo workspace can be reset with the Reset demo data button.

## Future improvements

- Add filters by status and priority
- Add password change flow
- Add optional demo data auto-reset
- Improve mobile layout
- Add tests for database and utility functions
- Add export/download backup option

## Status

Work in progress.
The app is deployed on Streamlit Cloud and is being improved step by step.
