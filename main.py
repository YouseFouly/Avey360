import os
import requests

from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie


from gemini_utility import (avey_agent_response,
                            gemini_flash_vision_response,
                            alternative_medicine_response)

# -------------------- Setup --------------------
working_dir = os.path.dirname(os.path.abspath(__file__))

# -------------------- Lottie Function --------------------
def load_lottie_url(url: str):
    response = requests.get(url)
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print("❌ Failed to parse JSON from URL.")
        print("Response content:", response.text[:200])
        return None

# -------------------- Lottie Animations --------------------
chat_json = load_lottie_url("https://lottie.host/cc13fe2f-25c4-4547-b89a-5059f4044de4/Gn62lcFzBl.json")
DocuScan_json = load_lottie_url("https://lottie.host/e41ef2f2-47f8-45c6-acb0-eb671ec4ffa1/WlBXFt2yPX.json")
Radiology_json = load_lottie_url("https://lottie.host/e0b74159-de28-4cfd-bae6-581698ce79e2/lME5BM0Pd9.json")  
drug_json = load_lottie_url("https://lottie.host/14286a5b-1c1f-4045-a115-151fc05aae31/cdAdHR3dND.json")

# -------------------- Page Configuration --------------------
st.set_page_config(
    page_title="Avey360",
    page_icon="🩺",
    layout="centered",
)

# -------------------- Sidebar --------------------
st.set_page_config(
    page_title="Avey360",
    page_icon="🩺",
    layout="centered",
)

# -------------------- Sidebar --------------------
with st.sidebar:
    selected = option_menu(
        menu_title="Avey360",
        options=["Avey Therapist", "Avey Radiology", "Avey DocuScan", "Avey PharmaGuide"],
        icons=["chat-dots", "lungs", "file-earmark-text", "capsule"],
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#ffffff", "border-radius": "10px"},
            "icon": {"color": "#004080", "font-size": "20px"},  # blue icons
            "nav-link": {
                "color": "#001f3f",
                "font-size": "16px",
                "text-align": "left",
                "margin": "5px 0",
                "--hover-color": "#e6f0ff",  # light blue hover
            },
            "nav-link-selected": {
                "background-color": "#007bff",  # bright blue instead of red
                "color": "white",
                "font-weight": "bold",
            },
        }
    )


# -------------------- Avey Therapist page  --------------------
if selected == 'Avey Therapist':
    st.title("🫂 𝓐vey therapist is here for you ")

    if chat_json:
        st_lottie(chat_json, speed=1, loop=True, height=250)
    else:
        st.error("❌ Failed to load animation.")

    # Function to translate roles between Gemini-flash and Streamlit terminology
    def translate_role_for_streamlit(user_role):
        if user_role == "model":
            return "assistant"
        else:
            return user_role

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display history
    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(msg)

    # Input field
    user_prompt = st.chat_input("Take a deep breath and share what’s on your mind…")
    if user_prompt:
        st.session_state.chat_history.append(("user", user_prompt))
        with st.chat_message("user"):
            st.markdown(user_prompt)

        ans = avey_agent_response(user_prompt)

        st.session_state.chat_history.append(("assistant", ans))
        with st.chat_message("assistant"):
            st.markdown(ans)


# -------------------- Avey Radiology Page --------------------
if selected == "Avey Radiology":

    st.title("🫁 Medical Image Analysis")


    if Radiology_json:
        st_lottie(Radiology_json, speed=1, loop=True, height=250)
    else:
        st.error("❌ Failed to load animation.")

    uploaded_image = st.file_uploader("Upload an X-ray, CT, or MRI to get a thorough AI analysis of the image", type=["jpg", "jpeg", "png"])


    if st.button("Analyze Image"):
        image = Image.open(uploaded_image)

        st.image(image)

        default_prompt = """
                You are a highly experienced medical AI assistant. 
                I will provide you with a medical image (X-ray, MRI, CT scan, or other radiology images). 
                Your tasks are:

                1. Identify the type of image and what part of the body it shows. 
                2. Analyze the image carefully, explaining your observations in simple, professional language. 
                3. Identify any potential diseases, abnormalities, or conditions the patient may have, based on the image. 
                4. Recommend the most effective medications or treatments for the diagnosed condition, including alternative drugs with the same active ingredient if the main drug is unavailable. 
                5. Present your answer in a clear, structured, and easy-to-understand format for both medical professionals and patients.

                Be precise, professional, and empathetic in your explanation.

                """


        Explanation = gemini_flash_vision_response(default_prompt, image)

        st.info(Explanation)

# -------------------- Doctor Documents Interpreter page --------------------
if selected == "Avey DocuScan":


    st.title("📋️ Doctor Documents Interpreter")

    if DocuScan_json:
        st_lottie(DocuScan_json, speed=1, loop=True, height=250)
    else:
        st.error("❌ Failed to load animation.")

    uploaded_image = st.file_uploader("Upload a doctor’s document to extract drugs, dates, and get clear explanations of each medication.", type=["jpg", "jpeg", "png"])

    if st.button("Explain Document"):
        image = Image.open(uploaded_image)

        st.image(image, use_container_width=False, caption=" ", output_format="PNG")

        default_prompt = """
            You are a medical AI assistant. When given a doctor’s document or prescription, analyze and summarize it.

            Tasks:

            Extract all drug names and their prescribed dates.

            Identify the purpose of each drug and its medical use.

            Explain each medication in simple, accurate language (what it treats, how it works, key precautions).

            If multiple drugs relate to one condition, group them together.

            Maintain a clear, structured format with bullet points.

            End with a disclaimer:

            “This summary is for educational purposes only. Always follow your doctor’s advice.”
            """

        Explanation_C = gemini_flash_vision_response(default_prompt, image)

        st.info(Explanation_C)


# -------------------- Avey PharmaGuide Page --------------------
if selected == "Avey PharmaGuide":

    st.title("Drug Alternatives💊")

    if drug_json:
        st_lottie(drug_json, speed=1, loop=True, height=250)
    else:
        st.error("❌ Failed to load animation.")

    # text box to enter prompt

    user_prompt = st.text_area(label='Enter a drug to get effective alternatives and key differences.', placeholder="Ask me anything...")

    if st.button("Get Alternative"):
        response = alternative_medicine_response(user_prompt)
        st.markdown(response)

