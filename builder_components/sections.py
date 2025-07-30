import streamlit as st
from typing import Dict, List, Any
from .session import safe_text_input, safe_text_area

def projects_form():
    """Enhanced projects form with multiple entries - exact same as original"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<h3>🚀 Projects</h3>', unsafe_allow_html=True)
    
    if 'project_entries' not in st.session_state:
        st.session_state.project_entries = [{}]
    
    for i, project in enumerate(st.session_state.project_entries):
        with st.expander(f"Project {i+1}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                project['name'] = st.text_input(
                    "Project Name",
                    key=f"proj_name_{i}",
                    placeholder="E-commerce Web Application",
                    value=project.get('name', '')
                )
                
                project['technologies'] = st.text_input(
                    "Technologies Used",
                    key=f"proj_tech_{i}",
                    placeholder="React, Node.js, MongoDB, AWS",
                    value=project.get('technologies', '')
                )
            
            with col2:
                project['date'] = st.text_input(
                    "Date",
                    key=f"proj_date_{i}",
                    placeholder="Mar 2023 - Jun 2023",
                    value=project.get('date', '')
                )
                
                project['link'] = st.text_input(
                    "Project Link (Optional)",
                    key=f"proj_link_{i}",
                    placeholder="https://github.com/username/project",
                    value=project.get('link', '')
                )
            
            project['description'] = st.text_area(
                "Project Description",
                key=f"proj_desc_{i}",
                placeholder="• Built a full-stack e-commerce platform\n• Implemented user authentication and payment processing\n• Achieved 99% uptime...",
                height=120,
                value=project.get('description', '')
            )
            
            if i > 0:
                if st.button(f"Remove Project {i+1}", key=f"remove_proj_{i}"):
                    st.session_state.project_entries.pop(i)
                    st.rerun()
    
    if st.button("Add Another Project"):
        st.session_state.project_entries.append({})
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def achievements_form():
    """Enhanced achievements form - exact same as original"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<h3>🏆 Achievements & Awards</h3>', unsafe_allow_html=True)
    
    if 'achievement_entries' not in st.session_state:
        st.session_state.achievement_entries = [{}]
    
    for i, achievement in enumerate(st.session_state.achievement_entries):
        with st.expander(f"Achievement {i+1}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                achievement['title'] = st.text_input(
                    "Achievement Title",
                    key=f"ach_title_{i}",
                    placeholder="Employee of the Year",
                    value=achievement.get('title', '')
                )
            
            with col2:
                achievement['date'] = st.text_input(
                    "Date",
                    key=f"ach_date_{i}",
                    placeholder="2023",
                    value=achievement.get('date', '')
                )
            
            achievement['description'] = st.text_area(
                "Description",
                key=f"ach_desc_{i}",
                placeholder="Awarded for outstanding performance and leadership...",
                height=80,
                value=achievement.get('description', '')
            )
            
            if i > 0:
                if st.button(f"Remove Achievement {i+1}", key=f"remove_ach_{i}"):
                    st.session_state.achievement_entries.pop(i)
                    st.rerun()
    
    if st.button("Add Another Achievement"):
        st.session_state.achievement_entries.append({})
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def additional_sections_form():
    """Additional sections form - exact same as original"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<h3>📚 Additional Sections</h3>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Publications", "Languages", "Volunteer Work"])
    
    with tab1:
        if 'publication_entries' not in st.session_state:
            st.session_state.publication_entries = [{}]
        
        for i, pub in enumerate(st.session_state.publication_entries):
            with st.expander(f"Publication {i+1}", expanded=True):
                pub['title'] = st.text_input(
                    "Publication Title",
                    key=f"pub_title_{i}",
                    value=pub.get('title', '')
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    pub['journal'] = st.text_input(
                        "Journal/Conference",
                        key=f"pub_journal_{i}",
                        value=pub.get('journal', '')
                    )
                with col2:
                    pub['date'] = st.text_input(
                        "Date",
                        key=f"pub_date_{i}",
                        value=pub.get('date', '')
                    )
                
                if i > 0:
                    if st.button(f"Remove Publication {i+1}", key=f"remove_pub_{i}"):
                        st.session_state.publication_entries.pop(i)
                        st.rerun()
        
        if st.button("Add Publication"):
            st.session_state.publication_entries.append({})
            st.rerun()
    
    with tab2:
        if 'language_entries' not in st.session_state:
            st.session_state.language_entries = [{}]
        
        for i, lang in enumerate(st.session_state.language_entries):
            with st.expander(f"Language {i+1}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    lang['language'] = st.text_input(
                        "Language",
                        key=f"lang_name_{i}",
                        value=lang.get('language', '')
                    )
                with col2:
                    lang['proficiency'] = st.selectbox(
                        "Proficiency",
                        ["Native", "Fluent", "Conversational", "Basic"],
                        key=f"lang_prof_{i}",
                        index=["Native", "Fluent", "Conversational", "Basic"].index(lang.get('proficiency', 'Conversational'))
                    )
                
                if i > 0:
                    if st.button(f"Remove Language {i+1}", key=f"remove_lang_{i}"):
                        st.session_state.language_entries.pop(i)
                        st.rerun()
        
        if st.button("Add Language"):
            st.session_state.language_entries.append({})
            st.rerun()
    
    with tab3:
        st.session_state.form_data['volunteer_work'] = safe_text_area(
            "Volunteer Experience",
            "volunteer_work",
            placeholder="• Community Outreach Coordinator - Local Food Bank (2022-Present)\n• Organized monthly food drives serving 200+ families",
            height=120
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
