"""Streamlit web UI wrapper for passifypdf.

Run locally with:
    streamlit run app/streamlit_app.py
"""

import io
import tempfile
from pathlib import Path

import streamlit as st

from passifypdf.encryptpdf import encrypt_pdf


# ── Page config ────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="passifypdf — PDF Password Protector",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Title ──────────────────────────────────────────────────────────────────

st.title("🔒 passifypdf")
st.subheader("Protect your PDF files with a password — right in the browser.")
st.markdown("---")

# ── File upload ────────────────────────────────────────────────────────────

uploaded_file = st.file_uploader(
    "Upload a PDF file",
    type=["pdf"],
    help="Select the PDF you want to encrypt.",
)

# ── Password ───────────────────────────────────────────────────────────────

col1, col2 = st.columns(2)
with col1:
    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter a strong password",
        help="This password will be required to open the encrypted PDF.",
    )
with col2:
    confirm_password = st.text_input(
        "Confirm password",
        type="password",
        placeholder="Re-enter the password",
    )

# ── Output filename ────────────────────────────────────────────────────────

output_name = st.text_input(
    "Output filename",
    value="protected.pdf",
    help="Name of the encrypted file you will download.",
)
if not output_name.lower().endswith(".pdf"):
    output_name += ".pdf"

# ── Encrypt button ─────────────────────────────────────────────────────────

if st.button("🔐 Encrypt PDF", type="primary", use_container_width=True):
    if not uploaded_file:
        st.error("Please upload a PDF file first.")
    elif not password:
        st.error("Please enter a password.")
    elif password != confirm_password:
        st.error("Passwords do not match. Please try again.")
    else:
        with st.spinner("Encrypting your PDF…"):
            try:
                # Write uploaded bytes to a temp input file
                with tempfile.NamedTemporaryFile(
                    suffix=".pdf", delete=False
                ) as tmp_in:
                    tmp_in.write(uploaded_file.read())
                    tmp_in_path = Path(tmp_in.name)

                # Encrypt to a temp output file
                with tempfile.NamedTemporaryFile(
                    suffix=".pdf", delete=False
                ) as tmp_out:
                    tmp_out_path = Path(tmp_out.name)

                encrypt_pdf(tmp_in_path, tmp_out_path, password)

                # Read the encrypted bytes and offer download
                encrypted_bytes = tmp_out_path.read_bytes()

                st.success("✅ PDF encrypted successfully!")
                st.download_button(
                    label="⬇️ Download encrypted PDF",
                    data=encrypted_bytes,
                    file_name=output_name,
                    mime="application/pdf",
                    use_container_width=True,
                )

            except Exception as exc:
                st.error(f"❌ Encryption failed: {exc}")
            finally:
                # Clean up temp files
                tmp_in_path.unlink(missing_ok=True)
                tmp_out_path.unlink(missing_ok=True)

# ── Footer ─────────────────────────────────────────────────────────────────

st.markdown("---")
st.caption(
    "passifypdf — open source PDF encryption tool. "
    "[View on GitHub](https://github.com/SUPAIDEAS/passifypdf)"
)
