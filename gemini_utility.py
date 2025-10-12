import os
import json
from PIL import Image

import google.generativeai as genai

# working directory path
working_dir = os.path.dirname(os.path.abspath(__file__))

# path of config_data file
config_file_path = f"{working_dir}/config.json"
config_data = json.load(open("config.json"))

# loading the GOOGLE_API_KEY
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]

# configuring google.generativeai with API key
genai.configure(api_key=GOOGLE_API_KEY)

# System prompt for Avey agent
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

def avey_agent_response(user_prompt):
    gemini_model = genai.GenerativeModel("gemini-2.0-flash-001")
    full_prompt = f"{AVEY_SYSTEM}\n\nQuestion:\n{user_prompt}"
    response = gemini_model.generate_content(full_prompt)
    return response.text


# get response from gemini-2.0-flash model - image/text to text
def gemini_flash_vision_response(prompt, image):
    gemini_flash_vision_model = genai.GenerativeModel("gemini-2.0-flash-001")
    response = gemini_flash_vision_model.generate_content([prompt, image])
    result = response.text
    return result


# get response from gemini-2.0-flash model - text to text
ALTERNATIVE_DRUG_PROMPT = ("""
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

    - give me all the prices for each medicine

    End with a disclaimer:

“This information is for educational purposes only. Consult a healthcare provider before changing any medication.”
""")

def alternative_medicine_response(user_prompt):
    gemini_model = genai.GenerativeModel("gemini-2.0-flash-001")
    full_prompt = f"{ALTERNATIVE_DRUG_PROMPT}\n\nQuestion:\n{user_prompt}"
    response = gemini_model.generate_content(full_prompt)

    return response.text
