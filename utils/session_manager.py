import streamlit as st

def initialize_session_state():
    """Initialize session state with default values (Logic Unchanged)"""
    defaults = {
        'resume_text': '', 
        'job_role': '', 
        'analysis_result': None, 
        'analysis_complete': False, 
        'chat_history': []
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def get_session_value(key, default=None):
    """Get a value from session state with optional default"""
    return st.session_state.get(key, default)

def set_session_value(key, value):
    """Set a value in session state"""
    st.session_state[key] = value

def update_session_values(updates_dict):
    """Update multiple session state values at once"""
    for key, value in updates_dict.items():
        st.session_state[key] = value

def clear_analysis_results():
    """Clear analysis results from session state"""
    st.session_state.analysis_result = None
    st.session_state.analysis_complete = False

def add_chat_message(role, content):
    """Add a message to chat history"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    st.session_state.chat_history.append({"role": role, "content": content})

def get_chat_history():
    """Get the current chat history"""
    return st.session_state.get('chat_history', [])

def clear_chat_history():
    """Clear the chat history"""
    st.session_state.chat_history = []

def is_analysis_ready():
    """Check if analysis requirements are met"""
    return bool(st.session_state.get('resume_text') and st.session_state.get('job_role'))

def has_analysis_results():
    """Check if analysis results are available"""
    return bool(st.session_state.get('analysis_complete') and st.session_state.get('analysis_result'))
