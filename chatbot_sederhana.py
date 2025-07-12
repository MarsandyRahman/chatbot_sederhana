
import random
import streamlit as st

responses = {
    "lomba": [
        "Beberapa lomba yang sering diadakan saat 17 Agustus antara lain balap karung, makan kerupuk, panjat pinang, dan tarik tambang.",
        "Lomba-lomba seperti balap karung, makan kerupuk, dan panjat pinang sangat populer di Hari Kemerdekaan Indonesia.",
    ],
    "sejarah": [
        "17 Agustus adalah hari kemerdekaan Indonesia yang diproklamasikan oleh Ir. Soekarno dan Drs. Mohammad Hatta pada tahun 1945.",
        "Pada tanggal 17 Agustus 1945, Indonesia memproklamasikan kemerdekaannya dari penjajahan.",
    ],
    "upacara": [
        "Upacara bendera biasanya dilakukan di pagi hari untuk memperingati Hari Kemerdekaan Indonesia.",
        "Upacara bendera 17 Agustus diikuti oleh berbagai kalangan, mulai dari pelajar hingga pegawai negeri.",
    ],
    "makna": [
        "Hari 17 Agustus memiliki makna penting sebagai hari kemerdekaan dan pengingat perjuangan para pahlawan.",
        "Makna 17 Agustus adalah semangat persatuan dan cinta tanah air.",
    ],
    "dekorasi": [
        "Dekorasi yang umum digunakan saat 17 Agustus adalah bendera merah putih, umbul-umbul, dan gapura.",
        "Lingkungan biasanya dihias dengan bendera dan pernak-pernik bernuansa merah putih.",
    ],
}

def chatbot_response(user_input):
    user_input = user_input.lower()
    for key in responses:
        if key in user_input:
            return random.choice(responses[key])
    return "Maaf, saya hanya bisa menjawab pertanyaan seputar kegiatan 17 Agustus seperti lomba, sejarah, upacara, makna, dan dekorasi."

st.set_page_config(page_title="Chatbot 17 Agustus", page_icon="🇮🇩")
st.title("Chatbot 17 Agustus")
st.write("Tanyakan apa saja tentang kegiatan 17 Agustus!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Anda:", "", key="input")
send = st.button("Kirim")

if send and user_input:
    response = chatbot_response(user_input)
    st.session_state.chat_history.append((user_input, response))

for q, a in st.session_state.chat_history:
    st.markdown(f"**Anda:** {q}")
    st.markdown(f"**Chatbot:** {a}")
