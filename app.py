import streamlit as st
import requests
from PIL import Image

# ----------------- PAGE SETUP -----------------
st.set_page_config(page_title="AI Health Guidance Demo", page_icon="🩺")
st.title("🩺 AI Health Guidance (B.Pharm Demo)")
st.caption("⚠️ For awareness/education only. Not a medical diagnosis tool.")

# ----------------- HUGGING FACE SETTINGS -----------------
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

# ✅ Use a text2text model (good for instructions + structured output)
TEXT_MODEL = "google/flan-t5-base"

# ----------------- DEMO CASES -----------------
demo_cases = {
    "Case 1: Fever + Body pain": "I have fever, body pain, weakness since 2 days.",
    "Case 2: Cough + Sore throat": "I have cough, sore throat and mild fever since 3 days.",
    "Case 3: Itching + Ring rash (suspected fungal)": "I have itching and circular red rash on my arm since 1 week.",
    "Case 4: Loose motion + Vomiting": "I have vomiting and loose motion since 1 day.",
    "Case 5: Chest pain + Breathlessness (Emergency)": "I have chest pain and breathlessness suddenly."
}

st.subheader("✅ Select a Demo Case")
selected_case = st.selectbox("Choose a case", list(demo_cases.keys()))
symptoms_text = demo_cases[selected_case]
st.info(symptoms_text)

# ----------------- IMAGE UPLOAD (OPTIONAL) -----------------
st.subheader("📷 Upload Image (Optional)")
uploaded_file = st.file_uploader("Upload a rash / wound / skin image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)

# ----------------- HF ROUTER TEXT GENERATION FUNCTION -----------------
def hf_text_generate(prompt: str) -> str:
    if not HF_TOKEN:
        return "❌ HF_TOKEN missing. Add it in Streamlit → Manage App → Secrets."

    # ✅ New Router endpoint
    url = f"https://router.huggingface.co/hf-inference/models/{TEXT_MODEL}"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
        "x-use-cache": "false"
    }

    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }

    r = requests.post(url, headers=headers, json=payload, timeout=60)

    # If response is not JSON
    try:
        data = r.json()
    except:
        return f"❌ Text model error: {r.status_code}\n\n{r.text}"

    # If API returned error JSON
    if r.status_code != 200:
        return f"❌ Text model error: {r.status_code}\n\n{data}"

    # flan-t5 returns list of generated outputs
    if isinstance(data, list) and len(data) > 0:
        return data[0].get("generated_text", "No response")

    return str(data)

# ----------------- GENERATE BUTTON -----------------
st.subheader("🧾 Get Result")

if st.button("Generate Guidance ✅"):
    prompt = f"""
You are a health assistant for a pharmacy college demo project.
You MUST NOT give confirmed diagnosis.
You must give probable causes, risk level, simple advice, and when to consult doctor urgently.
Do not prescribe strong medicines. Keep it safe.

User symptoms: {symptoms_text}

Return output exactly in this format:
1) Possible condition (probable)
2) Risk level: Low/Medium/High
3) What to do now (simple steps)
4) When to visit doctor urgently
5) Disclaimer (1 line)
"""

    output = hf_text_generate(prompt)
    st.success(output)

st.caption("⚠️ For demo/education only. Always consult a qualified doctor for diagnosis and treatment.")
