import streamlit as st
from datetime import datetime
from typing import Dict, List, Any
from .config import get_latex_handler

def generate_resume_pdf():
    """Generate resume PDF using exact Anubhav Singh template"""
    try:
        pdf_handler = get_latex_handler()
        
        if not pdf_handler:
            st.error("PDF generation service is not available")
            return None
        
        # Collect all form data
        resume_data = {
            'personal_info': st.session_state.form_data,
            'education': st.session_state.education_entries,
            'experience': st.session_state.experience_entries,
            'projects': st.session_state.project_entries,
            'achievements': st.session_state.achievement_entries,
            'publications': st.session_state.publication_entries,
            'languages': st.session_state.language_entries
        }
        
        # Generate PDF with exact template
        with st.spinner("🔄 Generating your professional resume using Anubhav Singh template..."):
            pdf_content = pdf_handler.generate_resume_pdf(resume_data)
            
            if pdf_content:
                st.session_state.generated_pdf = pdf_content
                st.session_state.generation_time = datetime.now()
                return pdf_content
            else:
                st.error("Failed to generate PDF")
                return None
                
    except Exception as e:
        st.error(f"Error generating resume: {str(e)}")
        return None

def display_generation_section():
    """Display PDF generation section"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<h3>📄 Generate Professional Resume</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: var(--light-slate); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <strong>🎯 Template:</strong> Anubhav Singh Professional LaTeX Template<br>
        <strong>📏 Format:</strong> A4 Paper, 20pt Font, Professional Spacing<br>
        <strong>✨ Quality:</strong> ATS-Optimized, Clean Design, Industry Standard
    </div>
    """, unsafe_allow_html=True)
    
    # Check if minimum required fields are filled
    required_fields = [
        st.session_state.form_data.get('full_name', ''),
        st.session_state.form_data.get('email', ''),
    ]
    
    has_education = any(edu.get('degree', '') for edu in st.session_state.education_entries)
    has_experience = any(exp.get('job_title', '') for exp in st.session_state.experience_entries)
    
    if not all(required_fields):
        st.warning("⚠️ Please fill in your name and email address to generate resume.")
    elif not (has_education or has_experience):
        st.warning("⚠️ Please add at least one education entry or work experience.")
    else:
        st.success("✅ Ready to generate your professional resume with Anubhav Singh template!")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Generate Professional Resume", type="primary", use_container_width=True):
                pdf_content = generate_resume_pdf()
                
                if pdf_content:
                    st.success("✅ Professional resume generated successfully!")
                    st.balloons()
    
    # Display download button if PDF was generated
    if st.session_state.generated_pdf:
        st.markdown("---")
        st.markdown("### 📥 Download Your Professional Resume")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            filename = f"resume_{st.session_state.form_data.get('full_name', 'professional').replace(' ', '_').lower()}.pdf"
            
            st.download_button(
                label="📄 Download Professional Resume",
                data=st.session_state.generated_pdf,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True
            )
        
        generation_time = st.session_state.generation_time
        if generation_time:
            st.caption(f"Generated on: {generation_time.strftime('%B %d, %Y at %I:%M %p')}")
            st.caption("📋 Template: Anubhav Singh Professional LaTeX Resume")
    
    st.markdown('</div>', unsafe_allow_html=True)
