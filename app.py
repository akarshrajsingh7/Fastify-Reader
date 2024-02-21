import streamlit as st
from PyPDF2 import PdfReader
from concurrent.futures import ThreadPoolExecutor
from base64 import b64encode
from fpdf import FPDF
import io, string, re, math
from io import StringIO

# Importing the Fastify Class
from fast_reader import Fastify_Reader

def pdf_extract_text(pdf_docs):
    '''
    Basic function for extracting text from the PDFs
    '''
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def text_to_pdf_fastify(text):    
    '''
    Basic function to apply fastification on the input text and convert it to bytes for PDF rendering
    '''
    # Applying the Fastify Logic
    bold_text = Fastify_Reader(text).fastify()
    bold_text = bold_text.encode('latin-1', 'ignore').decode('latin-1') #since fpdf works with latin-1 encoding
    
    # Creating the PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    pdf.multi_cell(0, 10, txt = bold_text, markdown=True)
    return bytes(pdf.output()), bold_text

def text_to_pdf(text):
    '''
    Basic function on the input text and convert it to bytes for PDF rendering
    '''
    text = text.encode('latin-1', 'ignore').decode('latin-1') #since fpdf works with latin-1 encoding
    # Creating the PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    pdf.multi_cell(0, 10, txt = text, markdown=True)
    return bytes(pdf.output()), text

#Setting the page config
st.set_page_config(page_title="Fastify Reader",
                   page_icon=":books:",
                   layout="wide")

# Due to browser cache and streamlit issue, sometimes the PDFs are not rendered properly.
note_text = """
                    If the PDF is not being rendered by your browser, <br>
                    &emsp;1. Try this link - (https://akarshrajsingh7-fastify-reader.hf.space/) <br>
                    &emsp;2. Download the PDF and open it in a PDF viewer.
                    """
# Sidebar
with st.sidebar:
    st.image("Logo.jpg")
    st.markdown("<div style='text-align: center;'>How fast can you read?</div>", unsafe_allow_html=True)

# Main Page
tab1, tab2= st.tabs(["Input Text", "PDF file"])

# First tab where Text is input
with tab1:
    user_input = st.text_input("Enter some text")

    # Compare Check Box
    compare = st.checkbox('Compare with Fastified Text', value=False, key='compare')
    
    # Submit Button
    if st.button("Submit", key="input-text"):
        #Progess Bar for the processing
        with st.spinner("Processing"):
            text = user_input

            # Generating base64 encoded text bytes for PDF rendering
            original_pdf = b64encode(text_to_pdf(text)[0]).decode("utf-8")
            base64_pdf = b64encode(text_to_pdf_fastify(text)[0]).decode("utf-8")

            # Embedding the PDFs in the HTML
            original_display = f'<embed src="data:application/pdf;base64,{original_pdf}" width = "100%" height = 600 type="application/pdf" download="original.pdf">'
            pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width = "100%" height = 600 type="application/pdf" download="Modified.pdf">'
            
            # Compare Logic implementation
            if compare:
                col1, col2, col3 = st.columns(3)
                with col3:
                    st.download_button(label="Download Fastified PDF", data=text_to_pdf_fastify(text)[0], file_name='output.pdf', mime='application/pdf')
                
                # Side by Side comparison
                col1, col2 = st.columns([1, 1], gap="small")
                with col1:
                    with st.container(border = True):
                        st.markdown("<div style='text-align: center;'><strong>Original PDF viewer</strong></div>", unsafe_allow_html=True)
                        st.markdown(original_display, unsafe_allow_html=True)
                with col2:
                    with st.container(border = True):
                        st.markdown("<div style='text-align: center;'><strong>Fastified PDF viewer</strong></div>", unsafe_allow_html=True)
                        st.markdown(pdf_display, unsafe_allow_html=True)
                
                # Browser Cache Note
                st.markdown(f"""
                        <div style='background-color: #FFD580; border-radius: 5px;'>
                            <p style='color: black;'><strong>Note</strong> - {note_text}</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                # No Comparisons
                col1, col2, col3 = st.columns(3)
                with col2:
                    st.download_button(label="Download Fastified PDF", data=text_to_pdf_fastify(text)[0], file_name='output.pdf', mime='application/pdf')
                with st.container(border = True):
                    st.markdown("<div style='text-align: center;'><strong>Fastified PDF viewer</strong></div>", unsafe_allow_html=True)
                    st.markdown(pdf_display, unsafe_allow_html=True)
                
                # Browser Cache Note
                    st.markdown(f"""
                        <div style='background-color: #FFD580; border-radius: 5px;'>
                            <p style='color: black;'><strong>Note</strong> - {note_text}</p>
                        </div>
                        """, unsafe_allow_html=True)
    
# Added support for PDFs having text
with tab2:
        uploaded_file = st.file_uploader("Upload a PDF file", type="pdf", accept_multiple_files=True)

        # Compare Check Box
        compare = st.checkbox('Compare with Fastified Text', value=False, key='compare_pdf')

        # Submit Button
        if st.button("Submit", key="pdf"):
            #Progess Bar for the processing
            with st.spinner("Processing"):
                text = pdf_extract_text(uploaded_file)

                # Generating base64 encoded text bytes for PDF rendering
                original_pdf = b64encode(text_to_pdf(text)[0]).decode("utf-8")
                base64_pdf = b64encode(text_to_pdf_fastify(text)[0]).decode("utf-8")

                # Embedding the PDFs in the HTML
                original_display = f'<embed src="data:application/pdf;base64,{original_pdf}" width = "100%" height = 600 type="application/pdf">'
                pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width = "100%" height = 600 type="application/pdf">'

                # Compare Logic implementation
                if compare:
                    col1, col2, col3 = st.columns(3)
                    with col3:
                        st.download_button(label="Download Fastified PDF", data=text_to_pdf_fastify(text)[0], file_name='output.pdf', mime='application/pdf')
                    
                    # Side by Side comparison
                    col1, col2 = st.columns([1, 1], gap="small")
                    with col1:
                        with st.container(border = True):
                            st.markdown("<div style='text-align: center;'><strong>Original PDF viewer</strong></div>", unsafe_allow_html=True)
                            st.markdown(original_display, unsafe_allow_html=True)
                    with col2:
                        with st.container(border = True):
                            st.markdown("<div style='text-align: center;'><strong>Fastified PDF viewer</strong></div>", unsafe_allow_html=True)
                            st.markdown(pdf_display, unsafe_allow_html=True)
                    # Browser Cache Note
                    st.markdown(f"""
                        <div style='background-color: #FFD580; border-radius: 5px;'>
                            <p style='color: black;'><strong>Note</strong> - {note_text}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    # No Comparison
                    col1, col2, col3 = st.columns(3)
                    with col2:
                        st.download_button(label="Download Fastified PDF", data=text_to_pdf_fastify(text)[0], file_name='output.pdf', mime='application/pdf')
                    with st.container(border = True):
                        st.markdown("<div style='text-align: center;'><strong>Fastified PDF viewer</strong></div>", unsafe_allow_html=True)
                        st.markdown(pdf_display, unsafe_allow_html=True)
                    
                    # Browser Cache Note
                    st.markdown(f"""
                        <div style='background-color: #FFD580; border-radius: 5px;'>
                            <p style='color: black;'><strong>Note</strong> - {note_text}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
