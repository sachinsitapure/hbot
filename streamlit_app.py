import streamlit as st
import openai

# Initialize OpenAI with secret key
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🩺 Health Symptom Checker")

# Broader health keywords
MEDICAL_KEYWORDS = [
    "headache", "fever", "cough", "cold", "flu", "pain", "throat", "burning",
    "nausea", "vomit", "diarrhea", "loose motion", "dizzy", "dizziness", 
    "fatigue", "rash", "infection", "breathing", "congestion", "sinus", 
    "stomach", "cramp", "ache", "sore", "body ache", "sick", "symptom", 
    "health", "chills", "sneeze", "runny nose", "bleeding", "allergy", "dry eyes"
]

# Emergency indicators
EMERGENCY_KEYWORDS = [
    "chest pain", "shortness of breath", "difficulty breathing", "stroke",
    "faint", "unconscious", "seizure", "sudden confusion", "heart attack",
    "numbness", "blurry vision", "can't breathe"
]

# Guardrail logic
def is_medical_query(text):
    return any(word in text.lower() for word in MEDICAL_KEYWORDS)

def is_emergency(text):
    return any(emergency in text.lower() for emergency in EMERGENCY_KEYWORDS)

# Session messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a professional AI assistant specialized in health and symptom checking. "
                "You can provide general suggestions for symptoms and minor ailments. "
                "Do not give diagnoses or emergency advice. For unrelated topics, refuse politely."
            )
        }
    ]

# Display previous messages (skip system)
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Describe your symptoms...")

def get_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message["content"]

# On user input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Emergency guard
    if is_emergency(user_input):
        warning = (
            "🚨 **These symptoms may indicate a medical emergency.**\n\n"
            "Please **seek immediate medical attention** or **call emergency services.**"
        )
        st.session_state.messages.append({"role": "assistant", "content": warning})
        with st.chat_message("assistant"):
            st.markdown(warning)

    # Off-topic guard
    elif not is_medical_query(user_input):
        note = (
            "⚠️ I'm here to assist with **health-related symptoms and concerns**.\n\n"
            "Please ask about issues like pain, fever, cold, or other medical symptoms.\n\n"
            "_For food, recipes, or non-medical questions, I cannot help._"
        )
        st.session_state.messages.append({"role": "assistant", "content": note})
        with st.chat_message("assistant"):
            st.markdown(note)

    # Valid health input
    else:
        response = get_response(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# Footer disclaimer
st.markdown("---")
st.markdown(
    "🛑 **Disclaimer:** This chatbot does not provide medical advice, diagnosis, or treatment. "
    "Always consult a qualified healthcare provider for medical concerns.",
    unsafe_allow_html=True
)
