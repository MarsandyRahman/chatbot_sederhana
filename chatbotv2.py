
import streamlit as st
import google.generativeai as genai
import PyPDF2
import docx
import openpyxl

API_KEY = "AIzaSyACp3kIp5xBecvU0L0mbnRmeqvMltpezdY"
genai.configure(api_key=API_KEY)

def read_txt(file):
    return file.read().decode("utf-8")

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def read_xlsx(file):
    wb = openpyxl.load_workbook(file)
    text = ""
    for sheet in wb.worksheets:
        for row in sheet.iter_rows(values_only=True):
            text += "\t".join([str(cell) if cell else "" for cell in row]) + "\n"
    return text

def extract_text(uploaded_file):
    if uploaded_file is None:
        return ""
    if uploaded_file.type == "text/plain":
        return read_txt(uploaded_file)
    elif uploaded_file.type == "application/pdf":
        return read_pdf(uploaded_file)
    elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
        return read_docx(uploaded_file)
    elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        return read_xlsx(uploaded_file)
    else:
        return "Format file tidak didukung."



# Model yang digunakan: Gemini 2.5 Flash (nama API: gemini-1.5-flash)
MODEL_NAME = "gemini-1.5-flash"

def gemini_answer(question, context):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"Jawablah pertanyaan berikut hanya berdasarkan informasi dari file yang di-upload.\n\nKonteks:\n{context}\n\nPertanyaan:\n{question}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Terjadi error: {e}"


st.set_page_config(page_title="Chatbot Gemini Berbasis File", page_icon="🤖")
st.title("Chatbot Gemini Berbasis File")
st.write("Upload file (.txt, .pdf, .docx, .xlsx) sebagai konteks. Chatbot hanya akan menjawab berdasarkan isi file yang di-upload.")


# Bantuan dengan expander di pojok kanan bawah
help_css = """
<style>
.floating-help {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
  width: 340px;
}
</style>
"""
st.markdown(help_css, unsafe_allow_html=True)


# Expander bantuan di pojok kanan bawah tanpa container
st.markdown("""
<div class="floating-help">
    <details>
        <summary style="font-size:16px; background:#ff4b4b; color:white; border-radius:50px; padding:12px 24px; cursor:pointer;">❓ Bantuan</summary>
        <div style="background:white; color:#222; border-radius:12px; box-shadow:0 2px 16px rgba(0,0,0,0.18); padding:20px; margin-top:10px;">
            <b>Cara Memakai Chatbot:</b><br><br>
            1. Upload file (.txt, .pdf, .docx, .xlsx) yang berisi informasi yang ingin dijadikan konteks.<br>
            2. Setelah file berhasil dibaca, masukkan pertanyaan Anda pada kolom yang tersedia.<br>
            3. Tekan Enter untuk mengirim pertanyaan.<br>
            4. Jawaban akan muncul di bawah kolom pertanyaan, berdasarkan isi file yang di-upload.<br><br>
            <i>Catatan: Chatbot hanya menjawab berdasarkan isi file yang di-upload.</i>
        </div>
    </details>
</div>
""", unsafe_allow_html=True)



uploaded_file = st.file_uploader("Upload file", type=["txt", "pdf", "docx", "xlsx"])
context = ""
if uploaded_file:
    context = extract_text(uploaded_file)
    st.session_state["context"] = context
    st.success("File berhasil dibaca!")
else:
    context = st.session_state.get("context", "")


question = st.text_input("Pertanyaan Anda:", on_change=None)

if question:
    if not context:
        st.warning("Silakan upload file terlebih dahulu.")
    else:
        with st.spinner("Memproses jawaban..."):
            answer = gemini_answer(question, context)
        st.markdown(f"**Jawaban:** {answer}")
