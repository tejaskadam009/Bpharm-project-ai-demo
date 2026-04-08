import streamlit as st
from PIL import Image

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Health Guidance System",
    page_icon="🩺",
    layout="centered"
)

# ---------------- DISCLAIMER POPUP ----------------
if "accepted" not in st.session_state:
    st.session_state.accepted = False


@st.dialog("⚠️ Important Notice")
def disclaimer():
    st.markdown("""
### AI Health Guidance System

This application provides:

✔ Possible condition (probable)  
✔ Risk level estimation  
✔ Guidance and referral suggestions  

This application does NOT provide:

❌ Confirmed diagnosis  
❌ Emergency treatment  
❌ Prescription  

🚨 If symptoms are severe, contact a healthcare professional immediately.
""")

    if st.checkbox("I understand and wish to continue"):
        if st.button("Continue"):
            st.session_state.accepted = True
            st.rerun()


if not st.session_state.accepted:
    disclaimer()
    st.stop()

# ---------------- HEADER ----------------
st.title("🩺 AI Health Guidance System")
st.caption("Symptom Screening • Risk Assessment • Referral Guidance")

# ---------------- 100 SYMPTOMS ----------------
symptoms_list = [
"Fever","High fever","Chills","Night sweats","Body ache","Weakness","Shivering","Persistent fever","Sweating","Weight loss",
"Cough","Dry cough","Wet cough","Sore throat","Runny nose","Nasal congestion","Sneezing","Breathlessness","Wheezing","Chest tightness",
"Chest pain","Blood in sputum","Hoarseness","Rapid breathing","Shortness of breath",
"Nausea","Vomiting","Loose motion","Constipation","Stomach pain","Severe abdominal pain","Bloating","Acidity","Loss of appetite","Blood in stool",
"Dehydration","Black stool","Yellow eyes","Gas","Indigestion",
"Headache","Severe headache","Dizziness","Fainting","Blurred vision","Confusion","Memory loss","Seizures","Neck stiffness","Tremors",
"Loss of balance","Numbness","Slurred speech","Sensitivity to light","Migraine",
"Itching","Rash","Redness","Swelling","Pus discharge","Burning skin","Dry skin","Hives","Blisters","Skin peeling",
"Dark patches","Open wound","Painful lesion","Ring rash","Skin infection",
"Burning urination","Frequent urination","Lower abdominal pain","Blood in urine","Back pain kidney","Urine retention","Cloudy urine","Foul urine","Pain urination","Night urination",
"Watery eyes","Face swelling","Lip swelling","Tongue swelling","Difficulty swallowing","Severe allergy","Itchy throat","Runny eyes","Skin allergy","Breathing allergy",
"Joint pain","Muscle cramps","Muscle weakness","Back pain","Neck pain","Shoulder pain","Leg swelling","High thirst","Frequent urination thirst","Fatigue after activity"
]

# ---------------- RISK ENGINE ----------------
def assess(symptoms):

    s = set(symptoms)

    # HIGH RISK CONDITIONS
    if "Chest pain" in s or "Breathlessness" in s:
        return "Medical Emergency Possible", "HIGH", [
            "Seek emergency medical care immediately.",
            "Avoid physical exertion."
        ]

    if "Seizures" in s or "Confusion" in s:
        return "Neurological Emergency Possible", "HIGH", [
            "Immediate hospital evaluation required."
        ]

    if "Blood in stool" in s or "Blood in urine" in s:
        return "Possible Internal Bleeding", "HIGH", [
            "Urgent doctor consultation required."
        ]

    # MEDIUM RISK CONDITIONS
    if "Fever" in s and "Cough" in s:
        return "Viral Fever / Respiratory Infection", "MEDIUM", [
            "Rest and stay hydrated.",
            "Monitor temperature regularly.",
            "Consult doctor if fever persists >3 days."
        ]

    if "Vomiting" in s or "Loose motion" in s:
        return "Acute Gastroenteritis Possibility", "MEDIUM", [
            "Use ORS frequently.",
            "Maintain hydration.",
            "Eat light food."
        ]

    if "Burning urination" in s:
        return "Urinary Tract Infection Possibility", "MEDIUM", [
            "Increase water intake.",
            "Consult doctor for urine test."
        ]

    # LOW RISK CONDITIONS
    if "Rash" in s or "Itching" in s:
        return "Skin Allergy / Infection Possibility", "LOW", [
            "Keep area clean and dry."
        ]

    if "Acidity" in s:
        return "Acidity / Indigestion Possibility", "LOW", [
            "Avoid spicy food.",
            "Eat small frequent meals."
        ]

    return "Insufficient Information", "UNKNOWN", [
        "Select more symptoms for better assessment."
    ]


# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["Symptom Checker", "Clinical Scenarios"])

# ---------------- TAB 1 ----------------
with tab1:

    selected_symptoms = st.multiselect("Select Symptoms", symptoms_list)

    uploaded_img = st.file_uploader(
        "Upload image (optional)",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_img:
        st.image(Image.open(uploaded_img), use_container_width=True)

    if st.button("Analyze Symptoms"):

        if not selected_symptoms:
            st.warning("Please select symptoms.")
        else:

            condition, risk, advice = assess(selected_symptoms)

            st.subheader("Possible Condition")
            st.success(condition)

            st.subheader("Risk Level")
            st.write(risk)

            st.subheader("Guidance")

            for a in advice:
                st.write("•", a)

        # ---------------- EMERGENCY BUTTONS ----------------

if risk == "HIGH":

    st.error("🚨 Serious symptoms detected")

    st.markdown("### Emergency Assistance")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            '<a href="tel:108"><button style="width:100%;padding:14px;background:red;color:white;border:none;border-radius:8px;">🚑 Call Ambulance (108)</button></a>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<a href="tel:112"><button style="width:100%;padding:14px;background:orange;color:white;border:none;border-radius:8px;">☎ Emergency (112)</button></a>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<a href="tel:+919999999999"><button style="width:100%;padding:14px;background:green;color:white;border:none;border-radius:8px;">👨‍⚕️ Call Doctor</button></a>',
            unsafe_allow_html=True
        )
