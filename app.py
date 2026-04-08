import streamlit as st
from PIL import Image

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Health Guidance System",
    page_icon="🩺",
    layout="centered"
)

# ---------------- APPEARANCE TOGGLE ----------------
if "mode" not in st.session_state:
    st.session_state.mode = "dark"

col1, col2 = st.columns([6,1])

with col2:
    if st.button("🌓"):
        if st.session_state.mode == "dark":
            st.session_state.mode = "light"
        else:
            st.session_state.mode = "dark"
        st.rerun()

# ---------------- STYLE SETTINGS ----------------
if st.session_state.mode == "light":

    CARD_STYLE = """
    background:#f8fafc;
    color:black;
    border:1px solid #e2e8f0;
    padding:18px;
    border-radius:12px;
    """

else:

    CARD_STYLE = """
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.15);
    padding:18px;
    border-radius:12px;
    """

# ---------------- DISCLAIMER SCREEN ----------------
if "accepted" not in st.session_state:
    st.session_state.accepted = False


if not st.session_state.accepted:

    st.markdown(
        f"""
        <div style="{CARD_STYLE}">

        <h2>🩺 AI Health Guidance System</h2>

        <b>Clinical Decision Support Prototype</b>

        <hr>

        This system performs symptom-based screening using rule-based clinical logic
        to assist early health risk identification.

        <br><br>

        <b>This application provides:</b>

        <ul>
        <li>Preliminary clinical impression</li>
        <li>Risk classification (Low / Moderate / High)</li>
        <li>Pharmacist counselling guidance</li>
        <li>Emergency referral recommendations</li>
        </ul>

        <b>This application does NOT provide:</b>

        <ul>
        <li>Confirmed diagnosis</li>
        <li>Prescription decisions</li>
        <li>Emergency treatment replacement</li>
        </ul>

        This system is intended strictly for educational screening support purposes.

        </div>
        """,
        unsafe_allow_html=True
    )

    agree = st.checkbox(
        "I understand this system is for educational screening support only"
    )

    if agree:
        if st.button("Launch Clinical Screening Interface"):
            st.session_state.accepted = True
            st.rerun()

    st.stop()


# ---------------- HEADER ----------------
st.title("🩺 AI Health Guidance System")

st.caption(
    "Symptom Screening • Risk Classification • Pharmacist Counselling Support"
)

st.info(
    "Step 1: Select symptoms → Step 2: Run screening → Step 3: Review risk classification"
)

st.divider()

# ---------------- SYMPTOMS ----------------
st.subheader("Patient Symptom Intake")

symptoms_list = [

"Fever","Cough","Sore throat","Runny nose","Sneezing",
"Breathlessness","Chest pain","Wheezing",
"Headache","Dizziness","Confusion","Seizures",
"Vomiting","Loose motion","Constipation",
"Abdominal pain","Loss of appetite",
"Burning urination","Frequent urination",
"Blood in urine","Blood in stool",
"Skin rash","Itching","Swelling",
"Acidity","Heartburn",
"Joint pain","Muscle pain",
"Fatigue","Weakness",
"Weight loss","Night sweats",
"Blurred vision","Back pain",
"Neck stiffness","Sensitivity to light",
"Dehydration","High thirst",
"Face swelling","Tongue swelling",
"Difficulty swallowing","Hoarseness",
"Rapid breathing","Black stool",
"Yellow eyes","Gas","Indigestion",
"Skin infection","Ring-shaped rash"
]

selected_symptoms = st.multiselect(
    "Select symptoms observed",
    symptoms_list
)

st.divider()

# ---------------- IMAGE INPUT ----------------
uploaded_img = st.file_uploader(
    "Upload clinical image (optional)",
    type=["jpg","jpeg","png"]
)

if uploaded_img:
    st.image(Image.open(uploaded_img), use_container_width=True)

st.divider()

# ---------------- CLINICAL ENGINE ----------------
def assess(symptoms):

    s = set(symptoms)

    if "Chest pain" in s or "Breathlessness" in s:
        return "Possible Cardiac or Respiratory Emergency", "HIGH"

    if "Seizures" in s or "Confusion" in s:
        return "Possible Neurological Emergency", "HIGH"

    if "Fever" in s and "Cough" in s:
        return "Upper Respiratory Infection / Viral Fever", "MEDIUM"

    if "Burning urination" in s:
        return "Urinary Tract Infection", "MEDIUM"

    if "Skin rash" in s or "Itching" in s:
        return "Skin Allergy / Fungal Infection", "LOW"

    if "Acidity" in s:
        return "Acidity / Gastritis", "LOW"

    return "Insufficient Clinical Information", "UNKNOWN"


# ---------------- ANALYSIS BUTTON ----------------
if st.button("Run Clinical Screening"):

    if not selected_symptoms:

        st.warning("Please select at least one symptom")

    else:

        condition, risk = assess(selected_symptoms)

        st.divider()

        st.subheader("Preliminary Clinical Impression")
        st.success(condition)

        st.subheader("Risk Classification")

        if risk == "HIGH":
            st.error("🔴 HIGH RISK – Immediate medical evaluation recommended")

        elif risk == "MEDIUM":
            st.warning("🟠 MODERATE RISK – Clinical consultation advised")

        elif risk == "LOW":
            st.success("🟢 LOW RISK – Routine monitoring recommended")

        else:
            st.info("Insufficient data for classification")

st.divider()

st.caption(
    "AI Health Guidance System | Clinical Decision Support Prototype | Developed for B.Pharm Final Year Project"
)
