import streamlit as st
from anonymizer.anonymize import anonymize_text
from anonymizer.file_readers import read_docx_contents, read_pdf_contents, read_image_contents
import pandas as pd
import time
import re

st.set_page_config(page_title="Resume Anonymizer", page_icon="📑", layout="wide")

# Display logo (if available)
try:
    st.image("logo.png", width=100)
except Exception:
    pass

st.title("📄 Fair Hire : Automated Resume Anonymizer for Bias-Free Recruitment")
st.write("""
Upload resumes in TXT, DOCX, PDF, JPG, or PNG format and get anonymized versions instantly!
Resumes with scanned images will be auto-processed with OCR.
""")

# Sample resume for download
def get_sample_resume():
    return (
        "Jane Doe\n123 Main St, City\nEmail: jane@email.com\nPhone: 1234567890\nLinkedIn: linkedin.com/in/janedoe\n\nObjective\nTo obtain a challenging position as a Data Analyst.\n\nEducation\nB.Sc. in Computer Science, University of City, 2018-2022\n\nExperience\nData Analyst Intern, DataCorp, 2021\n- Analyzed sales data using Python and SQL.\n\nSkills\nPython, SQL, Tableau, Data Visualization\n\nReferences available upon request."
    )

# Clear All button
if st.button("Clear All"):
    st.rerun()

# Modern two-column layout for upload & instructions
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_files = st.file_uploader(
        "Select one or more resumes to anonymize",
        type=["txt", "docx", "pdf", "jpg", "jpeg", "png"],
        accept_multiple_files=True,
        help="Supports TXT, DOCX, PDF, JPG, PNG files"
    )
    st.download_button(
        label="Download Sample Resume",
        data=get_sample_resume(),
        file_name="sample_resume.txt",
        mime="text/plain"
    )

with col2:
    st.info("""
    **How it works:**
    - Upload any supported file type
    - Scanned images and PDFs handled
    - Anonymized outputs are downloadable
    [No data leaves your machine]
    """)
    st.sidebar.header("Help / FAQ")
    st.sidebar.markdown("""
    - **What formats are supported?** TXT, DOCX, PDF, JPG, PNG
    - **Is my data private?** Yes, all processing is local.
    - **What is anonymized?** Names, emails, phone numbers, addresses, social links, and more.
    """)
 

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) successfully uploaded.")
    progress = st.progress(0)
    for i, uploaded_file in enumerate(uploaded_files):
        filetype = uploaded_file.name.split('.')[-1].lower()
        size_kb = uploaded_file.size / 1024
        st.caption(f"File type: {filetype.upper()} | Size: {size_kb:.1f} KB")
        resume_text = ""
        try:
            if filetype == "txt":
                resume_text = uploaded_file.read().decode("utf-8")
            elif filetype == "docx":
                resume_text = read_docx_contents(uploaded_file.read())
            elif filetype == "pdf":
                resume_text = read_pdf_contents(uploaded_file.read())
            elif filetype in ["jpg", "jpeg", "png"]:
                resume_text = read_image_contents(uploaded_file.read())
            else:
                st.error("Unsupported file type.")
                continue
            st.markdown(f"### `{uploaded_file.name}`")
            if filetype in ["jpg", "jpeg", "png"]:
                st.image(uploaded_file, width=200, caption="Uploaded image resume")
            with st.expander("🔎 Preview Resume Text", expanded=True):
                st.text_area("Preview", resume_text, height=200, key=f"orig_{uploaded_file.name}")
            if st.button(f"Anonymize: {uploaded_file.name}", key=f"an_btn_{uploaded_file.name}"):
                start_time = time.time()
                anonymized_text, summary = anonymize_text(resume_text)
                end_time = time.time()
                st.balloons()  # Celebrate!
                with st.expander("✅ Anonymized Text Ready!", expanded=True):
                    # Highlight placeholders in anonymized text
                    highlighted = re.sub(r'(\[.*?\])', r'**\1**', anonymized_text)
                    st.markdown(highlighted, unsafe_allow_html=True)
                    st.caption(f"Download will be: anonymized_{uploaded_file.name}")
                    st.download_button(
                        label=f"Download anonymized_{uploaded_file.name}",
                        data=anonymized_text,
                        file_name=f"anonymized_{uploaded_file.name}",
                        mime="text/plain"
                    )
                # Redaction summary report
                st.subheader("Redaction Summary")
                if summary:
                    df = pd.DataFrame(list(summary.items()), columns=["Entity Type", "Count"])
                    st.table(df)
                    st.download_button(
                        label="Download Redaction Report",
                        data=df.to_csv(index=False),
                        file_name=f"redaction_report_{uploaded_file.name}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No entities were redacted.")
                st.caption(f"Processing time: {end_time - start_time:.2f} seconds")
                st.success(f"{uploaded_file.name} processed successfully!")
        except Exception as e:
            st.error(f"Failed to process {uploaded_file.name}: {e}")
        progress.progress((i + 1) / len(uploaded_files))
    progress.empty()

with st.sidebar:
    st.header("About")
    st.write("Automated Resume Anonymizer for fair, private hiring.")
    st.header("Created by Valentino, Joel & Vibhav")
    st.write("Contact: +91 9769437244")
