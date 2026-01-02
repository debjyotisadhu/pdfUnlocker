import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import io
import os

st.set_page_config(page_title="PDF Unlocker", layout="centered")

st.title("🔓 PDF Password Unlocker")

st.write("Upload a password-protected PDF and download an unlocked version.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
password = st.text_input("PDF Password", type="password")

if uploaded_file and password:
    try:
        reader = PdfReader(uploaded_file)

        if reader.is_encrypted:
            if not reader.decrypt(password):
                st.error("❌ Incorrect password. Please try again.")
            else:
                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)

                output_buffer = io.BytesIO()
                writer.write(output_buffer)
                output_buffer.seek(0)

                input_name = os.path.splitext(uploaded_file.name)[0]
                output_name = f"{input_name}_unlocked.pdf"

                st.success("✅ PDF successfully unlocked!")

                st.download_button(
                    label="📥 Download Unlocked PDF",
                    data=output_buffer,
                    file_name=output_name,
                    mime="application/pdf"
                )
        else:
            st.info("ℹ️ This PDF is not password protected.")

    except Exception as e:
        st.error(f"⚠️ Error processing PDF: {str(e)}")
