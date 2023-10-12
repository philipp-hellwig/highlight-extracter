import streamlit as st
import pdf_highlights
import streamlit as st
import pyperclip


highlights = ""
st.set_page_config(page_title="Condensed")
st.write(f'<span style="color:#000000;font-size:24px;border-radius:2%;">Text </span>',
         f'<span style="background-color:yellow;color:#000000;font-size:24px;border-radius:2%;">Condensed</span>.\n',
         '***',
         unsafe_allow_html=True)
st.markdown(f"How it works:\n"
            "1. <span style='background-color:yellow;color:#000000;'>upload</span> your .pdf file\n "
            "2. click <span style='background-color:yellow;color:#000000;'>'Generate Highlights'</span>\n"
            "3. <span style='background-color:yellow;color:#000000;'>copy</span> the highlighted text <span style='background-color:yellow;color:#000000;'>or download</span> it as a .txt file.",
         unsafe_allow_html=True)
upload = st.file_uploader("Upload your pdf here:", type="pdf", label_visibility="hidden")

st.markdown(f"#### Output Options")
specify_pages = st.checkbox("Specify pages")
if specify_pages:
    col1, col2 = st.columns([1, 1])
    start = col1.number_input("from", value=1, step=1, min_value=1)
    end = col2.number_input("to", value=2, step=1, min_value=1)
page_no = st.checkbox("Indicate page numbers")

if st.button("Generate Highlights"):
    if upload is None:
        st.write("Please upload a file first.")
    else:
        st.write("#### Preview")
        if specify_pages:
            highlights = pdf_highlights.find_highlights(upload.getvalue(), start, end, display_pages=page_no)
        else:
            highlights = pdf_highlights.find_highlights(upload.getvalue(), display_pages=page_no)
        st.markdown(highlights)
        col1, col2, _ = st.columns([1.5, 1.5, 2.5])
        with col1:
            st.download_button("Download as .txt", highlights)
        with col2:
            clipboard = st.button(":clipboard: Copy to clipboard")
        if clipboard:
            # @todo: make clipboard work
            pyperclip.copy("hi")
