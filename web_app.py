import pdf_highlights
import streamlit as st


highlights = ""
st.set_page_config(page_title="Quick Highlights")
# header
st.write(
    f'<span style="background-color:yellow;color:#000000;font-size:24px;border-radius:2%;">Condensed</span>.info\n',
    '***',
    unsafe_allow_html=True)
# info text
st.markdown(f"This site enables you to extract highlighted text from your pdfs to create summaries of papers more efficiently. Completely free of charge!\n")
st.markdown("How it works:\n"
            "1. <span style='background-color:yellow;color:#000000;'>upload</span> your .pdf file\n "
            "2. adjust the options to your liking\n"
            "3. click <span style='background-color:yellow;color:#000000;'>'Generate Highlights'</span>\n"
            "4. <span style='background-color:yellow;color:#000000;'>download</span> it as a .txt file",
            unsafe_allow_html=True)

upload = st.file_uploader("Upload your pdf here:", type="pdf", label_visibility="hidden")

st.markdown(f"#### Options")
specify_pages = st.checkbox("Specify pages")
if specify_pages:
    col1, col2 = st.columns([1, 1])
    start = col1.number_input("from", value=1, step=1, min_value=1)
    end = col2.number_input("to", value=2, step=1, min_value=1)
page_no = st.checkbox("Indicate page numbers")
md = st.checkbox("Markdown headings")
if st.button("Generate Highlights"):
    if upload is None:
        st.write("Please upload a file first.")
    else:
        if specify_pages:
            highlights = pdf_highlights.get_highlights(upload.getvalue(), start, end, display_pages=page_no,
                                                       markdown=md)
        else:
            highlights = pdf_highlights.get_highlights(upload.getvalue(), display_pages=page_no, markdown=md)
        st.markdown(highlights)

        # download section
        col1, _ = st.columns([1.5, 4])
        with col1:
            st.download_button("Download as .txt", highlights)
