import pandas as pd
import streamlit as st
from auth import show_auth_screen

from task_utils import (
    DEFAULT_TASKS,
    analyze_tasks,
    create_task,
    load_css,
    load_tasks_from_file,
    save_tasks_to_file,
)

from database import (
    load_tasks_from_db,
    add_task_to_db,
    update_task_in_db,
    delete_task_from_db,
)

def add_task(title, status, priority, minutes, is_scary=False):
    new_task = create_task(title, status, priority, minutes, is_scary)
    st.session_state.tasks.append(new_task)


def remove_task(task_index):
    st.session_state.tasks.pop(task_index)


st.set_page_config(page_title="Task Tracker", page_icon="📝", layout="wide")

if "user" not in st.session_state:
    show_auth_screen()
    st.stop()

current_user_id = st.session_state.user["id"]

st.markdown(load_css(), unsafe_allow_html=True)

st.session_state.tasks = load_tasks_from_db(current_user_id)
tasks = st.session_state.tasks

st.title("📝 Task Tracker")
st.caption("A small Streamlit app for tracking tasks, priorities, and time.")


with st.sidebar:
    if "user" in st.session_state:
        st.caption(f"Logged in as: {st.session_state.user['username']}")

        if st.button("Log out"):
            del st.session_state.user
            st.rerun()

    st.header("Add new task")

    with st.form("add_task_form", clear_on_submit=True):
        title = st.text_input("Task title")
        status = st.selectbox("Status", ["planned", "done"])
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
        minutes = st.number_input("Minutes", min_value=1, step=5, value=30)
        is_scary = st.checkbox("This task is scary")

        submitted = st.form_submit_button("Add task")

        if submitted:
            if title.strip() == "":
                st.error("Please enter a task title.")
            else:
                add_task_to_db(
                    title=title,
                    status=status,
                    priority=priority,
                    minutes=int(minutes),
                    is_scary=is_scary,
                    user_id=current_user_id,
                )

                st.session_state.tasks = load_tasks_from_db(current_user_id)
                st.success(f"Added task: {title}")
                st.rerun()

    st.divider()

    st.header("Save / load")

    if st.button("Save tasks"):
        save_tasks_to_file(st.session_state.tasks)
        st.success("Tasks saved to tasks.csv.")

    if st.button("Load tasks"):
        st.session_state.tasks = load_tasks_from_file()
        st.success("Tasks loaded.")

    if st.button("Reset to default tasks"):
        st.session_state.tasks = DEFAULT_TASKS.copy()
        st.warning("Tasks reset to default.")


tasks = st.session_state.tasks
result = analyze_tasks(tasks)

col1, col2, col3 = st.columns(3)

col1.metric("Total minutes", result["total_minutes"])
col2.metric("Done minutes", result["done_minutes"])
col3.metric("Planned minutes", result["planned_minutes"])

main_col, side_col = st.columns([2.4, 1], gap="small")

with main_col:
    st.subheader("Current tasks")

    if len(tasks) == 0:
        st.info("No tasks yet.")
    else:
        for index, task in enumerate(tasks):
                with st.container(border=True):

                    st.markdown(f"**{task['title']}**")

                    scary_text = "🕯️ scary" if task.get("is_scary") == True else "not scary"

                    st.markdown(
                        f"<span class='task-caption'>{task['status']} · {task['priority']} · {task['minutes']} min · {scary_text}</span>",
                        unsafe_allow_html=True,
                    )

                    st.markdown("<div style='height: 0.7rem;'></div>", unsafe_allow_html=True)

                    if st.button("Edit", key=f"edit_{task['id']}", use_container_width=True):
                        st.session_state.editing_task_index = index
                        st.rerun()

                    if st.button("Del", key=f"delete_{task['id']}", use_container_width=True):
                        deleted_title = task["title"]

                        delete_task_from_db(task["id"], current_user_id)
                        st.session_state.tasks = load_tasks_from_db(current_user_id)

                        if "editing_task_index" in st.session_state:
                            del st.session_state.editing_task_index

                        st.success(f"Deleted task: {deleted_title}")
                        st.rerun()

                if st.session_state.get("editing_task_index") == index:
                    st.markdown("#### Edit task")

                    with st.form(f"edit_task_form_{task['id']}"):
                        edited_title = st.text_input(
                            "Task title",
                            value=task["title"],
                                key=f"edit_title_{task['id']}"
                        )

                        edited_status = st.selectbox(
                            "Status",
                            ["planned", "done"],
                            index=["planned", "done"].index(task["status"]),
                            key=f"edit_status_{task['id']}"
                        )

                        edited_priority = st.selectbox(
                            "Priority",
                            ["low", "medium", "high"],
                            index=["low", "medium", "high"].index(task["priority"]),
                            key=f"edit_priority_{task['id']}"
                        )

                        edited_minutes = st.number_input(
                            "Minutes",
                            min_value=1,
                            step=5,
                            value=int(task["minutes"]),
                            key=f"edit_minutes_{task['id']}"
                        )

                        edited_is_scary = st.checkbox(
                                "This task is scary",
                                value=task.get("is_scary", False),
                                key=f"edit_is_scary_{task['id']}"
                            )

                        save_changes = st.form_submit_button("Save changes")
                        cancel_edit = st.form_submit_button("Cancel")
                        if cancel_edit:
                            if "editing_task_index" in st.session_state:
                                del st.session_state.editing_task_index
                            st.rerun()

                        if save_changes:
                            if edited_title.strip() == "":
                                st.error("Please enter a task title.")
                            else:
                                update_task_in_db(
                                    task_id=task["id"],
                                    title=edited_title,
                                    status=edited_status,
                                    priority=edited_priority,
                                    minutes=int(edited_minutes),
                                    is_scary=edited_is_scary,
                                    user_id=current_user_id,
                                )

                                st.session_state.tasks = load_tasks_from_db(current_user_id)

                                if "editing_task_index" in st.session_state:
                                    del st.session_state.editing_task_index

                                st.success("Task updated.")
                                st.rerun()
                                    
with side_col:
    st.subheader("Quick summary")

    st.markdown(
        f"""
        <div class="summary-card">
            <div class="summary-row">
                <span>Total tasks</span>
                <strong>{len(tasks)}</strong>
            </div>
            <div class="summary-row">
                <span>Done</span>
                <strong>{result["by_status"].get("done", 0)}</strong>
            </div>
            <div class="summary-row">
                <span>Planned</span>
                <strong>{result["by_status"].get("planned", 0)}</strong>
            </div>
            <div class="summary-row">
                <span>High priority</span>
                <strong>{result["by_priority"].get("high", 0)}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

task_lists_col, empty_col = st.columns([2.7, 1], gap="medium")

with task_lists_col:
    st.subheader("Task lists")

    list_col1, list_col2, list_col3 = st.columns(3)

    with list_col1:
        st.markdown("#### Done")

        if len(result["done_tasks"]) == 0:
            st.caption("No completed tasks yet.")
        else:
            for title in result["done_tasks"]:
                st.write(f"✅ {title}")

    with list_col2:
        st.markdown("#### Planned")

        if len(result["planned_tasks"]) == 0:
            st.caption("No planned tasks yet.")
        else:
            for title in result["planned_tasks"]:
                st.write(f"📝 {title}")

    with list_col3:
        st.markdown("#### Important")

        if len(result["important_tasks"]) == 0:
            st.caption("No high-priority tasks yet.")
        else:
            for title in result["important_tasks"]:
                st.write(f"⭐ {title}")

st.caption("Data is saved automatically to tasks.csv after adding, editing, or deleting tasks.")