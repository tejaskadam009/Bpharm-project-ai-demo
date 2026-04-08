import streamlit as st
from PIL import Image

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Health Guidance System",
    page_icon="🩺",
    layout="centered"
)

# ---------------- SESSION STATE ----------------

if "accepted" not in st.session_state:
    st.session_state.accepted = False


# ================= ENTRY CONSENT SCREEN =================

if not st.session_state.accepted:

    st.markdown("""
    <div style="
        padding:30px;
        border-radius:16px;
        background:rgba(255,255,255,0.05);
        border:1px solid rgba(255,255,255,0.15);
        line-height:1.6;
    ">

    <h2>🩺 AI Health Guidance System</h2>

    <h4>Community Pharmacy Clinical Screening Interface</h4>

    <hr>

    <b>Purpose of this system</b>

    This application supports early symptom-based screening and referral decisions
    before physician consultation.

    <br><br>

    <b>✔ Provides</b>

    • Preliminary clinical impression  
    • Risk classification  
    • Pharmacist counselling guidance  
    • Emergency referral suggestions  

    <br>

    <b>❌ Does NOT provide</b>

    • Confirmed diagnosis  
    • Prescription decisions  
    • Lab interpretation  

    <br>

    <b>⚠ Educational B.Pharm Clinical Prototype</b>

    Always consult a healthcare professional.

    </div>
    """, unsafe_allow_html=True)

    agree = st.checkbox(
        "I understand this system provides screening support only."
    )

    if agree:
        if st.button("Enter Clinical Screening Interface"):
            st.session_state.accepted = True
            st.rerun()

    st.stop()


# ================= HEADER =================

st.title("🩺 AI Health Guidance System")

st.caption(
    "Community Pharmacy Clinical Screening Assistant | Risk Classification | Referral Guidance"
)

st.divider()


# ================= PATIENT INFO PANEL =================

st.subheader("👤 Patient Information")

col1, col2, col3 = st.columns(3)

age = col1.number_input("Age", 1, 100, 25)

gender = col2.selectbox(
    "Gender",
    ["Male", "Female", "Other"]
)

duration = col3.selectbox(
    "Symptom Duration",
    ["< 1 day", "1 – 3 days", "3 – 7 days", "> 1 week"]
)

severity = st.slider(
    "Symptom Severity Level",
    1,
    10,
    3
)

st.divider()


# ================= SYMPTOM DATABASE =================

st.subheader("📋 Symptom Selection")

symptoms_list = [

"Fever","Cough","Sneezing","Runny nose","Sore throat",
"Breathlessness","Chest pain","Wheezing",
"Headache","Dizziness","Confusion","Seizures",
"Vomiting","Loose motion","Constipation",
"Abdominal pain","Loss of appetite",
"Burning urination","Frequent urination",
"Blood in urine","Blood in stool",
"Skin rash","Itching","Ring-shaped rash",
"Swelling","Blisters",
"Acidity","Heartburn",
"Joint pain","Muscle pain","Back pain",
"Fatigue","Weakness",
"Weight loss","Night sweats",
"Blurred vision","Sensitivity to light",
"Dehydration","High thirst",
"Face swelling","Tongue swelling",
"Difficulty swallowing","Hoarseness",
"Rapid breathing","Black stool",
"Yellow eyes","Gas","Indigestion",
"Palpitations","Dry mouth","Reduced urination"
]

selected_symptoms = st.multiselect(
    "Select observed symptoms",
    symptoms_list
)

uploaded_img = st.file_uploader(
    "Upload rash / wound image (optional)",
    type=["jpg","jpeg","png"]
)

if uploaded_img:
    st.image(Image.open(uploaded_img))
    st.info("Image uploaded — dermatologist consultation recommended if worsening")

st.divider()


# ================= CLINICAL ENGINE =================

def assess(symptoms, severity, age, duration):

    s = set(symptoms)

    risk_score = severity


# ================= AGE-BASED RISK =================

    if age < 5 and "Fever" in s:
        return (
            "Pediatric Fever Risk",
            "HIGH",
            "Children under 5 with fever require urgent evaluation",
            ["Persistent fever"],
            ["Immediate pediatric consultation required"]
        )

    if age > 60:
        risk_score += 2


# ================= DURATION RISK =================

    if duration == "> 1 week":
        risk_score += 3


# ================= EMERGENCY SYMPTOMS =================

    emergency_symptoms = [

        "Chest pain",
        "Breathlessness",
        "Seizures",
        "Confusion",
        "Blood in stool",
        "Blood in urine",
        "Black stool",
        "Tongue swelling",
        "Face swelling"
    ]

    for symptom in emergency_symptoms:

        if symptom in s:

            risk_score += 6


# ================= MODERATE SYMPTOMS =================

    moderate_symptoms = [

        "Fever",
        "Vomiting",
        "Loose motion",
        "Burning urination",
        "Palpitations"
    ]

    for symptom in moderate_symptoms:

        if symptom in s:

            risk_score += 3


# ================= MILD SYMPTOMS =================

    mild_symptoms = [

        "Sneezing",
        "Runny nose",
        "Headache",
        "Acidity",
        "Gas"
    ]

    for symptom in mild_symptoms:

        if symptom in s:

            risk_score += 1


# ================= HIGH RISK =================

    if risk_score >= 12:

        return (

            "Possible Medical Emergency",
            "HIGH",

            "Critical symptom cluster detected requiring urgent evaluation",

            emergency_symptoms,

            ["Immediate hospital referral required"]

        )


# ================= RESPIRATORY =================

    if "Sneezing" in s and "Runny nose" in s:

        return (

            "Common Cold / Allergic Rhinitis",
            "LOW",

            "Typical upper respiratory irritation pattern",

            ["Symptoms worsening > 5 days"],

            ["Steam inhalation", "Hydration", "Rest"]

        )


    if "Fever" in s and "Cough" in s:

        return (

            "Upper Respiratory Infection",

            "MEDIUM",

            "Suggestive respiratory infection",

            ["Persistent fever > 3 days"],

            ["Paracetamol", "Steam inhalation", "Consult pharmacist"]

        )


# ================= GI =================

    if "Loose motion" in s and "Vomiting" in s:

        return (

            "Acute Gastroenteritis",

            "MEDIUM",

            "GI infection pattern detected",

            ["Severe dehydration"],

            ["ORS therapy", "Hydration", "Medical consultation if persistent"]

        )


# ================= UTI =================

    if "Burning urination" in s and "Frequent urination" in s:

        return (

            "Urinary Tract Infection",

            "MEDIUM",

            "Typical urinary infection symptoms",

            ["Back pain with fever"],

            ["Increase fluids", "Consult physician"]

        )


# ================= SKIN =================

    if "Ring-shaped rash" in s:

        return (

            "Fungal Skin Infection",

            "LOW",

            "Dermatophyte infection suspected",

            ["Spreading rash"],

            ["Topical antifungal cream advised"]

        )


# ================= MULTI SYMPTOM =================

    if len(s) >= 5:

        return (

            "Multiple Symptom Cluster Detected",

            "MEDIUM",

            "Multiple symptoms detected requiring consultation",

            ["Persistent symptoms"],

            ["Consult physician"]

        )


# ================= DEFAULT =================

    return (

        "Non-specific Mild Symptom Pattern",

        "LOW",

        "Symptoms suggest mild condition",

        ["Symptoms worsening"],

        ["Monitor symptoms"]

    )


# ================= SCREENING BUTTON =================

if st.button("Run Clinical Screening"):

    if not selected_symptoms:

        st.warning("Please select symptoms")

    else:

        condition, risk, explanation, redflags, guidance = assess(
            selected_symptoms,
            severity,
            age,
            duration
        )

        st.subheader("🧠 Clinical Impression")
        st.success(condition)


        st.subheader("⚠ Risk Level")

        if risk == "HIGH":

            st.error("HIGH RISK – Immediate evaluation required")

        elif risk == "MEDIUM":

            st.warning("MODERATE RISK – Consultation advised")

        else:

            st.success("LOW RISK – Routine monitoring recommended")


        st.subheader("📖 Clinical Explanation")
        st.write(explanation)


        st.subheader("🚨 Red Flag Indicators")

        for r in redflags:
            st.write("•", r)


        st.subheader("💊 Pharmacist Guidance")

        for g in guidance:
            st.write("•", g)


# ================= EMERGENCY BUTTONS =================

        if risk == "HIGH":

            st.error("Emergency referral recommended")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(
                    '<a href="tel:108"><button style="width:100%;padding:12px;background:red;color:white;border:none;border-radius:8px;">🚑 Ambulance</button></a>',
                    unsafe_allow_html=True
                )

            with c2:
                st.markdown(
                    '<a href="tel:112"><button style="width:100%;padding:12px;background:orange;color:white;border:none;border-radius:8px;">☎ Emergency</button></a>',
                    unsafe_allow_html=True
                )

            with c3:
                st.markdown(
                    '<a href="tel:+919999999999"><button style="width:100%;padding:12px;background:green;color:white;border:none;border-radius:8px;">👨‍⚕️ Call Doctor</button></a>',
                    unsafe_allow_html=True
                )


st.divider()

st.caption(
    "AI Health Guidance System | Clinical Decision Support Prototype | B.Pharm Final Year Project"
)
