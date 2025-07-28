import streamlit as st
import openai

# Load API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

# App title
st.title("🩺 Health Symptom Checker")

# Emergency-related keywords for triage
EMERGENCY_KEYWORDS = [
    "chest pain", "difficulty breathing", "shortness of breath", 
    "sudden confusion", "unconscious", "faint", "stroke", "heart attack"
]

# Emergency checker function
def is_emergency(text):
    text = text.lower()
    return any(phrase in text for phrase in EMERGENCY_KEYWORDS)

# Initial system prompt for AI behavior
system_prompt = (
    "You are a professional AI assistant specialized in health and symptom checking. "
    "Your role is to help users understand their symptoms and suggest possible common causes "
    "based on the information they provide. You must clearly state that you are not a doctor, "
    "and you do not provide medical diagnoses or emergency advice. "
    "If a user describes emergency symptoms like chest pain, difficulty breathing, or sudden confusion, respond: "
    "'These symptoms may indicate a medical emergency. Please seek immediate medical attention or call emergency services.' "
    "If a user asks about anything unrelated to health or symptoms, politely say: "
    "'I'm here to help with health-related questions and symptom checking. Please ask about symptoms, conditions, or health concerns.'"
)

# Initialize chat history with system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

# Display past messages (excluding system prompt)
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Describe your symptoms...")

# Function to fetch assistant response
def get_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message["content"]

# Handle user interaction
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Emergency warning, if detected
    if is_emergency(user_input):
        emergency_message = (
            "🚨 **These symptoms may indicate a medical emergency.**\n\n"
            "Please **seek immediate medical attention** or **call emergency services.**"
        )
        st.session_state.messages.append({"role": "assistant", "content": emergency_message})
        with st.chat_message("assistant"):
            st.markdown(emergency_message)

    else:
        # Get AI's response
        response = get_response(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# Add footer disclaimer
st.markdown("---")
st.markdown(
    "🛑 **Disclaimer:** This chatbot does not provide medical advice, diagnosis, or treatment. "
    "Always consult a qualified healthcare provider for medical concerns.",
    unsafe_allow_html=True
)
