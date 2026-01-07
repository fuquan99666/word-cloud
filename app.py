# in this file , we create a streamlit app to run the word cloud generator 
import streamlit as st
from new_version.main import generate_word_cloud_from_text

st.title("Word Cloud Generator")
st.header("Generate a word cloud from your input text.")

text_input = st.text_area("Enter your text here or paste here:", height=200)

input_text = st.file_uploader(
    "Upload a text file or enter text manually",
    type=["txt"]
)
text = ""
if input_text is not None:
    text = input_text.read().decode("utf-8")
elif text_input.strip():
    text = text_input.strip()
mask_file = st.file_uploader(
    "Optional: Upload a mask image",
    type=["png", "jpg", "jpeg"]
)
line_mode = st.checkbox("Line mode (treat each line as a separate word)", value=False)
max_num = st.number_input("Maximum number of words to include in the word cloud:", min_value=100, max_value=2000, value=800, step=100)

if st.button("Generate Word Cloud"):
    if not text:
        st.warning("Please enter some text or upload a text file.")
    else:
        with st.spinner("Generating word cloud..."):
            word_cloud_image = generate_word_cloud_from_text(text, mask_file, line_mode, max_num)
            st.image(word_cloud_image, caption="Generated Word Cloud", use_column_width=True)
            st.success("Word cloud generated!")
