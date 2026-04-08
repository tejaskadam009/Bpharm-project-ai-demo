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
This system provides:

✔ Possible condition (probable)
✔ Risk level estimation
✔ Pharmacy guidance
✔ Emergency referral suggestions

This system does NOT provide:

❌ Confirmed diagnosis
❌ Prescription
❌ Emergency treatment replacement
""")

    if st.checkbox("I understand and wish to continue"):
        if st.button("Continue"):
            st.session_state.accepted = True
            st.rerun()

    st.stop()


# ---------------- HEADER ----------------
st.title("🩺 AI Health Guidance System")
st.caption("Symptom Screening • Risk Assessment • Pharmacy Guidance")


# ---------------- SYMPTOMS ----------------
symptoms_list = [
    "Fever","Cough","Sore throat","Breathlessness","Chest pain",
    "Vomiting","Loose motion","Burning urination",
    "Rash","Itching","Acidity",
    "Seizures","Confusion",
    "Blood in stool","Blood in urine"
]


# ---------------- CLINICAL ENGINE ----------------
def assess(symptoms):

    s = set(symptoms)

    # ---------------- HIGH RISK ----------------
    if "Chest pain" in s or "Breathlessness" in s:

        return (
            "Possible Cardiac or Respiratory Emergency",
            "HIGH",
            [
                "Chest pain with breathlessness may indicate heart attack or lung emergency.",
                "Immediate medical evaluation is required."
            ],
            [
                "Pain spreading to arm or jaw",
                "Severe breathlessness",
                "Bluish lips or fingers"
            ],
            [
                "Do NOT self-medicate",
                "Seek emergency hospital care immediately"
            ]
        )

    if "Seizures" in s or "Confusion" in s:

        return (
            "Possible Neurological Emergency",
            "HIGH",
            [
                "Seizures or confusion indicate possible brain emergency.",
                "Immediate neurological evaluation required."
            ],
            [
                "Repeated seizures",
                "Loss of consciousness",
                "Severe headache with vomiting"
            ],
            [
                "Emergency hospital visit required"
            ]
        )

    if "Blood in stool" in s or "Blood in urine" in s:

        return (
            "Possible Internal Bleeding",
            "HIGH",
            [
                "Presence of blood in stool or urine requires urgent diagnosis."
            ],
            [
                "Persistent bleeding",
                "Weakness or dizziness"
            ],
            [
                "Immediate doctor consultation recommended"
            ]
        )

    # ---------------- MEDIUM RISK ----------------
    if "Fever" in s and "Cough" in s:

        return (
            "Viral Fever / Respiratory Infection",
            "MEDIUM",
            [
                "Symptoms suggest respiratory infection.",
                "Rest and hydration recommended."
            ],
            [
                "Fever lasting more than 3 days",
                "Breathing difficulty"
            ],
            [
                "Paracetamol may help reduce fever",
                "Steam inhalation recommended"
            ]
        )

    if "Vomiting" in s or "Loose motion" in s:

        return (
            "Acute Gastroenteritis",
            "MEDIUM",
            [
                "Vomiting or diarrhea suggest stomach infection."
            ],
            [
                "Severe dehydration",
                "Blood in stool"
            ],
            [
                "ORS recommended",
                "Avoid oily and spicy food"
            ]
        )

    if "Burning urination" in s:

        return (
            "Possible Urinary Tract Infection",
            "MEDIUM",
            [
                "Burning urination indicates possible urinary infection."
            ],
            [
                "Back pain with fever",
                "Blood in urine"
            ],
            [
                "Increase water intake",
                "Urine test recommended"
            ]
        )

    # ---------------- LOW RISK ----------------
    if "Rash" in s or "Itching" in s:

        return (
            "Skin Allergy or Fungal Infection",
            "LOW",
            [
                "Skin rash with itching usually indicates allergy or fungal infection."
            ],
            [
                "Rapid spreading rash",
                "Pus formation"
            ],
            [
                "Topical antifungal may help",
                "Keep area clean and dry"
            ]
        )

    if "Acidity" in s:

        return (
            "Acidity / Gastritis",
            "LOW",
            [
                "Acidity usually occurs due to irregular meals or spicy food."
            ],
            [
                "Vomiting blood",
                "Severe abdominal pain"
            ],
            [
                "Antacid may help",
                "Avoid late-night meals"
            ]
        )

    # ---------------- DEFAULT ----------------
    return (
        "Insufficient Clinical Information",
        "UNKNOWN",
        [
            "Selected symptoms are not enough for assessment."
        ],
        [
            "Persistent symptoms",
            "High fever",
            "Breathing difficulty"
        ],
        [
            "Consult doctor if symptoms worsen"
        ]
    )


# ---------------- USER INPUT ----------------
selected_symptoms = st.multiselect("Select Symptoms", symptoms_list)

uploaded_img = st.file_uploader("Upload image (optional)", type=["jpg","png","jpeg"])

if uploaded_img:
    st.image(Image.open(uploaded_img))


# ---------------- ANALYZE BUTTON ----------------
if st.button("Analyze Symptoms"):

    if not selected_symptoms:

        st.warning("Please select symptoms")

    else:

        condition, risk, explanation, redflags, otc = assess(selected_symptoms)

        st.subheader("Possible Condition")
        st.success(condition)

        st.subheader("Risk Level")
        st.write(risk)

        st.subheader("Clinical Explanation")
        for e in explanation:
            st.write("•", e)

        st.subheader("Red Flag Symptoms")
        for r in redflags:
            st.write("•", r)

        st.subheader("Pharmacy Guidance")
        for o in otc:
            st.write("•", o)


        # ---------------- EMERGENCY BUTTONS ----------------
        if risk == "HIGH":

            st.error("🚨 Emergency condition detected")

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
