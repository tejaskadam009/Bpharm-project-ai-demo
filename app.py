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

    st.markdown(
        """
<div style="padding:20px;border-radius:12px;
background:rgba(255,255,255,0.05);
border:1px solid rgba(255,255,255,0.15);">

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
    "Select symptoms below → Run screening → Review clinical guidance"
)

st.divider()


# ---------------- SYMPTOM LIST ----------------
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
    "Select observed symptoms",
    symptoms_list
)

st.divider()


# ---------------- IMAGE INPUT ----------------
uploaded_img = st.file_uploader(
    "Upload rash / wound image (optional)",
    type=["jpg", "jpeg", "png"]
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
            ["May indicate myocardial infarction or acute respiratory condition"],
            ["Pain radiating to arm/jaw", "Severe breathing difficulty"],
            ["Immediate hospital referral required"]
        )

    if "Seizures" in s or "Confusion" in s:
        return (
            "Possible Neurological Emergency",
            "HIGH",
            ["Possible seizure disorder or CNS pathology"],
            ["Repeated seizures", "Loss of consciousness"],
            ["Urgent neurological consultation required"]
        )

    # MODERATE RISK CONDITIONS
    if "Fever" in s and "Cough" in s:
        return (
            "Upper Respiratory Infection",
            "MEDIUM",
            ["Suggestive of viral respiratory infection"],
            ["Persistent fever >3 days", "Breathlessness"],
            ["Paracetamol + steam inhalation recommended"]
        )

    if "Vomiting" in s or "Loose motion" in s:
        return (
            "Acute Gastroenteritis",
            "MEDIUM",
            ["Suggestive of GI infection"],
            ["Severe dehydration", "Blood in stool"],
            ["ORS + hydration recommended"]
        )

    # LOW RISK CONDITIONS
    if "Skin rash" in s or "Itching" in s:
        return (
            "Skin Allergy / Fungal Infection",
            "LOW",
            ["Likely dermatological irritation"],
            ["Spreading rash"],
            ["Topical antifungal may help"]
        )

    return (
        "Insufficient Clinical Information",
        "UNKNOWN",
        ["More symptoms required for assessment"],
        ["Persistent symptoms"],
        ["Consult healthcare professional"]
    )


# ---------------- SCREENING BUTTON ----------------
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
            st.error("🔴 HIGH RISK – Immediate evaluation recommended")

        elif risk == "MEDIUM":
            st.warning("🟠 MODERATE RISK – Consultation advised")

        elif risk == "LOW":
            st.success("🟢 LOW RISK – Routine monitoring advised")

        else:
            st.info("Insufficient data")

        st.subheader("Clinical Explanation")
        for e in explanation:
            st.write("•", e)

        st.subheader("Urgent Warning Indicators")
        for r in redflags:
            st.write("•", r)

        st.subheader("Pharmacist Counselling Guidance")
        for g in guidance:
            st.write("•", g)

        # ---------------- EMERGENCY BUTTONS ----------------
        if risk == "HIGH":

            st.error("Emergency referral recommended")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(
                    '<a href="tel:108"><button style="width:100%;padding:14px;background:red;color:white;border:none;border-radius:10px;">🚑 Ambulance</button></a>',
                    unsafe_allow_html=True
                )

            with c2:
                st.markdown(
                    '<a href="tel:112"><button style="width:100%;padding:14px;background:orange;color:white;border:none;border-radius:10px;">☎ Emergency</button></a>',
                    unsafe_allow_html=True
                )

            with c3:
                st.markdown(
                    '<a href="tel:+919999999999"><button style="width:100%;padding:14px;background:green;color:white;border:none;border-radius:10px;">👨‍⚕️ Doctor</button></a>',
                    unsafe_allow_html=True
                )

st.divider()

st.caption(
    "AI Health Guidance System | Clinical Decision Support Prototype | B.Pharm Final Year Project"
)
