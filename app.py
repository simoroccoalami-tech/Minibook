import streamlit as st
import sqlite3
import hashlib

# إعدادات الصفحة
st.set_page_config(page_title="Minibook", page_icon="📱", layout="centered")

# --- إعداد قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('minibook.db', check_same_thread=False)
    c = conn.cursor()
    # جدول المستخدمين
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    # جدول المنشورات
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            content TEXT,
            likes INTEGER
        )
    ''')
    # جدول التعليقات
    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            username TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    return conn

conn = init_db()
cursor = conn.cursor()

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return True
    return False

# --- تنسيق التصميم والشعار ---
st.markdown("""
    <style>
    .brand-logo {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        background: linear-gradient(45deg, #b91c1c, #15803d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #65676b;
        font-size: 16px;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #15803d;
        color: white;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #b91c1c;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='brand-logo'>Minibook</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>شبكتك الاجتماعية المصغرة الحقيقية</div>", unsafe_allow_html=True)
st.write("---")

# إدارة الجلسة لتسجيل الدخول
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# --- واجهة تسجيل الدخول وإنشاء الحساب ---
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔑 تسجيل الدخول", "📝 إنشاء حساب جديد"])
    
    with tab1:
        st.subheader("تسجيل الدخول إلى حسابك")
        l_user = st.text_input("اسم المستخدم", key="l_user")
        l_pass = st.text_input("كلمة المرور", type="password", key="l_pass")
        if st.button("دخول"):
            cursor.execute('SELECT password FROM users WHERE username = ?', (l_user,))
            result = cursor.fetchone()
            if result and check_hashes(l_pass, result[0]):
                st.session_state.logged_in = True
                st.session_state.username = l_user
                st.success(f"مرحباً بك مجدداً يا {l_user}!")
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة المرور غير صحيحة.")
                
    with tab2:
        st.subheader("إنشاء حساب جديد على Minibook")
        n_user = st.text_input("اختر اسم مستخدم", key="n_user")
        n_pass = st.text_input("اختر كلمة مرور", type="password", key="n_pass")
        if st.button("تسجيل الحساب"):
            if n_user and n_pass:
                try:
                    cursor.execute('INSERT INTO users(username, password) VALUES (?, ?)', (n_user, make_hashes(n_pass)))
                    conn.commit()
                    st.success("تم إنشاء الحساب بنجاح! يمكنك الانتقال لتبويب تسجيل الدخول.")
                except sqlite3.IntegrityError:
                    st.error("اسم المستخدم هذا مستخدم مسبقاً، اختر اسمآ آخر.")
            else:
                st.warning("الرجاء ملء جميع الحقول.")

else:
    # --- التطبيق الرئيسي بعد تسجيل الدخول ---
    st.sidebar.success(مرحباً بك، {st.session_state.username})
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
        
    # صندوق نشر منشور جديد
    st.subheader("✍️ ماذا يدور في ذهنك اليوم؟")
    with st.form("new_post_form", clear_on_submit=True):
        post_content = st.text_area("اكتب منشورك هنا...", placeholder="شارك أفكارك مع المجتمع...")
        post_submit = st.form_submit_button("نشر")
        
        if post_submit:
            if post_content.strip():
                cursor.execute('INSERT INTO posts (username, content, likes) VALUES (?, ?, ?)', (st.session_state.username, post_content, 0))
                conn.commit()
                st.success("تم نشر منشورك بنجاح!")
                st.rerun()
            else:
                st.warning("لا يمكن نشر منشور فارغ.")
                
    st.write("---")
    st.subheader("📰 الحائط العام")
    
    # جلب المنشورات من قاعدة البيانات
    cursor.execute('SELECT id, username, content, likes FROM posts ORDER BY id DESC')
    posts = cursor.fetchall()
    
    if not posts:
        st.info("لا توجد منشورات حتى الآن. كن أول من ينشر!")
    
    for post in posts:
        post_id, p_user, p_content, p_likes = post
        with st.container():
            st.markdown(f"**👤 {p_user}**")
            st.write(p_content)
            
            # زر الإعجاب
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button(f"❤️ أعجبني ({p_likes})", key=f"like_{post_id}"):
                    cursor.execute('UPDATE posts SET likes = likes + 1 WHERE id = ?', (post_id,))
                    conn.commit()
                    st.rerun()
                    
            # جلب التعليقات الخاصة بهذا المنشور
            cursor.execute('SELECT username, content FROM comments WHERE post_id = ?', (post_id,))
            comments = cursor.fetchall()
            
            if comments:
                for c_user, c_content in comments:
                    st.caption(f"💬 **{c_user}**: {c_content}")
                    
            # إضافة تعليق جديد
            with st.form(key=f"comm_form_{post_id}", clear_on_submit=True):
                c_text = st.text_input("اكتب تعليقاً...", key=f"c_input_{post_id}")
                c_submit = st.form_submit_button("إرسال التعليق", key=f"c_btn_{post_id}")
                if c_submit:
                    if c_text.strip():
                        cursor.execute('INSERT INTO comments (post_id, username, content) VALUES (?, ?, ?)', (post_id, st.session_state.username, c_text))
                        conn.commit()
                        st.rerun()
                        
            st.write("---")
