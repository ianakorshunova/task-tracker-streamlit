import streamlit as st

from task_utils import create_task, load_css, load_tasks_from_file, save_tasks_to_file

st.set_page_config(page_title="Completed Tasks", page_icon="✅", layout="wide")

st.markdown(load_css(), unsafe_allow_html=True)

st.title("✅ Completed Tasks")
st.caption("A small place to see what you have already finished.")


if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks_from_file()


tasks = st.session_state.tasks

completed_tasks = [
    task for task in tasks
    if task["status"] == "done"
]


st.subheader("Completed tasks")

if len(completed_tasks) == 0:
    st.info("No completed tasks yet.")
else:
    for completed_index, task in enumerate(completed_tasks):
        col1, col2, col3, col4, col5, col6 = st.columns([4, 2, 2, 2, 1, 1])

        with col1:
            st.write(task["title"])

        with col2:
            st.write(task["priority"])

        with col3:
            st.write(f"{task['minutes']} min")

        with col4:
            if task.get("is_scary") == True:
                st.write("🕯️ scary")
            else:
                st.write("—")

        with col5:
            if st.button("Edit", key=f"edit_completed_{completed_index}"):
                st.session_state.editing_completed_task_index = completed_index

        with col6:
            if st.button("Delete", key=f"delete_completed_{completed_index}"):
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

                if "editing_completed_task_index" in st.session_state:
                    del st.session_state.editing_completed_task_index

                st.success(f"Deleted task: {deleted_title}")
                st.rerun()

        if st.session_state.get("editing_completed_task_index") == completed_index:
            st.markdown("#### Edit completed task")

            with st.form(f"edit_completed_task_form_{completed_index}"):
                edited_title = st.text_input(
                    "Task title",
                    value=task["title"],
                    key=f"edit_completed_title_{completed_index}",
                )

                edited_status = st.selectbox(
                    "Status",
                    ["planned", "done"],
                    index=["planned", "done"].index(task["status"]),
                    key=f"edit_completed_status_{completed_index}",
                )

                edited_priority = st.selectbox(
                    "Priority",
                    ["low", "medium", "high"],
                    index=["low", "medium", "high"].index(task["priority"]),
                    key=f"edit_completed_priority_{completed_index}",
                )

                edited_minutes = st.number_input(
                    "Minutes",
                    min_value=1,
                    step=5,
                    value=int(task["minutes"]),
                    key=f"edit_completed_minutes_{completed_index}",
                )

                edited_is_scary = st.checkbox(
                    "This task is scary",
                    value=task.get("is_scary", False),
                    key=f"edit_completed_is_scary_{completed_index}",
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
                                    status=edited_status,
                                    priority=edited_priority,
                                    minutes=edited_minutes,
                                    is_scary=edited_is_scary,
                                )
                                break

                        save_tasks_to_file(st.session_state.tasks)

                        del st.session_state.editing_completed_task_index

                        st.success("Completed task updated.")
                        st.rerun()

                if cancel_edit:
                    del st.session_state.editing_completed_task_index
                    st.rerun()

total_completed_minutes = sum(task["minutes"] for task in completed_tasks)

st.metric("Completed minutes", total_completed_minutes)


if len(completed_tasks) > 0:
    scary_completed = [
        task for task in completed_tasks
        if task.get("is_scary") == True
    ]

    st.metric("Completed scary tasks", len(scary_completed))

st.caption("Data is saved automatically to tasks.csv.")