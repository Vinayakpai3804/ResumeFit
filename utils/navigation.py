import streamlit as st

def create_enhanced_navigation_sidebar():
    """Create enhanced navigation sidebar with resume builder and analysis features"""
    with st.sidebar:
        # Brand Header
        st.markdown("""
        <div class="sidebar-brand">
            <div class="icon">🎯</div>
            <h1>ResumeFit AI</h1>
            <p>Professional Resume Tools</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Main Features Section
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown("### 🚀 Main Features")
        
        # Two main buttons - Resume Analysis and Resume Builder
        if st.button("📊 Resume Analysis", use_container_width=True, help="Analyze your existing resume"):
            st.rerun()
        
        if st.button("📝 Resume Builder", use_container_width=True, help="Create a new professional resume"):
            try:
                st.switch_page("pages/resume_builder.py")
            except:
                st.info("Resume builder feature available!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # About Resume Builder Section
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown("### 📝 About Resume Builder")
        
        st.markdown("""
        <div style="color: var(--text-secondary); font-size: 0.9rem; line-height: 1.6;">
        <p><strong>Create Professional Resumes</strong></p>
        <ul style="padding-left: 1rem; margin: 0.5rem 0;">
            <li>📄 LaTeX-powered templates</li>
            <li>🎯 ATS-optimized formatting</li>
            <li>⚡ Instant PDF generation</li>
            <li>🛠️ Customizable sections</li>
            <li>📱 Mobile-friendly builder</li>
        </ul>
        <p style="margin-top: 1rem;"><em>Build your resume from scratch with our professional templates and AI guidance.</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Analysis Status
        if st.session_state.analysis_result:
            st.markdown('<div class="nav-section">', unsafe_allow_html=True)
            st.markdown("### 📊 Current Analysis")
            
            result = st.session_state.analysis_result
            
            st.markdown(f"""
            <div style="background: var(--surface-elevated); padding: 1rem; border-radius: 12px; margin: 0.5rem 0;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <span>✅</span>
                    <strong style="color: var(--text-primary);">Analysis Complete</strong>
                </div>
                <div style="color: var(--text-secondary); font-size: 0.9rem;">
                    Score: {result.get('overall_score', 0)}/10 | Match: {result.get('match_percentage', 0)}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Tools & Resources
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown("### 🛠️ Tools & Resources")
        
        st.markdown("""
        <div style="color: var(--text-secondary); font-size: 0.9rem; line-height: 1.6;">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.75rem 0;">
            <span>🧠</span>
            <div>
                <strong>AI Analysis</strong><br>
                <small style="opacity: 0.8;">Smart resume insights</small>
            </div>
        </div>
        
        <div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.75rem 0;">
            <span>💬</span>
            <div>
                <strong>Chat Assistant</strong><br>
                <small style="opacity: 0.8;">Get personalized advice</small>
            </div>
        </div>
        
        <div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.75rem 0;">
            <span>📥</span>
            <div>
                <strong>Export Reports</strong><br>
                <small style="opacity: 0.8;">Download analysis results</small>
            </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Tips Section
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown("### 💡 Pro Tips")
        
        st.markdown("""
        <div style="color: var(--text-muted); font-size: 0.85rem; line-height: 1.6;">
        <div style="margin-bottom: 0.5rem;">• Use action verbs in descriptions</div>
        <div style="margin-bottom: 0.5rem;">• Quantify your achievements</div>
        <div style="margin-bottom: 0.5rem;">• Tailor for each application</div>
        <div style="margin-bottom: 0.5rem;">• Keep formatting consistent</div>
        <div>• Include relevant keywords</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
