import html
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from google import genai
from google.genai import types
import streamlit as st 
from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE_TEMPLATE,SUMMARY_REQUEST_PROMPT

gemini_api_key = st.secrets["GEMINI_API_KEY"]
gmail_address = st.secrets["GMAIL_ADDRESS"]
gmail_app_password = st.secrets["GMAIL_APP_PASSWORD"]

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key = gemini_api_key)



gemini_client = get_gemini_client()
model_name = "gemini-3.6-flash"

# ---------------- UI styling ----------------
CUSTOM_CSS = """
<style>
/* hide default Streamlit menu/footer (keep header so sidebar toggle works) */
#MainMenu, footer {visibility: hidden;}

.block-container {padding-top: 4.5rem; padding-bottom: 6rem; max-width: 820px;}

/* consistent vertical rhythm between elements */
[data-testid="stVerticalBlock"] {gap: 0.9rem;}
[data-testid="stHorizontalBlock"] {gap: 0.8rem;}
[data-testid="stAlert"] {border-radius: 12px; margin: 0.2rem 0 0.6rem 0;}

/* ---- hero banner (onboarding) ---- */
.hero {
    background: linear-gradient(135deg, #1b5e20 0%, #43a047 60%, #81c784 100%);
    border-radius: 20px;
    padding: 2.2rem 1.5rem;
    text-align: center;
    color: #ffffff;
    margin-bottom: 1.2rem;
    box-shadow: 0 8px 24px rgba(46, 125, 50, 0.25);
}
.hero h1 {color: #ffffff; margin: 0; font-size: 2.4rem; padding: 0;}
.hero p  {color: rgba(255,255,255,0.92); margin: 0.5rem 0 0 0; font-size: 1.05rem;}

/* ---- feature cards (onboarding) ---- */
.feature-card {
    background: rgba(46, 125, 50, 0.08);
    border: 1px solid rgba(46, 125, 50, 0.25);
    border-radius: 16px;
    padding: 1.1rem 0.8rem;
    text-align: center;
    height: 100%;
    box-sizing: border-box;
}
.feature-card .icon  {font-size: 1.9rem;}
.feature-card .title {font-weight: 700; margin-top: 0.3rem;}
.feature-card .desc  {font-size: 0.85rem; opacity: 0.8; margin-top: 0.2rem;}

/* ---- onboarding form ---- */
[data-testid="stForm"] {
    border: 1px solid rgba(46, 125, 50, 0.3);
    border-radius: 18px;
    padding: 1.6rem 1.4rem 1.4rem 1.4rem;
    background: rgba(46, 125, 50, 0.04);
    margin-top: 0.6rem;
}
[data-testid="stForm"] h3 {margin: 0 0 0.4rem 0; padding: 0;}
[data-testid="stForm"] [data-testid="stFormSubmitButton"] {margin-top: 0.6rem;}

/* ---- main app header ---- */
.app-title {
    font-size: 2.1rem;
    font-weight: 800;
    background: linear-gradient(90deg, #43a047, #81c784);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}
.user-pill {
    display: inline-block;
    background: rgba(46, 125, 50, 0.12);
    border: 1px solid rgba(46, 125, 50, 0.3);
    border-radius: 999px;
    padding: 0.25rem 0.9rem;
    font-size: 0.82rem;
    margin: 0 0 0.4rem 0;
}

/* ---- buttons ---- */
.stButton > button, [data-testid="stFormSubmitButton"] > button {
    border-radius: 12px;
    font-weight: 600;
    min-height: 2.8rem;
    padding: 0.5rem 1rem;
    white-space: nowrap;
    transition: all 0.15s ease-in-out;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(46, 125, 50, 0.25);
}
button[kind="primary"],
button[data-testid="stBaseButton-primary"],
button[data-testid="stBaseButton-primaryFormSubmit"] {
    background-color: #2e7d32 !important;
    border-color: #2e7d32 !important;
    color: #ffffff !important;
}
button[kind="primary"]:hover,
button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
    background-color: #1b5e20 !important;
    border-color: #1b5e20 !important;
}

/* ---- chat bubbles ---- */
[data-testid="stChatMessage"] {
    border-radius: 16px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.4rem;
    background: rgba(46, 125, 50, 0.07);
    border: 1px solid rgba(46, 125, 50, 0.15);
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: rgba(100, 150, 200, 0.10);
    border: 1px solid rgba(100, 150, 200, 0.25);
}
[data-testid="stChatMessage"] img {border-radius: 12px;}

/* ---- chat input ---- */
[data-testid="stChatInput"] {border-radius: 16px;}

/* ---- sidebar ---- */
[data-testid="stSidebar"] {border-right: 1px solid rgba(46, 125, 50, 0.2);}
.side-brand {font-size: 1.4rem; font-weight: 800; color: #4caf50;}
.side-brand {margin-top: -0.5rem;}
[data-testid="stSidebarUserContent"] {padding-top: 1rem;}
[data-testid="stExpander"] li {font-size: 0.92rem; line-height: 1.5;}
.side-tagline {font-size: 0.8rem; opacity: 0.7; margin: 0 0 0.6rem 0;}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {gap: 0.7rem;}
[data-testid="stExpander"] {border-radius: 12px; margin-top: 0.2rem;}
[data-testid="stExpander"] ul {margin-bottom: 0; padding-left: 1.2rem;}
.user-card {
    display: flex; align-items: center; gap: 0.7rem;
    background: rgba(46, 125, 50, 0.1);
    border: 1px solid rgba(46, 125, 50, 0.25);
    border-radius: 14px;
    padding: 0.7rem 0.8rem;
    margin-bottom: 0.2rem;
}
.avatar {
    width: 42px; height: 42px; min-width: 42px;
    border-radius: 50%;
    background: linear-gradient(135deg, #2e7d32, #81c784);
    color: #ffffff; font-weight: 700; font-size: 1.1rem;
    display: flex; align-items: center; justify-content: center;
}
.user-info {overflow: hidden;}
.user-name  {font-weight: 700; line-height: 1.2;}
.user-email {font-size: 0.78rem; opacity: 0.75; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;}
</style>
"""

def hero(title, subtitle):
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True
    )

def feature_card(icon, title, desc):
    return (
        f'<div class="feature-card"><div class="icon">{icon}</div>'
        f'<div class="title">{title}</div><div class="desc">{desc}</div></div>'
    )

def build_email_body(name, summary):
    line = "─" * 32
    return (
        f"Hello {name},\n\n"
        "Thank you for using Plant Doctor AI! 🌱\n"
        "Here is the summary of your plant diagnosis.\n\n"
        f"{line}\n\n"
        f"{summary}\n\n"
        f"{line}\n\n"
        "⚠️ Please note: This report is generated by AI from the photos you shared. "
        "It is a helpful guide, not a final verdict. For serious or fast-spreading "
        "problems, please also consult a local agriculture expert or nursery. "
        "When using any pesticide or fertilizer, always follow the product label.\n\n"
        "Wishing you and your plants good health,\n"
        "Plant Doctor AI 🌿"
    )

def send_email(to_address, subject, body):
    try:
        message = MIMEText(body, "plain", "utf-8")
        message["Subject"] = Header(subject, "utf-8")
        message["From"] = gmail_address
        message["To"] = to_address

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_address, gmail_app_password)
            server.send_message(message)

        return True, "Email sent successfully"

    except Exception as e:
        return False, str(e)

def format_response(response):
    if not response:
        return "Sorry, I couldn't analyze that image. Please try again with a clearer photo. 🌿"
    return response.strip()

def render_message(message):
    avatar = "🌱" if message["role"] == "assistant" else "🧑‍🌾"
    with st.chat_message(message["role"], avatar=avatar):
        if message["kind"] == "text":
            st.write(message["content"])
        elif message["kind"] == "image":
            st.image(message["content"], width=320)

def add_message(role, kind, content):
    st.session_state.messages.append({"role": role, "kind": kind, "content": content})
    render_message(st.session_state.messages[-1])

def ask_gemini(parts):
    try:
        response = st.session_state.chat.send_message(parts)   
        if not response or not response.text:
            return (
                "I couldn't make out the image clearly. 📷 "
                "Please upload a clearer, well-lit photo of the plant and try again."
            )
        return response.text
    except Exception as error:
        print(error)
        return None

st.set_page_config(
    page_title="Plant Doctor AI",
    page_icon="🌱",
    layout="centered"
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

#step 1 --> Onboarding 
if "onboarded" not in st.session_state:
    hero("🌱 Plant Doctor AI", "Upload a plant image. Get an AI diagnosis. Receive the report by email.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(feature_card("📸", "Upload", "Snap or upload a photo of your plant"), unsafe_allow_html=True)
    with c2:
        st.markdown(feature_card("🔬", "Diagnose", "AI checks for disease, pests & deficiencies"), unsafe_allow_html=True)
    with c3:
        st.markdown(feature_card("📧", "Get Report", "Receive the full report in your inbox"), unsafe_allow_html=True)

    with st.form("onboarding_form"):
        st.subheader("👋 Let's get started")
        name = st.text_input("Your name")
        email = st.text_input(
            "Email Address",
            placeholder="example@gmail.com",
            help="This is the email where Plant Doctor AI will send your report"
        )
        submitted = st.form_submit_button("Get Started 🚀", type="primary", use_container_width=True)
    if submitted:
        if not name.strip() or not email.strip():
            st.warning("Please Fill the details")
        else:
            st.session_state.name = name.strip()
            st.session_state.email = email.strip()
            #activate gemini
            st.session_state.chat = gemini_client.chats.create(
                model=model_name,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
            )
            st.session_state.messages = []
            st.session_state.summary_response = None
            st.session_state.has_analysis = False
            st.session_state.onboarded = True
            st.rerun()
    st.stop()

safe_name = html.escape(st.session_state.name)
safe_email = html.escape(st.session_state.email)

with st.sidebar:
    st.markdown('<div class="side-brand">🌱 Plant Doctor AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-tagline">AI Powered Plant Diagnosis</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="user-card"><div class="avatar">{safe_name[:1].upper()}</div>'
        f'<div class="user-info"><div class="user-name">{safe_name}</div>'
        f'<div class="user-email">{safe_email}</div></div></div>',
        unsafe_allow_html=True
    )
    if st.button("🗑️ Clear Chat", use_container_width=True):
        # start a fresh Gemini chat and wipe the saved messages/report
        st.session_state.chat = gemini_client.chats.create(
            model=model_name,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
        )
        st.session_state.messages = []
        st.session_state.summary_response = None
        st.session_state.has_analysis = False
        st.rerun()
    with st.expander("📸 Image Tips", expanded=True):
        st.markdown("""
        - 🌿 Capture the affected leaf.
        - ☀️ Use natural daylight.
        - 📷 Avoid blurry images.
        - 🍃 Keep one plant in focus.
        """)
    with st.expander("✅ Supported"):
        st.markdown("""
        - Leaves
        - Flowers
        - Fruits
        - Vegetables
        - Crops
        - Indoor Plants
        """)
    st.caption("Plant Doctor AI v1.0")

#Chat interface
header_col, button_col = st.columns([5, 2], vertical_alignment="center")
with header_col:
    st.markdown('<div class="app-title">🌱 Plant Doctor AI</div>', unsafe_allow_html=True)
with button_col:
    # enabled only after the first diagnosis
    send_disabled = not st.session_state.has_analysis
    send_clicked = st.button("📤 Send Report", disabled=send_disabled, type="primary", use_container_width=True)

st.markdown(
    f'<div class="user-pill">👤 {safe_name} &nbsp;•&nbsp; 📧 Reports go to {safe_email}</div>',
    unsafe_allow_html=True
)

# handled outside the columns so the messages use the full page width
if send_clicked:
    # generate the summary from the chat, then email it
    with st.spinner("Preparing your report..."):
        summary = ask_gemini([SUMMARY_REQUEST_PROMPT])

    if summary:
        st.session_state.summary_response = format_response(summary)
        success, info = send_email(
            st.session_state.email,
            "🌱 Your Plant Doctor AI Report",
            build_email_body(st.session_state.name, st.session_state.summary_response)
        )

        if success:
            st.success("📧 Report sent! Please check your inbox (and spam folder, just in case).")
        else:
            st.error("😕 We couldn't send the email right now. Please try again in a little while.")
    else:
        st.error("😕 We couldn't prepare your report right now. Please try again in a little while.")

if not st.session_state.messages:
    add_message("assistant", "text", WELCOME_MESSAGE_TEMPLATE.format(name=st.session_state.name))
else:
    for message in st.session_state.messages:
        render_message(message)

user_input = st.chat_input(
    "Ask a question or upload a plant image...",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)

if user_input:
    
    photo = user_input.files[0] if user_input.files else None
    text = user_input.text
    parts = []

    if photo is not None:
        photo_bytes = photo.getvalue()
        add_message("user", "image", photo_bytes)
        parts.append(types.Part.from_bytes(data=photo_bytes, mime_type=photo.type))
    if text:
        add_message("user", "text", text)
        parts.append(text)
    elif photo is not None:
        parts.append(
            "Please analyze this plant image using your standard diagnosis format. "
            "If the image is unclear, ask me for a better photo instead of guessing."
        )

    with st.spinner("Analyzing the plant...."):
        answer = ask_gemini(parts)

        if answer:
            formatted_answer = format_response(answer)
            add_message("assistant", "text", formatted_answer)

            # first successful reply -> refresh so Send Report becomes enabled
            if not st.session_state.has_analysis:
                st.session_state.has_analysis = True
                st.rerun()

        else:
            st.warning(
                "🌧️ Plant Doctor AI is taking a short break. Please try again in a few moments."
            )