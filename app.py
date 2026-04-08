import streamlit as st
from PIL import Image

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Health Guidance System",
    page_icon="🩺",
    layout="centered"
)

# ---------------- DARK/LIGHT MODE TOGGLE ----------------
if "mode" not in st.session_state:
    st.session_state.mode = "dark"

col_left, col_toggle = st.columns([6,1])

with col_toggle:
    if st.button("🌓"):
        if st.session_state.mode == "dark":
            st.session_state.mode = "light"
        else:
            st.session_state.mode = "dark"
        st.rerun()


# ---------------- STYLE ENGINE ----------------
if st.session_state.mode == "light":

    CARD_STYLE = """
    background:#f8fafc;
    border:1px solid #e2e8f0;
    padding:18px;
    border-radius:12px;
    color:black;
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

        <br>

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


# ---------------- SYMPTOM INPUT ----------------
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
            ["Chest pain with breathlessness may indicate heart attack or lung emergency"],
            ["Pain spreading to arm or jaw", "Severe breathing difficulty"],
            ["Immediate hospital evaluation required"]
        )

    if "Seizures" in s or "Confusion" in s:
        return (
            "Possible Neurological Emergency",
            "HIGH",
            ["Seizures may indicate brain-related emergency"],
            ["Loss of consciousness", "Repeated seizures"],
            ["Emergency neurological consultation required"]
        )

    if "Fever" in s and "Cough" in s:
        return (
            "Upper Respiratory Infection",
            "MEDIUM",
            ["Symptoms indicate viral respiratory infection"],
            ["Fever lasting >3 days", "Breathing difficulty"],
            ["Paracetamol may help", "Steam inhalation recommended"]
        )

    if "Vomiting" in s or "Loose motion" in s:
        return (
            "Acute Gastroenteritis",
            "MEDIUM",
            ["Vomiting or diarrhea indicates GI infection"],
            ["Severe dehydration"],
            ["ORS recommended"]
        )

    if "Skin rash" in s or "Itching" in s:
        return (
            "Skin Allergy or Fungal Infection",
            "LOW",
            ["Dermatological irritation suspected"],
            ["Spreading rash"],
            ["Topical antifungal recommended"]
        )

    return (
        "Insufficient Clinical Information",
        "UNKNOWN",
        ["More symptoms required"],
        ["Persistent symptoms"],
        ["Consult healthcare professional"]
    )


# ---------------- ANALYSIS BUTTON ----------------
if st.button("Run Clinical Screening"):

    if not selected_symptoms:

        st.warning("Please select at least one symptom")

    else:

        condition, risk, explanation, redflags, guidance = assess(selected_symptoms)

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


        st.subheader("Clinical Interpretation")
        for e in explanation:
            st.write("•", e)

        st.subheader("Urgent Warning Indicators")
        for r in redflags:
            st.write("•", r)

        st.subheader("Pharmacist Counselling Guidance")
        for g in guidance:
            st.write("•", g)


        if risk == "HIGH":

            st.error("Emergency referral recommended")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(
                    '<a href="tel:108"><button style="width:100%;padding:14px;background:red;color:white;border:none;border-radius:10px;">🚑 Ambulance</button></a>',
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    '<a href="tel:112"><button style="width:100%;padding:14px;background:orange;color:white;border:none;border-radius:10px;">☎ Emergency</button></a>',
                    unsafe_allow_html=True
                )

            with col3:
                st.markdown(
                    '<a href="tel:+919999999999"><button style="width:100%;padding:14px;background:green;color:white;border:none;border-radius:10px;">👨‍⚕️ Doctor</button></a>',
                    unsafe_allow_html=True
                )


st.divider()

st.caption(
    "AI Health Guidance System | Clinical Decision Support Prototype | Developed for B.Pharm Final Year Project"
)
