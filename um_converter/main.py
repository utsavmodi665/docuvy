"""import streamlit as st
from pathlib import Path
import os
from converter import convert_file

st.set_page_config(page_title="UM Converter", layout="wide")

st.title("🔄 UM Converter")

uploaded_files = st.file_uploader(
    "Upload Files",
    type=["pdf", "docx", "txt", "pptx", "jpg", "png", "jpeg"],
    accept_multiple_files=True
)

conv_type = st.selectbox("Select Conversion", [
    "To PDF",
    "PDF → DOCX",
    "PDF → TXT",
    "PDF → PPTX",
    "PDF → Image"
])

if uploaded_files and st.button("🚀 Convert"):

    progress = st.progress(0)

    for i, file in enumerate(uploaded_files):

        input_path = file.name
        with open(input_path, "wb") as f:
            f.write(file.getbuffer())

        ext = Path(input_path).suffix.lower()

        try:
            # -------- TO PDF --------
            if conv_type == "To PDF":
                if ext == ".docx":
                    ctype = "docx_to_pdf"
                    output = input_path.replace(".docx", ".pdf")
                elif ext == ".txt":
                    ctype = "txt_to_pdf"
                    output = input_path.replace(".txt", ".pdf")
                elif ext in [".jpg", ".jpeg", ".png"]:
                    ctype = "image_to_pdf"
                    output = input_path.rsplit(".",1)[0] + ".pdf"
                elif ext == ".pptx":
                    ctype = "pptx_to_pdf"
                    output = input_path.replace(".pptx", ".pdf")
                else:
                    st.error(f"{file.name}: Unsupported")
                    continue

            # -------- FROM PDF --------
            elif conv_type == "PDF → DOCX" and ext == ".pdf":
                ctype = "pdf_to_docx"
                output = input_path.replace(".pdf", ".docx")

            elif conv_type == "PDF → TXT" and ext == ".pdf":
                ctype = "pdf_to_txt"
                output = input_path.replace(".pdf", ".txt")

            elif conv_type == "PDF → PPTX" and ext == ".pdf":
                ctype = "pdf_to_pptx"
                output = input_path.replace(".pdf", ".pptx")

            elif conv_type == "PDF → Image" and ext == ".pdf":
                ctype = "pdf_to_image"
                output = input_path.replace(".pdf", ".png")

            else:
                st.error(f"{file.name}: Invalid conversion")
                continue

            result = convert_file(input_path, ctype, output)

            st.success(f"✅ Converted: {file.name}")

            # Multiple images support
            if isinstance(result, list):
                for r in result:
                    with open(r, "rb") as f:
                        st.download_button(f"Download {Path(r).name}", f, Path(r).name)
            else:
                with open(result, "rb") as f:
                    st.download_button(f"Download {Path(result).name}", f, Path(result).name)

        except Exception as e:
            st.error(f"{file.name}: {e}")

        progress.progress((i + 1) / len(uploaded_files))

st.markdown("---")
st.caption("UM Converter • FINAL WORKING VERSION 🚀")"""
import streamlit as st
from pathlib import Path
import tempfile
import os
from converter import convert_file

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Docuvy",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Inter:wght@400;500&display=swap');

html, body {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #0F172A, #020617);
    color: #F8FAFC;
}

/* Glass Header */
.glass-header {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(14px);
    border-radius: 18px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
}

/* Logo Glow */
.logo-glow {
    border-radius: 12px;
    box-shadow: 0 0 25px rgba(124,58,237,0.6),
                0 0 60px rgba(37,99,235,0.4);
    transition: all 0.3s ease;
}
.logo-glow:hover {
    transform: scale(1.05);
}

/* Gradient Title */
@keyframes gradientMove {
    0% {background-position: 0%}
    50% {background-position: 100%}
    100% {background-position: 0%}
}

.docuvy-title {
    font-family: 'Poppins';
    font-size: 48px;
    font-weight: 700;
}

.docuvy-gradient {
    background: linear-gradient(270deg, #2563EB, #7C3AED);
    background-size: 200% 200%;
    animation: gradientMove 4s ease infinite;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #2563EB, #7C3AED);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px;
    transition: 0.3s;
}
.stButton > button:hover {
    transform: translateY(-2px);
}

/* Upload */
[data-testid="stFileUploader"] {
    border: 2px dashed #64748B50;
    border-radius: 16px;
    padding: 20px;
    background: rgba(255,255,255,0.05);
}

/* Progress */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #2563EB, #7C3AED);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
col1, col2 = st.columns([1, 4])

with col1:
    if os.path.exists("logo.png"):
        st.markdown('<div class="logo-glow">', unsafe_allow_html=True)
       # st.image("logo.png")
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-header">
        <h1 class="docuvy-title docuvy-gradient">Docuvy</h1>
        <p style="color:#94A3B8;">Transform Files. Instantly.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["✨ Convert", "🔗 Merge"])

# =====================================================
# 🔄 CONVERT
# =====================================================
with tab1:

    uploaded_files = st.file_uploader(
        "📤 Drag & Drop Files",
        type=["pdf", "docx", "txt", "pptx", "jpg", "png", "jpeg"],
        accept_multiple_files=True
    )

    conv_type = st.selectbox("🎯 Conversion Type", [
        "To PDF",
        "PDF → DOCX",
        "PDF → TXT",
        "PDF → PPTX",
        "PDF → Image"
    ])

    if uploaded_files and st.button("🚀 Convert Files", use_container_width=True):

        progress = st.progress(0)

        for i, file in enumerate(uploaded_files):

            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.name).suffix) as tmp:
                tmp.write(file.getbuffer())
                input_path = tmp.name

            ext = Path(input_path).suffix.lower()

            try:
                if conv_type == "To PDF":
                    conv_map = {
                        '.docx': 'docx_to_pdf',
                        '.txt': 'txt_to_pdf',
                        '.pptx': 'pptx_to_pdf',
                        '.jpg': 'image_to_pdf',
                        '.jpeg': 'image_to_pdf',
                        '.png': 'image_to_pdf'
                    }
                    ctype = conv_map.get(ext)
                    if not ctype:
                        st.error(f"{file.name}: Unsupported")
                        continue
                    output = input_path + ".pdf"

                elif conv_type == "PDF → DOCX":
                    ctype = "pdf_to_docx"
                    output = input_path + ".docx"

                elif conv_type == "PDF → TXT":
                    ctype = "pdf_to_txt"
                    output = input_path + ".txt"

                elif conv_type == "PDF → PPTX":
                    ctype = "pdf_to_pptx"
                    output = input_path + ".pptx"

                elif conv_type == "PDF → Image":
                    ctype = "pdf_to_image"
                    output = input_path + ".png"

                result = convert_file(input_path, ctype, output)

                st.success(f"✅ {file.name} converted")

                if isinstance(result, list):
                    for r in result:
                        with open(r, "rb") as f:
                            st.download_button(f"⬇️ {Path(r).name}", f, file_name=Path(r).name)
                else:
                    with open(result, "rb") as f:
                        st.download_button(f"⬇️ Download", f, file_name=Path(result).name)

            except Exception as e:
                st.error(f"{file.name}: {e}")

            progress.progress((i + 1) / len(uploaded_files))


# =====================================================
# 🔗 MERGE
# =====================================================
with tab2:

    uploaded_files = st.file_uploader(
        "📤 Upload files to merge",
        type=["pdf", "docx", "txt", "pptx", "jpg", "png", "jpeg"],
        accept_multiple_files=True
    )

    if uploaded_files and len(uploaded_files) > 1:

        if st.button("🔗 Merge to PDF", use_container_width=True):

            with st.spinner("Merging files..."):

                paths = []

                for file in uploaded_files:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.name).suffix) as tmp:
                        tmp.write(file.getbuffer())
                        paths.append(tmp.name)

                try:
                    output = "merged_docuvy.pdf"
                    result = convert_file(paths, "merge_to_pdf", output)

                    st.success("✅ Merge completed")

                    with open(result, "rb") as f:
                        st.download_button("⬇️ Download PDF", f, file_name="docuvy_merged.pdf")

                except Exception as e:
                    st.error(str(e))

    else:
        st.info("Upload at least 2 files")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Docuvy • Fast • Clean • Smart 🚀")