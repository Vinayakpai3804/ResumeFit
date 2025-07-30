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

from utils.latex_handler import ProfessionalLaTeXHandler as FreePDFHandler

# Page configuration
st.set_page_config(
    page_title="Professional Resume Builder - ResumeFit AI",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_professional_css():
    """Load enhanced professional CSS styling"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --success-gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        --warning-gradient: linear-gradient(135deg, #ff6b6b 0%, #ffa500 100%);
        --info-gradient: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        --dark-surface: rgba(15, 23, 42, 0.95);
        --medium-surface: rgba(30, 41, 59, 0.9);
        --light-surface: rgba(51, 65, 85, 0.8);
        --accent-color: #10b981;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --border-color: rgba(16, 185, 129, 0.3);
        --shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    }
    
    html, body, .stApp, .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: var(--primary-gradient);
        padding: 4rem 2rem;
        border-radius: 32px;
        margin-bottom: 3rem;
        text-align: center;
        color: white;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 4.5rem;
        font-weight: 900;
        letter-spacing: -3px;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        margin: 1.5rem 0 0 0;
        font-size: 1.5rem;
        opacity: 0.95;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    .form-section {
        background: var(--medium-surface);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 2rem 0;
        border: 2px solid var(--border-color);
        box-shadow: var(--shadow);
    }
    
    .section-card {
        background: var(--light-surface);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
    }
    
    .template-card {
        background: var(--medium-surface);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 3px solid var(--border-color);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .template-card:hover {
        border-color: var(--accent-color);
        transform: translateY(-4px);
    }
    
    .template-card.selected {
        border-color: var(--accent-color);
        background: linear-gradient(135deg, var(--medium-surface), rgba(16, 185, 129, 0.1));
    }
    
    .success-message {
        background: var(--success-gradient);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        font-weight: 600;
        box-shadow: var(--shadow);
    }
    
    .error-message {
        background: var(--warning-gradient);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        font-weight: 600;
        box-shadow: var(--shadow);
    }
    
    .info-message {
        background: var(--info-gradient);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        font-weight: 600;
        box-shadow: var(--shadow);
    }
    
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 1.2rem 2.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }
    
    .stTextInput > div > input, .stTextArea > div > textarea {
        background: var(--dark-surface) !important;
        color: var(--text-primary) !important;
        border-radius: 16px !important;
        border: 2px solid var(--border-color) !important;
        font-size: 1rem !important;
        padding: 1rem 1.5rem !important;
    }
    
    .stTextInput > div > input:focus, .stTextArea > div > textarea:focus {
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.15) !important;
    }
    
    .stSelectbox > div > div {
        background: var(--dark-surface) !important;
        color: var(--text-primary) !important;
        border-radius: 16px !important;
        border: 2px solid var(--border-color) !important;
    }
    
    .metric-card {
        background: var(--light-surface);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid var(--border-color);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: var(--accent-color);
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .professional-badge {
        display: inline-block;
        background: var(--accent-color);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .stProgress > div > div > div {
        background: var(--primary-gradient);
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state with proper data types"""
    defaults = {
        'form_data': {},
        'education_entries': [{}],
        'experience_entries': [{}],
        'project_entries': [{}],
        'achievement_entries': [{}],
        'publication_entries': [{}],
        'certification_entries': [{}],
        'language_entries': [{}],
        'selected_template': None,
        'generated_pdf': None,
        'generation_time': None,
        'last_generated': None,
        'form_progress': 0,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def calculate_form_progress(data: Dict[str, Any]) -> int:
    """Calculate form completion progress"""
    total_sections = 10
    completed_sections = 0
    
    # Check personal info
    personal = data.get('personal', {})
    if personal.get('full_name') and personal.get('email'):
        completed_sections += 1
    
    # Check other sections
    sections = ['education', 'experience', 'projects', 'achievements', 
                'publications', 'certifications', 'languages', 'interests']
    
    for section in sections:
        section_data = data.get(section, [])
        if section_data and any(section_data):
            completed_sections += 1
    
    # Check skills
    skills = data.get('skills', {})
    if skills and any(skills.values()):
        completed_sections += 1
    
    return int((completed_sections / total_sections) * 100)

def safe_text_input(label: str, key: str, placeholder: str = "", help_text: str = "") -> str:
    """Safe text input that handles session state properly"""
    return st.text_input(
        label, 
        key=key, 
        placeholder=placeholder, 
        help=help_text if help_text else None
    )

def safe_text_area(label: str, key: str, placeholder: str = "", height: int = 100, help_text: str = "") -> str:
    """Safe text area that handles session state properly"""
    return st.text_area(
        label, 
        key=key, 
        placeholder=placeholder, 
        height=height,
        help=help_text if help_text else None
    )

def personal_info_form():
    """Personal information form"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### 👤 Personal Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        full_name = safe_text_input("Full Name *", "full_name", "e.g., John Doe")
        email = safe_text_input("Email Address *", "email", "e.g., john.doe@email.com")
        phone = safe_text_input("Phone Number", "phone", "e.g., +1 (555) 123-4567")
        
    with col2:
        linkedin = safe_text_input("LinkedIn Profile", "linkedin", "e.g., linkedin.com/in/johndoe")
        github = safe_text_input("GitHub Profile", "github", "e.g., github.com/johndoe")
        website = safe_text_input("Personal Website", "website", "e.g., johndoe.com")
    
    address = safe_text_input("Address", "address", "e.g., San Francisco, CA")
    summary = safe_text_area("Professional Summary", "summary", 
                             "Write a compelling 2-3 sentence summary highlighting your key qualifications...", 120)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return {
        'full_name': full_name,
        'email': email,
        'phone': phone,
        'linkedin': linkedin,
        'github': github,
        'website': website,
        'address': address,
        'summary': summary
    }

def education_form():
    """Education form with dynamic entries"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### 🎓 Education")
    
    education_data = []
    
    for i, entry in enumerate(st.session_state.education_entries):
        st.markdown(f'<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f"**Education Entry {i+1}**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            degree = safe_text_input("Degree", f"degree_{i}", "e.g., Bachelor of Computer Science")
            institution = safe_text_input("Institution", f"institution_{i}", "e.g., Stanford University")
            
        with col2:
            graduation_year = safe_text_input("Graduation Year", f"grad_year_{i}", "e.g., 2024")
            gpa = safe_text_input("GPA (optional)", f"gpa_{i}", "e.g., 3.8/4.0")
        
        location = safe_text_input("Location", f"edu_location_{i}", "e.g., Stanford, CA")
        relevant_courses = safe_text_area("Relevant Courses", f"courses_{i}", 
                                        "List key courses separated by commas...", 80)
        
        education_data.append({
            'degree': degree,
            'institution': institution,
            'graduation_year': graduation_year,
            'gpa': gpa,
            'location': location,
            'relevant_courses': relevant_courses
        })
        
        if i > 0:
            if st.button(f"🗑️ Remove Entry {i+1}", key=f"remove_edu_{i}"):
                st.session_state.education_entries.pop(i)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("➕ Add Education Entry"):
        st.session_state.education_entries.append({})
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    return education_data

def experience_form():
    """Experience form with dynamic entries"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### 💼 Work Experience")
    
    experience_data = []
    
    for i, entry in enumerate(st.session_state.experience_entries):
        st.markdown(f'<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f"**Experience Entry {i+1}**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            job_title = safe_text_input("Job Title", f"job_title_{i}", "e.g., Software Engineer")
            company = safe_text_input("Company", f"company_{i}", "e.g., Google")
            
        with col2:
            start_date = safe_text_input("Start Date", f"start_date_{i}", "e.g., Jan 2023")
            end_date = safe_text_input("End Date", f"end_date_{i}", "e.g., Present")
        
        location = safe_text_input("Location", f"exp_location_{i}", "e.g., San Francisco, CA")
        description = safe_text_area("Job Description & Achievements", f"description_{i}", 
                                    "Describe your key responsibilities and achievements...", 150)
        
        experience_data.append({
            'job_title': job_title,
            'company': company,
            'start_date': start_date,
            'end_date': end_date,
            'location': location,
            'description': description
        })
        
        if i > 0:
            if st.button(f"🗑️ Remove Entry {i+1}", key=f"remove_exp_{i}"):
                st.session_state.experience_entries.pop(i)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("➕ Add Experience Entry"):
        st.session_state.experience_entries.append({})
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    return experience_data

def projects_form():
    """Projects form with dynamic entries"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### 🚀 Projects")
    
    projects_data = []
    
    for i, entry in enumerate(st.session_state.project_entries):
        st.markdown(f'<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f"**Project Entry {i+1}**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = safe_text_input("Project Name", f"project_name_{i}", "e.g., E-commerce Platform")
            technologies = safe_text_input("Technologies Used", f"technologies_{i}", "e.g., React, Node.js, MongoDB")
        
        with col2:
            start_date = safe_text_input("Start Date", f"proj_start_{i}", "e.g., Jan 2023")
            end_date = safe_text_input("End Date", f"proj_end_{i}", "e.g., Mar 2023")
        
        github_link = safe_text_input("GitHub/Demo Link", f"github_link_{i}", "e.g., github.com/username/project")
        description = safe_text_area("Project Description", f"project_desc_{i}", 
                                    "Describe your project, role, and key achievements...", 120)
        
        projects_data.append({
            'name': name,
            'technologies': technologies,
            'start_date': start_date,
            'end_date': end_date,
            'github_link': github_link,
            'description': description
        })
        
        if i > 0:
            if st.button(f"🗑️ Remove Entry {i+1}", key=f"remove_proj_{i}"):
                st.session_state.project_entries.pop(i)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("➕ Add Project Entry"):
        st.session_state.project_entries.append({})
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    return projects_data

def achievements_form():
    """Achievements form with dynamic entries"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### 🏆 Achievements & Awards")
    
    achievements_data = []
    
    for i, entry in enumerate(st.session_state.achievement_entries):
        st.markdown(f'<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f"**Achievement Entry {i+1}**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            title = safe_text_input("Achievement Title", f"achievement_title_{i}", "e.g., Winner - TechHack 2024")
            organization = safe_text_input("Organization", f"achievement_org_{i}", "e.g., Stanford University")
        
        with col2:
            date = safe_text_input("Date", f"achievement_date_{i}", "e.g., March 2024")
        
        description = safe_text_area("Description", f"achievement_desc_{i}", 
                                    "Brief description of the achievement...", 100)
        
        achievements_data.append({
            'title': title,
            'organization': organization,
            'date': date,
            'description': description
        })
        
        if i > 0:
            if st.button(f"🗑️ Remove Entry {i+1}", key=f"remove_ach_{i}"):
                st.session_state.achievement_entries.pop(i)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("➕ Add Achievement Entry"):
        st.session_state.achievement_entries.append({})
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    return achievements_data

def publications_form():
    """Publications form with dynamic entries"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### 📚 Publications")
    
    publications_data = []
    
    for i, entry in enumerate(st.session_state.publication_entries):
        st.markdown(f'<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f"**Publication Entry {i+1}**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            title = safe_text_input("Publication Title", f"pub_title_{i}", "e.g., Deep Learning for Computer Vision")
            authors = safe_text_input("Authors", f"pub_authors_{i}", "e.g., J. Doe, A. Smith, B. Johnson")
            venue = safe_text_input("Venue/Journal", f"pub_venue_{i}", "e.g., NeurIPS 2024")
        
        with col2:
            year = safe_text_input("Year", f"pub_year_{i}", "e.g., 2024")
            doi = safe_text_input("DOI", f"pub_doi_{i}", "e.g., 10.1000/xyz123")
            url = safe_text_input("URL", f"pub_url_{i}", "e.g., https://arxiv.org/abs/2024.12345")
        
        publications_data.append({
            'title': title,
            'authors': authors,
            'venue': venue,
            'year': year,
            'doi': doi,
            'url': url
        })
        
        if i > 0:
            if st.button(f"🗑️ Remove Entry {i+1}", key=f"remove_pub_{i}"):
                st.session_state.publication_entries.pop(i)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("➕ Add Publication Entry"):
        st.session_state.publication_entries.append({})
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    return publications_data

def certifications_form():
    """Certifications form with dynamic entries"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### 🎖️ Certifications")
    
    certifications_data = []
    
    for i, entry in enumerate(st.session_state.certification_entries):
        st.markdown(f'<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f"**Certification Entry {i+1}**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = safe_text_input("Certification Name", f"cert_name_{i}", "e.g., AWS Solutions Architect - Professional")
            issuer = safe_text_input("Issuer", f"cert_issuer_{i}", "e.g., Amazon Web Services")
        
        with col2:
            date = safe_text_input("Issue Date", f"cert_date_{i}", "e.g., April 2024")
            credential_id = safe_text_input("Credential ID", f"cert_id_{i}", "e.g., ABC123XYZ")
        
        certifications_data.append({
            'name': name,
            'issuer': issuer,
            'date': date,
            'credential_id': credential_id
        })
        
        if i > 0:
            if st.button(f"🗑️ Remove Entry {i+1}", key=f"remove_cert_{i}"):
                st.session_state.certification_entries.pop(i)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("➕ Add Certification Entry"):
        st.session_state.certification_entries.append({})
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    return certifications_data

def languages_form():
    """Languages form with dynamic entries"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### 🌐 Languages")
    
    languages_data = []
    
    for i, entry in enumerate(st.session_state.language_entries):
        st.markdown(f'<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f"**Language Entry {i+1}**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            language = safe_text_input("Language", f"lang_name_{i}", "e.g., Spanish")
        
        with col2:
            proficiency = st.selectbox(
                "Proficiency Level", 
                key=f"lang_prof_{i}",
                options=["Native", "Fluent", "Proficient", "Intermediate", "Basic"],
                index=2
            )
        
        languages_data.append({
            'language': language,
            'proficiency': proficiency
        })
        
        if i > 0:
            if st.button(f"🗑️ Remove Entry {i+1}", key=f"remove_lang_{i}"):
                st.session_state.language_entries.pop(i)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("➕ Add Language Entry"):
        st.session_state.language_entries.append({})
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    return languages_data

def skills_form():
    """Skills form with proper string handling"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### 🛠️ Skills & Technologies")
    
    col1, col2 = st.columns(2)
    
    with col1:
        languages_input = safe_text_area("Programming Languages", "prog_langs_input", 
                                        "e.g., Python, JavaScript, Java, C++", 100,
                                        "Separate with commas")
        frameworks_input = safe_text_area("Frameworks & Libraries", "frameworks_input", 
                                        "e.g., React, Django, Express.js, TensorFlow", 100,
                                        "Separate with commas")
        databases_input = safe_text_area("Databases", "databases_input", 
                                       "e.g., PostgreSQL, MongoDB, Redis, MySQL", 100,
                                       "Separate with commas")
    
    with col2:
        tools_input = safe_text_area("Tools & Technologies", "tools_input", 
                                   "e.g., Docker, AWS, Git, Jenkins, Kubernetes", 100,
                                   "Separate with commas")
        technical_input = safe_text_area("Technical Skills", "technical_input", 
                                       "e.g., Machine Learning, DevOps, API Development", 100,
                                       "Separate with commas")
        soft_input = safe_text_area("Soft Skills", "soft_input", 
                                   "e.g., Leadership, Problem Solving, Communication", 100,
                                   "Separate with commas")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Convert strings to lists for processing
    return {
        'languages': [s.strip() for s in languages_input.split(',') if s.strip()],
        'frameworks': [s.strip() for s in frameworks_input.split(',') if s.strip()],
        'databases': [s.strip() for s in databases_input.split(',') if s.strip()],
        'tools': [s.strip() for s in tools_input.split(',') if s.strip()],
        'technical_skills': [s.strip() for s in technical_input.split(',') if s.strip()],
        'soft_skills': [s.strip() for s in soft_input.split(',') if s.strip()]
    }

def interests_form():
    """Interests form"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### 🎯 Interests & Hobbies")
    
    interests_input = safe_text_area("Interests & Hobbies", "interests_input", 
                                    "e.g., Photography, Hiking, Chess, Cooking, Reading", 100,
                                    "Separate with commas")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return [interest.strip() for interest in interests_input.split(',') if interest.strip()]

def template_selector():
    """Template selection interface"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### 🎨 Template Selection")
    
    templates = {
        'jake': {
            'name': "Jake's Clean Resume",
            'description': 'Clean, ATS-friendly single-column design perfect for tech roles',
            'features': ['Single column layout', 'ATS optimized', 'Clean typography', 'Professional sections'],
            'best_for': 'Software Engineers, Data Scientists, Tech Professionals'
        },
        'deedy': {
            'name': 'Deedy Professional',
            'description': 'Modern two-column template with elegant blue accents',
            'features': ['Two column layout', 'Color accents', 'Compact design', 'Modern typography'],
            'best_for': 'Consultants, Finance, Business Professionals'
        },
        'rendercv': {
            'name': 'RenderCV Academic',
            'description': 'Elegant serif template perfect for academic and research positions',
            'features': ['Academic styling', 'Serif typography', 'Publication ready', 'Professional spacing'],
            'best_for': 'Researchers, Academics, PhD candidates'
        }
    }
    
    selected_template = st.radio(
        "Select your preferred template:",
        options=list(templates.keys()),
        format_func=lambda x: f"{templates[x]['name']} - {templates[x]['description']}"
    )
    
    if selected_template:
        template_info = templates[selected_template]
        st.markdown(f"""
        <div class="template-card selected">
            <h4>{template_info['name']}</h4>
            <p>{template_info['description']}</p>
            <div style="margin-top: 1rem;">
                <strong>Best for:</strong> {template_info['best_for']}
            </div>
            <div style="margin-top: 0.5rem;">
                <strong>Features:</strong> {', '.join(template_info['features'])}
            </div>
            <div style="margin-top: 1rem; display: flex; gap: 1rem;">
                <span class="professional-badge">LaTeX Quality</span>
                <span class="professional-badge">ATS Compatible</span>
                <span class="professional-badge">Docker Powered</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    return selected_template

def display_progress_metrics(form_data):
    """Display form completion metrics"""
    progress = calculate_form_progress(form_data)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{progress}%</div>
            <div class="metric-label">Complete</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        sections_filled = sum([
            bool(form_data.get('personal', {}).get('full_name')),
            bool(form_data.get('education', [])),
            bool(form_data.get('experience', [])),
            bool(form_data.get('projects', [])),
            any(form_data.get('skills', {}).values()) if form_data.get('skills') else False,
            bool(form_data.get('achievements', [])),
            bool(form_data.get('publications', [])),
            bool(form_data.get('certifications', [])),
            bool(form_data.get('languages', [])),
            bool(form_data.get('interests', []))
        ])
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{sections_filled}/10</div>
            <div class="metric-label">Sections</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_entries = (
            len(form_data.get('education', [])) +
            len(form_data.get('experience', [])) +
            len(form_data.get('projects', []))
        )
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_entries}</div>
            <div class="metric-label">Total Entries</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        word_count = len(form_data.get('personal', {}).get('summary', '').split())
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{word_count}</div>
            <div class="metric-label">Summary Words</div>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
    try:
        initialize_session_state()
        load_professional_css()
        
        # Header
        st.markdown("""
        <div class="main-header">
            <h1>🏗️ Professional Resume Builder</h1>
            <p>Create authentic LaTeX-quality resumes with industry-standard templates</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("← Back to Main", use_container_width=True):
                try:
                    st.switch_page("main.py")
                except:
                    st.info("Navigation to main page not available. Continue with resume building.")
        
        with col2:
            st.markdown("""
            <div style="text-align: right; margin-top: 10px;">
                <span class="professional-badge">🐳 Docker + LaTeX</span>
                <span class="professional-badge">✨ Professional Quality</span>
                <span class="professional-badge">🆓 Completely Free</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Main tabs
        tab1, tab2, tab3 = st.tabs(["📝 Resume Details", "🎨 Template Selection", "📄 Generate Resume"])
        
        with tab1:
            st.markdown("### Complete Your Professional Resume Information")
            
            # Collect all form data
            personal_data = personal_info_form()
            education_data = education_form()
            experience_data = experience_form()
            projects_data = projects_form()
            skills_data = skills_form()
            achievements_data = achievements_form()
            publications_data = publications_form()
            certifications_data = certifications_form()
            languages_data = languages_form()
            interests_data = interests_form()
            
            # Store in session state
            st.session_state.form_data = {
                'personal': personal_data,
                'education': education_data,
                'experience': experience_data,
                'projects': projects_data,
                'skills': skills_data,
                'achievements': achievements_data,
                'publications': publications_data,
                'certifications': certifications_data,
                'languages': languages_data,
                'interests': interests_data
            }
            
            # Display progress metrics
            display_progress_metrics(st.session_state.form_data)
            
            # Progress bar
            progress = calculate_form_progress(st.session_state.form_data)
            st.progress(progress / 100, text=f"Form Completion: {progress}%")
            
            # Validation
            required_fields = ['full_name', 'email']
            missing_fields = [field for field in required_fields if not personal_data.get(field)]
            
            if missing_fields:
                st.markdown(f"""
                <div class="error-message">
                    ❌ Please fill required fields: {", ".join(missing_fields)}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="success-message">
                    ✅ Required information completed! Ready to proceed to template selection.
                </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("### Select Your Professional Template")
            
            selected_template = template_selector()
            st.session_state.selected_template = selected_template
            
            if selected_template:
                st.markdown("""
                <div class="success-message">
                    ✅ Template selected! Ready for authentic LaTeX PDF generation.
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="info-message">
                    <strong>🎯 Ready to Generate:</strong><br>
                    <strong>📄 Template:</strong> {selected_template.upper()}<br>
                    <strong>⚡ Engine:</strong> Docker + LaTeX Compilation<br>
                    <strong>📊 Quality:</strong> Professional Publication Standard<br>
                    <strong>⏱️ Est. Time:</strong> 3-8 seconds
                </div>
                """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown("### Generate Your Professional Resume")
            
            # Check prerequisites
            if not st.session_state.form_data.get('personal', {}).get('full_name'):
                st.markdown("""
                <div class="error-message">
                    ❌ Please complete the personal information in the "Resume Details" tab first
                </div>
                """, unsafe_allow_html=True)
                st.stop()
            
            if not st.session_state.selected_template:
                st.markdown("""
                <div class="error-message">
                    ❌ Please select a template in the "Template Selection" tab first
                </div>
                """, unsafe_allow_html=True)
                st.stop()
            
            # Display generation status
            progress = calculate_form_progress(st.session_state.form_data)
            
            if progress < 30:
                st.markdown("""
                <div class="error-message">
                    ❌ Resume completion too low. Please fill at least 30% of the form to generate a professional resume.
                </div>
                """, unsafe_allow_html=True)
                st.stop()
            
            # Generation interface
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if st.button("🚀 Generate Professional Resume", type="primary", use_container_width=True):
                    start_time = datetime.now()
                    
                    with st.spinner("🐳 Compiling LaTeX with Docker... Creating your professional resume..."):
                        try:
                            # Initialize PDF handler
                            pdf_handler = FreePDFHandler()
                            
                            # Generate PDF using real LaTeX compilation
                            pdf_data = pdf_handler.generate_resume_pdf(
                                st.session_state.form_data,
                                st.session_state.selected_template
                            )
                            
                            if pdf_data:
                                generation_time = (datetime.now() - start_time).total_seconds()
                                
                                st.session_state.generated_pdf = pdf_data
                                st.session_state.generation_time = generation_time
                                st.session_state.last_generated = datetime.now()
                                
                                st.markdown(f"""
                                <div class="success-message">
                                    ✅ Professional resume generated successfully!<br>
                                    <strong>⏱️ Generation Time:</strong> {generation_time:.2f} seconds<br>
                                    <strong>📄 Template:</strong> {st.session_state.selected_template.upper()}<br>
                                    <strong>🎯 Quality:</strong> Authentic LaTeX compilation
                                </div>
                                """, unsafe_allow_html=True)
                                
                                st.balloons()
                                st.rerun()
                            else:
                                st.markdown("""
                                <div class="error-message">
                                    ❌ Failed to generate resume. Please try again.
                                </div>
                                """, unsafe_allow_html=True)
                        
                        except Exception as e:
                            st.markdown(f"""
                            <div class="error-message">
                                ❌ Generation Error: {str(e)}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown("""
                            <div class="info-message">
                                💡 <strong>Troubleshooting Tips:</strong><br>
                                • Ensure Docker container is running<br>
                                • Check that LaTeX compilation is working<br>
                                • Verify all form fields are properly filled<br>
                                • Try a different template if the issue persists
                            </div>
                            """, unsafe_allow_html=True)
            
            with col2:
                if st.session_state.generated_pdf:
                    # Create safe filename
                    safe_name = re.sub(r'[^\w\s-]', '', st.session_state.form_data['personal']['full_name']).strip()
                    safe_name = re.sub(r'[-\s]+', '_', safe_name)
                    template_name = st.session_state.selected_template.upper()
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{safe_name}_{template_name}_Resume_{timestamp}.pdf"
                    
                    # File size calculation
                    file_size_mb = len(st.session_state.generated_pdf) / (1024 * 1024)
                    
                    st.download_button(
                        label="📥 Download Professional Resume",
                        data=st.session_state.generated_pdf,
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    st.markdown(f"""
                    <div style="text-align: center; margin-top: 1rem;">
                        <strong>📊 File Size:</strong> {file_size_mb:.2f} MB<br>
                        <strong>🕐 Generated:</strong> {st.session_state.last_generated.strftime('%Y-%m-%d %H:%M:%S')}<br>
                        <strong>⚡ Speed:</strong> {st.session_state.generation_time:.2f}s
                    </div>
                    """, unsafe_allow_html=True)
            
            # Additional actions if PDF is generated
            if st.session_state.generated_pdf:
                st.markdown("### 🎉 Resume Generated Successfully!")
                
                st.markdown(f"""
                <div class="info-message">
                    <strong>📄 Your professional resume is ready!</strong><br>
                    <strong>✨ Template:</strong> {st.session_state.selected_template.upper()}<br>
                    <strong>🎯 Quality:</strong> Authentic LaTeX compilation<br>
                    <strong>📊 ATS Compatible:</strong> Professional formatting maintained<br>
                    <strong>💾 Ready for Download:</strong> Click the download button above
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("🔄 Generate New Resume", use_container_width=True):
                        st.session_state.generated_pdf = None
                        st.session_state.generation_time = None
                        st.session_state.last_generated = None
                        st.rerun()
                
                with col2:
                    if st.button("📝 Edit Resume Details", use_container_width=True):
                        st.session_state.generated_pdf = None
                        st.rerun()
                
                with col3:
                    if st.button("🎨 Try Different Template", use_container_width=True):
                        st.session_state.generated_pdf = None
                        st.session_state.selected_template = None
                        st.rerun()
    
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please refresh the page and try again.")

if __name__ == "__main__":
    main()
