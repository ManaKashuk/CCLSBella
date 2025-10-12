
import streamlit as st
import os
import pandas as pd
from utils import staff_login, learner_login, read_leads


# ======== BEGIN: Static + CSV-Based FAQ Prompts ========
import pandas as pd
import os

# Default static questions per tab
STATIC_FAQ = {
    "Class Finder": [
        "What are your class schedules?",
        "Can I join a class mid-session?",
        "What levels do you offer?"
    ],
    "Chat": [
        "Do you offer online classes?",
        "Is Spanish hard to learn?",
        "Can Bella speak Portuguese?"
    ],
    "Book Trial": [
        "How do I book a trial class?",
        "What info do I need to provide?",
        "Can I cancel a trial booking?"
    ],
    "Learner": [
        "How do I track my progress?",
        "Can I save study notes?",
        "Where are my saved goals?"
    ],
    "Staff": [
        "How do I view leads?",
        "Can I export contact data?",
        "What does staff access allow?"
    ]
}

def load_faq():
    path = "faq_data.csv"
    if not os.path.exists(path):
        return pd.DataFrame(columns=["question", "answer", "Category"])

    df = pd.read_csv(path)

    # If not categorized, auto-add based on English keywords
    if "Category" not in df.columns:
        def categorize(q):
            q = q.lower()
            if any(w in q for w in ["schedule", "class", "join"]):
                return "Class Finder"
            elif any(w in q for w in ["online", "zoom", "chat"]):
                return "Chat"
            elif any(w in q for w in ["book", "trial", "submit"]):
                return "Book Trial"
            elif any(w in q for w in ["goal", "notes", "progress"]):
                return "Learner"
            elif any(w in q for w in ["staff", "lead", "contact"]):
                return "Staff"
            else:
                return "General"
        df["Category"] = df["question"].apply(categorize)

    return df

faq_df = load_faq()

def show_faq_suggestions(tab_category, lang="English"):
    labels = {
        "English": "💡 **Suggested questions:**",
        "Español": "💡 **Preguntas sugeridas:**",
        "Português": "💡 **Perguntas sugeridas:**"
    }
    st.markdown(labels.get(lang, "💡 **Suggested questions:**"))

    # Try to show from CSV
    matches = faq_df[faq_df["Category"] == tab_category]
    shown = False
    if not matches.empty:
        for i, row in matches.head(3).iterrows():
            if st.button(row["question"], key=f"faq_{tab_category}_{i}"):
                st.info("Bella: " + row["answer"])
                shown = True

    # If nothing found, fall back to static list
    if not shown and tab_category in STATIC_FAQ:
        for i, q in enumerate(STATIC_FAQ[tab_category]):
            if st.button(q, key=f"static_{tab_category}_{i}"):
                st.info(f"💃🏼: I'm still learning, but here's a tip about '{q}'.")
# ======== END: Static + CSV-Based FAQ Prompts ========

# Language selector
lang = st.sidebar.selectbox("🌐 Select Language", ["English", "Español", "Português"])

# Translation dictionaries
text = {
    "English": {
        "title": " 🗨️ Meet Bella: Your Spanish Class Assistant 💃🏼",
        "subtitle": "📚 Class finder, chatbot, trial booking, and progress tracking.",
        "tabs": ["Class Finder", "Chat", "Book Trial", "Learner", "Staff"],
        "class_q1": "Why Spanish?",
        "class_q2": "Class type",
        "class_q3": "When?",
        "class_q4": "Level",
        "class_btn": "Find Class",
        "chat_input": "You say:",
        "book_name": "Name",
        "book_email": "Email",
        "book_level": "Level",
        "book_schedule": "Schedule",
        "book_btn": "Submit",
        "learner_notes": "📝 Track your study notes or goals:",
        "save_btn": "Save Progress",
        "staff_msg": "Logged in as staff.",
    },
    "Español": {
        "title": "🗨️ Conoce a Bella: tu asistente de clase de español 💃🏼",
        "subtitle": "📚 Buscador de clases, chatbot, registro y seguimiento.",
        "tabs": ["Buscar Clase", "Chat", "Reservar Prueba", "Estudiante", "Staff"],
        "class_q1": "¿Por qué aprender español?",
        "class_q2": "Tipo de clase",
        "class_q3": "¿Cuándo?",
        "class_q4": "Nivel",
        "class_btn": "Buscar Clase",
        "chat_input": "Escribe algo:",
        "book_name": "Nombre",
        "book_email": "Correo electrónico",
        "book_level": "Nivel",
        "book_schedule": "Horario",
        "book_btn": "Enviar",
        "learner_notes": "📝 Anota tus metas o notas de estudio:",
        "save_btn": "Guardar progreso",
        "staff_msg": "Acceso del staff.",
    },
    "Português": {
        "title": "🗨️ Conheça Bella: sua assistente de aula de espanhol 💃🏼",
        "subtitle": "📚 Localizador de aulas, chatbot, agendamento e progresso.",
        "tabs": ["Encontrar Aula", "Chat", "Agendar Aula", "Aluno", "Equipe"],
        "class_q1": "Por que aprender espanhol?",
        "class_q2": "Tipo de aula",
        "class_q3": "Quando?",
        "class_q4": "Nível",
        "class_btn": "Buscar Aula",
        "chat_input": "Diga algo:",
        "book_name": "Nome",
        "book_email": "Email",
        "book_level": "Nível",
        "book_schedule": "Horário",
        "book_btn": "Enviar",
        "learner_notes": "📝 Anote seus objetivos de estudo:",
        "save_btn": "Salvar Progresso",
        "staff_msg": "Logado como equipe.",
    }
}[lang]

st.set_page_config(page_title=text['title'], layout="centered")
st.image("assets/logo.png", width=1000)
st.title(text['title'])
st.subheader(text['subtitle'])

tabs = st.tabs(text['tabs'])

# Class Finder
with tabs[0]:
    st.header(text['tabs'][0])
    show_faq_suggestions('Class Finder', lang)
    purpose = st.selectbox(text['class_q1'], ["Work", "Travel", "Family"])
    mode = st.radio(text['class_q2'], ["In-person", "Zoom"])
    time = st.selectbox(text['class_q3'], ["Weekdays", "Evenings", "Weekends"])
    level = st.selectbox(text['class_q4'], ["Beginner", "Intermediate", "Advanced"])
    if st.button(text['class_btn']):
        st.success("🎯 Bella suggests: Online Beginner Spanish – Tue/Thu @ 6PM")

# Chat
with tabs[1]:
    st.header(text['tabs'][1])
    show_faq_suggestions('Chat', lang)
    st.image("assets/chat.png", width=50)
    user_input = st.text_input(text['chat_input'])
    if user_input:
        if "hola" in user_input.lower() or "oi" in user_input.lower():
            st.write("💃🏼: ¡Hola! ¿Cómo estás?")
        elif "trabajo" in user_input.lower() or "trabalho" in user_input.lower():
            st.write("💃🏼: ¿Dónde trabajas?")
        else:
            st.write("💃🏼: ¡Sigue practicando!")

# Book Trial
with tabs[2]:
    st.header(text['tabs'][2])
    show_faq_suggestions('Book Trial', lang)
    with st.form("trial_form"):
        name = st.text_input(text['book_name'])
        email = st.text_input(text['book_email'])
        level = st.selectbox(text['book_level'], ["Beginner", "Intermediate", "Advanced"])
        schedule = st.selectbox(text['book_schedule'], ["Weekdays", "Evenings", "Weekends"])
        submit = st.form_submit_button(text['book_btn'])
        if submit:
            with open("bella_leads.txt", "a") as f:
                f.write(f"{name},{email},{level},{schedule}\n")
            st.success("✅ Bella saved your info!")

# Learner Portal
with tabs[3]:
    if learner_login():
        st.success("✅ " + text['tabs'][3] + " login successful.")
        notes = st.text_area(text['learner_notes'])
        if st.button(text['save_btn']):
            with open("progress.txt", "a") as f:
                f.write(notes + "\n")
            st.success("✅ Progress saved.")

# Staff Dashboard
with tabs[4]:
    if staff_login():
        st.success(text['staff_msg'])
        leads = read_leads("bella_leads.txt")
        st.dataframe(leads)
        st.download_button("Download Leads", leads.to_csv(index=False), "bella_leads.csv")

# Passwords (demo only - replace with env vars or hashed auth in production)
STAFF_PASSWORD = "staff123"
LEARNER_PASSWORD = "learner123"

def staff_login():
    st.subheader("🔐 Staff Login")
    password = st.text_input("Enter staff password:", type="password")
    if password == STAFF_PASSWORD:
        return True
    elif password:
        st.error("❌ Incorrect password")
    return False

def learner_login():
    st.subheader("🎓 Learner Login")
    password = st.text_input("Enter learner password:", type="password")
    if password == LEARNER_PASSWORD:
        return True
    elif password:
        st.error("❌ Incorrect password")
    return False

def read_leads(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path, header=None, names=["Name", "Email", "Level", "Schedule/Message"])
    return pd.DataFrame(columns=["Name", "Email", "Level", "Schedule/Message"])

# ---------- Footer ----------
st.markdown(
    """
    <hr style="margin-top:2rem; margin-bottom:0.5rem;">
    <div style="text-align:center; font-size:1rem; color:gray;">
        © 2025 CCLS Hoston | 701 N Post Oak Rd Suite 515 Houston, TX 77024 | (832) 562-0133<br>
    </div>
    """,
    unsafe_allow_html=True
)
