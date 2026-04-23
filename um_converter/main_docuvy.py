import streamlit as st
from pathlib import Path
import os
import tempfile
from converter import convert_file

# Page config with Docuvy branding
st.set_page_config(
    page_title="Docuvy",
    page_icon="logo.png",
    layout="wide"
)

# Docuvy Logo
#st.image("logo.png", width=222)


# Custom CSS for Docuvy brand
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@400;500&display=swap');
    
html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
    background-color: #0F172A;
    color: #F8FAFC;
}
h1, h2, h3 {
    font-family: 'Poppins', sans-serif !important;
    color: #F8FAFC !important;
}
.stButton > button {
    background: linear-gradient(135deg, #2563EB, #7C3AED) !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 12px 24px !important;
    font-weight: 500 !important;
    box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.4) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px 0 rgba(37, 99, 235, 0.5) !important;
}
.upload-card {
    background: linear-gradient(145deg, #FFFFFF10, #E2E8F00A) !important;
    border: 2px dashed #64748B40 !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    text-align: center !important;
    backdrop-filter: blur(10px);
}
.metric-card {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    border: 1px solid #E2E8F020 !important;
}
.success-box {
    background: linear-gradient(135deg, #22C55E20, #86EFAC20) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    border-left: 4px solid #22C55E !important;
}
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo.png")
with col2:
    st.markdown("# Docuvy")
    st.markdown("**Convert & Merge Files Instantly**")
    st.caption("Simple • Fast • Smart")

st.divider()

# Main tabs
tab1, tab2 = st.tabs(["✨ Convert", "🔗 Merge to PDF"])

with tab1:
    st.markdown("### Upload Files to Convert")
    
    # Styled upload card
    with st.container():
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            uploaded_files = st.file_uploader(
                "📤 Drop files here...",
                type=["pdf", "docx", "txt", "pptx", "jpg", "png", "jpeg"],
                accept_multiple_files=True,
                help="Supports PDF, DOCX, TXT, PPTX, Images"
            )
    
    if uploaded_files:
        conv_options = ["To PDF", "PDF → DOCX", "PDF → TXT", "PDF → PPTX", "PDF → Image"]
        conv_type = st.selectbox("🎯 Select Conversion", conv_options)
        
        if st.button("🚀 Convert Files", use_container_width=True):
            progress = st.progress(0)
            
            for i, uploaded_file in enumerate(uploaded_files):
                input_path = uploaded_file.name
                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                ext = Path(input_path).suffix.lower()
                
                try:
                    # Map to conv_type
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
                        if ctype:
                            output_path = input_path.rsplit('.', 1)[0] + '.pdf'
                        else:
                            st.error(f"❌ {input_path}: To PDF not supported")
                            continue
                    
                    elif conv_type == "PDF → DOCX" and ext == '.pdf':
                        ctype = 'pdf_to_docx'
                        output_path = input_path.replace('.pdf', '.docx')
                    
                    elif conv_type == "PDF → TXT" and ext == '.pdf':
                        ctype = 'pdf_to_txt'
                        output_path = input_path.replace('.pdf', '.txt')
                    
                    elif conv_type == "PDF → PPTX" and ext == '.pdf':
                        ctype = 'pdf_to_pptx'
                        output_path = input_path.replace('.pdf', '.pptx')
                    
                    elif conv_type == "PDF → Image" and ext == '.pdf':
                        ctype = 'pdf_to_image'
                        output_path = input_path.replace('.pdf', '_page.png')
                    
                    else:
                        st.error(f"❌ {input_path}: Invalid for {conv_type}")
                        continue
                    
                    result = convert_file(input_path, ctype, output_path)
                    
                    with st.container():
                        st.success(f"✅ {Path(input_path).name} → {Path(output_path).name}")
                        
                        if isinstance(result, list):
                            for r in result:
                                with open(r, "rb") as f:
                                    st.download_button(
                                        label=f"⬇️ {Path(r).name}",
                                        data=f,
                                        file_name=Path(r).name,
                                        use_container_width=True
                                    )
                        else:
                            with open(result, "rb") as f:
                                st.download_button(
                                    label=f"⬇️ Download {Path(output_path).name}",
                                    data=f,
                                    file_name=Path(output_path).name,
                                    use_container_width=True
                                )
                
                except Exception as e:
                    st.error(f"❌ {input_path}: {str(e)}")
                
                progress.progress((i + 1) / len(uploaded_files))

with tab2:
    st.markdown("### Merge Multiple Files into One PDF")
    
    uploaded_files = st.file_uploader(
        "📤 Upload multiple files to merge (PDF, DOCX, TXT, PPTX, Images)",
        type=["pdf", "docx", "txt", "pptx", "jpg", "png", "jpeg"],
        accept_multiple_files=True
    )
    
    if uploaded_files and len(uploaded_files) > 1:
        if st.button("🔗 Merge to PDF", use_container_width=True):
            with st.spinner("Merging files..."):
                input_paths = []
                for uploaded_file in uploaded_files:
                    input_path = uploaded_file.name
                    with open(input_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    input_paths.append(input_path)
                
                output_path = "docuvy_merged.pdf"
                try:
                    result = convert_file(input_paths, "merge_to_pdf", output_path)
                    st.success("✅ Files merged successfully!")
                    
                    with open(result, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Merged PDF",
                            data=f,
                            file_name="docuvy_merged.pdf",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"❌ Merge failed: {str(e)}")
    else:
        st.info("👆 Upload 2+ files to merge into a single PDF. All formats auto-converted to PDF first.")

# Footer
st.markdown("---")
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**Docuvy** • Fast, Clean File Conversion & Merge")
with col2:
    st.markdown("")

# Cleanup temp files (basic)
for f in Path('.').glob('*.tmp'):
    os.remove(f)

