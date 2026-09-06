import datetime as dt

import streamlit as st

from task_utils import load_css
from database import (
    load_week_goals_from_db,
    add_week_goal_to_db,
    update_week_goal_in_db,
    increment_week_goal_in_db,
    delete_week_goal_from_db,
)


st.set_page_config(page_title="Week Goals", page_icon="🎯", layout="wide")

if "user" not in st.session_state:
    st.warning("Please log in from the main page first.")
    st.stop()

current_user_id = st.session_state.user["id"]

st.markdown(load_css(), unsafe_allow_html=True)

st.title("🎯 Week Goals")
st.caption("A place for repeated weekly goals, habits, and small progress targets.")


def get_current_week_start():
    today = dt.date.today()
    return today - dt.timedelta(days=today.weekday())


week_start = get_current_week_start()

st.info(f"Current week starts on: {week_start}")


with st.sidebar:
    st.caption(f"Logged in as: {st.session_state.user['username']}")

    st.header("Add week goal")

    with st.form("add_week_goal_form", clear_on_submit=True):
        title = st.text_input("Goal title")
        target_count = st.number_input("Target count", min_value=1, step=1, value=5)
        unit = st.selectbox(
            "Unit",
            ["times", "days", "sessions", "tasks", "applications", "lessons"],
        )

        submitted = st.form_submit_button("Add goal")

        if submitted:
            if title.strip() == "":
                st.error("Please enter a goal title.")
            else:
                add_week_goal_to_db(
                    title=title.strip(),
                    target_count=int(target_count),
                    unit=unit,
                    week_start=week_start,
                    user_id=current_user_id,
                )

                st.success(f"Added week goal: {title}")
                st.rerun()


week_goals = load_week_goals_from_db(current_user_id)

current_week_goals = [
    goal for goal in week_goals
    if str(goal["week_start"]) == str(week_start)
]

if len(current_week_goals) == 0:
    st.info("No week goals yet. Add one from the sidebar.")
else:
    for goal in current_week_goals:
        goal_id = goal["id"]
        current_count = int(goal["current_count"])
        target_count = int(goal["target_count"])

        progress_value = min(current_count / target_count, 1.0)

        with st.container(border=True):
            st.markdown(f"### {goal['title']}")
            st.caption(
                f"{current_count} / {target_count} {goal['unit']}"
            )

            st.progress(progress_value)

            if current_count >= target_count:
                st.success("Goal completed for this week 🎉")

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("+1", key=f"increment_goal_{goal_id}", use_container_width=True):
                    increment_week_goal_in_db(goal_id, current_user_id)
                    st.rerun()

            with col2:
                if st.button("Edit", key=f"edit_goal_{goal_id}", use_container_width=True):
                    st.session_state.editing_week_goal_id = goal_id
                    st.rerun()

            with col3:
                if st.button("Delete", key=f"delete_goal_{goal_id}", use_container_width=True):
                    delete_week_goal_from_db(goal_id, current_user_id)

                    if "editing_week_goal_id" in st.session_state:
                        del st.session_state.editing_week_goal_id

                    st.success(f"Deleted week goal: {goal['title']}")
                    st.rerun()

        if st.session_state.get("editing_week_goal_id") == goal_id:
            st.markdown("#### Edit week goal")

            with st.form(f"edit_week_goal_form_{goal_id}"):
                edited_title = st.text_input(
                    "Goal title",
                    value=goal["title"],
                    key=f"edit_goal_title_{goal_id}",
                )

                edited_target_count = st.number_input(
                    "Target count",
                    min_value=1,
                    step=1,
                    value=target_count,
                    key=f"edit_goal_target_{goal_id}",
                )

                edited_current_count = st.number_input(
                    "Current count",
                    min_value=0,
                    step=1,
                    value=current_count,
                    key=f"edit_goal_current_{goal_id}",
                )

                edited_unit = st.selectbox(
                    "Unit",
                    ["times", "days", "sessions", "tasks", "applications", "lessons"],
                    index=["times", "days", "sessions", "tasks", "applications", "lessons"].index(goal["unit"])
                    if goal["unit"] in ["times", "days", "sessions", "tasks", "applications", "lessons"]
                    else 0,
                    key=f"edit_goal_unit_{goal_id}",
                )

                save_changes = st.form_submit_button("Save changes")
                cancel_edit = st.form_submit_button("Cancel")

                if cancel_edit:
                    if "editing_week_goal_id" in st.session_state:
                        del st.session_state.editing_week_goal_id
                    st.rerun()

                if save_changes:
                    if edited_title.strip() == "":
                        st.error("Please enter a goal title.")
                    else:
                        update_week_goal_in_db(
                            goal_id=goal_id,
                            title=edited_title.strip(),
                            target_count=int(edited_target_count),
                            current_count=int(edited_current_count),
                            unit=edited_unit,
                            week_start=week_start,
                            user_id=current_user_id,
                        )

                        if "editing_week_goal_id" in st.session_state:
                            del st.session_state.editing_week_goal_id

                        st.success("Week goal updated.")
                        st.rerun()