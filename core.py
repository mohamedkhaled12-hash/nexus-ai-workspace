import json
import uuid
from datetime import datetime
import google.generativeai as genai
import requests

# ================= المفاتيح =================
GEMINI_API_KEY = "AIzaSyB75FnXfQZpboY1bHfEVUkUpmj55SDj3I8"
LINKEDIN_ACCESS_TOKEN = "AQULY0mwQ2v1zhWRFvwspSPFLQyljE7LsuLdoSNFoUAI0EniBZw7K5qx2Rd43v-jbd8CtO2lGVxB8JT8cnLglnJv4pKilNHxIWk404TSLihHyCDKKEzdDCjCYthlR_8IHlQBDU2-VmNSxXQKXbPrSJ2XRFaZ_iy6kZqLlR8LEB6edWj7jerf1034wmXbT5R__XdfR4EjQNfvXHZ07xxF8833b55jG2i9wuDOricQzUtmhpITOjq-_hk5Z8KMhzdhwxiiC9q7_Vwyi05ViZxyLnu9833A0bGnbG3rFtKZI1jYefI6J0LfyMglk5KdpfUAlupUB2J0H4NtyaeofeD1UyaUxA4RSA"
LINKEDIN_AUTHOR_URN = "urn:li:person:GeRhTnLpiR" # تم إضافته بنجاح
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