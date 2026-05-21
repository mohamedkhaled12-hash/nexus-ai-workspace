import json
import uuid
from datetime import datetime
import google.generativeai as genai
import requests
import streamlit as st

# استدعاء المفاتيح بأمان من سيرفر ستريمليت
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
LINKEDIN_ACCESS_TOKEN = st.secrets["LINKEDIN_ACCESS_TOKEN"]
LINKEDIN_AUTHOR_URN = st.secrets["LINKEDIN_AUTHOR_URN"] # تم إضافته بنجاح
# ============================================

genai.configure(api_key=GEMINI_API_KEY)

def load_posts():
    try:
        with open("posts.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_posts(posts):
    with open("posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)

def generate_ai_post(topic, tone="Professional"):
    # بنستخدم أحدث موديل من جوجل
    model = genai.GenerativeModel('gemini-2.5-flash') 
    prompt = f"اكتب بوست احترافي ومميز على لينكد إن باللغة العربية عن: {topic}. نبرة الصوت: {tone}. استخدم إيموجيز مناسبة ونسق الكلام بفقرات قصيرة."
    
    try:
        response = model.generate_content(prompt)
        content = response.text
    except Exception as e:
        return {"error": str(e)}

    posts = load_posts()
    new_post = {
        "id": str(uuid.uuid4())[:8],
        "topic": topic,
        "content": content,
        "status": "Waiting Approval",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    posts.append(new_post)
    save_posts(posts)
    return new_post

def publish_to_linkedin(content):
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    payload = {
        "author": LINKEDIN_AUTHOR_URN,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code == 201
