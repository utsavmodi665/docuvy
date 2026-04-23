import os
import tempfile
import zipfile
import mimetypes
from pathlib import Path
import streamlit as st

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def validate_file(uploaded_file):
    '''Validate file size and type.'''
    if uploaded_file.size > MAX_FILE_SIZE:
        return False, f"File too large: {uploaded_file.size / (1024*1024):.1f}MB > 50MB"
    mime_type, _ = mimetypes.guess_type(uploaded_file.name)
    allowed_types = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                     'text/plain', 'image/jpeg', 'image/png', 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
    if mime_type not in allowed_types:
        return False, f"Unsupported type: {uploaded_file.name}"
    return True, "OK"

@st.cache_data
def get_output_path(input_path, output_dir="outputs", suffix="_converted"):
    path = Path(input_path)
    new_ext = ".pdf"  # Default to PDF, overridden by converter
    output_name = path.stem + suffix + new_ext
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, output_name)

def save_uploaded_files(uploaded_files, base_dir="uploads"):
    os.makedirs(base_dir, exist_ok=True)
    saved_paths = []
    for uploaded_file in uploaded_files:
        if uploaded_file is not None:
            path = os.path.join(base_dir, uploaded_file.name)
            with open(path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            saved_paths.append(path)
    return saved_paths

def create_zip(files, zip_path):
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for f in files:
            zf.write(f, Path(f).name)
    return zip_path

def cleanup_files(file_paths):
    for path in file_paths:
        if os.path.exists(path):
            os.remove(path)

