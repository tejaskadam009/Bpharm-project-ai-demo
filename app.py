import streamlit as st
from PIL import Image

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Health Guidance System",
    page_icon="🩺",
    layout="centered"
)

# ---------------- APPEARANCE MODE SWITCHER ----------------
if "appearance" not in st.session_state:
    st.session_state.appearance = "Dark"

st.sidebar.markdown("## ⚙️ Appearance Settings")

mode = st.sidebar.radio(
    "Select Interface Mode",
    ["Dark Mode", "Light Mode"]
)

if mode == "Light Mode":
    st.session_state.appearance = "Light"
else:
    st.session_state.appearance = "Dark"


# ---------------- CUSTOM UI STYLE ----------------
if st.session_state.appearance == "Light":

    CARD_STYLE = """
    background-color:#f8fafc;
    border:1px solid #e2e8f0;
    color:black;
    """

else:

    CARD_STYLE = """
    background-color: rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.15);
    """


# ---------------- DISCLAIMER SCREEN ----------------
if "accepted" not in st.session_state:
    st.session_state.accepted = False


if not st.session_state.accepted:

    st.markdown(f"""
    <div style="{CARD_STYLE}
    padding:18px;
    border-radius:12px;">

    <h2>🩺 AI Health Guidance System</h2>

    <b>Clinical Decision Support Prototype</b>

    <hr>

    This system performs symptom-based screening using rule-based clinical logic
    to assist early health risk identification.

    <br><br>

    <b>This application provides:</b>

    • Preliminary clinical impression  
    • Risk classification (Low / Moderate / High)  
    • Pharmacist counselling guidance  
    • Emergency referral recommendations  

    <br>

    <b>This application does NOT provide:</b>

    • Confirmed diagnosis  
    • Prescription decisions  
    • Emergency treatment replacement  

    <br>

    This system is intended strictly for educational screening support purposes.

    </div>
    """, unsafe_allow_html=True)

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


# ---------------- SYMPTOM INTAKE ----------------
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
        return (
            "Possible Cardiac or Respiratory Emergency",
            "HIGH",
            ["Chest pain with breathlessness may indicate serious cardiac or pulmonary condition"],
            ["Pain radiating to arm or jaw", "Severe breathing difficulty"],
            ["Immediate hospital evaluation required"]
        )

    if "Seizures" in s or "Confusion" in s:
        return (
            "Possible Neurological Emergency",
            "HIGH",
            ["Neurological symptoms detected requiring urgent evaluation"],
            ["Repeated seizures", "Loss of consciousness"],
            ["Immediate neurological consultation recommended"]
        )

    if "Fever" in s and "Cough" in s:
        return (
            "Upper Respiratory Infection / Viral Fever",
            "MEDIUM",
            ["Symptoms suggest respiratory infection"],
            ["Fever lasting more than 3 days", "Breathing difficulty"],
            ["Paracetamol may help reduce fever", "Steam inhalation recommended"]
        )

    return (
        "Insufficient Clinical Information",
        "UNKNOWN",
        ["More symptom data required"],
        ["Persistent symptoms"],
        ["Consult healthcare professional"]
    )


# ---------------- ANALYSIS BUTTON ----------------
if st.button("Run Clinical Screening"):

    if not selected_symptoms:

        st.warning("Please select at least one symptom")

    else:

        condition, risk, explanation, redflags, otc = assess(selected_symptoms)

        st.divider()

        st.subheader("Preliminary Clinical Impression")
        st.success(condition)

        st.subheader("Risk Classification")

        if risk == "HIGH":
            st.error("🔴 HIGH RISK – Immediate medical evaluation recommended")

        elif risk == "MEDIUM":
            st.warning("🟠 MODERATE RISK – Clinical consultation advised")

        else:
            st.info("Insufficient data for classification")


st.divider()

st.caption(
"AI Health Guidance System | Clinical Decision Support Prototype | Developed for B.Pharm Final Year Project"
)
