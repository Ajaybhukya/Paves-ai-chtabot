import time
import smtplib
import re  # for email validation
from datetime import date
import pyttsx3
import streamlit as st
import speech_recognition as sr
import google.generativeai as ai
from PIL import Image
import cv2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

about='''
## 🏢 Company Overview
- *Name*: Paves Technologies
- *Tagline: *The Future of Financial Services is AI-First.
- *Founded*: Born in the AI era (around 2024).
- *Focus: Transforming Financial Services using **AI, Generative AI, and Agentic AI*.
- *Mission*: Empower financial institutions, their customers, and partners in a fast-evolving digital ecosystem.
- *Approach*: AI-First by design; focused on innovation, trust, scalability, and security.
- *Director and founder and ceo of paves* : Sambi eada
- ** No of Emplyoees** : 20
-** Hr of paves** :  Sai Shruthi Varala 

---

## 🧠 Core Values
- *Always Ahead of the Curve*: Staying ahead in tech trends.
- *Culture Built to Innovate*: Focus on trust, security, and innovation.
- *Human-Centric AI*: Augmenting human intelligence, not replacing it.
- *Supercharging Workforce*: AI-first training, upskilling, cross-functional expertise.
- *Customer-Centric Approach*: Long-term partnerships with customers.

---

## 🚀 Services Offered
### Industry Verticals:
- *Payments*
  - Card Issuers
  - Merchant Acquirers
  - E-commerce
  - Embedded Finance
  - Payment Gateways
  - Real-Time Payments
- *Banking*
  - Retail Banking
  - Corporate and Commercial Banking
  - Consumer Lending
  - Digital Banking
  - Open Banking
- *Payments Fraud & AML*
- *Governance, Risk & Compliance*
- *Insurance*
- *Capital Markets*

### Technology and Consulting Services:
- *Business & Technology Advisory Consulting*
- *Artificial Intelligence Solutions*
- *Cloud Engineering & DevOps*
- *Data and Analytics*
- *Product Management & Engineering*
- *Enterprise Automation*
- *Legacy Support & Modernization*
- *Cyber Security*
- *Identity and Access Management*
- *Next-Gen Technologies*

---

## 🧪 Paves AI Labs
- Special division focused on cutting-edge AI research and solutions.
- Builds intelligent systems using *Generative AI* and *Agentic AI*.

---

## 🌎 Long-Term Strategic Partnerships
- Focuses on:
  - Trust-building
  - Transparency
  - Deep understanding of client needs
  - Measurable, long-term impact
  - Future-proofing clients’ businesses

---

## 🎯 Career and Work Culture
- *Opportunities*:
  - Work on cutting-edge technologies (AI, Cloud, Data Engineering, Cybersecurity)
  - Fast-track career growth
  - Collaborate with innovative teams
- *Benefits*:
  - Competitive compensation
  - Recognition programs
  - Career advancement
- *Core Beliefs*:
  - Innovation & Sustainability
  - Inclusivity & Growth
  - Real-world impact

---

## 🛡 Key Highlights
- *AI-First IT Consulting*: Consulting through AI-driven transformation.
- *Next-Gen Tech Solutions*: AI-augmented Software Development & DevOps.
- *AI-First Outsourcing*: Intelligent automation for app development, service desks, and business processes.
- *Trust & Compliance*: Strong emphasis on cybersecurity, risk mitigation, and data protection especially in financial services.

---

## 🌐 Online Links
- *Website*: https://pavestechnologies.com/
- *LinkedIn*: https://www.linkedin.com/company/paves-technologies
- *YouTube*:https://www.youtube.com/@pavestechnologies

---

## 🔥 Special Focus
- AI-powered financial services transformation
- Embedded finance systems
- Real-time payment infrastructures
- AI for fraud detection and regulatory compliance
- Innovation across banking, fintech, capital markets, and insurance
'''

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Voice Assistant", page_icon="🎙️", layout="wide")

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
        /* Global Styles */
        .stApp {
            background-color: #f9f9f9;
        }

        .main-title {
            background: rgba(0, 0, 0, 0.7);
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            color: white;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
            margin-bottom: 20px;
            transition: all 0.5s ease-in-out;
        }

        .main-title:hover {
            background: linear-gradient(180deg, skyblue 75%, white);
            box-shadow: 0px 4px 15px rgba(255,255,255,0.8);
            transform: scale(1.05);
        }

        .button-container {
            display: flex;
            margin-bottom: 30px;
            position:relative;
            left:20px;
        }

        .stButton > button {
            background: linear-gradient(120deg, white,skyblue);
            color: black;
            border-radius: 10px;
            font-size: 20px;
            letter-spacing:1.5px;
            height: 3em;
            width: 8em;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
            transform: scale(1.05);
            background: linear-gradient(90deg, white,grey);
            color: black;
            font-size: 22px;
            
        }

        .section-header {
            color: #0072ff;
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 20px;
            text-align: center;
        }

        .uploaded-image {
            border-radius: 15px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }

        .uploaded-image:hover {
            transform: scale(1.05);
            box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
        }
        
        }
        .text-input-style input {
            border-radius: 10px;
            padding: 10px;
            font-size: 18px;
            border: 2px solid #0072ff;
            transition: all 0.3s ease;
        }

        .text-input-style input:hover {
            border-color: #00c6ff;
        }

        /* Animation for Title */
        .main-title h1 {
            animation: fadeIn 2s ease-in-out;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
    </style>
""", unsafe_allow_html=True)
# --- Title Section ---
col1, col2, col3 = st.columns([1,100,1])
with col2:
    st.markdown("<div class='main-title'><h1>🎙🤖 Welcome to Paves AI Voice Assistant</h1><span style='font-size:40px;'>Speak Naturally - I'm Listening!</span></br>"
                "<span style='font-size:20px;'>Powered Paves Technologies</span>"
                "<img src='https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHczMWtvMmVxMnV4ODZjeHk5N3Y3bXdoZTY0aXZjZWQxYXd2MGkzdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/7ug57Ley6oQS5ulqvE/giphy.gif' width='200' height='200'  style='position: absolute; top: 25px; right: 30px; border-radius: 50%; object-fit: cover; object-position: 20% 20%;'>"
                "</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# --- AI System Instruction ---
instruction = (
    "You are a friendly and intelligent voice assistant designed to help users with a wide range of topics, including general knowledge, daily tasks, technical support, and more. "
    "Always provide accurate, helpful, and easy-to-understand answers.\n"
    "1. Present responses in new lines for clarity.\n"
    "2. Avoid using jargon, or unnecessary details.\n"
    "3. Only respond to questions or requests from the user.\n"
    "4. Keep answers brief—summarize clearly in 3-5 lines only.\n"
)

# --- Google Generative AI Configuration ---
API_KEY = "AIzaSyAFaiSryKD0F5ulWOjaWGEz4Ysws7Y9xnU"
ai.configure(api_key=API_KEY)
model = ai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=instruction)

# --- Function: Speech Recognition ---
def recognize_speech():
    recognizer = sr.Recognizer()
    status_placeholder = st.empty()
    with sr.Microphone() as source:
        status_placeholder.info("🎧 Listening... Speak now")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            status_placeholder.empty()
            return recognizer.recognize_google(audio).lower()
        except (sr.UnknownValueError, sr.RequestError):
            status_placeholder.empty()
            return None

# --- Function: Text-to-Speech Output ---
def speak_response(text):
    print(text)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Female voice
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
def capture_picture():
    cap = cv2.VideoCapture(0)  # Open webcam (0 means default camera)

    if not cap.isOpened():
        st.error("❌ Cannot access the camera")
        return None

    ret, frame = cap.read()  # Capture one frame
    cap.release()

    if ret:
        img_path = "captured_image.jpg"
        cv2.imwrite(img_path, frame)
        return img_path
    else:
        st.error("❌ Failed to capture image")
        return None


def send_email(to_mail, subject, message):
    mymail = 'projectface1213@gmail.com'
    password = 'gdkb zwnh akss wpjd'  # App Password (not real Gmail password)

    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(mymail, password)
        mail_content = f"Subject: {subject}\n\n{message}"
        s.sendmail(mymail, to_mail, mail_content)
        s.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)
if "compose_email" not in st.session_state:
    st.session_state.compose_email = False

# --- Buttons Section ---
st.markdown("<div class='button-container' style='display: flex; justify-content: center; gap: 20px;'>", unsafe_allow_html=True)

col4,col1, col2, col3,col5 = st.columns([1,2, 2, 1,1])

if "show_text_input" not in st.session_state:
    st.session_state.show_text_input = False

with col1:
    if st.button("🎤 Speak", key="speak"):
        status_placeholder = st.empty()
        keep_listening = True
        while keep_listening:
            user_input = recognize_speech()
            print(user_input)
            if not user_input:
                status_placeholder.info("⚠️ Sorry, didn't catch that. Try again.")
                speak_response("Sorry, didn't catch that. Try again.")
                status_placeholder.empty()
                keep_listening = False
            elif "take picture" in user_input:
                status_placeholder.info("📸 Taking a picture...")
                speak_response("Taking a picture now.")
                img_path = capture_picture()
                col9, col10, col11 = st.columns([1, 1, 1])
                with col10:
                    if img_path:
                        status_placeholder.empty()
                        st.image(img_path, caption="Captured Image", width=600)
                    keep_listening = False  # Stop after taking picture
                time.sleep(3)
                st.rerun()
            elif "send email" or " sent email" or "sent mail" or "send mail" or "compose email" in user_input.lower():
                st.session_state.compose_email = True
            else:
                status_placeholder.info("📣 You said: " + user_input)
                try:
                    with st.spinner("🤖 Thinking..."):
                        chat = model.start_chat()
                        if "paves" in user_input.lower():
                            user_input+=f"Here some about the company{about}.Now answer based on this information and user query."
                        response = chat.send_message(user_input).text
                    status_placeholder.success(response)
                    speak_response(response)
                    status_placeholder.empty()
                except Exception as e:
                    st.error("❌ AI Error")
                    speak_response("Sorry, I encountered an error.")
                    keep_listening = False

with col2:
    if st.button("📝 Text", key="text"):
        st.session_state.show_text_input = True  # Show text input on click

with col3:
    if st.button("🚫 Stop", key="stop"):
        keep_listening = False
        engine = pyttsx3.init()
        engine.stop()
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
# --- If Text Input is Shown ---
if st.session_state.show_text_input:
    with st.container():
        st.markdown("<h2 class='section-header'>✍️ Type your Question</h2>", unsafe_allow_html=True)
        user_query = st.text_input(" ", key="text_query", label_visibility="collapsed", placeholder="Type your question here...")
        if st.button("📩 Send", key="send_button"):
            if user_query.strip() != "":
                if "take picture" in user_query.lower():
                    st.info("📸 Taking a picture...")
                    speak_response("Taking a picture now.")
                    img_path = capture_picture()
                    col6,col7,col8 = st.columns([1,1,1])
                    with col7:
                        if img_path:
                            st.image(img_path, caption="Captured Image",width=600)
                        keep_listening = False  # Stop after taking picture
                    time.sleep(3)
                    st.session_state.show_text_input = False  # Hide text input after sending
                    st.rerun()
                elif 'mail' in user_query.lower():
                    st.session_state.compose_email = True
                    st.session_state.show_text_input = False  # Hide text input after sending
                    st.rerun()

                else:
                    with st.spinner("🤖 Thinking..."):
                        chat = model.start_chat()
                        if "paves" in user_query.lower():
                            user_query += f"Here some about the company{about}. Now answer based on this information and user query."
                        response = chat.send_message(user_query).text
                    st.success(response)
                    speak_response(response)
                    st.session_state.show_text_input = False  # Hide text input after sending
                    st.rerun()
            else:
                st.warning("⚠️ Please type something!")
if st.session_state.compose_email:
    st.markdown("<h2 class='section-header'>📧 Compose Email</h2>", unsafe_allow_html=True)
    to_mail = st.text_input("To:", key="email_to", placeholder="Enter recipient email")
    subject = st.text_input("Subject:", key="email_subject", placeholder="Enter email subject")
    message = st.text_area("Message:", key="email_message", placeholder="Enter email message")

    if st.button("Send Email"):
        if is_valid_email(to_mail):
            with st.spinner("Sending Email..."):
                send_email(to_mail, subject, message)
                st.success("Email sent successfully!")
                time.sleep(2)
                st.session_state.compose_email = False
                st.session_state.show_text_input = False
                st.rerun()
        else:
            st.error("Invalid email address.")
            time.sleep(2)
            st.session_state.compose_email =True
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
# --- File Upload Section ---
st.markdown("---")
st.markdown("<h2 class='section-header'>📤 Upload Image or Text File</h2>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload an Image or Text File (.png, .jpg, .jpeg, .txt)", type=["png", "jpg", "jpeg", "txt"])

if uploaded_file:
    if uploaded_file.type.startswith("image"):
        # Handling image file
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True, output_format="auto", clamp=True)
        img = Image.open(uploaded_file)

        user_question = st.text_input("💬 Ask something about the image:")

        if st.button("🔎 Analyze Image"):
            if user_question.strip() == "":
                with st.spinner("🤖 Analyzing Image..."):
                    response = model.generate_content(["Analyze this image and describe it.", img])
                    result = response.text
                st.success(result)
                speak_response(result)
            else:
                with st.spinner("🤖 Thinking based on your question..."):
                    response = model.generate_content([user_question, img])
                    result = response.text
                st.success(result)
                speak_response(result)

    elif uploaded_file.type == "text/plain":
        # Handling text file
        content = uploaded_file.read().decode("utf-8")
        st.text_area("📜 Uploaded Text Content", content, height=200)
        if st.button("📖 Analyze Text"):
            with st.spinner("🤖 Analyzing Text..."):
                chat = model.start_chat()
                response = chat.send_message(content)
                result = response.text
            st.success(result)
            speak_response(result)