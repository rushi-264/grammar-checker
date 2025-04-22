import streamlit as st
from utils import extract_text_from_pdf, check_grammar, correct_text, highlight_text

st.set_page_config(page_title="Grammar Checker", layout="wide")
st.title("📝 Grammar Checker with Error Highlighting")

# --- Text Input Section ---
uploaded_file = st.file_uploader("Upload a .txt or .pdf file", type=["txt", "pdf"])
input_text = ""

if uploaded_file:
    if uploaded_file.name.endswith(".txt"):
        input_text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".pdf"):
        input_text = extract_text_from_pdf(uploaded_file)

if not input_text:
    input_text = st.text_area("Or enter your text here:", height=200)

# --- Correction Mode ---
correction_mode = st.radio("Choose Correction Mode:", ["Auto-Correct", "Manual"])

if st.button("Check Grammar") and input_text:
    matches = check_grammar(input_text)

    if not matches:
        st.success("✅ No grammar issues found!")
    else:
        # --- Highlight Mistakes ---
        st.markdown("### 🖍️ Highlighted Mistakes:")
        st.markdown(highlight_text(input_text, matches), unsafe_allow_html=True)

        # --- Error Explanations ---
        st.markdown("### 💡 Error Explanations:")
        for i, match in enumerate(matches, 1):
            st.markdown(f"**{i}.** {match.message} *(Suggestion: {', '.join(match.replacements)})*")

        # --- Output Correction ---
        st.markdown("### 🛠️ Corrected Text:")
        if correction_mode == "Auto-Correct":
            corrected = correct_text(input_text, matches)
            st.text_area("Corrected Output:", value=corrected, height=200)
        else:
            updated_text = input_text
            for i, match in enumerate(matches):
                original = input_text[match.offset:match.offset + match.errorLength]
                options = [original] + match.replacements
                choice = st.selectbox(f"Correction for: '{original}'", options=options, key=i)
                if choice != original:
                    updated_text = updated_text[:match.offset] + choice + updated_text[match.offset + match.errorLength:]
            st.text_area("Manually Corrected Output:", value=updated_text, height=200)
