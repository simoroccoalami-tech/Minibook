import hashlib
import os
import sqlite3
import streamlit as st

# إعداد صفحة التطبيق
st.set_page_config(
    page_title="Minibook", page_icon="📱", layout="centered"
)

# --- تخصيص التصميم بالألوان الأحمر والأخضر وهيكل يشبه منصات التواصل ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f9f9f9;
    }
    h1 {
        color: #d9534f;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        text-align: center;
        font-weight: 800;
    }
    .post-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        border-left: 5px solid #5cb85c;
        border-right: 1px solid #eee;
        border-top: 1px solid #eee;
        border-bottom: 1px solid #eee;
    }
    .stButton>button {
        background-color: #5cb85c;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #4cae4c;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# مجلد حفظ الصور المرفوعة
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
  os.makedirs(UPLOAD_DIR)


# --- إعداد قاعدة البيانات (SQLite) ---
def init_db():
  conn = sqlite3.connect("minibook.db", check_same_thread=False)
  cursor = conn.cursor()

  cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
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
  if make_hashes(password) == hashed_text:
    return True
  return False


# --- إدارة الجلسة وتسجيل الدخول ---
if "logged_in" not in st.session_state:
  st.session_state["logged_in"] = False
  st.session_state["username"] = ""

# --- واجهة التطبيق الجانبية (القائمة) ---
st.sidebar.title("📖 Minibook Menu")

if not st.session_state["logged_in"]:
  choice = st.sidebar.selectbox("الخيارات", ["تسجيل الدخول", "إنشاء حساب جديد"])

  if choice == "تسجيل الدخول":
    st.subheader("🔑 تسجيل الدخول إلى حسابك")
    un = st.text_input("اسم المستخدم")
    ps = st.text_input("كلمة المرور", type="password")

    if st.button("دخول"):
      conn = sqlite3.connect("minibook.db", check_same_thread=False)
      cursor = conn.cursor()
      cursor.execute("SELECT password FROM users WHERE username = ?", (un,))
      result = cursor.fetchone()
      conn.close()

      if result and check_hashes(ps, result[0]):
        st.session_state["logged_in"] = True
        st.session_state["username"] = un
        st.success(f"مرحباً بك مجدداً يا {un}!")
        st.rerun()
      else:
        st.error("اسم المستخدم أو كلمة المرور غير صحيحة")

  elif choice == "إنشاء حساب جديد":
    st.subheader("📝 إنشاء حساب جديد")
    new_un = st.text_input("اختر اسم مستخدم")
    new_ps = st.text_input("اختر كلمة مرور", type="password")

    if st.button("تسجيل"):
      if new_un and new_ps:
        try:
          conn = sqlite3.connect("minibook.db", check_same_thread=False)
          cursor = conn.cursor()
          cursor.execute(
              "INSERT INTO users(username, password) VALUES (?, ?)",
              (new_un, make_hashes(new_ps)),
          )
          conn.commit()
          conn.close()
          st.success("تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن.")
        except:
          st.error("اسم المستخدم موجود مسبقاً، اختر اسمًا آخر.")
      else:
        st.warning("الرجاء ملء جميع الحقول.")

else:
  st.sidebar.write(f"👤 أهلاً بك: **{st.session_state['username']}**")
  if st.sidebar.button("تسجيل الخروج"):
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.rerun()

  st.markdown("<h1>Minibook 🔴🟢</h1>", unsafe_allow_html=True)
  st.write("---")

  st.markdown("### ✍️ ماذا يدور في ذهنك اليوم؟")
  with st.form("post_form", clear_on_submit=True):
    post_content = st.text_area("اكتب منشورك هنا...")
    uploaded_image = st.file_uploader(
        "أضف صورة للمنشور (اختياري)", type=["jpg", "png", "jpeg"]
    )
    submit_post = st.form_submit_button("نشر المنشور")

    if submit_post and (post_content or uploaded_image):
      image_path = None
      if uploaded_image is not None:
        image_path = os.path.join(UPLOAD_DIR, uploaded_image.name)
        with open(image_path, "wb") as f:
          f.write(uploaded_image.getbuffer())

      conn = sqlite3.connect("minibook.db", check_same_thread=False)
      cursor = conn.cursor()
      cursor.execute(
          "INSERT INTO posts (username, content, image_path, likes) VALUES"
          " (?, ?, ?, 0)",
          (st.session_state["username"], post_content, image_path),
      )
      conn.commit()
      conn.close()
      st.success("تم نشر منشورك بنجاح!")
      st.rerun()

  st.write("---")
  st.subheader("📰 آخر المنشورات")

  conn = sqlite3.connect("minibook.db", check_same_thread=False)
  cursor = conn.cursor()
  cursor.execute(
      "SELECT id, username, content, image_path, likes FROM posts ORDER BY id"
      " DESC"
  )
  posts = cursor.fetchall()

  for post in posts:
    post_id, p_user, p_content, p_image, p_likes = post

    st.markdown(
        f"""
        <div class="post-card">
            <h4 style="color: #d9534f; margin-bottom: 5px;">@ {p_user}</h4>
            <p style="font-size: 16px; color: #333;">{p_content}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if p_image and os.path.exists(p_image):
      st.image(p_image, use_column_width=True)

    col1, col2 = st.columns([1, 4])
    with col1:
      if st.button(f"❤️️ أعجبني ({p_likes})", key=f"like_{post_id}"):
        cursor.execute(
            "UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,)
        )
        conn.commit()
        st.rerun()

    with st.expander("💬 عرض / إضافة تعليقات"):
      cursor.execute(
          "SELECT username, comment FROM comments WHERE post_id = ?", (post_id,)
      )
      comments = cursor.fetchall()
      for c_user, c_text in comments:
        st.markdown(
            f"<small><b>{c_user}:</b> {c_text}</small>", unsafe_allow_html=True
        )

      with st.form(key=f"comment_form_{post_id}", clear_on_submit=True):
        comment_text = st.text_input("اكتب تعليقاً...", key=f"c_input_{post_id}")
        submit_comment = st.form_submit_button("إرسال التعليق")
        if submit_comment and comment_text:
          cursor.execute(
              "INSERT INTO comments (post_id, username, comment) VALUES (?, ?,"
              " ?)",
              (post_id, st.session_state["username"], comment_text),
          )
          conn.commit()
          conn.close()
          st.rerun()

    st.write("---")

  conn.close()
