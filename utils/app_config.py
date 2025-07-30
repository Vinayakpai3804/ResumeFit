import os
import sys
import streamlit as st
from datetime import datetime
import re
from typing import Dict, List, Any

# --- Project Root Setup (Logic Unchanged) ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def configure_streamlit_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="ResumeFit AI - AI-Powered Resume Analysis",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def import_backend_handlers():
    """Import backend handler classes with fallback dummy classes"""
    try:
        from utils.llm_handler import LLMHandler
        from utils.resume_processor import ResumeProcessor
        from utils.pdf_generator import PDFGenerator
        from utils.ui_component import UIComponents
        return LLMHandler, ResumeProcessor, PDFGenerator, UIComponents
    except ImportError:
        print("Warning: Backend utility classes not found. Using dummy classes for UI rendering.")
        
        class LLMHandler:
            def analyze_resume_comprehensive(self, resume_text, job_role):
                return {
                    'match_percentage': 88, 'overall_score': 8, 'found_skills': ['Python', 'Streamlit', 'UI/UX Design'],
                    'strengths': [{'title': 'Strong Experience', 'details': 'Great experience shown.'}],
                    'improvements': [{'title': 'Add Metrics', 'details': 'Quantify your achievements.'}],
                    'weak_sections': [], 'overview': 'This is a great resume.'
                }
            def chat_response(self, user_input, resume_text, job_role, history):
                return f"This is a dummy AI response to: '{user_input}'"
        
        class ResumeProcessor:
            def extract_text(self, uploaded_file):
                return "This is the extracted text from the uploaded resume PDF."
        
        class PDFGenerator:
            def generate_pdf(self, content):
                return b"dummy_pdf_content"
        
        class UIComponents:
            def display_overview(self, result): st.success("Overview displayed successfully.")
            def display_strengths(self, result): st.success("Strengths displayed successfully.")
            def display_improvements(self, result, weak_sections): st.success("Improvements displayed successfully.")
            def display_download_options(self, result, text, role, generator): st.success("Download options displayed.")
        
        return LLMHandler, ResumeProcessor, PDFGenerator, UIComponents

def get_backend_handlers():
    """Initialize and return backend handler instances"""
    LLMHandler, ResumeProcessor, PDFGenerator, UIComponents = import_backend_handlers()
    return {
        'llm_handler': LLMHandler(),
        'resume_processor': ResumeProcessor(),
        'pdf_generator': PDFGenerator(),
        'ui_components': UIComponents()
    }
