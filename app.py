# in this file , we create a streamlit app to run the word cloud generator 
import streamlit as st
from new_version.main import generate_word_cloud_from_text

st.title("Word Cloud Generator")
st.header("Generate a word cloud from your input text.")

input_text = st.file_uploader(
    "Upload a text file or enter text manually",
    type=["txt"]
)
mask_file = st.file_uploader(
    "Optional: Upload a mask image",
    type=["png", "jpg", "jpeg"]
)
line_mode = st.checkbox("Line mode (treat each line as a separate word)", value=False)
max_num = st.number_input("Maximum number of words to include in the word cloud:", min_value=100, max_value=2000, value=800, step=100)

if st.button("Generate Word Cloud"):
    if input_text.strip() == "":
        st.warning("Please enter some text to generate the word cloud.")
    else:
        with st.spinner("Generating word cloud..."):
            word_cloud_image = generate_word_cloud_from_text(input_text, mask_file, line_mode, max_num)
            st.image(word_cloud_image, caption="Generated Word Cloud", use_column_width=True)
            st.success("Word cloud generated!")
