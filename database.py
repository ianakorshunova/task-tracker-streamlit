import streamlit as st
import psycopg
from psycopg.rows import dict_row
import datetime as dt


def get_connection():
    return psycopg.connect(
        st.secrets["DATABASE_URL"],
        row_factory=dict_row,
    )


def load_tasks_from_db(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, title, status, priority, minutes, is_scary, user_id
                FROM tasks
                WHERE user_id = %s
                ORDER BY id;
                """,
                (user_id,),
            )
            return cur.fetchall()


def add_task_to_db(title, status, priority, minutes, is_scary, user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tasks (title, status, priority, minutes, is_scary, user_id)
                VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (title, status, priority, minutes, is_scary, user_id),
            )


def update_task_in_db(task_id, title, status, priority, minutes, is_scary, user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE tasks
                SET title = %s,
                    status = %s,
                    priority = %s,
                    minutes = %s,
                    is_scary = %s
                WHERE id = %s AND user_id = %s;
                """,
                (title, status, priority, minutes, is_scary, task_id, user_id),
            )


def delete_task_from_db(task_id, user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM tasks
                WHERE id = %s AND user_id = %s;
                """,
                (task_id, user_id),
            )

def reset_demo_tasks(user_id):
    today = dt.date.today()
    week_start = today - dt.timedelta(days=today.weekday())

    demo_tasks = [
        ("Clean up legacy CSV code", "done", "high", 60, False),
        ("Prepare portfolio README", "planned", "high", 45, False),
        ("Review Streamlit demo mode", "done", "medium", 30, False),
        ("Send client invoice", "planned", "medium", 15, False),
        ("Apply for localization role", "planned", "high", 40, True),
        ("Organize task backlog", "planned", "low", 25, False),
        ("Test mobile layout", "planned", "medium", 20, True),
    ]

    demo_week_goals = [
        ("Practice Python", 5, 0, "days"),
        ("Update portfolio", 3, 1, "sessions"),
        ("Apply for jobs", 3, 0, "applications"),
        ("Study Chinese", 4, 0, "days"),
        ("Take a proper break", 2, 0, "times"),
    ]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM tasks
                WHERE user_id = %s;
                """,
                (user_id,),
            )

            cur.executemany(
                """
                INSERT INTO tasks (title, status, priority, minutes, is_scary, user_id)
                VALUES (%s, %s, %s, %s, %s, %s);
                """,
                [
                    (title, status, priority, minutes, is_scary, user_id)
                    for title, status, priority, minutes, is_scary in demo_tasks
                ],
            )

            cur.execute(
                """
                DELETE FROM week_goals
                WHERE user_id = %s;
                """,
                (user_id,),
            )

            cur.executemany(
                """
                INSERT INTO week_goals (
                    title, target_count, current_count, unit, week_start, user_id
                )
                VALUES (%s, %s, %s, %s, %s, %s);
                """,
                [
                    (title, target_count, current_count, unit, week_start, user_id)
                    for title, target_count, current_count, unit in demo_week_goals
                ],
            )

def load_week_goals_from_db(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, user_id, title, target_count, current_count, unit, week_start
                FROM week_goals
                WHERE user_id = %s
                ORDER BY id;
                """,
                (user_id,),
            )
            return cur.fetchall()


def add_week_goal_to_db(title, target_count, unit, week_start, user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO week_goals (title, target_count, current_count, unit, week_start, user_id)
                VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (title, target_count, 0, unit, week_start, user_id),
            )


def update_week_goal_in_db(goal_id, title, target_count, current_count, unit, week_start, user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE week_goals
                SET title = %s,
                    target_count = %s,
                    current_count = %s,
                    unit = %s,
                    week_start = %s
                WHERE id = %s AND user_id = %s;
                """,
                (
                    title,
                    target_count,
                    current_count,
                    unit,
                    week_start,
                    goal_id,
                    user_id,
                ),
            )


def increment_week_goal_in_db(goal_id, user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE week_goals
                SET current_count = current_count + 1
                WHERE id = %s AND user_id = %s;
                """,
                (goal_id, user_id),
            )


def delete_week_goal_from_db(goal_id, user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM week_goals
                WHERE id = %s AND user_id = %s;
                """,
                (goal_id, user_id),
            )