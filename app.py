import streamlit as st
from PIL import Image

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Health Guidance System",
    page_icon="🩺",
    layout="centered"
)


# ---------------- DISCLAIMER SCREEN ----------------

if "accepted" not in st.session_state:
    st.session_state.accepted = False


if not st.session_state.accepted:

    st.markdown("""
    ### 🩺 AI Health Guidance System

    #### Clinical Decision Support Prototype

    This application performs **symptom-based screening using rule-based clinical logic**
    to assist early health risk identification.

    ---
    **Provides:**

    • Preliminary clinical impression  
    • Risk classification  
    • Pharmacist counselling guidance  
    • Emergency referral suggestions  

    ---
    **Does NOT provide:**

    • Confirmed diagnosis  
    • Prescription decisions  
    • Emergency treatment replacement  

    ---
    Intended strictly for **educational screening support purposes**
    """)

    agree = st.checkbox(
        "I understand this system is for educational screening support only"
    )

    if agree:
        if st.button("Launch Screening Interface"):
            st.session_state.accepted = True
            st.rerun()

    st.stop()


# ---------------- HEADER ----------------

st.title("🩺 AI Health Guidance System")

st.caption(
    "Community Pharmacy Clinical Screening Assistant"
)

st.info(
    "Select symptoms → Run screening → Review guidance"
)

st.divider()


# ---------------- DEMOGRAPHIC PANEL ----------------

st.subheader("👤 Patient Information")

col1, col2, col3 = st.columns(3)

age = col1.number_input("Age", 1, 100, 25)
gender = col2.selectbox("Gender", ["Male", "Female", "Other"])
duration = col3.selectbox(
    "Symptom Duration",
    ["<1 day", "1-3 days", "3-7 days", ">1 week"]
)

st.divider()


# ---------------- LARGE SYMPTOM DATABASE ----------------

st.subheader("📋 Symptom Selection")

symptoms_list = [

# GENERAL
"Fever","Weakness","Fatigue","Weight loss","Night sweats",

# RESPIRATORY
"Cough","Sneezing","Runny nose","Breathlessness",
"Wheezing","Sore throat","Chest tightness",

# GI
"Vomiting","Loose motion","Constipation",
"Abdominal pain","Heartburn","Acidity",
"Loss of appetite","Black stool","Blood in stool",

# URINARY
"Burning urination","Frequent urination","Blood in urine",

# NEURO
"Headache","Dizziness","Confusion",
"Seizures","Sensitivity to light","Blurred vision",

# MSK
"Joint pain","Muscle pain","Back pain",

# SKIN
"Skin rash","Itching","Ring-shaped rash",
"Swelling","Skin redness","Blisters",

# CARDIAC
"Chest pain","Palpitations",

# ALLERGY
"Face swelling","Tongue swelling",

# ENDOCRINE
"High thirst","Frequent urination diabetes",

# ENT
"Hoarseness","Difficulty swallowing",

# DEHYDRATION
"Dry mouth","Reduced urination"
]

selected_symptoms = st.multiselect(
    "Select observed symptoms",
    symptoms_list
)

uploaded_img = st.file_uploader(
    "Upload clinical image (optional)",
    type=["jpg","jpeg","png"]
)

if uploaded_img:
    st.image(Image.open(uploaded_img))


st.divider()


# ---------------- CLINICAL ENGINE ----------------

def assess(symptoms):

    s = set(symptoms)


# HIGH RISK CONDITIONS

    if "Chest pain" in s and "Breathlessness" in s:
        return(
            "Possible Cardiac Emergency",
            "HIGH",
            "Possible myocardial infarction pattern detected"
        )


    if "Seizures" in s:
        return(
            "Possible Neurological Emergency",
            "HIGH",
            "Seizure activity requires urgent evaluation"
        )


# RESPIRATORY CONDITIONS

    if "Sneezing" in s and "Runny nose" in s:
        return(
            "Allergic Rhinitis",
            "LOW",
            "Likely allergy-related nasal irritation"
        )


    if "Fever" in s and "Cough" in s:
        return(
            "Upper Respiratory Infection",
            "MEDIUM",
            "Likely viral respiratory infection"
        )


# GI CONDITIONS

    if "Loose motion" in s and "Vomiting" in s:
        return(
            "Acute Gastroenteritis",
            "MEDIUM",
            "Likely food-borne infection"
        )


    if "Acidity" in s:
        return(
            "GERD / Gastritis",
            "LOW",
            "Acid reflux pattern detected"
        )


# UTI

    if "Burning urination" in s:
        return(
            "Urinary Tract Infection",
            "MEDIUM",
            "Typical urinary infection symptoms"
        )


# SKIN

    if "Ring-shaped rash" in s:
        return(
            "Fungal Skin Infection",
            "LOW",
            "Dermatophyte infection likely"
        )


    if "Skin rash" in s:
        return(
            "Allergic Dermatitis",
            "LOW",
            "Possible allergy-based rash"
        )


# NEURO

    if "Headache" in s:
        return(
            "Tension Headache",
            "LOW",
            "Stress-related headache pattern"
        )


# DEFAULT

    return(
        "Insufficient Clinical Information",
        "UNKNOWN",
        "More symptoms required"
    )


# ---------------- SCREENING BUTTON ----------------

if st.button("Run Clinical Screening"):

    if not selected_symptoms:

        st.warning("Please select symptoms")

    else:

        condition, risk, explanation = assess(selected_symptoms)

        st.subheader("🧠 Clinical Impression")
        st.success(condition)

        st.subheader("⚠ Risk Level")

        if risk == "HIGH":
            st.error("HIGH RISK – Immediate medical evaluation required")

        elif risk == "MEDIUM":
            st.warning("MODERATE RISK – Consultation advised")

        elif risk == "LOW":
            st.success("LOW RISK – Routine monitoring")

        else:
            st.info("More data required")

        st.subheader("📖 Explanation")
        st.write(explanation)


# EMERGENCY BUTTONS

        if risk == "HIGH":

            st.error("Emergency referral recommended")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    '<a href="tel:108"><button style="width:100%;padding:12px;background:red;color:white;border:none;border-radius:8px;">🚑 Ambulance</button></a>',
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    '<a href="tel:112"><button style="width:100%;padding:12px;background:orange;color:white;border:none;border-radius:8px;">☎ Emergency</button></a>',
                    unsafe_allow_html=True
                )


st.divider()

st.caption(
    "AI Health Guidance System | B.Pharm Clinical Screening Prototype"
)
