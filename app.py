import warnings
warnings.filterwarnings("ignore")
import streamlit as st
from PyPDF2 import PdfReader
from concurrent.futures import ThreadPoolExecutor
from base64 import b64encode
from fpdf import FPDF
import io, string, re, math
from io import StringIO
from streamlit_pdf_viewer import pdf_viewer

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

def text_to_pdf_fastify(txt):    
    '''
    Basic function to apply fastification on the input text and convert it to bytes for PDF rendering
    '''
    text = (txt + '.')[:-1]
    # Applying the Fastify Logic
    bold_text = Fastify_Reader(text).fastify()
    bold_text = bold_text.encode('latin-1', 'ignore').decode('latin-1') #since fpdf works with latin-1 encoding
    
    # Creating the PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    pdf.multi_cell(0, 10, txt = bold_text, markdown=True)
    return bytes(pdf.output())

def text_to_pdf(txt):
    '''
    Basic function on the input text and convert it to bytes for PDF rendering
    '''
    text = (txt + '.')[:-1]
    text = text.encode('latin-1', 'ignore').decode('latin-1') #since fpdf works with latin-1 encoding
    # Creating the PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    pdf.multi_cell(0, 10, txt = text, markdown=True)
    return bytes(pdf.output())

#Setting the page config
st.set_page_config(page_title="Fastify Reader",
                   page_icon=":books:",
                   layout="wide")

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

            # Compare Logic implementation
            if compare:
                col1, col2, col3 = st.columns(3)
                with col3:
                    st.download_button(label="Download Fastified PDF", data=text_to_pdf_fastify(text), file_name='output.pdf', mime='application/pdf')
                
                # Side by Side comparison
                col1, col2 = st.columns([1, 1], gap="small")

                with col1:
                    with st.container(border = True):
                        st.markdown("<div style='text-align: center;'><strong>Original PDF viewer</strong></div>", unsafe_allow_html=True)
                        pdf_viewer(input = text_to_pdf(text), width = 600)
                with col2:
                    with st.container(border = True):
                        st.markdown("<div style='text-align: center;'><strong>Fastified PDF viewer</strong></div>", unsafe_allow_html=True)
                        pdf_viewer(text_to_pdf_fastify(text), width = 600)
                
            else:
                # # No Comparisons
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button(label="Download Fastified PDF", data=text_to_pdf_fastify(text), file_name='output.pdf', mime='application/pdf')
                
                with st.container():
                    st.markdown("<div><strong>Fastified PDF viewer</strong></div>", unsafe_allow_html=True)
                    pdf_viewer(text_to_pdf_fastify(text), width = 600)
                
    
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

                # Compare Logic implementation
                if compare:
                    col1, col2, col3 = st.columns(3)
                    with col3:
                        st.download_button(label="Download Fastified PDF", data=text_to_pdf_fastify(text), file_name='output.pdf', mime='application/pdf')
                    
                    # Side by Side comparison
                    col1, col2 = st.columns([1, 1], gap="small")
                    
                    with col1:
                        with st.container(border = True):
                            st.markdown("<div style='text-align: center;'><strong>Original PDF viewer</strong></div>", unsafe_allow_html=True)
                            pdf_viewer(text_to_pdf(text), width = 600)
                    with col2:
                        with st.container(border = True):
                            st.markdown("<div style='text-align: center;'><strong>Fastified PDF viewer</strong></div>", unsafe_allow_html=True)
                            pdf_viewer(text_to_pdf_fastify(text), width = 600)

                else:
                    # No Comparison
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.download_button(label="Download Fastified PDF", data=text_to_pdf_fastify(text), file_name='output.pdf', mime='application/pdf')
                    
                    with st.container():
                        st.markdown("<div><strong>Fastified PDF viewer</strong></div>", unsafe_allow_html=True)
                        pdf_viewer(text_to_pdf_fastify(text), width = 500)
