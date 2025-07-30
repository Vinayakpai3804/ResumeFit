import streamlit as st

def initialize_session_state():
    """Initialize session state - exact same as original"""
    defaults = {
        'form_data': {},
        'education_entries': [{}],
        'experience_entries': [{}],
        'project_entries': [{}],
        'achievement_entries': [{}],
        'publication_entries': [{}],
        'certification_entries': [{}],
        'language_entries': [{}],
        'generated_pdf': None,
        'generation_time': None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def safe_text_input(label: str, key: str, placeholder: str = "", help_text: str = "") -> str:
    """Safe text input with enhanced styling - exact same as original"""
    return st.text_input(
        label,
        key=key,
        placeholder=placeholder,
        help=help_text if help_text else None
    )

def safe_text_area(label: str, key: str, placeholder: str = "", height: int = 100, help_text: str = "") -> str:
    """Safe text area with enhanced styling - exact same as original"""
    return st.text_area(
        label,
        key=key,
        placeholder=placeholder,
        height=height,
        help=help_text if help_text else None
    )
