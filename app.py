import streamlit as st
import pandas as pd
from extract import extract_contacts_from_images

st.set_page_config(page_title="Contact Extractor", layout="centered")

st.title("📞 Contact Extractor from Images")
st.write("Upload JPEG images with phone numbers. This app will extract phone numbers and generate an Excel file.")

# OCR mode selection
ocr_mode = st.radio(
    "Choose OCR Mode:",
    ("🖨️ Typed (Tesseract)", "✍️ Handwritten (EasyOCR)")
)

method = "typed" if "Typed" in ocr_mode else "handwritten"

uploaded_files = st.file_uploader("Upload image(s)", type=["jpg", "jpeg"], accept_multiple_files=True)

# Disclaimer
st.markdown("""
> ⚠️ **Note:** Handwritten text extraction is experimental. Accuracy may be limited.  
> Please review extracted contacts carefully before use.
""", unsafe_allow_html=True)

if uploaded_files:
    all_results = []

    with st.spinner("🔍 Extracting contacts..."):
        for image_file in uploaded_files:
            df = extract_contacts_from_images([image_file], method=method)
            if not df.empty:
                df["Source File"] = image_file.name  # Add filename info
                all_results.append(df)

    if all_results:
        final_df = pd.concat(all_results, ignore_index=True)
        st.success(f"✅ Found {len(final_df)} contact(s) across {len(uploaded_files)} image(s).")
        st.dataframe(final_df)

        # Export to Excel
        excel_file = "extracted_contacts.xlsx"
        final_df.to_excel(excel_file, index=False)

        with open(excel_file, "rb") as f:
            st.download_button(
                label="📥 Download Excel",
                data=f,
                file_name="extracted_contacts.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.warning("⚠️ No contacts found in the uploaded images.")
