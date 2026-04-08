import streamlit as st
from PIL import Image

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Health Guidance System",
    page_icon="🩺",
    layout="centered"
)

# ---------------- DISCLAIMER ----------------
if "accepted" not in st.session_state:
    st.session_state.accepted = False

if not st.session_state.accepted:
    st.title("⚠️ Important Notice")

    st.write("""
This application provides:

✔ Possible condition (probable)
✔ Risk level estimation
✔ Guidance and referral suggestions

This application does NOT provide:

❌ Confirmed diagnosis
❌ Emergency treatment
❌ Prescription
""")

    if st.checkbox("I understand and wish to continue"):
        if st.button("Continue"):
            st.session_state.accepted = True
            st.rerun()

    st.stop()

# ---------------- HEADER ----------------
st.title("🩺 AI Health Guidance System")
st.caption("Symptom Screening • Risk Assessment • Referral Guidance")

# ---------------- SYMPTOMS LIST ----------------
symptoms_list = [
"Fever","Cough","Sore throat","Breathlessness","Chest pain",
"Vomiting","Loose motion","Burning urination",
"Rash","Itching","Acidity","Seizures","Confusion",
"Blood in stool","Blood in urine"
]

# ---------------- RISK ENGINE ----------------
def assess(symptoms):

    s = set(symptoms)

    if "Chest pain" in s or "Breathlessness" in s:
        return "Medical Emergency Possible", "HIGH", [
            "Seek emergency medical care immediately."
        ]

    if "Seizures" in s or "Confusion" in s:
        return "Neurological Emergency Possible", "HIGH", [
            "Immediate hospital evaluation required."
        ]

    if "Blood in stool" in s or "Blood in urine" in s:
        return "Possible Internal Bleeding", "HIGH", [
            "Urgent doctor consultation required."
        ]

    if "Fever" in s and "Cough" in s:
        return "Respiratory Infection Possible", "MEDIUM", [
            "Rest and hydration recommended."
        ]

    if "Vomiting" in s or "Loose motion" in s:
        return "Gastroenteritis Possible", "MEDIUM", [
            "ORS and hydration recommended."
        ]

    if "Burning urination" in s:
        return "UTI Possible", "MEDIUM", [
            "Consult doctor for urine test."
        ]

    if "Rash" in s or "Itching" in s:
        return "Skin Allergy Possible", "LOW", [
            "Keep area clean and dry."
        ]

    if "Acidity" in s:
        return "Acidity Possible", "LOW", [
            "Avoid spicy food."
        ]

    return "Insufficient Information", "UNKNOWN", [
        "Select more symptoms."
    ]


# ---------------- UI ----------------
selected_symptoms = st.multiselect(
    "Select Symptoms",
    symptoms_list
)

uploaded_img = st.file_uploader(
    "Upload image (optional)",
    type=["jpg","png","jpeg"]
)

if uploaded_img:
    st.image(Image.open(uploaded_img))

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

        if risk == "HIGH":

            st.error("🚨 Serious symptoms detected")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(
                    '<a href="tel:108"><button style="width:100%;padding:14px;background:red;color:white;border:none;border-radius:8px;">🚑 Call Ambulance</button></a>',
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    '<a href="tel:112"><button style="width:100%;padding:14px;background:orange;color:white;border:none;border-radius:8px;">☎ Emergency</button></a>',
                    unsafe_allow_html=True
                )

            with col3:
                st.markdown(
                    '<a href="tel:+919999999999"><button style="width:100%;padding:14px;background:green;color:white;border:none;border-radius:8px;">👨‍⚕️ Call Doctor</button></a>',
                    unsafe_allow_html=True
                )
