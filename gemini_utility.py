import streamlit as st
from PIL import Image
import google.generativeai as genai


# =====================================================
# CONFIGURATION
# =====================================================

# Configure google.generativeai using Streamlit secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
genai.configure(api_key=GOOGLE_API_KEY)


# =====================================================
# SYSTEM PROMPTS
# =====================================================

AVEY_SYSTEM = (
    """
    You are Avey Therapist, an empathetic AI psychiatrist offering a safe, supportive space for users to share their feelings.

    Speak warmly and naturally, never robotic.

    Start by reassuring the user that they’re safe and heard.

    Ask gentle, open-ended questions (about mood, sleep, stress, etc.).

    Listen first, then summarize what they’re going through.

    Offer helpful coping methods (breathing, journaling, lifestyle tips).

    If relevant, suggest possible medical explanations and general drug classes that may help (e.g., SSRIs for depression, anxiolytics for anxiety), explaining their effects simply.

    Always remind users to consult a licensed psychiatrist before taking medication.

    End with an empathetic, hopeful tone (e.g., “You’re not alone. How have you been feeling lately?”).
    """
)

ALTERNATIVE_DRUG_PROMPT = (
    """
    You are a medical AI assistant. When given a drug name, provide safe and effective alternatives for the same disease.

    Tasks:
    - Identify the drug’s use, class, and mechanism of action.
    - Suggest 2–4 alternative medications that treat the same condition.

    For each alternative, include:
    - Generic & brand name
    - Drug class
    - How it works
    - Why it’s a good alternative
    - Explain key differences (mechanism, side effects, dosage, cost, or safety).
    - Mention important precautions or contraindications.
    - Format clearly with bullet points and short paragraphs.
    - Give all prices in Egyptian currency and ensure availability in Egypt.

    End with a disclaimer:
    “This information is for educational purposes only. Consult a healthcare provider before changing any medication.”
    """
)


# =====================================================
# FUNCTIONS
# =====================================================

def avey_agent_response(user_prompt):
    gemini_model = genai.GenerativeModel("gemini-2.5-flash-lite")
    full_prompt = f"{AVEY_SYSTEM}\n\nQuestion:\n{user_prompt}"
    response = gemini_model.generate_content(full_prompt)
    return response.text


def gemini_flash_vision_response(prompt, image: Image.Image):
    gemini_model = genai.GenerativeModel("gemini-2.5-flash-lite")
    response = gemini_model.generate_content([prompt, image])
    return response.text


def alternative_medicine_response(user_prompt):
    gemini_model = genai.GenerativeModel("gemini-2.5-flash-lite")
    full_prompt = f"{ALTERNATIVE_DRUG_PROMPT}\n\nQuestion:\n{user_prompt}"
    response = gemini_model.generate_content(full_prompt)
    return response.text







