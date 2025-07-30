import streamlit as st

# --- Import Modular Components ---
from builder_components.config import configure_resume_builder, get_latex_handler
from builder_components.styles import load_modern_professional_css
from builder_components.session import initialize_session_state
from builder_components.navigation import create_enhanced_navigation_sidebar
from builder_components.forms import (
    personal_info_form, 
    education_form, 
    experience_form, 
    skills_form
)
from builder_components.sections import (
    projects_form, 
    achievements_form, 
    additional_sections_form
)
from builder_components.generator import display_generation_section

def main():
    """Main resume builder application"""
    # Initialize application
    configure_resume_builder()
    initialize_session_state()
    load_modern_professional_css()
    create_enhanced_navigation_sidebar()
    
    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>📝 Professional Resume Builder</h1>
        <p>Create high-quality LaTeX resumes with professional templates</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Form sections in tabs for better organization
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "👤 Personal Info", 
        "🎓 Education", 
        "💼 Experience", 
        "🛠️ Skills",
        "🚀 Projects & More", 
        "📄 Generate Resume"
    ])
    
    with tab1:
        personal_info_form()
    
    with tab2:
        education_form()
    
    with tab3:
        experience_form()
    
    with tab4:
        skills_form()
    
    with tab5:
        projects_form()
        achievements_form()
        additional_sections_form()
    
    with tab6:
        display_generation_section()

if __name__ == "__main__":
    main()
