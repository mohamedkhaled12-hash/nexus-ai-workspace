import streamlit as st
import pandas as pd
from datetime import datetime
from core import generate_ai_post, load_posts, save_posts, publish_to_linkedin

# ==================== 1. إعدادات الصفحة ====================
st.set_page_config(page_title="Nexus AI - RGB Workspace", page_icon="✨", layout="wide")

# ==================== 2. إدارة الحالة (شاشة الدخول والرجوع) ====================
if 'app_unlocked' not in st.session_state:
    st.session_state.app_unlocked = False

# ==================== 3. كود الـ CSS (نظام الـ RGB الشامل والتطوير الجديد) ====================
st.markdown("""
    <style>
    :root { color-scheme: dark; }
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Tajawal:wght@400;500;700;800&display=swap');
    
    [data-testid="stToolbar"] { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #020203; /* أسود أعمق لزيادة تباين الـ RGB */
        font-family: 'Inter', 'Tajawal', sans-serif;
        color: #F4F4F5;
    }

    /* ================= أنيميشن الـ RGB الأساسي ================= */
    @keyframes rgb-animate {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .rgb-text {
        background: linear-gradient(90deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000);
        background-size: 300% auto;
        color: #fff;
        background-clip: text;
        text-fill-color: transparent;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: rgb-animate 6s linear infinite;
    }

    .rgb-border {
        position: relative;
        background: #09090B;
        border-radius: 16px;
        z-index: 1;
        transition: transform 0.3s ease;
    }
    .rgb-border::before {
        content: ""; position: absolute; top: -2px; left: -2px; right: -2px; bottom: -2px;
        background: linear-gradient(90deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000);
        background-size: 300%; border-radius: 18px; z-index: -1;
        animation: rgb-animate 6s linear infinite; opacity: 0.5; transition: opacity 0.3s ease, filter 0.3s ease;
    }
    .rgb-border:hover { transform: translateY(-5px); }
    .rgb-border:hover::before { opacity: 1; filter: blur(8px); }

    /* ================= شاشة الدخول ================= */
    .welcome-screen {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        height: 75vh; text-align: center;
    }
    .welcome-title { font-size: 95px; font-weight: 800; margin-bottom: 5px; letter-spacing: -4px; text-transform: uppercase;}
    .welcome-subtitle { color: #A1A1AA; font-size: 20px; font-weight: 600; margin-bottom: 50px; letter-spacing: 5px; text-transform: uppercase; }

    /* ================= القائمة الجانبية ================= */
    div[role="radiogroup"]:not([aria-orientation="horizontal"]) { gap: 10px !important; }
    div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label {
        background: rgba(255, 255, 255, 0.02) !important; border: 1px solid rgba(255,255,255,0.03) !important; 
        border-radius: 10px !important; padding: 14px 18px !important; width: 100%; cursor: pointer; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label:hover { background: rgba(255, 255, 255, 0.06) !important; transform: translateX(8px); box-shadow: -5px 5px 15px rgba(0,0,0,0.3);}
    
    div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label[data-checked="true"] {
        background: rgba(15, 15, 19, 0.9) !important; 
        border-left: 4px solid transparent !important;
        border-image: linear-gradient(to bottom, #ff00c8, #00ffd5, #fffb00) 1 100% !important;
        box-shadow: inset 40px 0 50px -30px rgba(0, 255, 213, 0.2);
    }
    div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label > div:first-child { display: none !important; } 
    div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label p { font-size: 14px !important; font-weight: 600 !important; color: #81818A !important; margin: 0 !important; }
    div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label[data-checked="true"] p { color: #FFFFFF !important; font-weight: 800 !important; letter-spacing: 0.5px;}

    /* ================= الكروت الزجاجية (Metric Cards) ================= */
    .metric-card { 
        padding: 24px; height: 120px; margin-bottom: 20px; display: flex; flex-direction: column; justify-content: center;
        background: rgba(15, 15, 19, 0.6); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    }
    .metric-card-header { display: flex; justify-content: space-between; color: #A1A1AA; font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px;}
    .metric-card-value { font-size: 42px; font-weight: 800; color: #FFFFFF; margin-top: 5px; text-shadow: 0 0 20px rgba(255,255,255,0.2);}

    /* ================= مربعات النصوص ================= */
    div[data-baseweb="textarea"] textarea { 
        background-color: #0A0A0C !important; color: #E4E4E7 !important; border: 1px solid #27272A !important; 
        border-radius: 12px !important; font-size: 15px !important; line-height: 1.7 !important; transition: all 0.3s ease; 
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.4) !important; padding: 15px !important;
    }
    div[data-baseweb="textarea"] textarea:focus { 
        border-color: #00ffd5 !important; background-color: #050507 !important;
        box-shadow: 0 0 20px rgba(0, 255, 213, 0.15), inset 0 2px 10px rgba(0,0,0,0.5) !important; 
    }

    /* ================= تصميم الأزرار ================= */
    div.stButton > button { 
        border-radius: 12px !important; font-weight: 800 !important; transition: all 0.3s ease; padding: 22px !important; 
        background: #121215 !important; border: 1px solid #27272A !important; color: #E4E4E7 !important; text-transform: uppercase; letter-spacing: 1.5px; font-size: 13px !important;
    }
    div.stButton > button:hover { background: #1F1F24 !important; color: #FFFFFF !important; border-color: #3F3F46 !important; box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
    
    /* الأزرار الأساسية (RGB) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000) !important;
        background-size: 300% !important; color: white !important; border: none !important; 
        animation: rgb-animate 5s linear infinite !important; box-shadow: 0 5px 25px rgba(0, 255, 213, 0.3) !important;
    }
    div.stButton > button[kind="primary"]:hover { filter: brightness(1.2); box-shadow: 0 8px 35px rgba(255, 0, 200, 0.5) !important; transform: translateY(-2px); }

    /* ================= زرار الرجوع للشاشة الأساسية (Lock Button) ================= */
    .lock-btn-container > div > button {
        background: rgba(255, 0, 0, 0.05) !important;
        border: 1px solid rgba(255, 0, 0, 0.2) !important;
        color: #ff4d4d !important;
        margin-top: 30px;
        padding: 15px !important;
        box-shadow: none !important;
    }
    .lock-btn-container > div > button:hover {
        background: rgba(255, 0, 0, 0.15) !important;
        border-color: rgba(255, 0, 0, 0.5) !important;
        color: #ffffff !important;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.4) !important;
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# ==================== 4. إدارة البيانات (الكود الحساس - بدون أي تغيير) ====================
posts = load_posts()

total_generated = len(posts)
published_count = len([p for p in posts if "Published" in p.get('status', '')])
pending_posts = [p for p in posts if "Waiting Approval" in p.get('status', '')]
pending_count = len(pending_posts)

default_post = "التشغيل الآلي للينكد إن لم يعد رفاهية، بل أصبح ضرورة لكل محترف يسعى لتوسيع شبكته دون إهدار الوقت.\n\nمن خلال تجربتي مع أداة Nexus AI، تمكنت من مضاعفة إنتاجيتي بنسبة 100% 🚀\n\nما هي أداتك المفضلة لتوفير الوقت؟ 👇\n\n#الذكاء_الاصطناعي #تطوير_الأعمال"

if 'generated_text' not in st.session_state:
    st.session_state.generated_text = default_post

def draw_linkedin_preview(content_text):
    st.markdown(f"""
        <div class='rgb-border' style='background:#ffffff; border-radius:16px; padding:25px; color:#191919; text-align:right; direction:rtl;'>
            <div style='text-align:left; margin-bottom:20px;'><span class='rgb-text' style='font-weight:900; font-size:11px; letter-spacing:1.5px; text-transform:uppercase; background:rgba(0,0,0,0.05); padding:4px 10px; border-radius:4px;'>✦ Live Preview</span></div>
            <div style='display:flex; align-items:center; margin-bottom:18px; gap:12px;'>
                <div style='width:52px; height:52px; border-radius:50%; background:#09090B; color:white; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:18px;'>MK</div>
                <div>
                    <div style='font-weight:800; font-size:16px; color:#191919; margin-bottom:2px;'>Mohamed Khaled</div>
                    <div style='color:#71717A; font-size:12px; line-height:1.4;'>Junior Data Analyst & Student at Faculty of Commerce</div>
                    <div style='color:#71717A; font-size:12px;'>الآن • 🌐</div>
                </div>
            </div>
            <div style='font-size:15px; line-height:1.7; color:#27272A; white-space:pre-wrap; margin-bottom:18px;'>{content_text}</div>
            <div style='width:100%; height:160px; background:linear-gradient(135deg, #F4F4F5, #E4E4E7); border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:45px; margin-bottom:18px;'>📊</div>
            <div style='color:#71717A; font-size:13px; display:flex; justify-content:space-between; padding-bottom:14px; border-bottom:1px solid #E4E4E7; font-weight:600;'>
                <span>👍❤️ 24 إعجاب</span>
                <span>12 تعليق • 4 مشاركات</span>
            </div>
            <div style='display:flex; justify-content:space-between; padding-top:14px; color:#52525B; font-size:14px; font-weight:800;'>
                <span style='cursor:pointer;'>👍 أعجبني</span>
                <span style='cursor:pointer;'>💬 تعليق</span>
                <span style='cursor:pointer;'>🔁 إعادة نشر</span>
                <span style='cursor:pointer;'>➤ إرسال</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==================== 5. الهيكل الأساسي للتطبيق ====================

if not st.session_state.app_unlocked:
    st.markdown("""
        <div class="welcome-screen">
            <div class="welcome-title rgb-text">NEXUS AI PRO</div>
            <div class="welcome-subtitle">Advanced RGB Workspace</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.2, 1, 1.2])
    with col2:
        if st.button("🚀 INITIALIZE SYSTEM", type="primary", use_container_width=True):
            st.session_state.app_unlocked = True
            st.rerun()

else:
    col_nav, col_main = st.columns([1, 4.5], gap="large")

    with col_nav:
        st.markdown("""
            <div style='display:flex; align-items:center; margin-bottom: 45px; margin-top: 10px; padding: 0 5px;'>
                <div class='rgb-border' style='width: 45px; height: 45px; border-radius: 12px; margin-right: 15px; display: flex; align-items: center; justify-content: center; font-size: 20px;'>⚡</div>
                <div>
                    <div class="rgb-text" style='font-size:26px; font-weight:800; letter-spacing: -1px; margin-bottom:-4px;'>NEXUS</div>
                    <div style='font-size:10px; color:#A1A1AA; font-weight:800; letter-spacing:2px;'>PRO EDITION</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        selected_page = st.radio(
            "Navigation",
            [
                "📊 Dashboard", 
                "✨ Generator", 
                "📋 Queue", 
                "📚 Content Hub",
                "📈 Analytics",   
                "📅 Calendar",    
                "⚡ Automations", 
                "⚙️ Settings"     
            ],
            label_visibility="collapsed"
        )
        
        # ====== زرار الرجوع للشاشة الأساسية (الجديد) ======
        st.markdown("<div class='lock-btn-container'>", unsafe_allow_html=True)
        if st.button("🔒 قفل النظام (العودة للرئيسية)", use_container_width=True):
            st.session_state.app_unlocked = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_main:
        # -------------------- DASHBOARD --------------------
        if selected_page == "📊 Dashboard":
            st.markdown("<h2 class='rgb-text' style='margin-bottom:5px; font-weight:800; letter-spacing:-1px;'>System Overview</h2>", unsafe_allow_html=True)
            st.markdown("<div style='color: #00ffd5; font-size: 11px; font-weight: 800; margin-bottom: 30px; letter-spacing: 2px;'>● CORE ENGINE ONLINE</div>", unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"<div class='rgb-border metric-card'><div class='metric-card-header'><span>Total Generated</span><span class='rgb-text'>↗</span></div><div class='metric-card-value'>{total_generated}</div></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='rgb-border metric-card'><div class='metric-card-header'><span>Published Posts</span><span style='color:#00ffd5'>✓</span></div><div class='metric-card-value'>{published_count}</div></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div class='rgb-border metric-card'><div class='metric-card-header'><span>In Queue</span><span style='color:#ff00c8'>⏳</span></div><div class='metric-card-value'>{pending_count}</div></div>", unsafe_allow_html=True)

            st.divider()
            
            col_q, col_p = st.columns([1.2, 1], gap="large")
            with col_q:
                st.markdown("<h3 style='color:#F4F4F5; font-size:16px; font-weight:800; margin-bottom:15px; text-transform:uppercase; letter-spacing:1px;'>≡ Pending Tasks</h3>", unsafe_allow_html=True)
                if not pending_posts:
                    st.info("الطابور فارغ. اذهب لقسم التوليد لصنع محتوى جديد!")
                else:
                    for p in pending_posts[:3]: 
                        st.markdown(f"""
                        <div class='rgb-border' style='padding:18px 22px; margin-bottom:15px;'>
                            <div style='display:flex; justify-content:space-between; align-items:flex-start;'>
                                <div style='font-size:15px; font-weight:600; color:#E4E4E7; direction:rtl; text-align:right; line-height:1.6;'>{p['topic']}</div>
                                <div style='background:rgba(0, 255, 213, 0.1); color:#00ffd5; padding:4px 10px; border-radius:6px; font-size:10px; font-weight:800; margin-left:15px;'>READY</div>
                            </div>
                            <div style='color:#71717A; font-size:11px; margin-top:12px; font-weight:700;'>{p['date']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
            with col_p:
                preview_text = pending_posts[0]['content'] if pending_posts else default_post
                draw_linkedin_preview(preview_text)

        # -------------------- GENERATOR --------------------
        elif selected_page == "✨ Generator":
            st.markdown("<h2 class='rgb-text' style='margin-bottom:5px; font-weight:800; letter-spacing:-1px;'>Post Generator</h2>", unsafe_allow_html=True)
            st.markdown("<div style='color: #A1A1AA; font-size: 14px; margin-bottom: 30px; font-weight:600;'>Craft high-impact LinkedIn content with AI.</div>", unsafe_allow_html=True)

            col_gen, col_prev = st.columns([1, 1], gap="large")

            with col_gen:
                st.markdown("<div class='rgb-border' style='padding:25px;'>", unsafe_allow_html=True)
                tone = st.radio("اختر نبرة الكتابة (Tone):", ["احترافي Professional", "قصصي Storytelling", "غير رسمي Casual"], index=1, horizontal=True)
                st.write("")
                topic = st.text_area("عن ماذا تريد أن تكتب اليوم؟", placeholder="اكتب الفكرة أو الموضوع هنا...", height=120)
                st.write("")
                
                if st.button("✨ GENERATE AI POST", type="primary", use_container_width=True):
                    if topic:
                        with st.spinner("الذكاء الاصطناعي يقوم بصياغة المحتوى..."):
                            res = generate_ai_post(topic, tone)
                            if "error" not in res:
                                st.session_state.generated_text = res["content"]
                                st.rerun()
                            else:
                                st.error(f"تفاصيل الخطأ: {res['error']}")
                    else:
                        st.warning("رجاءً اكتب فكرة البوست أولاً!")
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.write("")
                st.markdown("<h4 style='color:#00ffd5; font-size:14px; font-weight:700; text-transform:uppercase; letter-spacing:1px;'>✍️ Edit Draft Before Publishing:</h4>", unsafe_allow_html=True)
                edited_draft = st.text_area("تعديل", value=st.session_state.generated_text, height=220, label_visibility="collapsed")

            with col_prev:
                draw_linkedin_preview(edited_draft)
                st.write("")
                if st.button("🚀 PUBLISH IMMEDIATELY", use_container_width=True):
                    if "التشغيل الآلي" not in edited_draft:
                        with st.spinner("جاري النشر على حسابك..."):
                            if publish_to_linkedin(edited_draft):
                                st.success("تم النشر على لينكد إن بنجاح! 🎉")
                            else:
                                st.error("فشل النشر. تأكد من صلاحية الـ Token.")
                    else:
                        st.warning("قم بتوليد بوست أولاً لنشره!")

        # -------------------- QUEUE --------------------
        elif selected_page == "📋 Queue":
            st.markdown("<h2 class='rgb-text' style='margin-bottom:5px; font-weight:800; letter-spacing:-1px;'>Publishing Queue</h2>", unsafe_allow_html=True)
            st.markdown("<div style='color: #00ffd5; font-size: 13px; margin-bottom: 30px; font-weight:600;'>Review, edit, and approve your pending drafts.</div>", unsafe_allow_html=True)
            
            if not pending_posts:
                st.info("🎉 الطابور فارغ! لا يوجد مسودات تنتظر الموافقة.")
            else:
                for p in pending_posts:
                    with st.container():
                        st.markdown(f"""
                        <div class='rgb-border' style='padding:20px; border-radius:16px 16px 0 0; border-bottom:none;'>
                            <div style='font-size:16px; font-weight:700; color:#E4E4E7; margin-bottom:8px; direction:rtl; text-align:right;'>📌 الفكرة: {p['topic']}</div>
                            <div style='font-size:12px; color:#A1A1AA; direction:rtl; text-align:right; font-weight:600;'>تاريخ الإنشاء: {p['date']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        edited_q_content = st.text_area("✍️ يمكنك تعديل المسودة هنا:", p['content'], height=180, key=f"txt_{p['id']}")
                        
                        c_btn1, c_btn2 = st.columns(2)
                        if c_btn1.button("✅ APPROVE & PUBLISH", type="primary", key=f"pub_{p['id']}", use_container_width=True):
                            with st.spinner("جاري النشر..."):
                                if publish_to_linkedin(edited_q_content):
                                    for index, item in enumerate(posts):
                                        if item['id'] == p['id']:
                                            posts[index]['status'] = "Approved & Published"
                                            posts[index]['content'] = edited_q_content
                                    save_posts(posts)
                                    st.rerun()
                        
                        if c_btn2.button("❌ REJECT & DELETE", key=f"rej_{p['id']}", use_container_width=True):
                            for index, item in enumerate(posts):
                                if item['id'] == p['id']:
                                    posts[index]['status'] = "Rejected"
                            save_posts(posts)
                            st.rerun()
                    st.write("")
                    st.write("")

        # -------------------- CONTENT Hub --------------------
        elif selected_page == "📚 Content Hub":
            st.markdown("<h2 class='rgb-text' style='margin-bottom:5px; font-weight:800; letter-spacing:-1px;'>Content Hub</h2>", unsafe_allow_html=True)
            st.markdown("<div style='color: #A1A1AA; font-size: 14px; margin-bottom: 30px; font-weight:600;'>أرشيف جميع البوستات التي تم توليدها مسبقاً.</div>", unsafe_allow_html=True)
            
            if posts:
                df = pd.DataFrame(posts)
                df = df[['date', 'topic', 'status']]
                st.dataframe(df, use_container_width=True)
            else:
                st.write("قاعدة البيانات فارغة.")
                
        # -------------------- ANALYTICS --------------------
        elif selected_page == "📈 Analytics":
            st.markdown("<h2 class='rgb-text' style='margin-bottom:5px; font-weight:800; letter-spacing:-1px;'>Advanced Analytics</h2>", unsafe_allow_html=True)
            st.markdown("<div style='color: #00ffd5; font-size: 13px; margin-bottom: 30px; font-weight:600;'>Real-time AI Efficiency & Content Insights.</div>", unsafe_allow_html=True)
            
            col_a1, col_a2, col_a3 = st.columns(3)
            with col_a1:
                st.markdown("<div class='rgb-border metric-card'><div class='metric-card-header'>AI Writing Speed</div><div class='metric-card-value'>4.2s <span style='font-size:14px; color:#00ffd5;'>avg</span></div></div>", unsafe_allow_html=True)
            with col_a2:
                st.markdown("<div class='rgb-border metric-card'><div class='metric-card-header'>Acceptance Rate</div><div class='metric-card-value'>94% <span style='font-size:14px; color:#00ffd5;'>↑</span></div></div>", unsafe_allow_html=True)
            with col_a3:
                st.markdown("<div class='rgb-border metric-card'><div class='metric-card-header'>Time Saved</div><div class='metric-card-value'>32 <span style='font-size:14px; color:#ff00c8;'>Hours</span></div></div>", unsafe_allow_html=True)
                
            st.markdown("""
            <div class='rgb-border' style='padding:30px; margin-top:15px;'>
                <h4 style='color:white; margin-top:0;'>📊 AI Model Performance (Gemini 2.5 Flash)</h4>
                <div style='width:100%; background:#1F1F24; border-radius:12px; height:24px; margin-top:20px; overflow:hidden;'>
                    <div style='width:94%; height:100%; background:linear-gradient(90deg, #ff00c8, #00ffd5); animation: rgb-animate 5s infinite;'></div>
                </div>
                <p style='text-align:right; color:#A1A1AA; font-size:13px; margin-top:8px; font-weight:bold;'>94% Optimized</p>
            </div>
            """, unsafe_allow_html=True)
            
        # -------------------- CALENDAR --------------------
        elif selected_page == "📅 Calendar":
            st.markdown("<h2 class='rgb-text' style='margin-bottom:5px; font-weight:800; letter-spacing:-1px;'>Content Calendar</h2>", unsafe_allow_html=True)
            st.markdown("<div style='color: #00ffd5; font-size: 13px; margin-bottom: 30px; font-weight:600;'>جدولة المحتوى الذكية وتخطيط النشر.</div>", unsafe_allow_html=True)
            st.info("📅 واجهة جدولة البوستات بالتواريخ قيد التطوير في الإصدار القادم.")
            
        # -------------------- AUTOMATIONS --------------------
        elif selected_page == "⚡ Automations":
            st.markdown("<h2 class='rgb-text' style='margin-bottom:5px; font-weight:800; letter-spacing:-1px;'>Automation Flows</h2>", unsafe_allow_html=True)
            st.markdown("<div style='color: #00ffd5; font-size: 13px; margin-bottom: 30px; font-weight:600;'>ربط العمليات الآلية (Webhook & API Triggers).</div>", unsafe_allow_html=True)
            st.info("⚡ واجهة الربط الآلي مع منصات خارجية مثل n8n قيد التطوير.")

        # -------------------- SETTINGS --------------------
        elif selected_page == "⚙️ Settings":
            st.markdown("<h2 class='rgb-text' style='margin-bottom:5px; font-weight:800; letter-spacing:-1px;'>System Settings</h2>", unsafe_allow_html=True)
            st.markdown("<div style='color: #A1A1AA; font-size: 14px; margin-bottom: 30px; font-weight:600;'>Manage API integrations and workspace preferences.</div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class='rgb-border' style='padding:30px; margin-bottom: 25px;'>
                <h4 style='margin-top:0; color:#fff; display:flex; align-items:center; gap:10px;'><span style='font-size:24px;'>🔑</span> API Connections</h4>
                <hr style='border-color:rgba(255,255,255,0.1); margin:20px 0;'>
                <div style='display:flex; justify-content:space-between; margin-bottom:20px; align-items:center;'>
                    <div>
                        <div style='font-weight:800; color:white; font-size:16px;'>LinkedIn UGC API</div>
                        <div style='color:#71717A; font-size:13px;'>urn:li:person:GeRhTnLpiR</div>
                    </div>
                    <div style='background:rgba(0, 255, 213, 0.1); color:#00ffd5; padding:8px 16px; border-radius:8px; font-weight:800; font-size:12px; letter-spacing:1px;'>CONNECTED</div>
                </div>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div>
                        <div style='font-weight:800; color:white; font-size:16px;'>Google Gemini Engine</div>
                        <div style='color:#71717A; font-size:13px;'>gemini-2.5-flash</div>
                    </div>
                    <div style='background:rgba(0, 255, 213, 0.1); color:#00ffd5; padding:8px 16px; border-radius:8px; font-weight:800; font-size:12px; letter-spacing:1px;'>CONNECTED</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.button("💾 SAVE CONFIGURATIONS", type="primary", use_container_width=True)
