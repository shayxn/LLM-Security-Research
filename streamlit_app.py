import streamlit as st
import base64
import os
from openai import OpenAI
from streamlit_ace import st_ace
import io
import contextlib


def truncate_string(s, max_length):
    if len(s) > max_length:
        return s[:max_length - 3] + '...'
    return s


# Title of the app
st.title('LLM Jailbreak - Security Research')

# Sidebar
st.sidebar.title('Options')

llm_model = st.sidebar.selectbox(
    'Select your LLM model',
    [
        'GPT-4o', 'GPT-4', 'Gemini', 'Claude 3', 'Claude 1.3',
        'Mistral', 'Llama 3-8b'
    ]
)

jailbreak_options = {
    'GPT-4o': ['Image Prompt Injection', 'Morse Code Injection'],
    'GPT-4': ['Image Prompt Injection', 'Morse Code Injection'],
    'Gemini': ['Technique 7', 'Technique 8'],
    'Claude 3': ['Technique 9', 'Technique 10'],
    'Claude 1.3': ['Technique 11', 'Technique 12'],
    'Mistral': ['Technique 13', 'Technique 14'],
    'Llama 3-8b': ['Technique 15', 'Technique 16'],
}

# Display the appropriate jailbreak techniques based on the selected LLM model
jailbreak_technique = st.sidebar.selectbox(
    'Select your LLM jailbreak technique',
    jailbreak_options.get(llm_model, [])
)
# Input field for entering the selected LLM model's API key
api_key = st.sidebar.text_input(
    f'Enter API key for {llm_model}', type='password')

# Continue button
if st.sidebar.button('Continue'):
    # Path to the folder and file
    folder_path = os.path.join(os.getcwd(), llm_model)
    file_path = os.path.join(folder_path, f"{jailbreak_technique}.py")

    # Check if the file exists
    if os.path.exists(file_path):
        # Read the content of the file
        with open(file_path, 'r') as file:
            code = file.read()

         # Store the code in session state
        st.session_state['code'] = code
        st.session_state['file_path'] = file_path
        st.session_state['api_key'] = api_key

        st.rerun()

if 'code' in st.session_state:
    # Display the code in an editable text area
    edited_code = st_ace(
        value=st.session_state['code'],
        language='python',
        theme='monokai',
        height=500
    )

    if st.button("Run Code"):
        try:
            exec_globals = {
                'base64': base64,
                'OpenAI': OpenAI,
                "ENTERED_API_KEY": str(api_key),
            }
            exec_locals = {}
            st.write('Code executed successfully!')
            st.write('Output:')
            output_buffer = io.StringIO()

            with contextlib.redirect_stdout(output_buffer):
                exec(edited_code, exec_globals, exec_locals)

            # Display the captured output
            output = output_buffer.getvalue()
            st.code(output, language='python')
        except Exception as e:
            st.write('Error executing code:')
            st.write(e)
