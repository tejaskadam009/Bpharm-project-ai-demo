import streamlit as st
import requests
from PIL import Image

# ----------------- PAGE SETUP -----------------
st.set_page_config(page_title="AI Health Guidance Demo", page_icon="🩺")
st.title("🩺 AI Health Guidance (B.Pharm Demo)")
st.caption("⚠️ For awareness/education only. Not a medical diagnosis tool.")

HF_TOKEN = st.secrets.get("HF_TOKEN", "")

# ✅ This model works well with text-generation API
TEXT_MODEL = "google/flan-t5-base"

# ----------------- DEMO CASES -----------------
demo_cases = {
    "Case 1: Fever + Body pain": "I have fever, body pain, weakness since 2 days.",
    "Case 2: Cough + Sore throat": "I have cough, sore throat and mild fever since 3 days.",
    "Case 3: Itching + Ring rash": "I have itching and circular red rash on my arm since 1 week.",
    "Case 4: Loose motion + Vomiting": "I have vomiting and loose motion since 1 day.",
    "Case 5: Chest pain + Breathlessness (Emergency)": "I have chest pain and breathlessness suddenly."
}

st.subheader("✅ Select a Demo Case")
selected_case = st.selectbox("Choose a case", list(demo_cases.keys()))
symptoms_text = demo_cases[selected_case]
st.info(symptoms_text)

# ----------------- IMAGE UPLOAD -----------------
st.subheader("📷 Upload Image (Optional)")
uploaded_file = st.file_uploader("Upload a rash / wound / skin image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)

# ----------------- FUNCTION: HF ROUTER TEXT GENERATION -----------------
def hf_text_generate(prompt: str) -> str:
    if not HF_TOKEN:
        return "❌ HF_TOKEN missing. Add it in Streamlit → Manage App → Secrets."

    url = f"https://router.huggingface.co/hf-inference/models/{TEXT_MODEL}/pipeline/text2text-generation"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 250,
            "temperature": 0.4
        },
        "options": {
            "wait_for_model": True
        }
    }

    r = requests.post(url, headers=headers, json=payload, timeout=60)

    # If HTML/text response comes
    if "application/json" not in r.headers.get("content-type", ""):
        return f"❌ Text model error: {r.status_code}\n{r.text}"

    data = r.json()

    if r.status_code != 200:
        return f"❌ Text model error: {r.status_code}\n{data}"

    # flan-t5 returns list format
    if isinstance(data, list) and len(data) > 0:
        return data[0].get("generated_text", "No response")

    return str(data)

# ----------------- GENERATE BUTTON -----------------
st.subheader("🧾 Get Result")
if st.button("Generate Guidance ✅"):
    prompt = f"""
You are a health assistant for a pharmacy college demo project.
Do NOT give confirmed diagnosis.
Give only probable conditions, risk level, basic advice, and when to see doctor urgently.

Symptoms: {symptoms_text}

Return output exactly in format:
1) Possible condition (probable)
2) Risk level: Low/Medium/High
3) What to do now (simple steps)
4) When to visit doctor urgently
5) Disclaimer (1 line)
"""

    output = hf_text_generate(prompt)
    st.success(output)

st.caption("⚠️ For demo/education only. Always consult a qualified doctor for diagnosis and treatment.")
