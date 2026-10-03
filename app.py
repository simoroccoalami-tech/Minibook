import hashlib
import os
import sqlite3
import streamlit as st

# إعداد صفحة التطبيق
st.set_page_config(
    page_title="Minibook - شبيه فيسبوك", page_icon="📱", layout="centered"
)

# --- تنسيق CSS حديث ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f5;
    }
    .title-red {
        color: #e4405f;
        font-family: Helvetica, Arial, sans-serif;
        font-weight: 900;
        font-size: 2.5rem;
    }
    .title-green {
        color: #00a400;
        font-family: Helvetica, Arial, sans-serif;
        font-weight: 900;
        font-size: 2.5rem;
    }
    .fb-card {
        background-color: #ffffff;
        padding: 16px;
        border-radius: 8px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        margin-bottom: 12px;
        border: 1px solid #ced0d4;
    }
    .stButton>button {
        background-color: #1877f2;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 6px 16px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #166fe5;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
  os.makedirs(UPLOAD_DIR)


def init_db():
  conn = sqlite3.connect("minibook_perfect.db", check_same_thread=False)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            profile_pic TEXT
        )
    """)
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            content TEXT,
            image_path TEXT,
            likes INTEGER DEFAULT 0
        )
    """)
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            username TEXT,
            comment TEXT
        )
    """)
  conn.commit()
  conn.close()


init_db()


def make_hashes(password):
  return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
  return make_hashes(password) == hashed_text


if "logged_in" not in st.session_state:
  st.session_state["logged_in"] = False
  st.session_state["username"] = ""

# --- القائمة الجانبية (تسجيل الدخول / إنشاء حساب) ---
st.sidebar.markdown("### 🌐 القائمة الرئيسية")

if not st.session_state["logged_in"]:
  auth_mode = st.sidebar.selectbox(
      "اختر العملية", ["تسجيل الدخول", "حساب جديد"]
  )

  # عنوان التطبيق في الصفحة الرئيسية
  st.markdown(
      "<div style='text-align: center; margin-bottom: 20px;'><span"
      " class='title-red'>Mini</span><span"
      " class='title-green'>book</span></div>",
      unsafe_allow_html=True,
  )

  if auth_mode == "تسجيل الدخول":
    st.subheader("🔑 تسجيل الدخول")
    username_input = st.text_input("اسم المستخدم", key="login_user")
    password_input = st.text_input(
        "كلمة المرور", type="password", key="login_pass"
    )

    if st.button("دخول النظام", key="login_btn"):
      if username_input and password_input:
        conn = sqlite3.connect("minibook_perfect.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password FROM users WHERE username = ?", (username_input,)
        )
        res = cursor.fetchone()
        conn.close()

        if res and check_hashes(password_input, res[0]):
          st.session_state["logged_in"] = True
          st.session_state["username"] = username_input
          st.success("تم تسجيل الدخول بنجاح!")
          st.rerun()
        else:
          st.error("خطأ في اسم المستخدم أو كلمة المرور.")
      else:
        st.warning("الرجاء إدخال بيانات الدخول.")

  elif auth_mode == "حساب جديد":
    st.subheader("📝 إنشاء حساب جديد")
    new_user = st.text_input("اسم المستخدم الجديد", key="reg_user")
    new_pass = st.text_input("كلمة المرور", type="password", key="reg_pass")
    uploaded_profile_pic = st.file_uploader(
        "اختر صورة الملف الشخصي (Profile)", type=["jpg", "png", "jpeg"]
    )

    if st.button("إنشاء الحساب", key="reg_btn"):
      if new_user and new_pass:
        pic_path = None
        if uploaded_profile_pic is not None:
          pic_path = os.path.join(UPLOAD_DIR, f"profile_{new_user}.jpg")
          with open(pic_path, "wb") as f:
            f.write(uploaded_profile_pic.getbuffer())

        try:
          conn = sqlite3.connect(
              "minibook_perfect.db", check_same_thread=False
          )
          cursor = conn.cursor()
          cursor.execute(
              "INSERT INTO users (username, password, profile_pic) VALUES (?,"
              " ?, ?)",
              (new_user, make_hashes(new_pass), pic_path),
          )
          conn.commit()
          conn.close()
          st.success("تم إنشاء الحساب بنجاح! انتقل لتبويب تسجيل الدخول.")
        except Exception:
          st.error("اسم المستخدم مستخدم مسبقاً، اختر اسماً فريداً.")
      else:
        st.warning("الرجاء ملء الحقول الإجبارية.")

else:
  # القائمة الجانبية للمستخدم المسجل
  conn = sqlite3.connect("minibook_perfect.db", check_same_thread=False)
  cursor = conn.cursor()
  cursor.execute(
      "SELECT profile_pic FROM users WHERE username = ?",
      (st.session_state["username"],),
  )
  user_data = cursor.fetchone()
  conn.close()

  if user_data and user_data[0] and os.path.exists(user_data[0]):
    st.sidebar.image(user_data[0], width=100)

  st.sidebar.write(f"مرحباً بك: **{st.session_state['username']}**")
  if st.sidebar.button("تسجيل الخروج"):
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.rerun()

  # --- واجهة المنصّة الأساسية (News Feed) ---
  st.markdown(
      "<div style='text-align: center; margin-bottom: 20px;'><span"
      " class='title-red'>Mini</span><span"
      " class='title-green'>book</span></div>",
      unsafe_allow_html=True,
  )

  st.markdown(
      "<div class='fb-card'><h4>✍️ إنشاء منشور جديد</h4>", unsafe_allow_html=True
  )
  with st.form("create_post_form", clear_on_submit=True):
    post_text = st.text_area(
        "بماذا تفكر يا " + st.session_state["username"] + "؟"
    )
    post_image = st.file_uploader(
        "إرفاق صورة للمنشور", type=["jpg", "png", "jpeg"]
    )
    submit_btn = st.form_submit_button("نشر المنشور")

    if submit_btn and (post_text or post_image):
      img_path = None
      if post_image is not None:
        img_path = os.path.join(UPLOAD_DIR, post_image.name)
        with open(img_path, "wb") as f:
          f.write(post_image.getbuffer())

      conn = sqlite3.connect("minibook_perfect.db", check_same_thread=False)
      cursor = conn.cursor()
      cursor.execute(
          "INSERT INTO posts (username, content, image_path, likes) VALUES"
          " (?, ?, ?, 0)",
          (st.session_state["username"], post_text, img_path),
      )
      conn.commit()
      conn.close()
      st.success("تم النشر بنجاح!")
      st.rerun()
  st.markdown("</div>", unsafe_allow_html=True)

  st.markdown("---")
  st.subheader("📰 آخر الأخبار والمنشورات")

  conn = sqlite3.connect("minibook_perfect.db", check_same_thread=False)
  cursor = conn.cursor()
  cursor.execute(
      "SELECT id, username, content, image_path, likes FROM posts ORDER BY id"
      " DESC"
  )
  all_posts = cursor.fetchall()

  for post in all_posts:
    p_id, p_owner, p_content, p_img, p_likes = post

    cursor.execute(
        "SELECT profile_pic FROM users WHERE username = ?", (p_owner,)
    )
    owner_pic = cursor.fetchone()

    st.markdown("<div class='fb-card'>", unsafe_allow_html=True)

    col_avatar, col_name = st.columns([1, 10])
    with col_avatar:
      if owner_pic and owner_pic[0] and os.path.exists(owner_pic[0]):
        st.image(owner_pic[0], width=45)
      else:
        st.write("👤")
    with col_name:
      st.markdown(
          f"<b style='font-size: 16px; color: #050505;'>{p_owner}</b>",
          unsafe_allow_html=True,
      )

    if p_content:
      st.write(p_content)

    if p_img and os.path.exists(p_img):
      st.image(p_img, use_column_width=True)

    st.write("---")

    col_like, col_space = st.columns([2, 8])
    with col_like:
      if st.button(f"❤️ أعجبني ({p_likes})", key=f"like_btn_{p_id}"):
        cursor.execute(
            "UPDATE posts SET likes = likes + 1 WHERE id = ?", (p_id,)
        )
        conn.commit()
        st.rerun()

    with st.expander("💬 عرض التعليقات وإضافتها"):
      cursor.execute(
          "SELECT username, comment FROM comments WHERE post_id = ?", (p_id,)
      )
      post_comments = cursor.fetchall()
      for c_user, c_text in post_comments:
        st.markdown(
            f"<div style='background-color: #f0f2f5; padding: 8px;"
            f" border-radius: 12px; margin-bottom: 5px;'><b"
            f" style='color: #050505;'>{c_user}:</b> {c_text}</div>",
            unsafe_allow_html=True,
        )

      with st.form(key=f"comment_form_{p_id}", clear_on_submit=True):
        comment_input = st.text_input(
            "اكتب تعليقاً...", key=f"c_input_val_{p_id}"
        )
        submit_comment = st.form_submit_button("تعليق")
        if submit_comment and comment_input:
          cursor.execute(
              "INSERT INTO comments (post_id, username, comment) VALUES (?, ?,"
              " ?)",
              (p_id, st.session_state["username"], comment_input),
          )
          conn.commit()
          conn.close()
          st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

  conn.close()
