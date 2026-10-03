import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="Minibook", page_icon="📱", layout="centered")

# تنسيق الألوان (أخضر وأحمر) وتصميم الشعار بارزاً
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

# عرض شعار Minibook البارز
st.markdown("<div class='brand-logo'>Minibook</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>شبكتك الاجتماعية المصغرة</div>", unsafe_allow_html=True)
st.write("---")

# تخزين المنشورات في الذاكرة المؤقتة للتطبيق
if 'posts' not in st.session_state:
    st.session_state.posts = [
        {"name": "إبراهيم", "text": "أهلاً بالجميع، شعار Minibook أصبح يزين التطبيق بشكل رائع 🚀", "likes": 10, "comments": ["تبارك الله، شعار ممتاز!"]}
    ]

# صندوق إنشاء منشور جديد
st.subheader("✍️ ماذا تخطط أو تشارك اليوم؟")
with st.form("post_form", clear_on_submit=True):
    user_name = st.text_input("اسمك الكريم:", placeholder="اكتب اسمك هنا...")
    post_text = st.text_input("ما يدور في ذهنك؟", placeholder="اكتب منشورك هنا...")
    submit_button = st.form_submit_button("نشر المنشور")

    if submit_button:
        if user_name and post_text:
            st.session_state.posts.insert(0, {"name": user_name, "text": post_text, "likes": 0, "comments": []})
            st.success("تم نشر منشورك بنجاح!")
        else:
            st.warning("الرجاء إدخال الاسم ومحتوى المنشور قبل النشر.")

st.write("---")
st.subheader("📰 حائط المنشورات")

# عرض المنشورات وتفاعلاتها
for idx, post in enumerate(st.session_state.posts):
    with st.container():
        st.markdown(f"**👤 {post['name']}**")
        st.write(post['text'])
        
        # أزرار الإعجاب والتعليق
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button(f"❤️ أعجبني ({post['likes']})", key=f"like_{idx}"):
                st.session_state.posts[idx]['likes'] += 1
                st.rerun()
                
        # عرض التعليقات الحالية
        if post['comments']:
            for comment in post['comments']:
                st.caption(f"💬 {comment}")
                
        # إضافة تعليق جديد
        new_comment = st.text_input("اكتب تعليقاً...", key=f"comm_input_{idx}")
        if st.button("إرسال التعليق", key=f"comm_btn_{idx}"):
            if new_comment:
                st.session_state.posts[idx]['comments'].append(new_comment)
                st.rerun()
                
        st.write("---")
