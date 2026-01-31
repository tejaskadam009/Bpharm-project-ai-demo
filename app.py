import streamlit as st
from PIL import Image

st.set_page_config(page_title="AI Health Guidance Demo", page_icon="🩺")

st.title("🩺 AI Health Guidance System (B.Pharm Final Year Demo)")
st.caption("⚠️ Educational prototype only. Not a medical diagnosis tool.")

# ---------------- DEMO CASES ----------------
cases = {
    "Case 1: Fever + Body pain": {
        "symptoms": "Fever, body pain, weakness since 2 days.",
        "output": """✅ Possible condition (probable): Viral fever / Flu-like illness
📌 Risk level: Medium
✅ What to do now:
- Rest, fluids, ORS
- Monitor temperature
- Light food
🚨 Visit doctor urgently if:
- Fever > 102°F > 2–3 days, breathing issue, dehydration
⚠️ Disclaimer: Awareness only, not confirmed diagnosis."""
    },

    "Case 2: Cough + Sore throat": {
        "symptoms": "Cough, sore throat, mild fever since 3 days.",
        "output": """✅ Possible condition (probable): Common cold / URTI
📌 Risk level: Low–Medium
✅ What to do now:
- Warm gargles, steam inhalation
- Hydration + rest
🚨 Visit doctor urgently if:
- High fever, chest pain, breathing difficulty
⚠️ Disclaimer: Awareness only."""
    },

    "Case 3: Itching + Ring rash": {
        "symptoms": "Itching and circular red rash since 1 week.",
        "output": """✅ Possible condition (probable): Fungal infection (Tinea/Ringworm)
📌 Risk level: Low
✅ What to do now:
- Keep area dry, avoid scratching
- Don’t share towels/clothes
🚨 Visit doctor urgently if:
- Spreading fast, pus, fever, no improvement 7–10 days
⚠️ Disclaimer: Awareness only."""
    },

    "Case 4: Loose motion + Vomiting": {
        "symptoms": "Vomiting + loose motions since 1 day.",
        "output": """✅ Possible condition (probable): Acute gastroenteritis / food infection
📌 Risk level: Medium
✅ What to do now:
- ORS small sips frequently
- Light foods (banana, toast, khichdi)
🚨 Visit doctor urgently if:
- Blood in stool, severe pain, dehydration signs
⚠️ Disclaimer: Awareness only."""
    },

    "Case 5: Chest pain + Breathlessness": {
        "symptoms": "Sudden chest pain + breathlessness.",
        "output": """✅ Possible condition (probable): Medical emergency
📌 Risk level: HIGH
✅ What to do now:
- Emergency care immediately
🚨 Visit doctor urgently if:
- NOW (ER immediately)
⚠️ Disclaimer: Emergency warning only."""
    },

    "Case 6: Headache + nausea + light sensitivity": {
        "symptoms": "Severe headache with nausea and light sensitivity.",
        "output": """✅ Possible condition (probable): Migraine
📌 Risk level: Medium
✅ What to do now:
- Rest in dark quiet room
- Hydration
🚨 Visit doctor urgently if:
- Sudden worst headache of life, fainting, weakness, confusion
⚠️ Disclaimer: Awareness only."""
    },

    "Case 7: Burning urination + frequent urination": {
        "symptoms": "Burning sensation while urinating + frequent urge.",
        "output": """✅ Possible condition (probable): Urinary tract infection (UTI)
📌 Risk level: Medium
✅ What to do now:
- Drink more water
- Maintain hygiene
🚨 Visit doctor urgently if:
- Fever, back pain, blood in urine
⚠️ Disclaimer: Awareness only."""
    },

    "Case 8: Sneezing + runny nose + itchy eyes": {
        "symptoms": "Sneezing, runny nose, itchy/watery eyes.",
        "output": """✅ Possible condition (probable): Allergic rhinitis
📌 Risk level: Low
✅ What to do now:
- Avoid dust/pollen triggers
- Steam inhalation
🚨 Visit doctor urgently if:
- Wheezing, breathlessness
⚠️ Disclaimer: Awareness only."""
    },

    "Case 9: Fever + red spots + joint pain": {
        "symptoms": "Fever with body rash/red spots + joint pain.",
        "output": """✅ Possible condition (probable): Viral infection (Dengue/Chikungunya possibility)
📌 Risk level: HIGH
✅ What to do now:
- Visit doctor for blood test
- Hydration
🚨 Visit doctor urgently if:
- Bleeding, severe weakness, abdominal pain
⚠️ Disclaimer: Needs medical evaluation."""
    },

    "Case 10: Stomach burning after meals": {
        "symptoms": "Burning in stomach and acidity after meals.",
        "output": """✅ Possible condition (probable): Acidity / GERD
📌 Risk level: Low–Medium
✅ What to do now:
- Avoid spicy/oily food
- Don’t lie down after eating
🚨 Visit doctor urgently if:
- Chest pain, vomiting blood, weight loss
⚠️ Disclaimer: Awareness only."""
    },

    "Case 11: Toothache + swelling": {
        "symptoms": "Tooth pain with swelling in gum/face.",
        "output": """✅ Possible condition (probable): Dental infection / abscess
📌 Risk level: Medium–High
✅ What to do now:
- Warm salt water rinse
- Dental consultation ASAP
🚨 Visit doctor urgently if:
- Fever, spreading swelling, difficulty opening mouth
⚠️ Disclaimer: Needs dental care."""
    },

    "Case 12: Eye redness + pain + discharge": {
        "symptoms": "Red eyes, irritation, discharge.",
        "output": """✅ Possible condition (probable): Conjunctivitis
📌 Risk level: Medium
✅ What to do now:
- Do not touch eyes
- Hand hygiene
🚨 Visit doctor urgently if:
- Severe pain, blurred vision, light sensitivity
⚠️ Disclaimer: Awareness only."""
    },

    "Case 13: Wheezing + breathlessness history": {
        "symptoms": "Wheezing and tightness in chest, history of asthma.",
        "output": """✅ Possible condition (probable): Asthma exacerbation
📌 Risk level: HIGH
✅ What to do now:
- Use prescribed inhaler
- Seek medical help if not improving
🚨 Visit doctor urgently if:
- Severe breathlessness, bluish lips, unable to speak
⚠️ Disclaimer: Emergency possible."""
    },

    "Case 14: Small cut/wound with redness": {
        "symptoms": "Small wound with redness and mild pain.",
        "output": """✅ Possible condition (probable): Local infection/inflammation
📌 Risk level: Medium
✅ What to do now:
- Clean gently, keep dry
- Watch for pus/swelling
🚨 Visit doctor urgently if:
- Fever, spreading redness, severe pain
⚠️ Disclaimer: Awareness only."""
    },

    "Case 15: Dizziness on standing": {
        "symptoms": "Feeling dizzy when standing up quickly.",
        "output": """✅ Possible condition (probable): Low BP / dehydration / weakness
📌 Risk level: Medium
✅ What to do now:
- Hydrate, eat properly
- Stand up slowly
🚨 Visit doctor urgently if:
- Fainting, chest pain, persistent dizziness
⚠️ Disclaimer: Awareness only."""
    }
}

# -------------------- UI --------------------
st.subheader("✅ Demo Mode (Predefined cases)")
selected = st.selectbox("Choose a case for demo", list(cases.keys()))
st.info("📌 Symptoms: " + cases[selected]["symptoms"])

st.subheader("📷 Upload Image (Optional)")
uploaded_file = st.file_uploader("Upload rash / wound / skin photo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)

if st.button("Generate Demo Guidance ✅"):
    st.success(cases[selected]["output"])

st.divider()

# -------------------- CUSTOM CHAT STYLE INPUT --------------------
st.subheader("💬 Custom Symptoms Chat Box (Prototype)")

user_input = st.text_area(
    "Type your symptoms here (example: fever + cough + tiredness)",
    placeholder="Write your symptoms..."
)

def rule_based_response(text: str) -> str:
    t = text.lower()

    # Emergency rules
    if "chest pain" in t or "breathless" in t or "breathlessness" in t:
        return """✅ Possible condition (probable): Emergency condition
📌 Risk level: HIGH
✅ What to do now:
- Seek emergency medical care immediately
🚨 Urgent warning:
- Go to hospital NOW
⚠️ Disclaimer: Not a diagnosis tool."""

    if "blood" in t and ("vomit" in t or "stool" in t):
        return """✅ Possible condition (probable): Internal bleeding possibility
📌 Risk level: HIGH
✅ What to do now:
- Emergency doctor consultation immediately
⚠️ Disclaimer: Not a diagnosis tool."""

    # Common conditions
    if "fever" in t and ("cough" in t or "sore throat" in t):
        return """✅ Possible condition (probable): Viral fever / cold/flu
📌 Risk level: Medium
✅ What to do now:
- Rest + fluids + monitor fever
🚨 Visit doctor if fever >3 days or breathing issue
⚠️ Disclaimer: Not a diagnosis tool."""

    if "itch" in t or "ring rash" in t or "circular rash" in t:
        return """✅ Possible condition (probable): Fungal infection possibility
📌 Risk level: Low
✅ What to do now:
- Keep dry, avoid scratching
🚨 Visit doctor if spreading/no improvement
⚠️ Disclaimer: Not a diagnosis tool."""

    if "vomit" in t or "loose motion" in t or "diarrhea" in t:
        return """✅ Possible condition (probable): Gastroenteritis / food poisoning possibility
📌 Risk level: Medium
✅ What to do now:
- ORS + hydration
🚨 Visit doctor if severe weakness/blood/dehydration
⚠️ Disclaimer: Not a diagnosis tool."""

    if "burning urination" in t or "burning urine" in t:
        return """✅ Possible condition (probable): UTI possibility
📌 Risk level: Medium
✅ What to do now:
- Hydration + consult doctor for testing
🚨 Urgent if fever/back pain/blood in urine
⚠️ Disclaimer: Not a diagnosis tool."""

    return """✅ Possible condition (probable): Not enough information
📌 Risk level: Unknown
✅ What to do now:
- Provide duration, severity, age group, and main symptom
🚨 Visit doctor if symptoms are severe/worsening
⚠️ Disclaimer: Not a diagnosis tool."""

if st.button("Check My Symptoms ✅"):
    if user_input.strip() == "":
        st.error("Please type your symptoms first.")
    else:
        st.success(rule_based_response(user_input))

st.caption("⚠️ This prototype is for demo purposes only. Always consult a doctor for medical diagnosis.")
