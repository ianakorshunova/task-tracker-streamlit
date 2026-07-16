import streamlit as st
import bcrypt
from database import get_connection


def hash_password(password):
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def check_password(password, password_hash):
    password_bytes = password.encode("utf-8")
    hash_bytes = password_hash.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hash_bytes)


def create_user(username, password):
    password_hash = hash_password(password)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (username, password_hash)
                VALUES (%s, %s)
                RETURNING id, username;
                """,
                (username, password_hash),
            )
            return cur.fetchone()


def login_user(username, password):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, username, password_hash
                FROM users
                WHERE username = %s;
                """,
                (username,),
            )
            user = cur.fetchone()

    if user is None:
        return None

    if check_password(password, user["password_hash"]):
        return {
            "id": user["id"],
            "username": user["username"],
        }

    return None


def show_auth_screen():
    st.title("Task Tracker")

    auth_tab, register_tab = st.tabs(["Login", "Register"])

    with auth_tab:
        st.subheader("Login")

        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Login")

            if submitted:
                if username.strip() == "" or password.strip() == "":
                    st.error("Please enter username and password.")
                else:
                    user = login_user(username.strip(), password)

                    if user is None:
                        st.error("Invalid username or password.")
                    else:
                        st.session_state.user = user
                        st.success(f"Welcome, {user['username']}!")
                        st.rerun()

    with register_tab:
        st.subheader("Register")

        with st.form("register_form"):
            username = st.text_input("Username", key="register_username")
            password = st.text_input("Password", type="password", key="register_password")
            password_confirm = st.text_input(
                "Confirm password",
                type="password",
                key="register_password_confirm",
            )
            submitted = st.form_submit_button("Create account")

            if submitted:
                if username.strip() == "" or password.strip() == "":
                    st.error("Please enter username and password.")
                elif password != password_confirm:
                    st.error("Passwords do not match.")
                else:
                    try:
                        user = create_user(username.strip(), password)
                        st.session_state.user = {
                            "id": user["id"],
                            "username": user["username"],
                        }
                        st.success("Account created!")
                        st.rerun()
                    except Exception:
                        st.error("Could not create account. Username may already exist.")