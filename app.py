import streamlit as st
from PIL import Image

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Health Guidance System",
    page_icon="🩺",
    layout="centered"
)

# ---------------- GLOBAL STYLING ----------------
st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
}

.big-title {
    font-size:32px;
    font-weight:700;
}

.subtitle {
    font-size:17px;
    opacity:0.85;
}

.card {
    background-color: rgba(255,255,255,0.05);
    padding:18px;
    border-radius:12px;
    border:1px solid rgba(255,255,255,0.15);
}

</style>
""", unsafe_allow_html=True)


# ---------------- PROFESSIONAL WELCOME SCREEN ----------------
if "accepted" not in st.session_state:
    st.session_state.accepted = False


if not st.session_state.accepted:

    st.markdown('<div class="big-title">🩺 AI Health Guidance System</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="subtitle">Clinical Decision Support Prototype for Symptom-Based Risk Assessment</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown("""
<div class="card">

This clinical screening system assists users in identifying possible health conditions based on symptom input.

The system provides:

• preliminary clinical impression  
• risk classification  
• pharmacist counselling guidance  
• referral recommendation support  

This system is intended for early screening assistance only and does not replace professional medical diagnosis.

</div>
""", unsafe_allow_html=True)

    st.write("")

    if st.checkbox("I understand this system provides guidance only and I wish to continue"):

        if st.button("Launch Clinical Screening Interface"):
            st.session_state.accepted = True
            st.rerun()

    st.stop()


# ---------------- HEADER ----------------
st.markdown('<div class="big-title">🩺 AI Health Guidance System</div>', unsafe_allow_html=True)

st.markdown(
'<div class="subtitle">Symptom Screening • Risk Classification • Pharmacist Counselling Support</div>',
unsafe_allow_html=True
)

st.caption("Step 1: Select symptoms  →  Step 2: Run screening  →  Step 3: Review risk classification")

st.info("This system performs symptom-based screening using rule-based clinical decision support logic.")

st.divider()


# ---------------- SYMPTOMS DATABASE ----------------
st.markdown("## Patient Symptom Intake")

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


# ---------------- OPTIONAL IMAGE INPUT ----------------
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

    # HIGH RISK CONDITIONS
    if "Chest pain" in s or "Breathlessness" in s:
        return (
            "Possible Cardiac or Respiratory Emergency",
            "HIGH",
            ["Chest pain with breathlessness may indicate serious cardiac or pulmonary condition."],
            ["Pain radiating to arm or jaw", "Severe breathing difficulty"],
            ["Immediate hospital evaluation required"]
        )

    if "Seizures" in s or "Confusion" in s:
        return (
            "Possible Neurological Emergency",
            "HIGH",
            ["Neurological symptoms detected requiring urgent evaluation."],
            ["Repeated seizures", "Loss of consciousness"],
            ["Immediate neurological consultation recommended"]
        )

    if "Blood in stool" in s or "Black stool" in s:
        return (
            "Possible Gastrointestinal Bleeding",
            "HIGH",
            ["Blood in stool suggests internal bleeding risk."],
            ["Persistent weakness", "Ongoing bleeding"],
            ["Urgent medical consultation required"]
        )

    # MEDIUM RISK CONDITIONS
    if "Fever" in s and "Cough" in s:
        return (
            "Upper Respiratory Infection / Viral Fever",
            "MEDIUM",
            ["Symptoms suggest respiratory infection."],
            ["Fever lasting more than 3 days", "Breathing difficulty"],
            ["Paracetamol may help reduce fever", "Steam inhalation recommended"]
        )

    if "Vomiting" in s or "Loose motion" in s:
        return (
            "Acute Gastroenteritis",
            "MEDIUM",
            ["Vomiting or diarrhea indicates gastrointestinal infection."],
            ["Severe dehydration", "Blood in stool"],
            ["ORS recommended", "Avoid oily foods"]
        )

    if "Burning urination" in s:
        return (
            "Urinary Tract Infection",
            "MEDIUM",
            ["Burning urination indicates urinary infection."],
            ["Back pain with fever"],
            ["Increase water intake", "Urine test recommended"]
        )

    # LOW RISK CONDITIONS
    if "Skin rash" in s or "Itching" in s:
        return (
            "Skin Allergy / Fungal Infection",
            "LOW",
            ["Dermatological irritation likely."],
            ["Spreading rash", "Pus formation"],
            ["Topical antifungal may help"]
        )

    if "Acidity" in s or "Heartburn" in s:
        return (
            "Acidity / Gastritis",
            "LOW",
            ["Likely related to dietary factors."],
            ["Vomiting blood"],
            ["Antacid therapy may help"]
        )

    return (
        "Insufficient Clinical Information",
        "UNKNOWN",
        ["More symptom data required."],
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

        for o in otc:
            st.write("•", o)

        if risk == "HIGH":

            st.error("Emergency referral recommended")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(
                    '<a href="tel:108"><button style="width:100%;padding:14px;background:#dc2626;color:white;border:none;border-radius:10px;">🚑 Ambulance</button></a>',
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    '<a href="tel:112"><button style="width:100%;padding:14px;background:#f97316;color:white;border:none;border-radius:10px;">☎ Emergency</button></a>',
                    unsafe_allow_html=True
                )

            with col3:
                st.markdown(
                    '<a href="tel:+919999999999"><button style="width:100%;padding:14px;background:#16a34a;color:white;border:none;border-radius:10px;">👨‍⚕️ Doctor</button></a>',
                    unsafe_allow_html=True
                )


st.divider()

st.caption(
"AI Health Guidance System | Clinical Decision Support Prototype | Developed for B.Pharm Final Year Project"
)
