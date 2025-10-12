
import streamlit as st
import pandas as pd
import os
from utils import staff_login, read_leads

# Language selector
lang = st.sidebar.selectbox("🌐 Select Language", ["English", "Español", "Português"])

# Translation dictionaries
text = {
    "English": {
        "title": "Ana – International Student Advisor",
        "subtitle": "🌍 Admissions, Visa Help & Application Tracking",
        "tabs": ["FAQ", "F-1 Checker", "Upload Docs", "Contact", "Student Login", "Staff"],
        "faq_q": "Your question:",
        "f1_q1": "Are you in the U.S.?",
        "f1_q2": "Current Visa",
        "f1_q3": "Studied English before?",
        "upload_name": "Your Full Name",
        "upload_file": "Upload Passport, Financial Proof, etc.",
        "contact_name": "Name",
        "contact_email": "Email",
        "contact_msg": "Message",
        "student_email": "Enter your email to login:",
        "doc_header": "📄 Your Uploaded Documents",
        "upload_more": "Upload more documents",
        "app_status": "📊 Your Application Status",
        "staff_login": "Logged in as staff.",
        "student_portal": "Future Student Portal",
        "faq_response": "Ana: Great question! A staff member will follow up with details."
    },
    "Español": {
        "title": "Ana – Asesora Internacional",
        "subtitle": "🌍 Admisiones, Visa y Seguimiento",
        "tabs": ["Preguntas", "Elegibilidad F-1", "Subir Documentos", "Contacto", "Portal del Estudiante", "Staff"],
        "faq_q": "Tu pregunta:",
        "f1_q1": "¿Estás en EE.UU.?",
        "f1_q2": "Tipo de visa actual",
        "f1_q3": "¿Has estudiado inglés antes?",
        "upload_name": "Tu Nombre Completo",
        "upload_file": "Sube pasaporte, prueba financiera, etc.",
        "contact_name": "Nombre",
        "contact_email": "Correo Electrónico",
        "contact_msg": "Mensaje",
        "student_email": "Ingresa tu correo para acceder:",
        "doc_header": "📄 Tus Documentos Subidos",
        "upload_more": "Sube más documentos",
        "app_status": "📊 Estado de tu Aplicación",
        "staff_login": "Acceso del staff.",
        "student_portal": "Portal del Estudiante",
        "faq_response": "Ana: ¡Buena pregunta! Alguien del equipo te responderá pronto."
    },
    "Português": {
        "title": "Ana – Consultora Internacional",
        "subtitle": "🌍 Admissão, Visto e Acompanhamento",
        "tabs": ["Perguntas", "Verificação F-1", "Enviar Documentos", "Contato", "Portal do Aluno", "Equipe"],
        "faq_q": "Sua pergunta:",
        "f1_q1": "Você está nos EUA?",
        "f1_q2": "Tipo de visto atual",
        "f1_q3": "Já estudou inglês antes?",
        "upload_name": "Seu Nome Completo",
        "upload_file": "Envie passaporte, comprovante financeiro, etc.",
        "contact_name": "Nome",
        "contact_email": "Email",
        "contact_msg": "Mensagem",
        "student_email": "Digite seu email para acessar:",
        "doc_header": "📄 Seus Documentos Enviados",
        "upload_more": "Enviar mais documentos",
        "app_status": "📊 Status da Sua Inscrição",
        "staff_login": "Logado como equipe.",
        "student_portal": "Portal do Aluno",
        "faq_response": "Ana: Boa pergunta! Alguém da equipe entrará em contato."
    }
}[lang]

# Page setup
st.set_page_config(page_title=text['title'], layout="centered")
st.image("assets/logo.png", width=200)
st.title(text['title'])
st.subheader(text['subtitle'])

tabs = st.tabs(text['tabs'])

# FAQ Tab
with tabs[0]:
    st.header(text['tabs'][0])
    st.image("assets/chat.png", width=50)
    query = st.text_input(text['faq_q'])
    if query:
        st.write(text['faq_response'])

# F1 Checker
with tabs[1]:
    st.header(text['tabs'][1])
    in_us = st.radio(text['f1_q1'], ["Yes", "No"] if lang == "English" else ["Sí", "No"] if lang == "Español" else ["Sim", "Não"])
    visa = st.selectbox(text['f1_q2'], ["None", "Tourist", "F-1", "Other"])
    studied = st.radio(text['f1_q3'], ["Yes", "No"] if lang == "English" else ["Sí", "No"] if lang == "Español" else ["Sim", "Não"])
    if st.button("Check" if lang == "English" else "Verificar"):
        if in_us == "No" or visa == "None":
            st.success("✅ Likely eligible! Start with a placement test.")
        elif visa == "Tourist" and studied == "No":
            st.info("⚠️ May need to change status before studying.")
        else:
            st.warning("❌ You may not be eligible without a visa change.")

# Upload Docs
with tabs[2]:
    st.header(text['tabs'][2])
    name = st.text_input(text['upload_name'])
    doc = st.file_uploader(text['upload_file'], type=["pdf", "jpg", "png"])
    if doc and name:
        path = f"uploads/{name.replace(' ', '_')}_{doc.name}"
        with open(path, "wb") as f:
            f.write(doc.read())
        st.success("✅ Uploaded successfully.")

# Contact Form
with tabs[3]:
    st.header(text['tabs'][3])
    with st.form("contact"):
        name = st.text_input(text['contact_name'])
        email = st.text_input(text['contact_email'])
        msg = st.text_area(text['contact_msg'])
        if st.form_submit_button("Send" if lang == "English" else "Enviar"):
            with open("ana_leads.txt", "a") as f:
                f.write(f"{name},{email},{msg}\n")
            st.success("✅ Sent!")

# Student Login
with tabs[4]:
    st.header(text['student_portal'])
    student_email = st.text_input(text['student_email'])
    if student_email:
        st.success(f"📂 Logged in as {student_email}")
        doc_folder = "uploads/"
        uploaded = [f for f in os.listdir(doc_folder) if f.startswith(student_email.replace("@", "_"))]
        st.subheader(text['doc_header'])
        if uploaded:
            for f in uploaded:
                st.markdown(f"- {f}")
        else:
            st.info("No uploads found.")
        new_doc = st.file_uploader(text['upload_more'], type=["pdf", "jpg", "png"])
        if new_doc:
            save_path = f"{doc_folder}/{student_email.replace('@', '_')}_{new_doc.name}"
            with open(save_path, "wb") as f:
                f.write(new_doc.read())
            st.success("✅ Uploaded.")
        st.subheader(text['app_status'])
        if os.path.exists("student_status.csv"):
            df = pd.read_csv("student_status.csv")
            row = df[df.email == student_email]
            if not row.empty:
                st.markdown(f"**Status:** {row.iloc[0]['status']}")
                st.markdown(f"**Next Step:** {row.iloc[0]['next_step']}")
            else:
                st.info("No status found.")

# Staff Login
with tabs[5]:
    if staff_login():
        st.success(text['staff_login'])
        leads = read_leads("ana_leads.txt")
        st.dataframe(leads)
        st.download_button("Download Leads", leads.to_csv(index=False), "ana_leads.csv")
