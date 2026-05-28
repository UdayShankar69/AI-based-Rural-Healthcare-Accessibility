# misinformation.py
# --- 1. MISINFORMATION DATABASE (Your existing data) ---
misinfo_db = {
    "fever cured by alcohol": "This is false. Alcohol does not cure fever. Fact: Drink plenty of water and rest. Do not use alcohol on your skin or drink it.",
    "vaccines cause infertility": "False. Vaccines are safe and effective. Fact: They do not affect fertility in men or women.",
    "smoke cure": "False. Smoking or using smoke to treat illness, especially for respiratory issues, is dangerous. Fact: It can worsen lung conditions and is harmful to your health."
}
# --- 2. BASIC HEALTH & TREATMENT DATABASE (NEW AND EXPANDED DATA) ---
health_db = {
    # Existing entries
    "fever": {
        "condition": "Fever (High Temperature)",
        "information": "A fever is usually a sign that your body is fighting an infection. For adults, a temperature above 100.4°F (38°C) is considered a fever.",
        "treatment": "Take Paracetamol (Acetaminophen) or Ibuprofen as directed. Stay hydrated. If the fever lasts longer than 3 days, or is severe, consult a local health worker immediately."
    },
    "cough": {
        "condition": "Common Cough",
        "information": "A cough is a reflex action to clear your airways of mucus or irritants.",
        "treatment": "Use a simple cough syrup. Drink warm water mixed with honey and lemon for soothing relief. *eek help if the cough is severe or lasts more than a week."
    },
    "headache": {
        "condition": "Tension Headache",
        "information": "The most common headache, often caused by stress and dehydration.",
        "treatment": "Rest in a dark, quiet room. Take an over-the-counter pain reliever like Paracetamol or Ibuprofen. If the headache is sudden and severe, seek emergency medical care."
    },
    # NEW ENTRIES
    "chest pain": {
        "condition": "Chest Discomfort / Potential Heart Issue",
        "information": "Chest pain should never be ignored. It can be caused by muscle strain, but it may also signal a serious heart condition (like angina or a heart attack).",
        "treatment": "⚠️ EMERGENCY ACTION REQUIRED: If the pain is severe, crushing, radiates to the arm/jaw, or is accompanied by shortness of breath or dizziness, CALL EMERGENCY SERVICES (or your local equivalent) IMMEDIATELY! If stable, seek urgent medical assessment; rest and avoid strain."
    },
    "heart trouble": { # Secondary keyword for safety
        "condition": "Chest Discomfort / Potential Heart Issue",
        "information": "Symptoms like persistent chest pressure, fluttering heartbeats, or shortness of breath require immediate attention.",
        "treatment": "⚠️ EMERGENCY ACTION REQUIRED: If the pain is severe, crushing, radiates to the arm/jaw, or is accompanied by shortness of breath or dizziness, CALL EMERGENCY SERVICES (or your local equivalent) IMMEDIATELY! If stable, seek urgent medical assessment; rest and avoid strain."
    },
    "tingling": {
        "condition": "Nerve Paresthesia (Tingling/Numbness)",
        "information": "Often caused by temporary pressure on a nerve ('pinched nerve') or nutrient deficiency. Persistent, worsening, or widespread tingling can signal a nerve disorder or circulatory issue.",
        "treatment": "Change your position and stretch gently. Take a basic **Vitamin B complex** supplement. Avoid repetitive strain. **If tingling is sudden, involves a whole side of the body, or causes loss of movement, seek emergency medical attention."
    },
    "stomach pain": {
        "condition": "General Abdominal Discomfort",
        "information": "Most stomach pain is temporary, caused by indigestion, gas, or mild infection.",
        "treatment": "Rest, apply a warm compress. Avoid spicy, fatty, or highly acidic foods. Drink clear fluids. An antacid like Ranitidine or Omeprazole may help. If pain is severe, localized (especially bottom right), or accompanied by high fever, consult a doctor urgently."
    },
    "diarrhea": {
        "condition": "Acute Diarrhea",
        "information": "Frequent loose or watery bowel movements, often due to a viral or bacterial infection.",
        "treatment": "The primary concern is **hydration**. Drink plenty of water and **Oral Rehydration Salts (ORS)**. Take **Loperamide** to slow down bowel movements. Consume bland foods (rice, bananas). **Seek help if diarrhea lasts more than 2 days, or if there is blood or severe vomiting."
    }
}
# --------------------------------------------------------
def check_misinformation(statement: str):
    """Checks for misinformation and returns correction or 'No misinformation detected.'"""
    statement_lower = statement.lower()
    for myth, fact in misinfo_db.items():
        if myth in statement_lower:
            return {"input": statement, "corrected_info": fact}
    return {"input": statement, "corrected_info": "No misinformation detected."}
def get_medical_guidance(statement: str):
    """
    Checks for a known condition and returns detailed information and treatment.
    """
    statement_lower = statement.lower()
    # Check for keywords in the health database (priority matters here)
    for keyword, data in health_db.items():
        if keyword in statement_lower:
            return data
    return None