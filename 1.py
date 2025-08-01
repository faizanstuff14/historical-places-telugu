import streamlit as st
import sqlite3
import os
from datetime import datetime
import pandas as pd
from PIL import Image

# ----------------- Constants / Config -------------------
DB_PATH = 'app_data.db'
IMG_DIR = 'uploaded_images'
ADMIN_EMAILS = ['faizanstuff14@gmail.com']  # <-- Update with actual admin email(s)!

# ----------------- Ensure folders and DB exist ---------
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            name TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            image_path TEXT,
            description_te TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ------------------ Helper functions --------------------
def user_exists(email):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def signup_user(email, name):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO users (email, name) VALUES (?, ?)", (email, name))
    conn.commit()
    conn.close()

# ------------------ Login / Sign Up Page ----------------
def login_signup_page():
    st.header("Login / Sign Up with Gmail")
    email = st.text_input("Gmail Address", key='auth_email')
    name = st.text_input("Name (పేరు)", key='auth_name')

    col1, col2 = st.columns(2)
    login_clicked = col1.button("Login")
    signup_clicked = col2.button("Sign Up")

    if login_clicked:
        if not email or '@gmail.com' not in email:
            st.error("Please enter a valid Gmail address.")
        elif user_exists(email):
            st.session_state['user_email'] = email
            st.session_state['user_name'] = name if name else "User"
            st.session_state['is_admin'] = email in ADMIN_EMAILS
            st.session_state['logged_in'] = True
            st.success(f"Welcome back, {st.session_state['user_name']}!")
            st.experimental_rerun()
        else:
            st.error("User not found. Please sign up first.")

    if signup_clicked:
        if not email or '@gmail.com' not in email:
            st.error("Please enter a valid Gmail address.")
        elif user_exists(email):
            st.error("User already exists. Please login.")
        elif not name:
            st.error("Please enter your name for sign up.")
        else:
            try:
                signup_user(email, name)
                st.success("Sign up successful! You may now login.")
            except Exception as e:
                st.error(f"Sign up failed: {e}")

# ------------------ User Page (initial + form) ----------------
def user_page():
    st.header("User Page (ఉపయోగకర్త పేజీ)")
    st.write(f"Welcome, {st.session_state.get('user_name', '')}! Here you can upload images and provide Telugu descriptions.")

    if 'show_input' not in st.session_state:
        st.session_state.show_input = False

    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        plus_clicked = st.button("+", key="add_image_button", help="Add Image and Telugu Description")

    if plus_clicked:
        st.session_state.show_input = True

    if st.session_state.show_input:
        with st.form("image_desc_form", clear_on_submit=True):
            image_file = st.file_uploader("Select Image (చిత్రాన్ని ఎంచుకోండి)", type=["jpg", "jpeg", "png"])
            description = st.text_area("Enter Description in Telugu (తెలుగులో వివరాలు నమోదు చేయండి)")

            submitted = st.form_submit_button("Submit (సబ్మిట్ చెయ్యండి)")
            cancel = st.form_submit_button("Cancel")

            if submitted:
                if not image_file:
                    st.error("Please upload an image!")
                elif not description.strip():
                    st.error("Please enter a description!")
                else:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{timestamp}_{image_file.name}"
                    img_path = os.path.join(IMG_DIR, filename)
                    with open(img_path, "wb") as f:
                        f.write(image_file.getbuffer())

                    conn = get_conn()
                    c = conn.cursor()
                    c.execute(
                        "INSERT INTO submissions (user_email, image_path, description_te, timestamp) VALUES (?, ?, ?, ?)",
                        (st.session_state['user_email'], img_path, description.strip(), timestamp)
                    )
                    conn.commit()
                    conn.close()

                    st.success("Your data has been successfully saved! (మీ డేటా విజయవంతంగా సేవ్ చేయబడింది!)")
                    st.session_state.show_input = False  # hide form after submit
                    st.experimental_rerun()  # refresh to update

            if cancel:
                st.session_state.show_input = False
                st.experimental_rerun()  # refresh to hide form

    else:
        st.info("Click the + button to add an image and its Telugu description.")

# ------------------ Admin Login Modal for Home Page ----------------
def admin_login_modal():
    st.subheader("Admin Login")
    with st.form("admin_login_form", clear_on_submit=True):
        email = st.text_input("Admin Gmail", key="admin_email")
        name = st.text_input("Admin Name (పేరు)", key="admin_name")
        submitted = st.form_submit_button("Admin Login")
        if submitted:
            if email in ADMIN_EMAILS:
                st.session_state['user_email'] = email
                st.session_state['user_name'] = name if name else "Admin"
                st.session_state['is_admin'] = True
                st.session_state['logged_in'] = True
                st.success("Admin login successful.")
                st.session_state['page'] = "Admin Dashboard"
                st.experimental_rerun()
            else:
                st.error("Access denied. Only authorized admin emails allowed.")

# ------------------ Admin Dashboard with Analytics -------------------
def admin_dashboard():
    if not st.session_state.get('logged_in', False):
        st.warning("Please login first.")
        return
    if not st.session_state.get('is_admin', False):
        st.error("Access denied: Admins only!")
        return

    st.header("Admin Dashboard (అడ్మిన్ డాష్‌బోర్డ్)")

    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM submissions", conn)
    users_df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()

    if df.empty:
        st.info("No submissions from users yet.")
        return

    # Merge submissions with user names
    merged_df = df.merge(users_df, left_on='user_email', right_on='email', how='left')
    merged_df = merged_df.rename(columns={'name': 'user_name'})

    st.subheader("User Submission Counts")
    user_counts = merged_df.groupby(['user_email','user_name']).size().reset_index(name='Submissions')
    st.table(user_counts)

    st.subheader("Submission Activity by User")
    chart_df = user_counts.set_index('user_email')['Submissions']
    st.bar_chart(chart_df)

    st.subheader("All User Submissions")
    for _, row in merged_df.sort_values(by='timestamp', ascending=False).iterrows():
        st.markdown(f"*User:* {row['user_name']} ({row['user_email']})")
        st.markdown(f"*Timestamp:* {row['timestamp']}")
        st.markdown(f"*Description (Telugu):* {row['description_te']}")
        if os.path.exists(row['image_path']):
            try:
                img = Image.open(row['image_path'])
                st.image(img, width=300)
            except Exception as e:
                st.warning(f"Could not display image: {e}")
        else:
            st.warning("Image file missing.")
        st.markdown("---")

    csv_data = merged_df[['user_email', 'user_name', 'image_path', 'description_te', 'timestamp']].to_csv(index=False)
    st.download_button("Download All Submissions as CSV", csv_data, file_name="all_user_submissions.csv")

# ------------------ Main app with home page and dynamic pages -----------------------
def main():
    st.title("చారిత్రక ప్రదేశాలు సేకరణ")

    # Initialize session state variables if not present
    for key, default in [('logged_in', False), ('is_admin', False), ('page', None)]:
        if key not in st.session_state:
            st.session_state[key] = default

    if st.session_state.get('logged_in', False):
        # Main nav after login
        menu = ["User Page"]
        if st.session_state.get('is_admin', False):
            menu.append("Admin Dashboard")
        menu.append("Logout")
        choice = st.sidebar.selectbox("Navigate", menu, key='nav')

        if choice == "User Page":
            st.session_state['page'] = "User Page"
        elif choice == "Admin Dashboard":
            st.session_state['page'] = "Admin Dashboard"
        elif choice == "Logout":
            st.session_state.clear()
            st.success("You have logged out successfully.")
            st.experimental_rerun()

        # Dynamic page content
        if st.session_state.get('page') == "User Page":
            user_page()
        elif st.session_state.get('page') == "Admin Dashboard":
            admin_dashboard()
        else:
            user_page()
    else:
        # Home page before login
        st.header("Home Page")
        st.header("చారిత్రక డేటా సేకరణకు స్వాగతం.!")
        st.write("Please login or sign up to continue.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login / Sign Up as User"):
                st.session_state['show_user_login'] = True
                st.session_state['show_admin_login'] = False
        with col2:
            if st.button("Admin Login"):
                st.session_state['show_admin_login'] = True
                st.session_state['show_user_login'] = False

        if st.session_state.get('show_user_login', False):
            login_signup_page()
        if st.session_state.get('show_admin_login', False):
            admin_login_modal()

if __name__ == "_main_":
    main()
