import streamlit as st
import requests
from PIL import Image

st.set_page_config(page_title="AI Health Guidance Demo", page_icon="🩺")
st.title("🩺 AI Health Guidance (Demo)")
st.caption("⚠️ For awareness only. Not a diagnosis tool.")

HF_TOKEN = st.secrets.get("HF_TOKEN", "")
TEXT_MODEL = "distilbert/distilgpt2"

demo_cases = {
    "Case 1: Fever + Body pain": "I have fever, body pain, weakness since 2 days.",
    "Case 2: Cough + Sore throat": "I have cough, sore throat and mild fever since 3 days.",
    "Case 3: Itching + Ring rash": "I have itching and circular red rash on my arm since 1 week.",
    "Case 4: Loose motion + Vomiting": "I have vomiting and loose motion since 1 day.",
    "Case 5: Chest pain + Breathlessness": "I have chest pain and breathlessness suddenly."
}

st.subheader("✅ Select Demo Case")
selected_case = st.selectbox("Choose a case", list(demo_cases.keys()))
symptoms_text = demo_cases[selected_case]

st.info(symptoms_text)

st.subheader("📷 Upload Image (Optional)")
uploaded_file = st.file_uploader("Upload rash/wound image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)

def hf_text_generate(prompt):
    if not HF_TOKEN:
        return "HF token missing in Streamlit secrets."

    url = f"https://api-inference.huggingface.co/models/{TEXT_MODEL}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt}

    r = requests.post(url, headers=headers, json=payload, timeout=60)

    if r.status_code != 200:
        return f"Text model error: {r.status_code}"

    data = r.json()
    if isinstance(data, list) and len(data) > 0:
        return data[0].get("generated_text", "No response")
    return "No response"

if st.button("Generate Guidance ✅"):
    prompt = f"""
You are a health assistant for a pharmacy college demo project.
Do NOT give confirmed diagnosis.
Give possible causes, risk level, home care tips, and when to see doctor.

Symptoms: {symptoms_text}

Return output exactly in this format:
1) Possible condition (probable)
2) Risk level: Low/Medium/High
3) What to do now (simple steps)
4) When to visit doctor urgently
5) Disclaimer (1 line)
"""
    out = hf_text_generate(prompt)
    st.success(out)
