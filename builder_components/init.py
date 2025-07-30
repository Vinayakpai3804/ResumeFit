"""
ResumeFit AI Resume Builder Components
Professional LaTeX-powered resume creation with enhanced UI

This module provides all the necessary components for the resume builder:
- Configuration and setup utilities
- Professional CSS styling
- Session state management
- Form components for data input
- PDF generation capabilities
- Navigation and UI elements
"""

# Core configuration and setup
from .config import (
    configure_resume_builder, 
    get_latex_handler, 
    get_project_root
)

# Styling and UI
from .styles import load_modern_professional_css

# Session management
from .session import (
    initialize_session_state, 
    safe_text_input, 
    safe_text_area
)

# Navigation components
from .navigation import create_enhanced_navigation_sidebar

# Form components
from .forms import (
    personal_info_form,
    education_form,
    experience_form,
    skills_form
)

# Additional sections
from .sections import (
    projects_form,
    achievements_form,
    additional_sections_form
)

# PDF generation
from .generator import (
    generate_resume_pdf,
    display_generation_section
)

__version__ = "1.0.0"
__author__ = "ResumeFit AI Team"

# Export all public components
__all__ = [
    # Configuration
    'configure_resume_builder',
    'get_latex_handler',
    'get_project_root',
    
    # Styling
    'load_modern_professional_css',
    
    # Session management
    'initialize_session_state',
    'safe_text_input',
    'safe_text_area',
    
    # Navigation
    'create_enhanced_navigation_sidebar',
    
    # Forms
    'personal_info_form',
    'education_form',
    'experience_form',
    'skills_form',
    
    # Sections
    'projects_form',
    'achievements_form',
    'additional_sections_form',
    
    # Generation
    'generate_resume_pdf',
    'display_generation_section'
]

# Module metadata
COMPONENTS = {
    'config': 'Configuration and LaTeX handler setup',
    'styles': 'Professional CSS styling for resume builder',
    'session': 'Session state management and input helpers',
    'navigation': 'Enhanced sidebar navigation',
    'forms': 'Core form components for data input',
    'sections': 'Additional resume sections and forms',
    'generator': 'PDF generation and download functionality'
}

def get_component_info():
    """Get information about available components"""
    return COMPONENTS

def get_version():
    """Get module version"""
    return __version__
