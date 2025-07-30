import streamlit as st

def display_enhanced_metrics():
    """Display analysis metrics with professional card design"""
    if not st.session_state.analysis_result:
        return
    
    result = st.session_state.analysis_result
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card blue">
            <div class="metric-value blue">{result.get('match_percentage', 0)}%</div>
            <div class="metric-label">Resume Match Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card green">
            <div class="metric-value green">{result.get('overall_score', 0)}/10</div>
            <div class="metric-label">Overall Quality Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card amber">
            <div class="metric-value amber">{len(result.get('found_skills', []))}</div>
            <div class="metric-label">Key Skills Found</div>
        </div>
        """, unsafe_allow_html=True)


def create_welcome_section():
    """Create welcome section using proper Streamlit components instead of raw HTML"""
    # Welcome title using CSS styling
    st.markdown('<h2 class="welcome-title">Welcome to ResumeFit AI</h2>', unsafe_allow_html=True)
    st.markdown('<p class="welcome-subtitle">Get AI-powered insights to optimize your resume for any job role</p>', unsafe_allow_html=True)
    
    # Create step cards using Streamlit columns and containers
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.markdown("""
            <div class="step-card">
                <div class="step-number">1</div>
                <h3 style="color: var(--text-primary); font-size: 1.2rem; font-weight: 600; margin-bottom: 0.75rem;">Upload Resume</h3>
                <p style="color: var(--text-secondary); line-height: 1.6; margin: 0; font-size: 0.95rem;">Upload your resume in PDF, DOCX, or TXT format and let our AI extract and analyze the content.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown("""
            <div class="step-card">
                <div class="step-number">2</div>
                <h3 style="color: var(--text-primary); font-size: 1.2rem; font-weight: 600; margin-bottom: 0.75rem;">Set Target Role</h3>
                <p style="color: var(--text-secondary); line-height: 1.6; margin: 0; font-size: 0.95rem;">Enter your target job title to get role-specific analysis and tailored improvement suggestions.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        with st.container():
            st.markdown("""
            <div class="step-card">
                <div class="step-number">3</div>
                <h3 style="color: var(--text-primary); font-size: 1.2rem; font-weight: 600; margin-bottom: 0.75rem;">Get AI Insights</h3>
                <p style="color: var(--text-secondary); line-height: 1.6; margin: 0; font-size: 0.95rem;">Receive comprehensive analysis with match scores, strengths, improvements, and chat with AI assistant.</p>
            </div>
            """, unsafe_allow_html=True)


def create_main_upload_section():
    """Create the main upload section in the center of the page"""
    from utils.resume_processor import ResumeProcessor
    
    st.markdown("""
    <div class="upload-section">
        <h2>📤 Upload Your Resume</h2>
        <p style="text-align: center; color: var(--text-secondary); font-size: 1rem; margin-bottom: 1.5rem;">
            Upload your resume in PDF, DOCX, or TXT format to get started
        </p>
    """, unsafe_allow_html=True)
    
    # File upload with enhanced styling
    uploaded_file = st.file_uploader(
        "Choose your resume file",
        type=["pdf", "txt", "docx"],
        help="Supported formats: PDF, DOCX, TXT (Max size: 10MB)",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        with st.spinner("🔄 Processing your resume..."):
            try:
                resume_processor = ResumeProcessor()
                resume_text = resume_processor.extract_text(uploaded_file)
                if resume_text:
                    st.session_state.resume_text = resume_text
                    st.markdown("""
                    <div class="success-message">
                        ✅ <strong>Resume processed successfully!</strong><br>
                        Your resume has been analyzed and is ready for job role matching.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show preview
                    with st.expander("👀 Resume Preview", expanded=False):
                        preview_text = resume_text[:800] + "..." if len(resume_text) > 800 else resume_text
                        st.text_area("Resume Content", preview_text, height=200, disabled=True)
                        st.caption(f"📊 Total characters: {len(resume_text):,}")
                else:
                    st.markdown("""
                    <div class="error-message">
                        ❌ <strong>Processing Failed</strong><br>
                        Unable to extract text from your resume. Please try a different file.
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="error-message">
                    ❌ <strong>Error:</strong> {str(e)}<br>
                    Please try uploading a different file or contact support.
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def create_job_role_section():
    """Create the job role input section"""
    st.markdown("""
    <div class="section-divider">
        <h3>🎯 Target Job Role</h3>
        <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
            Enter the specific job title or role you're targeting for better analysis results
        </p>
    """, unsafe_allow_html=True)
    
    job_role = st.text_input(
        "Target Job Title",
        value=st.session_state.job_role,
        placeholder="e.g., Senior Software Engineer, Data Scientist, Product Manager, Marketing Director",
        help="Be as specific as possible for more accurate analysis"
    )
    
    if job_role != st.session_state.job_role:
        st.session_state.job_role = job_role
    
    # Industry context (optional)
    col1, col2 = st.columns(2)
    with col1:
        industry = st.selectbox(
            "Industry (Optional)",
            ["Select industry...", "Technology", "Finance", "Healthcare", "Marketing", 
             "Consulting", "Education", "Retail", "Manufacturing", "Other"],
            help="Helps provide industry-specific insights"
        )
    
    with col2:
        experience_level = st.selectbox(
            "Experience Level",
            ["Select level...", "Entry Level (0-2 years)", "Mid Level (3-5 years)", 
             "Senior Level (6-10 years)", "Executive Level (10+ years)"],
            help="Helps tailor feedback to your career stage"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)


def create_analysis_section():
    """Create the analysis button section"""
    from utils.llm_handler import LLMHandler
    
    st.markdown("""
    <div class="section-divider">
        <h3>🧠 AI Analysis</h3>
    """, unsafe_allow_html=True)
    
    # Check requirements
    requirements_met = st.session_state.resume_text and st.session_state.job_role
    
    if not st.session_state.resume_text:
        st.markdown("""
        <div class="warning-message">
            ⚠️ <strong>Resume Required</strong><br>
            Please upload your resume above to continue.
        </div>
        """, unsafe_allow_html=True)
    
    if not st.session_state.job_role:
        st.markdown("""
        <div class="warning-message">
            ⚠️ <strong>Job Role Required</strong><br>
            Please enter your target job role above to continue.
        </div>
        """, unsafe_allow_html=True)
    
    if requirements_met:
        st.markdown("""
        <div class="success-message">
            ✅ <strong>Ready for Analysis</strong><br>
            All requirements met. Click below to start your AI-powered resume analysis.
        </div>
        """, unsafe_allow_html=True)
    
    # Analysis button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Analyze My Resume", 
                    type="primary", 
                    use_container_width=True,
                    disabled=not requirements_met):
            if requirements_met:
                with st.spinner("🤖 AI is analyzing your resume... This may take a moment."):
                    try:
                        llm_handler = LLMHandler()
                        result = llm_handler.analyze_resume_comprehensive(
                            st.session_state.resume_text,
                            st.session_state.job_role
                        )
                        st.session_state.analysis_result = result
                        st.session_state.analysis_complete = True
                        
                        st.markdown("""
                        <div class="success-message">
                            ✅ <strong>Analysis Complete!</strong><br>
                            Your resume analysis is ready. Scroll down to view detailed results.
                        </div>
                        """, unsafe_allow_html=True)
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.markdown(f"""
                        <div class="error-message">
                            ❌ <strong>Analysis Failed</strong><br>
                            {str(e)}
                        </div>
                        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def create_main_header():
    """Create the main header section"""
    st.markdown("""
    <div class="main-header">
        <h1>🎯 ResumeFit AI</h1>
        <p>Transform your career with AI-powered resume analysis and personalized feedback</p>
    </div>
    """, unsafe_allow_html=True)
