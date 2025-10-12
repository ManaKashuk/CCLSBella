
import streamlit as st
import os
import pandas as pd
from utils import staff_login, learner_login, read_leads

# Language selector
lang = st.sidebar.selectbox("🌐 Select Language", ["English", "Español", "Português"])

# Translation dictionaries
text = {
    "English": {
        "title": "Bella – Spanish Class Assistant",
        "subtitle": "🧭 Class finder, chatbot, trial booking, and progress tracking.",
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
        "title": "Bella – Asistente de Clases de Español",
        "subtitle": "🧭 Buscador de clases, chatbot, registro y seguimiento.",
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
        "title": "Bella – Assistente de Aulas de Espanhol",
        "subtitle": "🧭 Localizador de aulas, chatbot, agendamento e progresso.",
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
st.image("assets/logo.png", width=200)
st.title(text['title'])
st.subheader(text['subtitle'])

tabs = st.tabs(text['tabs'])

# Class Finder
with tabs[0]:
    st.header(text['tabs'][0])
    purpose = st.selectbox(text['class_q1'], ["Work", "Travel", "Family"])
    mode = st.radio(text['class_q2'], ["In-person", "Zoom"])
    time = st.selectbox(text['class_q3'], ["Weekdays", "Evenings", "Weekends"])
    level = st.selectbox(text['class_q4'], ["Beginner", "Intermediate", "Advanced"])
    if st.button(text['class_btn']):
        st.success("🎯 Bella suggests: Online Beginner Spanish – Tue/Thu @ 6PM")

# Chat
with tabs[1]:
    st.header(text['tabs'][1])
    st.image("assets/chat.png", width=50)
    user_input = st.text_input(text['chat_input'])
    if user_input:
        if "hola" in user_input.lower() or "oi" in user_input.lower():
            st.write("Bella: ¡Hola! ¿Cómo estás?")
        elif "trabajo" in user_input.lower() or "trabalho" in user_input.lower():
            st.write("Bella: ¿Dónde trabajas?")
        else:
            st.write("Bella: ¡Sigue practicando!")

# Book Trial
with tabs[2]:
    st.header(text['tabs'][2])
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
