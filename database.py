import streamlit as st
import psycopg
from psycopg.rows import dict_row


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