import streamlit as st
from PIL import Image

# ------------------- PAGE CONFIG -------------------
st.set_page_config(
    page_title="AI Health Guidance System",
    page_icon="🩺",
    layout="centered"
)

# ------------------- STYLING -------------------
st.markdown("""
<style>
.big-title {
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 0px;
}
.sub-title {
    font-size: 16px;
    opacity: 0.85;
    margin-top: 4px;
    margin-bottom: 18px;
}
.card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    padding: 16px;
    border-radius: 14px;
    margin-top: 10px;
}
.result-box {
    background: rgba(0, 255, 120, 0.08);
    border: 1px solid rgba(0, 255, 120, 0.25);
    padding: 16px;
    border-radius: 14px;
}
.warn-box {
    background: rgba(255, 165, 0, 0.08);
    border: 1px solid rgba(255, 165, 0, 0.30);
    padding: 14px;
    border-radius: 14px;
}
.danger-box {
    background: rgba(255, 0, 0, 0.08);
    border: 1px solid rgba(255, 0, 0, 0.25);
    padding: 14px;
    border-radius: 14px;
}
.small-note {
    opacity: 0.75;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ------------------- DISCLAIMER POPUP -------------------
if "accepted_disclaimer" not in st.session_state:
    st.session_state.accepted_disclaimer = False

@st.dialog("⚠️ Important Notice")
def disclaimer_modal():
    st.markdown("""
### 🩺 AI Health Guidance System

This tool is created for **educational and awareness purposes**.

✅ It provides:
- Possible condition (probable)
- Risk level estimate (Low/Medium/High)
- Basic guidance + referral suggestion

❌ It does NOT provide:
- Confirmed diagnosis
- Emergency treatment
- Prescription or medical replacement

🚨 **If symptoms are severe/worsening, consult a doctor immediately.**
""")
    agree = st.checkbox("I understand and I want to continue.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Continue ✅", use_container_width=True, disabled=not agree):
            st.session_state.accepted_disclaimer = True
            st.rerun()
    with col2:
        if st.button("Exit ❌", use_container_width=True):
            st.stop()

if not st.session_state.accepted_disclaimer:
    disclaimer_modal()
    st.stop()

# ------------------- HEADER -------------------
st.markdown('<div class="big-title">🩺 AI Health Guidance System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Symptom Screening • Risk Assessment • Referral Guidance</div>', unsafe_allow_html=True)

# ------------------- 50 SYMPTOMS LIST -------------------
symptoms_list = [
    # Fever / Infection
    "Fever", "Chills", "Body ache", "Weakness/Fatigue", "Night sweats",

    # Respiratory
    "Cough", "Dry cough", "Sore throat", "Runny nose", "Nasal congestion",
    "Sneezing", "Breathlessness", "Wheezing", "Chest tightness", "Chest pain",

    # Gastrointestinal
    "Nausea", "Vomiting", "Loose motion/Diarrhea", "Constipation",
    "Stomach pain/Abdominal pain", "Bloating", "Acidity/Heartburn",
    "Loss of appetite", "Blood in stool", "Dehydration",

    # Head/Neuro
    "Headache", "Dizziness", "Fainting", "Blurred vision",
    "Confusion", "Seizures", "Neck stiffness",

    # Skin
    "Itching", "Rash", "Redness", "Swelling", "Pus/wound discharge",
    "Burning sensation on skin", "Dry/flaky skin", "Hives (allergy bumps)",

    # Urinary
    "Burning urination", "Frequent urination", "Lower abdominal pain (urine)",
    "Blood in urine", "Back pain (kidney area)",

    # Allergy/General
    "Watery eyes", "Face swelling", "Difficulty swallowing",
    "Severe allergy reaction",

    # Others
    "Joint pain", "Muscle cramps", "Weight loss", "High thirst"
]

# ------------------- RULE BASED ENGINE -------------------
def assess(symptoms_selected, custom_text):
    s = set(symptoms_selected)
    t = (custom_text or "").lower()

    # --- Emergency Flags ---
    emergency_reasons = []

    if "Chest pain" in s or "Breathlessness" in s:
        emergency_reasons.append("Chest pain or breathlessness can be serious.")

    if "Seizures" in s or "Confusion" in s or "Fainting" in s:
        emergency_reasons.append("Neurological danger signs (seizures/confusion/fainting).")

    if "Blood in stool" in s or "Blood in urine" in s:
        emergency_reasons.append("Blood present in stool/urine needs urgent evaluation.")

    if "Neck stiffness" in s and "Fever" in s:
        emergency_reasons.append("Fever + neck stiffness can indicate serious infection.")

    if "Severe allergy reaction" in s or "Face swelling" in s or "Difficulty swallowing" in s:
        emergency_reasons.append("Possible severe allergic reaction.")

    # Also check custom text for emergency phrases
    if "chest pain" in t or "can't breathe" in t or "cannot breathe" in t:
        emergency_reasons.append("Emergency symptoms mentioned in text.")

    if len(emergency_reasons) > 0:
        return {
            "condition": "⚠️ Medical emergency possible",
            "risk": "HIGH",
            "advice": [
                "Seek emergency medical care immediately.",
                "Do not delay if symptoms are severe or worsening.",
                "If available, call local emergency services / go to hospital."
            ],
            "redflags": emergency_reasons
        }

    # --- Condition Patterns (Simple & Safe) ---
    # Viral cold/flu
    if ("Fever" in s or "Chills" in s) and ("Cough" in s or "Sore throat" in s or "Runny nose" in s):
        return {
            "condition": "Viral fever / Cold-Flu like illness (probable)",
            "risk": "MEDIUM",
            "advice": [
                "Rest and drink plenty of fluids.",
                "Warm gargles + steam inhalation can help.",
                "Monitor temperature and symptoms daily.",
                "Avoid cold drinks and smoke exposure."
            ],
            "redflags": [
                "High fever for more than 3 days",
                "Breathing difficulty",
                "Severe weakness or dehydration"
            ]
        }

    # Gastroenteritis
    if ("Vomiting" in s or "Loose motion/Diarrhea" in s or "Nausea" in s):
        return {
            "condition": "Acute gastroenteritis / Food-related infection (probable)",
            "risk": "MEDIUM",
            "advice": [
                "Use ORS frequently in small sips.",
                "Eat light foods (banana, toast, khichdi).",
                "Avoid oily/spicy foods and dairy for 24 hours.",
                "Maintain hygiene and rest."
            ],
            "redflags": [
                "Blood in stool",
                "Severe abdominal pain",
                "Signs of dehydration (dizziness, dry mouth, low urine)"
            ]
        }

    # Fungal skin infection
    if ("Itching" in s and "Rash" in s) or ("Dry/flaky skin" in s and "Itching" in s):
        return {
            "condition": "Skin allergy / Fungal infection possibility",
            "risk": "LOW",
            "advice": [
                "Keep the affected area clean and dry.",
                "Avoid scratching and avoid sharing towels/clothes.",
                "Wear loose cotton clothing.",
                "If spreading, consult a doctor/dermatologist."
            ],
            "redflags": [
                "Rash spreading quickly",
                "Pus/wound discharge",
                "Fever with rash"
            ]
        }

    # UTI
    if ("Burning urination" in s or "Frequent urination" in s):
        return {
            "condition": "Urinary tract infection (UTI) possibility",
            "risk": "MEDIUM",
            "advice": [
                "Drink more water.",
                "Maintain hygiene.",
                "Consult doctor for urine test if symptoms persist.",
                "Avoid holding urine for long time."
            ],
            "redflags": [
                "Fever with back pain",
                "Blood in urine",
                "Severe lower abdominal pain"
            ]
        }

    # Allergy
    if ("Sneezing" in s and "Watery eyes" in s) or ("Hives (allergy bumps)" in s):
        return {
            "condition": "Allergic rhinitis / Allergy possibility",
            "risk": "LOW",
            "advice": [
                "Avoid triggers (dust, pollen, smoke).",
                "Keep room clean and ventilated.",
                "Monitor for breathing difficulty.",
                "Consult doctor if symptoms are frequent."
            ],
            "redflags": [
                "Face swelling",
                "Difficulty swallowing",
                "Breathlessness"
            ]
        }

    # Acidity / GERD
    if "Acidity/Heartburn" in s or "Bloating" in s:
        return {
            "condition": "Acidity / Indigestion (probable)",
            "risk": "LOW",
            "advice": [
                "Avoid spicy, oily and very late meals.",
                "Eat small frequent meals.",
                "Do not lie down immediately after eating.",
                "Stay hydrated."
            ],
            "redflags": [
                "Severe abdominal pain",
                "Vomiting blood",
                "Unexplained weight loss"
            ]
        }

    # Migraine-like
    if "Headache" in s and ("Nausea" in s or "Blurred vision" in s):
        return {
            "condition": "Migraine / Headache disorder possibility",
            "risk": "MEDIUM",
            "advice": [
                "Rest in a quiet, dark room.",
                "Hydrate well and avoid screen strain.",
                "Track triggers (stress, sleep, food).",
                "Consult doctor if frequent or severe."
            ],
            "redflags": [
                "Worst headache of life",
                "Fainting or confusion",
                "Neck stiffness with fever"
            ]
        }

    # Default unknown
    return {
        "condition": "Not enough information (needs more details)",
        "risk": "UNKNOWN",
        "advice": [
            "Add more symptoms, duration and severity.",
            "If symptoms are worsening, consult a doctor.",
            "Do not self-medicate for serious symptoms."
        ],
        "redflags": [
            "Severe or worsening symptoms",
            "Breathing difficulty or chest pain",
            "Persistent high fever"
        ]
    }

# ------------------- UI LAYOUT -------------------
tab1, tab2 = st.tabs(["✅ Symptom Checker", "📚 Clinical Scenarios"])

# ------------------- TAB 1: Symptom Checker -------------------
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧾 Select Symptoms (Choose multiple)")
    selected_symptoms = st.multiselect("Symptoms", symptoms_list)

    st.subheader("✍️ Additional Description (Optional)")
    custom_text = st.text_area(
        "Write any extra details (duration, severity, etc.)",
        placeholder="Example: fever since 2 days, cough is dry, feeling weak..."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📷 Upload Image (Optional)")
    uploaded_img = st.file_uploader("Upload rash / wound / skin photo", type=["jpg", "jpeg", "png"])

    if uploaded_img:
        img = Image.open(uploaded_img)
        st.image(img, caption="Uploaded Image", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Analyze Symptoms ✅", use_container_width=True):
        if len(selected_symptoms) == 0 and custom_text.strip() == "":
            st.markdown('<div class="warn-box">', unsafe_allow_html=True)
            st.error("Please select symptoms or write your condition.")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            result = assess(selected_symptoms, custom_text)

            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(f"### ✅ Possible condition (probable)\n**{result['condition']}**")
            st.markdown(f"### 📌 Risk Level\n**{result['risk']}**")

            st.markdown("### ✅ What to do now")
            for a in result["advice"]:
                st.write("•", a)

            st.markdown("### 🚨 Red flags (consult doctor urgently if)")
            for r in result["redflags"]:
                st.write("•", r)

            st.markdown('</div>', unsafe_allow_html=True)

# ------------------- TAB 2: Clinical Cases -------------------
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📚 Clinical Scenarios (For Project Presentation)")

    cases = {
        "Fever + Body pain": "Fever, body pain, weakness since 2 days.",
        "Cough + Sore throat": "Cough, sore throat, mild fever since 3 days.",
        "Itching + Circular rash": "Itching and circular red rash since 1 week.",
        "Vomiting + Loose motions": "Vomiting and loose motions since 1 day.",
        "Chest pain + Breathlessness": "Sudden chest pain and breathlessness.",
        "Burning urination": "Burning urination and frequent urge.",
        "Acidity after meals": "Burning in stomach after meals.",
        "Headache + Nausea": "Headache with nausea and light sensitivity.",
        "Sneezing + watery eyes": "Sneezing and watery/itchy eyes.",
        "Fever + rash + joint pain": "Fever with rash and joint pain."
    }

    selected_case = st.selectbox("Choose scenario", list(cases.keys()))
    st.info(cases[selected_case])

    if st.button("Generate Guidance ✅", use_container_width=True):
        result = assess([], cases[selected_case])

        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown(f"### ✅ Possible condition (probable)\n**{result['condition']}**")
        st.markdown(f"### 📌 Risk Level\n**{result['risk']}**")

        st.markdown("### ✅ What to do now")
        for a in result["advice"]:
            st.write("•", a)

        st.markdown("### 🚨 Red flags (consult doctor urgently if)")
        for r in result["redflags"]:
            st.write("•", r)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.write("")
st.markdown('<div class="small-note">Made for B.Pharm Final Year Project • Symptom Guidance + Risk Assessment</div>', unsafe_allow_html=True)
