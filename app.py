def assess(symptoms):

    s = set(symptoms)

    # HIGH RISK CONDITIONS
    if any(x in s for x in ["Chest pain", "Breathlessness", "Shortness of breath"]):
        return "Medical Emergency Possible", "HIGH", [
            "Seek emergency medical care immediately.",
            "Avoid physical exertion."
        ]

    if any(x in s for x in ["Seizures", "Confusion", "Fainting"]):
        return "Neurological Emergency Possible", "HIGH", [
            "Immediate hospital evaluation required."
        ]

    if any(x in s for x in ["Blood in stool", "Blood in urine"]):
        return "Possible Internal Bleeding", "HIGH", [
            "Urgent doctor consultation required."
        ]


    # MEDIUM RISK CONDITIONS

    if "Fever" in s and ("Cough" in s or "Sore throat" in s):
        return "Viral Fever / Respiratory Infection", "MEDIUM", [
            "Rest and stay hydrated.",
            "Monitor temperature regularly.",
            "Consult doctor if fever persists more than 3 days."
        ]

    if any(x in s for x in ["Vomiting", "Loose motion"]):
        return "Acute Gastroenteritis Possibility", "MEDIUM", [
            "Use ORS frequently.",
            "Maintain hydration.",
            "Eat light food."
        ]

    if any(x in s for x in ["Burning urination", "Frequent urination"]):
        return "Urinary Tract Infection Possibility", "MEDIUM", [
            "Increase water intake.",
            "Consult doctor for urine test."
        ]


    # LOW RISK CONDITIONS

    if any(x in s for x in ["Rash", "Itching", "Skin infection"]):
        return "Skin Allergy / Infection Possibility", "LOW", [
            "Keep area clean and dry.",
            "Avoid scratching affected area."
        ]

    if "Acidity" in s:
        return "Acidity / Indigestion Possibility", "LOW", [
            "Avoid spicy food.",
            "Eat small frequent meals."
        ]


    # DEFAULT RESPONSE

    return "Insufficient Information", "UNKNOWN", [
        "Select more symptoms for better assessment."
    ]
