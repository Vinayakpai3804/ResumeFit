import streamlit as st

def create_enhanced_navigation_sidebar():
    """Create enhanced navigation sidebar matching main.py design - exact same as original"""
    with st.sidebar:
        # Brand Header - Matching main.py
        st.markdown("""
        <div class="sidebar-brand">
            <div class="icon">📝</div>
            <h1>Resume Builder</h1>
            <p>Professional LaTeX Templates</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Main Features Section
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown("### 🚀 Main Features")
        
        if st.button("📊 Resume Analysis", use_container_width=True):
            st.switch_page("resume_analyser.py")
        
        if st.button("📝 Resume Builder", use_container_width=True, disabled=True):
            pass  # Already on builder page
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Progress tracker
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown("### 📋 Build Progress")
        
        progress_items = [
            ("👤 Personal Info", bool(st.session_state.form_data.get('full_name', ''))),
            ("🎓 Education", bool(st.session_state.education_entries[0].get('degree', '') if st.session_state.education_entries else False)),
            ("💼 Experience", bool(st.session_state.experience_entries[0].get('job_title', '') if st.session_state.experience_entries else False)),
            ("🛠️ Skills", bool(st.session_state.form_data.get('technical_skills', ''))),
            ("🚀 Projects", bool(st.session_state.project_entries[0].get('name', '') if st.session_state.project_entries else False))
        ]
        
        for item, completed in progress_items:
            status = "✅" if completed else "⭕"
            st.markdown(f"{status} {item}")
        
        completion = sum(1 for _, completed in progress_items if completed)
        st.progress(completion / len(progress_items))
        st.caption(f"Progress: {completion}/{len(progress_items)} sections completed")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick tips
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown("### 💡 Quick Tips")
        
        tips = [
            "Use action verbs in descriptions",
            "Quantify achievements with numbers",
            "Keep bullet points concise",
            "Include relevant keywords",
            "Proofread for errors"
        ]
        
        for tip in tips:
            st.markdown(f"• {tip}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Template info
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown("### 📄 Template Info")
        
        st.markdown("""
        **Professional LaTeX Template**
        • ATS-friendly formatting
        • Clean, modern design  
        • Optimized for readability
        • Industry-standard layout
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)
