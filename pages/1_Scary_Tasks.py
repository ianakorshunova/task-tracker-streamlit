import random

import streamlit as st

from task_utils import create_task, load_css, load_tasks_from_file, save_tasks_to_file

SCARY_DONE_MESSAGES = [
    "You spooked out the spooky task!",
    "The tiny ghost has left the building.",
    "Scary task? Not anymore.",
    "The monster has been defeated.",
    "You bonked the spooky task with a productivity stick.",
    "One brave human, zero scary tasks.",
    "The task screamed and vanished.",
]

st.set_page_config(page_title="Scary Tasks", page_icon="🕯️", layout="wide")

st.markdown(load_css(), unsafe_allow_html=True)

st.title("🕯️ Scary Tasks")
st.caption("For tasks you keep avoiding because they feel uncomfortable, annoying, or scary.")

if "scary_done_message" in st.session_state:
    st.toast(st.session_state.scary_done_message, icon="👻")
    del st.session_state.scary_done_message


if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks_from_file()


tasks = st.session_state.tasks


with st.sidebar:
    st.header("Add scary task")

    with st.form("add_scary_task_form", clear_on_submit=True):
        title = st.text_input("Task title")
        minutes = st.number_input("Minutes", min_value=1, step=5, value=10)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

        submitted = st.form_submit_button("Add scary task")

        if submitted:
            if title.strip() == "":
                st.error("Please enter a task title.")
            else:
                new_task = create_task(
                    title=title,
                    status="planned",
                    priority=priority,
                    minutes=minutes,
                    is_scary=True,
                )

                st.session_state.tasks.append(new_task)
                save_tasks_to_file(st.session_state.tasks)

                st.success(f"Added scary task: {title}")


scary_tasks = [
    task for task in tasks
    if task.get("is_scary") == True and task["status"] == "planned"
]

left_col, right_col = st.columns([3.2, 1])

with right_col:
    st.markdown("<div style='height: 0.7rem;'></div>", unsafe_allow_html=True)
    st.subheader("Scary rules")

    st.markdown(
        """
        - Pick one scary thing.
        - Do not negotiate with the ghost.
        - Tiny progress counts.
        - Done is better than haunted.
        """
    )

    st.info("Lottery rule: when everything feels awful, let the app choose one scary task.")

with left_col:
    st.subheader("Scary task lottery")

    if len(scary_tasks) == 0:
        info_col, empty_col = st.columns([2, 1])
        with info_col:
            st.info("No planned scary tasks yet.")
    else:
        if st.button("Make a choice"):
            st.session_state.chosen_scary_task = random.choice(scary_tasks)

        if "chosen_scary_task" in st.session_state:
            chosen_task = st.session_state.chosen_scary_task

            st.warning(f"Today's scary task: **{chosen_task['title']}**")

            if st.button("Mark this task as done"):
                for task in st.session_state.tasks:
                    if (
                        task["title"] == chosen_task["title"]
                        and task.get("is_scary") == True
                        and task["status"] == "planned"
                    ):
                        task["status"] = "done"
                        break

                save_tasks_to_file(st.session_state.tasks)

                st.session_state.scary_done_message = random.choice(SCARY_DONE_MESSAGES)

                del st.session_state.chosen_scary_task
                st.rerun()

    st.subheader("Planned scary tasks")

    if len(scary_tasks) == 0:
        st.markdown(
            "<p class='empty-message'>Nothing scary in the list. Suspiciously peaceful.</p>",
            unsafe_allow_html=True,
        )
    else:
        for scary_index, task in enumerate(scary_tasks):
            card_col, empty_col = st.columns([3, 1])

            with card_col:
                with st.container(border=True):
                    text_col, button_col = st.columns([3, 1.5])

                    with text_col:
                        st.markdown(f"**🕯️ {task['title']}**")

                        st.markdown(
                            f"<span class='task-caption'>{task['priority']} · {task['minutes']} min</span>",
                            unsafe_allow_html=True,
                        )

                    with button_col:
                        st.markdown("<div style='height: 0.7rem;'></div>", unsafe_allow_html=True)

                        if st.button("Edit", key=f"edit_scary_{scary_index}", use_container_width=True):
                            st.session_state.editing_scary_task_index = scary_index
                            st.rerun()

                        if st.button("Del", key=f"delete_scary_{scary_index}", use_container_width=True):
                            deleted_title = task["title"]

                            for index, original_task in enumerate(st.session_state.tasks):
                                if (
                                    original_task["title"] == task["title"]
                                    and original_task["status"] == task["status"]
                                    and original_task["priority"] == task["priority"]
                                    and original_task["minutes"] == task["minutes"]
                                    and original_task.get("is_scary", False) == task.get("is_scary", False)
                                ):
                                    st.session_state.tasks.pop(index)
                                    break

                            save_tasks_to_file(st.session_state.tasks)

                            if "chosen_scary_task" in st.session_state:
                                del st.session_state.chosen_scary_task

                            if "editing_scary_task_index" in st.session_state:
                                del st.session_state.editing_scary_task_index

                            st.success(f"Deleted scary task: {deleted_title}")
                            st.rerun()

            if st.session_state.get("editing_scary_task_index") == scary_index:
                st.markdown("#### Edit scary task")

                with st.form(f"edit_scary_task_form_{scary_index}"):
                    edited_title = st.text_input(
                        "Task title",
                        value=task["title"],
                        key=f"edit_scary_title_{scary_index}",
                    )

                    edited_priority = st.selectbox(
                        "Priority",
                        ["low", "medium", "high"],
                        index=["low", "medium", "high"].index(task["priority"]),
                        key=f"edit_scary_priority_{scary_index}",
                    )

                    edited_minutes = st.number_input(
                        "Minutes",
                        min_value=1,
                        step=5,
                        value=int(task["minutes"]),
                        key=f"edit_scary_minutes_{scary_index}",
                    )

                    edited_is_scary = st.checkbox(
                        "This task is still scary",
                        value=task.get("is_scary", True),
                        key=f"edit_scary_is_scary_{scary_index}",
                    )

                    save_changes = st.form_submit_button("Save changes")
                    cancel_edit = st.form_submit_button("Cancel")

                    if save_changes:
                        if edited_title.strip() == "":
                            st.error("Please enter a task title.")
                        else:
                            for index, original_task in enumerate(st.session_state.tasks):
                                if (
                                    original_task["title"] == task["title"]
                                    and original_task["status"] == task["status"]
                                    and original_task["priority"] == task["priority"]
                                    and original_task["minutes"] == task["minutes"]
                                    and original_task.get("is_scary", False) == task.get("is_scary", False)
                                ):
                                    st.session_state.tasks[index] = create_task(
                                        title=edited_title,
                                        status="planned",
                                        priority=edited_priority,
                                        minutes=edited_minutes,
                                        is_scary=edited_is_scary,
                                    )
                                    break

                            save_tasks_to_file(st.session_state.tasks)

                            if "chosen_scary_task" in st.session_state:
                                del st.session_state.chosen_scary_task

                            del st.session_state.editing_scary_task_index

                            st.success("Scary task updated.")
                            st.rerun()

                    if cancel_edit:
                        del st.session_state.editing_scary_task_index
                        st.rerun()

st.caption("Data is saved automatically to tasks.csv.")


