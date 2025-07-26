import streamlit as st
import openai

# Initialize OpenAI with your secret API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set the app title
st.title("🩺 Health Symptom Checker")

# Guardrail: keywords to detect medical relevance
MEDICAL_KEYWORDS = [
    "headache", "fever", "cough", "pain", "sick", "nausea", "vomit", "dizzy",
    "symptom", "rash", "breathing", "chest", "fatigue", "infection", "cold", "flu"
]

EMERGENCY_KEYWORDS = [
    "chest pain", "difficulty breathing", "shortness of breath", 
    "sudden confusion", "unconscious", "faint", "stroke", "heart attack"
]

# Guardrail check functions
def is_medical_query(text):
    return any(keyword in text.lower() for keyword in MEDICAL_KEYWORDS)

def is_emergency(text):
    return any(phrase in text.lower() for phrase in EMERGENCY_KEYWORDS)

# Initialize chat history with a system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a professional AI assistant specialized in health and symptom checking. "
                "Your role is to help users understand their symptoms and suggest possible common causes "
                "based on the information they provide. You must clearly state that you are not a doctor, "
                "and you do not provide medical diagnoses or emergency advice. "
                "If a user asks about anything unrelated to health or symptoms, reply: "
                "'I'm here to help with health-related questions and symptom checking. "
                "Please ask about symptoms, conditions, or health concerns.' "
                "If a user describes emergency symptoms like chest pain, difficulty breathing, or sudden confusion, respond: "
                "'These symptoms may indicate a medical emergency. Please seek immediate medical attention or call emergency services.'"
            )
        }
    ]

# Display all previous messages (excluding system)
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Describe your symptoms...")

# Function to get OpenAI GPT response
def get_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message["content"]

# Handle input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Emergency handling
    if is_emergency(user_input):
        warning = (
            "🚨 **These symptoms may indicate a medical emergency.**\n\n"
            "Please **seek immediate medical attention** or **call emergency services.**"
        )
        st.session_state.messages.append({"role": "assistant", "content": warning})
        with st.chat_message("assistant"):
            st.markdown(warning)

    # Non-medical filtering
    elif not is_medical_query(user_input):
        note = (
            "🧠 I'm here to help with **health-related questions and symptom checking**.\n\n"
            "Please ask about **symptoms, conditions, or health concerns**."
        )
        st.session_state.messages.append({"role": "assistant", "content": note})
        with st.chat_message("assistant"):
            st.markdown(note)

    # Valid health-related input
    else:
        response = get_response(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# Disclaimer
st.markdown("---")
st.markdown(
    "🛑 **Disclaimer:** This chatbot does not provide medical advice, diagnosis, or treatment. "
    "Always consult a qualified healthcare provider for medical concerns.",
    unsafe_allow_html=True
)
