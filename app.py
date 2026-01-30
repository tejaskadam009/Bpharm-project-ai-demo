import streamlit as st
import requests
from PIL import Image

# ----------------- PAGE SETUP -----------------
st.set_page_config(page_title="AI Health Guidance Demo", page_icon="🩺")
st.title("🩺 AI Health Guidance (B.Pharm Demo)")
st.caption("⚠️ For awareness/education only. Not a medical diagnosis tool.")

# ----------------- HUGGING FACE SETTINGS -----------------
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

# A good open instruct model (works well for demo)
TEXT_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

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

# ----------------- IMAGE UPLOAD (OPTIONAL) -----------------
st.subheader("📷 Upload Image (Optional)")
uploaded_file = st.file_uploader("Upload a rash / wound / skin image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)

# ----------------- FUNCTION: CALL HF ROUTER CHAT API -----------------
def hf_chat_generate(prompt: str) -> str:
    if not HF_TOKEN:
        return "❌ HF_TOKEN missing. Add it in Streamlit → Manage App → Secrets."

    url = f"https://router.huggingface.co/hf-inference/models/{TEXT_MODEL}/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
    }

    system_msg = (
        "You are an AI Health Guidance assistant made for a pharmacy college demo project. "
        "Do NOT give a confirmed diagnosis. "
        "Give only possible condition (probable), risk level, basic guidance, and when to see a doctor urgently. "
        "Do not prescribe strong medicines. Keep it safe."
    )

    payload = {
        "model": TEXT_MODEL,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 350,
        "temperature": 0.4
    }

    r = requests.post(url, headers=headers, json=payload, timeout=60)

    if r.status_code != 200:
        return f"❌ Text model error: {r.status_code}\n\n{r.text}"

    data = r.json()
    return data["choices"][0]["message"]["content"]

# ----------------- GENERATE BUTTON -----------------
st.subheader("🧾 Get Result")

if st.button("Generate Guidance ✅"):
    prompt = f"""
User Symptoms:
{symptoms_text}

Task:
Return output in EXACT format:
1) Possible condition (probable)
2) Risk level: Low/Medium/High
3) What to do now (simple steps)
4) When to visit doctor urgently
5) Disclaimer (1 line)
"""
    output = hf_chat_generate(prompt)
    st.success(output)

st.caption("⚠️ For demo/education only. Always consult a qualified doctor for diagnosis and treatment.")
