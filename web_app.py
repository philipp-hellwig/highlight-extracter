import streamlit as st
import pdf_highlights

highlights = ""
st.set_page_config(page_title="Home")
st.write("# Extract Highlights")
upload = st.file_uploader("Upload your pdf here:")

if st.button("Generate Highlights") and upload is not None:
    st.write("### Preview")
    highlights = pdf_highlights.find_highlights(upload.getvalue())
    st.write(highlights)
    col1, col2, _ = st.columns([1.5, 1.5, 2.5])
    with col1:
        st.download_button("Download as .txt", highlights)
    with col2:
        st.button(":clipboard: Copy to clipboard")

