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

    # ---------------- HIGH RISK ----------------

    if "Chest pain" in s or "Breathlessness" in s:
        return (
            "Possible Cardiac or Respiratory Emergency",
            "HIGH",
            [
                "Chest pain and breathlessness may indicate heart attack or serious lung condition.",
                "Sit upright and avoid physical activity.",
                "Immediate hospital evaluation is strongly recommended."
            ],
            [
                "Severe chest tightness",
                "Pain spreading to arm/jaw",
                "Bluish lips or fingers"
            ],
            [
                "Do NOT self-medicate.",
                "Emergency medical care required immediately."
            ]
        )

    if "Seizures" in s or "Confusion" in s:
        return (
            "Possible Neurological Emergency",
            "HIGH",
            [
                "Seizures or confusion may indicate brain-related emergency.",
                "Ensure patient safety during seizure.",
                "Immediate medical supervision required."
            ],
            [
                "Loss of consciousness",
                "Repeated seizures",
                "Severe headache with vomiting"
            ],
            [
                "Emergency neurological assessment required."
            ]
        )

    if "Blood in stool" in s or "Blood in urine" in s:
        return (
            "Possible Internal Bleeding",
            "HIGH",
            [
                "Presence of blood in stool or urine requires urgent evaluation.",
                "Avoid delaying consultation."
            ],
            [
                "Weakness or dizziness",
                "Black-colored stool",
                "Persistent bleeding"
            ],
            [
                "Hospital consultation immediately recommended."
            ]
        )

    # ---------------- MEDIUM RISK ----------------

    if "Fever" in s and "Cough" in s:
        return (
            "Viral Fever / Upper Respiratory Infection",
            "MEDIUM",
            [
                "Symptoms indicate possible viral respiratory infection.",
                "Maintain hydration and rest.",
                "Monitor body temperature regularly."
            ],
            [
                "Persistent fever beyond 3 days",
                "Breathing difficulty",
                "Severe weakness"
            ],
            [
                "Paracetamol may be used for fever (if not contraindicated).",
                "Steam inhalation and warm fluids recommended."
            ]
        )

    if "Vomiting" in s or "Loose motion" in s:
        return (
            "Acute Gastroenteritis",
            "MEDIUM",
            [
                "Vomiting and diarrhea suggest gastrointestinal infection.",
                "Maintain hydration using ORS."
            ],
            [
                "Severe dehydration",
                "Blood in stool",
                "Continuous vomiting"
            ],
            [
                "ORS recommended.",
                "Avoid oily and spicy foods."
            ]
        )

    if "Burning urination" in s:
        return (
            "Possible Urinary Tract Infection",
            "MEDIUM",
            [
                "Burning urination commonly indicates urinary infection.",
                "Increase fluid intake."
            ],
            [
                "Fever with back pain",
                "Blood in urine"
            ],
            [
                "Urine examination advised.",
                "Doctor consultation recommended."
            ]
        )

    # ---------------- LOW RISK ----------------

    if "Rash" in s or "Itching" in s:
        return (
            "Skin Allergy or Fungal Infection",
            "LOW",
            [
                "Skin rash with itching often indicates allergy or fungal infection.",
                "Keep affected area dry and clean."
            ],
            [
                "Rapid spreading rash",
                "Pus formation",
                "Fever with rash"
            ],
            [
                "Topical antifungal or antihistamine may help.",
                "Consult doctor if spreading."
            ]
        )

    if "Acidity" in s:
        return (
            "Acidity / Gastritis",
            "LOW",
            [
                "Acidity commonly occurs due to irregular meals or spicy food.",
                "Avoid late-night meals."
            ],
            [
                "Severe abdominal pain",
                "Vomiting blood"
            ],
            [
                "Antacid may provide relief.",
                "Avoid spicy food."
            ]
        )

    # ---------------- DEFAULT ----------------

    return (
        "Insufficient Clinical Information",
        "UNKNOWN",
        [
            "Selected symptoms are not sufficient for assessment.",
            "Add more symptoms for better evaluation."
        ],
        [
            "Persistent symptoms",
            "Breathing difficulty",
            "High fever"
        ],
        [
            "Consult doctor if symptoms worsen."
        ]
    )

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

        condition, risk, explanation, redflags, otc = assess(selected_symptoms)

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
