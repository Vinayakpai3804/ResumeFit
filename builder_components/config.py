import os
import sys
import streamlit as st
from datetime import datetime
import re
from typing import Dict, List, Any

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def configure_resume_builder():
    """Configure Streamlit page settings for resume builder"""
    st.set_page_config(
        page_title="ResumeFit AI - Professional Resume Builder",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def get_latex_handler():
    """Import and return LaTeX handler from refactored modules"""
    from builder_components.latex_generator import ProfessionalLaTeXHandler
    return ProfessionalLaTeXHandler()

def get_project_root():
    """Get project root directory"""
    return PROJECT_ROOT
