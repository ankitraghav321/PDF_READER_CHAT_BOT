import streamlit as st
import fitz  # PyMuPDF
import openai
import os
import tempfile

# Set up OpenAI API
openai.api_key = "sk-proj-jbSAsKj5LFkSc7GT8affT3BlbkFJDb4XzYyHZhOqIletqKTh"

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    # text = ""
    # with fitz.open(uploaded_file) as doc:
    #     for page in doc:
    #         text += page.get_text()
    # return text

    # Save uploaded file to a temporary location
    temp_dir = tempfile.TemporaryDirectory()
    temp_file_path = os.path.join(temp_dir.name, uploaded_file.name)
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.getbuffer())

    # Extract text from PDF
    text = ""
    with fitz.open(temp_file_path) as doc:
        for page in doc:
            text += page.get_text()

    # Clean up temporary directory
    temp_dir.cleanup()

    return text

# Function to generate response from OpenAI API
def generate_response(input_text):
    response = openai.Completion.create(
        # engine="text-davinci-003",
        # engine="davinci-codex",
        engine="gpt-3.5-turbo-instruct",
        prompt=input_text,
        max_tokens=50
    )
    return response.choices[0].text.strip()

# Main Streamlit app
def main():
    st.title("PDF Chatbot")

    # File upload
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file is not None:
        # Extract text from PDF
        text = extract_text_from_pdf(uploaded_file)

        st.write("### PDF Contents:")
        st.write(text)

        # Chatbot
        user_input = st.text_input("You:", "")
        if st.button("Send"):
            if user_input.strip() != "":
                # Concatenate user input with PDF text
                input_text = text + "\nUser: " + user_input.strip() + "\nBot:"
                # Generate response
                response = generate_response(input_text)
                st.write("Bot:", response)

if __name__ == "__main__":
    main()
