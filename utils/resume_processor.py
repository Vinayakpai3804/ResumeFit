import streamlit as st
from typing import Optional
import io

class ResumeProcessor:
    """Process and extract text from various resume formats"""
    
    def extract_text(self, uploaded_file) -> Optional[str]:
        """Extract text from uploaded file"""
        try:
            if uploaded_file.type == "application/pdf":
                return self._extract_from_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return self._extract_from_docx(uploaded_file)
            elif uploaded_file.type == "text/plain":
                return self._extract_from_txt(uploaded_file)
            else:
                st.error(f"Unsupported file type: {uploaded_file.type}")
                return None
        except Exception as e:
            st.error(f"Error extracting text: {str(e)}")
            return None
    
    def _extract_from_pdf(self, uploaded_file) -> str:
        """Extract text from PDF file"""
        try:
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except ImportError:
            st.error("PyPDF2 not installed. Please install it: pip install PyPDF2")
            return ""
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return ""
    
    def _extract_from_docx(self, uploaded_file) -> str:
        """Extract text from DOCX file"""
        try:
            import docx
            doc = docx.Document(uploaded_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except ImportError:
            st.error("python-docx not installed. Please install it: pip install python-docx")
            return ""
        except Exception as e:
            st.error(f"Error reading DOCX: {str(e)}")
            return ""
    
    def _extract_from_txt(self, uploaded_file) -> str:
        """Extract text from TXT file"""
        try:
            return str(uploaded_file.read(), "utf-8")
        except Exception as e:
            st.error(f"Error reading TXT: {str(e)}")
            return ""
