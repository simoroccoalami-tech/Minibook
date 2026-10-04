import hashlib
import os
import sqlite3
import streamlit as st

# إعداد صفحة التطبيق
st.set_page_config(
    page_title="Minibook - شبيه فيسبوك", page_icon="📱", layout="centered"
)

# --- تنسيق CSS مخصص لاستهداف الحقول والشاشات على الهواتف بدقة ---
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
    .stTextInput input, .stTextArea textarea {
        background-color: #ffffff !important;
        border: 2px solid #1877f2 !important;
        border-radius: 8px !important;
        color: #000000 !important;
        padding: 10px !important;
    }
    .stButton>button {
        background-color: #1877f2;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 8px 16px;
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


# --- تهيئة قاعدة البيانات والجداول ---
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
        )إليك الكود النهائي الكامل والجاهز لتطبيق **Minibook** مصححاً بالكامل، ومتضمناً لجميع الميزات السابقة (تسجيل الدخول، إنشاء الحسابات، صور البروفايل، المنشورات مع رفع الصور، الإعجابات، التعليقات) بالإضافة إلى **خاصية حذف المنشورات لصاحب المنشور فقط**، مع واجهة منسقة بأسلوب فيسبوك (أحمر وأخضر) ومجهزة للهواتف المحمولة:

```python
import hashlib
import os
import sqlite3
import streamlit as st

# إعداد صفحة التطبيق
st.set_page_config(
    page_title="Minibook - شبيه فيسبوك", page_icon="📱", layout="centered"
)

# --- تنسيق CSS مخصص لاستهداف الحقول والواجهة على الهواتف ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f5;
    }
    .fb-card {
        background-color: #ffffff;
        padding: 16px;
        border-radius: 8px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        margin-bottom: 12px;
        border: 1px solid #ced0d4;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #ffffff !important;
        border: 2px solid #1877f2 !important;
        border-radius: 8px !important;
        color: #000000 !important;
        padding: 10px !important;
    }
    .stButton>button {
        background-color: #1877f2;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 8px 16px;
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

# مجلد حفظ الصور المرفوعة
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
  os.makedirs(UPLOAD_DIR)


# إعداد قاعدة البيانات وتحديث الجداول
def init_db():
  conn = sqlite3.connect("minibook_perfect.db", check_same_thread=False)
  cursor = conn.cursor()
  # جدول المستخدمين
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            profile_pic TEXT
        )
    """)
  # جدول المنشورات
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            content TEXT,
            image_path TEXT,
            likes INTEGER DEFAULT 0
        )
    """)
  # جدول التعليقات
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            username TEXT,
            content TEXT
        )
    """)
  conn.commit()
  conn.close()


init_db()


# دالة تشفير كلمة المرور
def make_hash(password):
  return hashlib.sha256(str.encode(password)).hexdigest()


def check_password(password, hashed_password):
  return make_hash(password) == hashed_password


# إدارة حالة تسجيل الدخول
if "logged_in" not in st.session_state:
  st.session_state["logged_in"] = False
  st.session_state["username"] = ""

# --- واجهة تسجيل الدخول وإنشاء الحساب ---
if not st.session_state["logged_in"]:
  st.markdown(
      "<h1 style='text-align: center;'><span style='color: #e4405f;'>Mini</span><span"
      " style='color: #00a400;'>book</span></h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='text-align: center; color: #65676b;'>تواصل مع أصدقائك وعالمك"
      " عبر Minibook</p>",
      unsafe_allow_html=True,
  )

  tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب جديد"])

  with tab1:
    st.subheader("تسجيل الدخول إلى حسابك")
    login_user = st.text_input("اسم المستخدم", key="login_user")
    login_pass = st.text_input(
        "كلمة المرور", type="password", key="login_pass"
    )

    if st.button("دخول"):
      conn = sqlite3.connect("minibook_perfect.db", check_same_thread=False)
      cursor = conn.cursor()
      cursor.execute(
          "SELECT password FROM users WHERE username = ?", (login_user,)
      )
      user_data = cursor.fetchone()
      conn.close()

      if user_data and check_password(login_pass, user_data[0]):
        st.session_state["logged_in"] = True
        st.session_state["username"] = login_user
        st.success("تم تسجيل الدخول بنجاح!")
        st.rerun()
      else:
        st.error("اسم المستخدم أو كلمة المرور غير صحيحة.")

  with tab2:
    st.subheader("انشئ حساباً جديداً")
    new_user = st.text_input("اختر اسم مستخدم", key="new_user")
    new_pass = st.text_input("اختر كلمة المرور", type="password", key="new_pass")
    uploaded_profile_pic = st.file_uploader(
        "اختر صورة الملف الشخصي", type=["jpg", "png", "jpeg"]
    )

    if st.button("تسجيل"):
      if new_user and new_pass:
        conn = sqlite3.connect("minibook_perfect.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ?", (new_user,)
        )
        if cursor.fetchone():
          st.warning("اسم المستخدم هذا مستخدم مسبقاً، اختر اسماً آخر.")
        else:
          pic_path = ""
          if uploaded_profile_pic is not None:
            pic_path = os.path.join(UPLOAD_DIR, uploaded_profile_pic.name)
            with open(pic_path, "wb") as f:
              f.write(uploaded_profile_pic.getbuffer())

          cursor.execute(
              "INSERT INTO users (username, password, profile_pic) VALUES"
              " (?, ?, ?)",
              (new_user, make_hash(new_pass), pic_path),
          )
          conn.commit()
          conn.close()
          st.success("تم إنشاء الحساب بنجاح! يمكنك الانتقال لتبويب تسجيل الدخول.")
      else:
        st.warning("الرجاء إدخال اسم المستخدم وكلمة المرور.")

else:
  # --- واجهة التطبيق الرئيسية (بعد تسجيل الدخول) ---
  st.sidebar.markdown(
      "<h2><span style='color: #e4405f;'>Mini</span><span style='color:"
      " #00a400;'>book</span></h2>",
      unsafe_allow_html=True,
  )
  st.sidebar.write(f"مرحباً بك، **{st.session_state['username']}** 👋")

  if st.sidebar.button("تسجيل الخروج"):
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.rerun()

  # جلب صورة البروفايل للمستخدم الحالي
  conn = sqlite3.connect("minibook_perfect.db", check_same_thread=False)
  cursor = conn.cursor()
  cursor.execute(
      "SELECT profile_pic FROM users WHERE username = ?",
      (st.session_state["username"],),
  )
  user_pic_res = cursor.fetchone()
  user_pic = user_pic_res[0] if user_pic_res and user_pic_res[0] else None

  if user_pic and os.path.exists(user_pic):
    st.sidebar.image(user_pic, width=80)

  st.sidebar.markdown("---")
  st.sidebar.info("تطبيقك يعمل بشكل ممتاز وجاهز للتطوير والتوسع.")

  # الصفحة الرئيسية لعرض المنشورات وكتابتها
  st.markdown("### 📰 آخر المنشورات")

  # صندوق كتابة منشور جديد
  with st.form("new_post_form", clear_on_submit=True):
    post_content = st.text_area(
        "بماذا تفكر يا " + st.session_state["username"] + "؟"
    )
    post_image = st.file_uploader(
        "إرفاق صورة مع المنشور", type=["jpg", "png", "jpeg"]
    )
    submitted = st.form_submit_button("نشر")

    if submitted:
      if post_content.strip() != "" or post_image is not None:
        img_path = ""
        if post_image is not None:
          img_path = os.path.join(UPLOAD_DIR, post_image.name)
          with open(img_path, "wb") as f:
            f.write(post_image.getbuffer())

        cursor.execute(
            "INSERT INTO posts (username, content, image_path, likes) VALUES"
            " (?, ?, ?, 0)",
            (st.session_state["username"], post_content, img_path),
        )
        conn.commit()
        st.success("تم نشر المنشور بنجاح!")
        st.rerun()
      else:
        st.warning("لا يمكنك نشر منشور فارغ!")

  st.markdown("---")

  # جلب وعرض المنشورات من قاعدة البيانات
  cursor.execute(
      "SELECT id, username, content, image_path, likes FROM posts ORDER BY id"
      " DESC"
  )
  posts = cursor.fetchall()

  for post in posts:
    p_id, p_owner, p_content, p_img, p_likes = post

    # جلب صورة صاحب المنشور
    cursor.execute("SELECT profile_pic FROM users WHERE username = ?", (p_owner,))
    owner_data = cursor.fetchone()
    owner_pic = owner_data[0] if owner_data and owner_data[0] else None

    st.markdown('<div class="fb-card">', unsafe_allow_html=True)

    # رأس المنشور (صورة البروفايل واسم المستخدم)
    col_img, col_name, col_del = st.columns([1, 6, 2])
    with col_img:
      if owner_pic and os.path.exists(owner_pic):
        st.image(owner_pic, width=40)
      else:
        st.write("👤")
    with col_name:
      st.markdown(f"**{p_owner}**")

    # زر الحذف يظهر فقط لصاحب المنشور
    with col_del:
      if p_owner == st.session_state["username"]:
        if st.button("🗑️ حذف", key=f"del_{p_id}"):
          cursor.execute("DELETE FROM posts WHERE id = ?", (p_id,))
          cursor.execute("DELETE FROM comments WHERE post_id = ?", (p_id,))
          conn.commit()
          st.rerun()

    # محتوى المنشور والصورة
    if p_content:
      st.write(p_content)
    if p_img and os.path.exists(p_img):
      st.image(p_img, use_container_width=True)

    # قسم التفاعل (الإعجابات والتعليقات)
    col_like, col_count = st.columns([1, 4])
    with col_like:
      if st.button(f"👍 أعجبني ({p_likes})", key=f"like_{p_id}"):
        cursor.execute(
            "UPDATE posts SET likes = likes + 1 WHERE id = ?", (p_id,)
        )
        conn.commit()
        st.rerun()

    st.markdown("---")
    st.markdown("**التعليقات:**")

    # عرض التعليقات الخاصة بهذا المنشور
    cursor.execute(
        "SELECT username, content FROM comments WHERE post_id = ?", (p_id,)
    )
    comments = cursor.fetchall()
    for c_user, c_content in comments:
      st.markdown(f"<small><b>{c_user}:</b> {c_content}</small>", unsafe_allow_html=True)

    # إضافة تعليق جديد
    with st.form(key=f"comment_form_{p_id}", clear_on_submit=True):
      c_text = st.text_input(
          "اكتب تعليقاً...", key=f"comment_input_{p_id}", label_visibility="collapsed"
      )
      c_submit = st.form_submit_button("تعليق")
      if c_submit and c_text.strip():
        cursor.execute(
            "INSERT INTO comments (post_id, username, content) VALUES (?, ?,"
            " ?)",
            (p_id, st.session_state["username"], c_text),
        )
        conn.commit()
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

  conn.close()
