import streamlit as st

from task_utils import create_task, load_css, load_tasks_from_file, save_tasks_to_file

st.set_page_config(page_title="Task Dump", page_icon="🧺", layout="wide")

st.markdown(load_css(), unsafe_allow_html=True)

st.title("🧺 Task Dump")
st.caption("A quick place to throw small tasks before they disappear from your brain.")


if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks_from_file()


with st.sidebar:
    st.header("Quick add")

    with st.form("task_dump_form", clear_on_submit=True):
        title = st.text_input("Task title")
        minutes = st.number_input("Minutes", min_value=1, step=5, value=5)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=0)
        is_scary = st.checkbox("This task is scary")

        submitted = st.form_submit_button("Add quick task")

        if submitted:
            if title.strip() == "":
                st.error("Please enter a task title.")
            else:
                new_task = create_task(
                    title=title,
                    status="planned",
                    priority=priority,
                    minutes=minutes,
                    is_scary=is_scary,
                )

                st.session_state.tasks.append(new_task)
                save_tasks_to_file(st.session_state.tasks)

                st.success(f"Added task: {title}")


tasks = st.session_state.tasks

dump_tasks = [
    task for task in tasks
    if task["status"] == "planned" and task["minutes"] <= 10
]

# st.subheader("Small planned tasks")

# if len(dump_tasks) == 0:
#     st.info("No small planned tasks yet.")
# else:
#     for dump_index, task in enumerate(dump_tasks):
#         card_col, empty_col = st.columns([2.3, 3])

#         with card_col:
#             with st.container(border=True):
#                 text_col, button_col = st.columns([3, 1.5])

#                 with text_col:
#                     st.markdown(f"**{task['title']}**")

#                     scary_text = "🕯️ scary" if task.get("is_scary") == True else "not scary"

#                     st.markdown(
#                         f"<span class='task-caption'>{task['priority']} · {task['minutes']} min · {scary_text}</span>",
#                         unsafe_allow_html=True,
#                     )
                
#     if st.session_state.get("editing_dump_task_index") == dump_index:
#         st.markdown("#### Edit task")

#         if st.session_state.get("editing_dump_task_index") == dump_index:
#             st.markdown("#### Edit task")

#             with st.form(f"edit_dump_task_form_{dump_index}"):
#                 edited_title = st.text_input(
#                     "Task title",
#                     value=task["title"],
#                     key=f"edit_dump_title_{dump_index}",
#                 )

#                 edited_priority = st.selectbox(
#                     "Priority",
#                     ["low", "medium", "high"],
#                     index=["low", "medium", "high"].index(task["priority"]),
#                     key=f"edit_dump_priority_{dump_index}",
#                 )

#                 edited_minutes = st.number_input(
#                     "Minutes",
#                     min_value=1,
#                     step=5,
#                     value=int(task["minutes"]),
#                     key=f"edit_dump_minutes_{dump_index}",
#                 )

#                 edited_is_scary = st.checkbox(
#                     "This task is scary",
#                     value=task.get("is_scary", False),
#                     key=f"edit_dump_is_scary_{dump_index}",
#                 )

#                 save_changes = st.form_submit_button("Save changes")
#                 cancel_edit = st.form_submit_button("Cancel")

#                 if save_changes:
#                     if edited_title.strip() == "":
#                         st.error("Please enter a task title.")
#                     else:
#                         for index, original_task in enumerate(st.session_state.tasks):
#                             if (
#                                 original_task["title"] == task["title"]
#                                 and original_task["status"] == task["status"]
#                                 and original_task["priority"] == task["priority"]
#                                 and original_task["minutes"] == task["minutes"]
#                                 and original_task.get("is_scary", False) == task.get("is_scary", False)
#                             ):
#                                 st.session_state.tasks[index] = create_task(
#                                     title=edited_title,
#                                     status="planned",
#                                     priority=edited_priority,
#                                     minutes=edited_minutes,
#                                     is_scary=edited_is_scary,
#                                 )
#                                 break

#                         save_tasks_to_file(st.session_state.tasks)

#                         del st.session_state.editing_dump_task_index

#                         st.success("Task updated.")
#                         st.rerun()

#                 if cancel_edit:
#                     del st.session_state.editing_dump_task_index
#                     st.rerun()

left_col, right_col = st.columns([3.2, 1])

with left_col:
    st.subheader("Small planned tasks")

    if len(dump_tasks) == 0:
        st.info("No small planned tasks yet.")
    else:
        for dump_index, task in enumerate(dump_tasks):
            card_col, empty_col = st.columns([3, 1])

            with card_col:
                with st.container(border=True):
                    text_col, button_col = st.columns([3, 1.5])

                    with text_col:
                        st.markdown(f"**{task['title']}**")

                        scary_text = "🕯️ scary" if task.get("is_scary") == True else "not scary"

                        st.markdown(
                            f"<span class='task-caption'>{task['priority']} · {task['minutes']} min · {scary_text}</span>",
                            unsafe_allow_html=True,
                        )

                    with button_col:
                        st.markdown("<div style='height: 1.1rem;'></div>", unsafe_allow_html=True)

                        edit_col, delete_col = st.columns(2)

                        with edit_col:
                            if st.button("Edit", key=f"edit_dump_{dump_index}"):
                                st.session_state.editing_dump_task_index = dump_index

                        with delete_col:
                            if st.button("Del", key=f"delete_dump_{dump_index}"):
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

                                if "editing_dump_task_index" in st.session_state:
                                    del st.session_state.editing_dump_task_index

                                st.success(f"Deleted task: {deleted_title}")
                                st.rerun()

            if st.session_state.get("editing_dump_task_index") == dump_index:
                st.markdown("#### Edit task")

                with st.form(f"edit_dump_task_form_{dump_index}"):
                    edited_title = st.text_input(
                        "Task title",
                        value=task["title"],
                        key=f"edit_dump_title_{dump_index}",
                    )

                    edited_priority = st.selectbox(
                        "Priority",
                        ["low", "medium", "high"],
                        index=["low", "medium", "high"].index(task["priority"]),
                        key=f"edit_dump_priority_{dump_index}",
                    )

                    edited_minutes = st.number_input(
                        "Minutes",
                        min_value=1,
                        step=5,
                        value=int(task["minutes"]),
                        key=f"edit_dump_minutes_{dump_index}",
                    )

                    edited_is_scary = st.checkbox(
                        "This task is scary",
                        value=task.get("is_scary", False),
                        key=f"edit_dump_is_scary_{dump_index}",
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

                            del st.session_state.editing_dump_task_index

                            st.success("Task updated.")
                            st.rerun()

                    if cancel_edit:
                        del st.session_state.editing_dump_task_index
                        st.rerun()

    st.subheader("Summary")

    total_dump_minutes = sum(task["minutes"] for task in dump_tasks)

    stats_col1, stats_col2, empty_stats_col = st.columns([1, 1, 1.4])

    with stats_col1:
        st.metric("Small tasks", len(dump_tasks))

    with stats_col2:
        st.metric("Total minutes", total_dump_minutes)


with right_col:
    st.subheader("Dump rules")

    st.markdown(
        """
        - Keep it tiny.
        - 5–10 minutes is enough.
        - No perfect planning.
        - Just catch the task before it disappears.
        """
    )

    st.info("Tiny task rule: if it takes less than 10 minutes, it belongs here.")

    st.caption("Data is saved automatically to tasks.csv.")