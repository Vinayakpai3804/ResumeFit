import streamlit as st
from datetime import datetime
from typing import Dict, List, Any
from .session import safe_text_input, safe_text_area

def personal_info_form():
    """Enhanced personal information form - exact same as original"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<h3>👤 Personal Information</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.form_data['full_name'] = safe_text_input(
            "Full Name *", 
            "full_name",
            placeholder="John Doe"
        )
        
        st.session_state.form_data['phone'] = safe_text_input(
            "Phone Number", 
            "phone",
            placeholder="+1 (555) 123-4567"
        )
        
        st.session_state.form_data['linkedin'] = safe_text_input(
            "LinkedIn URL", 
            "linkedin",
            placeholder="https://linkedin.com/in/johndoe"
        )
    
    with col2:
        st.session_state.form_data['email'] = safe_text_input(
            "Email Address *", 
            "email",
            placeholder="john.doe@email.com"
        )
        
        st.session_state.form_data['location'] = safe_text_input(
            "Location", 
            "location",
            placeholder="City, State"
        )
        
        st.session_state.form_data['website'] = safe_text_input(
            "Website/Portfolio", 
            "website",
            placeholder="https://johndoe.com"
        )
    
    st.session_state.form_data['professional_summary'] = safe_text_area(
        "Professional Summary",
        "professional_summary",
        placeholder="Write a compelling 2-3 sentence summary highlighting your key qualifications...",
        height=120
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

def education_form():
    """Enhanced education form with multiple entries - exact same as original"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<h3>🎓 Education</h3>', unsafe_allow_html=True)
    
    if 'education_entries' not in st.session_state:
        st.session_state.education_entries = [{}]
    
    for i, education in enumerate(st.session_state.education_entries):
        with st.expander(f"Education {i+1}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                education['degree'] = st.text_input(
                    "Degree",
                    key=f"edu_degree_{i}",
                    placeholder="Bachelor of Science in Computer Science",
                    value=education.get('degree', '')
                )
                
                education['school'] = st.text_input(
                    "School/University",
                    key=f"edu_school_{i}",
                    placeholder="University of Technology",
                    value=education.get('school', '')
                )
            
            with col2:
                education['graduation_date'] = st.text_input(
                    "Graduation Date",
                    key=f"edu_date_{i}",
                    placeholder="May 2023",
                    value=education.get('graduation_date', '')
                )
                
                education['gpa'] = st.text_input(
                    "GPA (Optional)",
                    key=f"edu_gpa_{i}",
                    placeholder="3.8/4.0",
                    value=education.get('gpa', '')
                )
            
            education['relevant_coursework'] = st.text_area(
                "Relevant Coursework (Optional)",
                key=f"edu_coursework_{i}",
                placeholder="Data Structures, Algorithms, Database Systems...",
                height=80,
                value=education.get('relevant_coursework', '')
            )
            
            if i > 0:
                if st.button(f"Remove Education {i+1}", key=f"remove_edu_{i}"):
                    st.session_state.education_entries.pop(i)
                    st.rerun()
    
    if st.button("Add Another Education"):
        st.session_state.education_entries.append({})
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def experience_form():
    """Enhanced experience form with multiple entries - exact same as original"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<h3>💼 Professional Experience</h3>', unsafe_allow_html=True)
    
    if 'experience_entries' not in st.session_state:
        st.session_state.experience_entries = [{}]
    
    for i, experience in enumerate(st.session_state.experience_entries):
        with st.expander(f"Experience {i+1}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                experience['job_title'] = st.text_input(
                    "Job Title",
                    key=f"exp_title_{i}",
                    placeholder="Software Engineer",
                    value=experience.get('job_title', '')
                )
                
                experience['company'] = st.text_input(
                    "Company",
                    key=f"exp_company_{i}",
                    placeholder="Tech Solutions Inc.",
                    value=experience.get('company', '')
                )
            
            with col2:
                experience['start_date'] = st.text_input(
                    "Start Date",
                    key=f"exp_start_{i}",
                    placeholder="Jan 2022",
                    value=experience.get('start_date', '')
                )
                
                experience['end_date'] = st.text_input(
                    "End Date",
                    key=f"exp_end_{i}",
                    placeholder="Present or Dec 2023",
                    value=experience.get('end_date', '')
                )
            
            experience['location'] = st.text_input(
                "Location (Optional)",
                key=f"exp_location_{i}",
                placeholder="San Francisco, CA",
                value=experience.get('location', '')
            )
            
            experience['description'] = st.text_area(
                "Job Description & Achievements",
                key=f"exp_desc_{i}",
                placeholder="• Developed web applications using React and Node.js\n• Improved system performance by 25%\n• Led team of 3 developers...",
                height=150,
                value=experience.get('description', ''),
                help="Use bullet points to describe your responsibilities and achievements. Include metrics when possible."
            )
            
            if i > 0:
                if st.button(f"Remove Experience {i+1}", key=f"remove_exp_{i}"):
                    st.session_state.experience_entries.pop(i)
                    st.rerun()
    
    if st.button("Add Another Experience"):
        st.session_state.experience_entries.append({})
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def skills_form():
    """Enhanced skills form - exact same as original"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<h3>🛠️ Skills</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.form_data['technical_skills'] = safe_text_area(
            "Technical Skills",
            "technical_skills",
            placeholder="Python, JavaScript, React, Node.js, SQL, Git...",
            height=100
        )
        
        st.session_state.form_data['tools_technologies'] = safe_text_area(
            "Tools & Technologies",
            "tools_technologies",
            placeholder="Docker, AWS, Jenkins, MongoDB, PostgreSQL...",
            height=100
        )
    
    with col2:
        st.session_state.form_data['soft_skills'] = safe_text_area(
            "Soft Skills",
            "soft_skills",
            placeholder="Leadership, Communication, Problem-solving, Team collaboration...",
            height=100
        )
        
        st.session_state.form_data['certifications'] = safe_text_area(
            "Certifications",
            "certifications",
            placeholder="AWS Certified Solutions Architect, Google Cloud Professional...",
            height=100
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
