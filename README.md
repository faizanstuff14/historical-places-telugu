# historical-places-telugu
# 📸 Telugu Image Collection Portal (చారిత్రక ప్రదేశాలు సేకరణ)

This is a bilingual (English + Telugu) web application built with **Streamlit** and **SQLite**, allowing users to upload images along with Telugu descriptions. Admins can log in to view submission analytics via a dashboard.

---

## 🚀 Features

- 📥 **User Uploads**: Upload images with descriptions in Telugu.
- 🔐 **Login & Sign Up**: User authentication using Gmail.
- 🧑‍💼 **Admin Panel**: Admins can view analytics of submissions.
- 📊 **Analytics Dashboard**: View user-wise counts and images.
- 💾 **Download Data**: Admins can download all submissions as CSV.
- 🗃️ **Data Storage**: Image files are saved in `uploaded_images/` and metadata in `SQLite`.

---

## 🛠️ Tech Stack

- **Frontend/UI**: [Streamlit](https://streamlit.io/)
- **Database**: SQLite (file-based)
- **Image Processing**: PIL (Pillow)
- **Analytics**: Pandas and Streamlit charts

---

## 📂 Folder Structure

├── app.py # Main Streamlit app

├── app_data.db # SQLite database

├── uploaded_images/ # Folder for uploaded images

└── README.md # Project README

## 1.Install requirements

pip install -r requirements.txt

If you don't have requirements.txt, create one with:
pip install streamlit pandas pillow
pip freeze > requirements.txt

## 2. Run the Streamlit app
streamlit run app.py

python -m streamlit run app.py

<h2>👤 Admin Access</h2>
To use the Admin Dashboard:

## 1.Update the ADMIN_EMAILS list in the code with authorized Gmail addresses:

ADMIN_EMAILS = ['your-admin@gmail.com']

## 2.Login using that email from the "Admin Login" section on the homepage.

## <h3>🧪 Sample Workflow</h3>

A user signs up using their Gmail and uploads an image with a Telugu description.

Admin logs in and views:

Total submissions

Submissions per user

Image previews

CSV download option

## <h3>🧳 Deployment Tips</h3>

Deploy to Streamlit Cloud, Railway, or Render.

Ensure you persist the uploaded_images folder and app_data.db using volume mounts or database migration if hosting elsewhere.

If deploying a backend separately (e.g., using Railway), consider turning this into a full-stack app with REST APIs.

## <h3>📝 License</h3>

MIT License. Feel free to fork and build upon this project.

## <h3>🙏 Acknowledgements</h3>

<h2>ప్రేమతో 💙 తెలుగు భాష కోసం</h2>
