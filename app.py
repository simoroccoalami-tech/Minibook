import streamlit as st

# إعدادات صفحة Minibook
st.set_page_config(page_title="Minibook", page_icon="🌐", layout="centered")

# عنوان التطبيق وشعار يشبه فيسبوك
st.markdown("<h1 style='text-align: center; color: #1877F2;'>شبكتي الاجتماعية المصغرة 🌐 Minibook</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>مرحباً بك! شارك أفكارك ومنشوراتك مع العالم.</p>", unsafe_allow_html=True)

# تهيئة ذاكرة المنشورات مؤقتاً
if "posts" not in st.session_state:
    st.session_state.posts = ["أهلاً بالجميع، هذا أول منشور لي على التطبيق 🚀"]

# خانة كتابة المنشور باستخدام st.text_input لتجنب مشاكل لوحة المفاتيح على الجوال
new_post = st.text_input("", placeholder="ماذا تخطط أو تشارك اليوم؟", label_visibility="collapsed")

# زر النشر
if st.button("نشر"):
    if new_post.strip() != "":
        # إضافة المنشور الجديد في أول القائمة
        st.session_state.posts.insert(0, new_post)
        st.success("تم نشر منشورك بنجاح!")
    else:
        st.warning("الرجاء كتابة شيء قبل النشر.")

st.markdown("---")
st.markdown("### 📰 حائط المنشورات")

# عرض المنشورات
for post in st.session_state.posts:
    st.info(post)
