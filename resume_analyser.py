import streamlit as st

# --- Import Configuration and Setup ---
from utils.app_config import configure_streamlit_page, get_backend_handlers
from utils.css_styles import load_modern_professional_css
from utils.session_manager import initialize_session_state
from utils.navigation import create_enhanced_navigation_sidebar
from utils.ui_sections import (
    display_enhanced_metrics, 
    create_welcome_section,
    create_main_upload_section,
    create_job_role_section,
    create_analysis_section,
    create_main_header
)
from utils.chat_interface import create_chat_interface


def main():
    """Main application with enhanced UI structure"""
    # Initialize application
    configure_streamlit_page()
    initialize_session_state()
    load_modern_professional_css()
    create_enhanced_navigation_sidebar()
    
    # Get backend handlers
    handlers = get_backend_handlers()
    llm_handler = handlers['llm_handler']
    ui_components = handlers['ui_components']
    pdf_generator = handlers['pdf_generator']
    
    # Main Header
    create_main_header()
    
    # Main Content Logic
    if st.session_state.analysis_complete and st.session_state.analysis_result:
        # Analysis Results Section
        st.markdown(f"## 📊 Analysis Results for: {st.session_state.job_role}")
        display_enhanced_metrics()
        
        # Professional tabbed interface
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Detailed Analysis", 
            "💪 Strengths", 
            "⚡ Improvements", 
            "💬 AI Assistant", 
            "📥 Export Results"
        ])
        
        with tab1:
            ui_components.display_overview(st.session_state.analysis_result)
        
        with tab2:
            ui_components.display_strengths(st.session_state.analysis_result)
        
        with tab3:
            weak_sections = st.session_state.analysis_result.get('weak_sections', [])
            ui_components.display_improvements(st.session_state.analysis_result, weak_sections)
        
        with tab4:
            create_chat_interface()
        
        with tab5:
            ui_components.display_download_options(
                st.session_state.analysis_result,
                st.session_state.resume_text,
                st.session_state.job_role,
                pdf_generator
            )
    
    else:
        # Welcome Section and Input Forms
        create_welcome_section()
        create_main_upload_section()
        create_job_role_section()
        create_analysis_section()


if __name__ == "__main__":
    main()
