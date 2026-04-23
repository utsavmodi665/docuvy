import streamlit as st
from pathlib import Path
import tempfile
import os
import json
import uuid
from concurrent.futures import ThreadPoolExecutor
from converter import convert_file
from auth import login, signup

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "is_pro" not in st.session_state:
    st.session_state.is_pro = False

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Docuvy", layout="wide")

# ---------------- HISTORY ----------------
HISTORY_FILE = "history.json"

def save_history(user, filename):
    data = {}
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)

    if user not in data:
        data[user] = []

    data[user].append(filename)

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_history(user):
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        data = json.load(f)
    return data.get(user, [])

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.markdown("## 🔐 Account")

    if not st.session_state.logged_in:

        option = st.radio("Select", ["Login", "Signup"])

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        # ---------------- FORGOT PASSWORD UI ----------------
        if option == "Login":
            show_reset = st.checkbox("🔑 Forgot Password?")

            if show_reset:
                reset_email = st.text_input("Enter email for reset")

                if st.button("Send Reset Link"):
                    if reset_email:
                        from auth import forgot_password
                        with st.spinner("Sending reset email..."):
                            result = forgot_password(reset_email)

                        if result["success"]:
                            st.success(result["message"])
                        else:
                            st.error(result["message"])
                    else:
                        st.warning("Please enter email")

        # ---------------- LOGIN / SIGNUP ----------------
        if st.button("Continue"):

            from auth import signup, login

            result = signup(email, password) if option == "Signup" else login(email, password)

            if result["success"]:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success(result["message"])
                st.rerun()
            else:
                st.error(result["message"])

    else:
        st.success(f"✅ {st.session_state.user_email}")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.session_state.is_pro = False
            st.rerun()

        st.markdown("### 💎 Upgrade")

        if not st.session_state.is_pro:
            if st.button("🚀 Upgrade to Pro"):
                st.session_state.is_pro = True
                st.success("Pro Activated ⚡")
        else:
            st.success("💎 Pro User")

# ---------------- HEADER ----------------
col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo.png")
with col2:
    st.title("Docuvy")
    st.caption("Transform Files Instantly")

if st.session_state.is_pro:
    st.success("💎 Pro Mode Enabled")
elif st.session_state.logged_in:
    st.info("Logged in • Upgrade for Pro features")
else:
    st.info("🆓 Free Mode")

st.divider()

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["✨ Convert", "🔗 Merge", "📜 History"])

# =====================================================
# 🔄 CONVERT
# =====================================================
with tab1:

    files = st.file_uploader(
        "Upload Files",
        type=["pdf","docx","txt","pptx","jpg","png","jpeg"],
        accept_multiple_files=True
    )

    conv_type = st.selectbox("Conversion Type", [
        "To PDF",
        "PDF → DOCX",
        "PDF → TXT",
        "PDF → PPTX",
        "PDF → Image"
    ])

    fast_mode = False
    if st.session_state.is_pro:
        fast_mode = st.toggle("⚡ Fast Mode (Pro)", value=True)
    else:
        st.caption("⚡ Fast Mode available in Pro")

    if not st.session_state.logged_in and files:
        if len(files) > 2:
            st.warning("Free users can convert only 2 files")
            files = files[:2]

    def process_file(file):

        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.name).suffix) as tmp:
            tmp.write(file.getbuffer())
            input_path = tmp.name

        ext = Path(input_path).suffix.lower()

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
                return None, f"{file.name}: Unsupported"
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

        try:
            result = convert_file(input_path, ctype, output)
            return result, None
        except Exception as e:
            return None, str(e)

    if files and st.button("🚀 Convert"):

        results = []
        if fast_mode:
            with ThreadPoolExecutor() as executor:
                results = list(executor.map(process_file, files))
        else:
            results = [process_file(f) for f in files]

        for i, (file, (result, error)) in enumerate(zip(files, results)):

            if error:
                st.error(error)
                continue

            st.success(f"✅ {file.name} converted")

            if st.session_state.logged_in:
                save_history(st.session_state.user_email, file.name)
                st.info("☁️ Saved to cloud")

            # DOWNLOAD FIX (UNIQUE KEYS)
            if isinstance(result, list):
                for j, r in enumerate(result):
                    with open(r, "rb") as f:
                        st.download_button(
                            label=f"⬇️ {Path(r).name}",
                            data=f,
                            file_name=Path(r).name,
                            key=f"download_{i}_{j}_{uuid.uuid4()}"
                        )
            else:
                with open(result, "rb") as f:
                    st.download_button(
                        label="⬇️ Download",
                        data=f,
                        file_name=Path(result).name,
                        key=f"download_{i}_{uuid.uuid4()}"
                    )

# =====================================================
# 🔗 MERGE
# =====================================================
with tab2:

    files = st.file_uploader(
        "Upload files to merge",
        type=["pdf","docx","txt","pptx","jpg","png","jpeg"],
        accept_multiple_files=True
    )

    if not st.session_state.logged_in and files:
        if len(files) > 3:
            st.warning("Free users max 3 files")
            files = files[:3]

    if files and len(files) > 1:

        if st.button("🔗 Merge to PDF"):

            with st.spinner("Merging..."):

                paths = []
                for file in files:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.name).suffix) as tmp:
                        tmp.write(file.getbuffer())
                        paths.append(tmp.name)

                try:
                    output = "merged_docuvy.pdf"
                    result = convert_file(paths, "merge_to_pdf", output)

                    st.success("✅ Merge complete")

                    if st.session_state.logged_in:
                        save_history(st.session_state.user_email, "Merged PDF")

                    with open(result, "rb") as f:
                        st.download_button(
                            "⬇️ Download PDF",
                            f,
                            file_name="docuvy_merged.pdf",
                            key=f"merge_{uuid.uuid4()}"
                        )

                except Exception as e:
                    st.error(str(e))

    else:
        st.info("Upload at least 2 files")

# =====================================================
# 📜 HISTORY
# =====================================================
with tab3:

    if not st.session_state.logged_in:
        st.warning("Login to view history")
    else:
        history = get_history(st.session_state.user_email)

        if not history:
            st.info("No history yet")
        else:
            for item in reversed(history):
                st.write("📄", item)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Docuvy • Fast • Clean • Smart 🚀")