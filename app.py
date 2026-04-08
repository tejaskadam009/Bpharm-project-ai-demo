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
This AI Health Guidance System provides:

✔ Possible condition (probable)  
✔ Risk level estimation  
✔ Pharmacy counselling guidance  
✔ Emergency referral suggestions  

It does NOT provide confirmed diagnosis or prescription.
Always consult a healthcare professional when required.
""")

    if st.checkbox("I understand and wish to continue"):
        if st.button("Continue"):
            st.session_state.accepted = True
            st.rerun()

    st.stop()


# ---------------- HEADER ----------------
st.title("🩺 AI Health Guidance System")
st.caption("Symptom Screening • Risk Assessment • Pharmacy Counselling Support")


# ---------------- SYMPTOMS DATABASE ----------------
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


# ---------------- CLINICAL ENGINE ----------------
def assess(symptoms):

    s = set(symptoms)

    # HIGH RISK CONDITIONS
    if "Chest pain" in s or "Breathlessness" in s:
        return (
            "Possible Cardiac or Respiratory Emergency",
            "HIGH",
            [
                "Chest pain with breathlessness may indicate heart attack or lung emergency."
            ],
            [
                "Pain spreading to arm or jaw",
                "Severe breathing difficulty"
            ],
            [
                "Immediate hospital visit required"
            ]
        )

    if "Seizures" in s or "Confusion" in s:
        return (
            "Possible Neurological Emergency",
            "HIGH",
            ["Seizures may indicate brain-related emergency"],
            ["Repeated seizures","Loss of consciousness"],
            ["Emergency neurological evaluation required"]
        )

    if "Blood in stool" in s or "Black stool" in s:
        return (
            "Possible Gastrointestinal Bleeding",
            "HIGH",
            ["Blood in stool indicates internal bleeding"],
            ["Weakness","Persistent bleeding"],
            ["Immediate doctor consultation required"]
        )


    # MEDIUM RISK CONDITIONS

    if "Fever" in s and "Cough" in s:
        return (
            "Upper Respiratory Infection / Viral Fever",
            "MEDIUM",
            ["Symptoms indicate respiratory infection"],
            ["Fever > 3 days","Breathing difficulty"],
            ["Paracetamol may help","Steam inhalation useful"]
        )

    if "Vomiting" in s or "Loose motion" in s:
        return (
            "Acute Gastroenteritis",
            "MEDIUM",
            ["Vomiting or diarrhea suggests GI infection"],
            ["Severe dehydration","Blood in stool"],
            ["ORS recommended","Avoid spicy food"]
        )

    if "Burning urination" in s:
        return (
            "Urinary Tract Infection",
            "MEDIUM",
            ["Burning urination suggests infection"],
            ["Back pain with fever"],
            ["Increase fluid intake","Urine test advised"]
        )

    if "Joint pain" in s and "Fever" in s:
        return (
            "Possible Viral Arthritis / Dengue Suspicion",
            "MEDIUM",
            ["Joint pain with fever requires monitoring"],
            ["Persistent fever","Bleeding gums"],
            ["Doctor consultation recommended"]
        )


    # LOW RISK CONDITIONS

    if "Skin rash" in s or "Itching" in s:
        return (
            "Skin Allergy / Fungal Infection",
            "LOW",
            ["Common dermatological reaction"],
            ["Spreading rash","Pus formation"],
            ["Topical antifungal may help"]
        )

    if "Acidity" in s or "Heartburn" in s:
        return (
            "Acidity / Gastritis",
            "LOW",
            ["Likely due to diet or irregular meals"],
            ["Vomiting blood"],
            ["Antacid recommended"]
        )

    if "Back pain" in s:
        return (
            "Musculoskeletal Back Pain",
            "LOW",
            ["Likely posture-related issue"],
            ["Persistent numbness"],
            ["Rest and posture correction"]
        )


    return (
        "Insufficient Clinical Information",
        "UNKNOWN",
        ["More symptoms required for assessment"],
        ["Persistent symptoms"],
        ["Consult doctor if symptoms worsen"]
    )


# ---------------- INPUT ----------------
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

        if risk == "HIGH":
            st.error(risk)

        elif risk == "MEDIUM":
            st.warning(risk)

        elif risk == "LOW":
            st.success(risk)

        else:
            st.info(risk)


        st.subheader("Clinical Explanation")
        for e in explanation:
            st.write("•", e)


        st.subheader("Red Flag Symptoms")
        for r in redflags:
            st.write("•", r)


        st.subheader("Pharmacy Guidance")
        for o in otc:
            st.write("•", o)


        # EMERGENCY CONTACT
        if risk == "HIGH":

            st.error("🚨 Emergency condition detected")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(
                    '<a href="tel:108"><button style="width:100%;padding:14px;background:red;color:white;border:none;border-radius:8px;">🚑 Ambulance</button></a>',
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    '<a href="tel:112"><button style="width:100%;padding:14px;background:orange;color:white;border:none;border-radius:8px;">☎ Emergency</button></a>',
                    unsafe_allow_html=True
                )

            with col3:
                st.markdown(
                    '<a href="tel:+919999999999"><button style="width:100%;padding:14px;background:green;color:white;border:none;border-radius:8px;">👨‍⚕️ Doctor</button></a>',
                    unsafe_allow_html=True
                )
