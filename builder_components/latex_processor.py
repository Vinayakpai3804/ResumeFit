import re
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class LaTeXDataProcessor:
    """Handles data cleaning, validation, and LaTeX text processing for Anubhav Singh template"""
    
    def clean_and_validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced data cleaning matching Anubhav Singh template structure"""
        cleaned = {}
        
        # Personal info with enhanced validation
        personal = data.get('personal_info', {})
        cleaned['personal'] = {
            'full_name': self._clean_text(personal.get('full_name', '')),
            'email': self._clean_text(personal.get('email', '')),
            'phone': self._clean_text(personal.get('phone', '')),
            'linkedin': self._clean_text(personal.get('linkedin', '')),
            'github': self._clean_text(personal.get('github', '')),
            'website': self._clean_text(personal.get('website', '')),
            'location': self._clean_text(personal.get('location', '')),
            'summary': self._clean_text(personal.get('professional_summary', ''))
        }
        
        # Education - matching template format
        cleaned['education'] = self._filter_valid_entries(
            data.get('education', []), 
            required_fields=['degree', 'school']
        )
        
        # Experience - matching template format  
        cleaned['experience'] = self._filter_valid_entries(
            data.get('experience', []), 
            required_fields=['job_title', 'company']
        )
        
        # Projects - matching template format
        cleaned['projects'] = self._filter_valid_entries(
            data.get('projects', []), 
            required_fields=['name']
        )
        
        # Skills mapping to match template structure
        cleaned['skills'] = {}
        form_data = data.get('personal_info', {})
        
        # Map to template skill categories
        skill_mappings = {
            'technical_skills': 'Languages',
            'tools_technologies': 'Tools', 
            'soft_skills': 'Soft Skills',
            'certifications': 'Platforms'
        }
        
        for form_field, template_key in skill_mappings.items():
            skill_value = form_data.get(form_field, '')
            if skill_value and skill_value.strip():
                if isinstance(skill_value, str):
                    skill_items = [item.strip() for item in skill_value.replace(',', '|').replace(';', '|').split('|') if item.strip()]
                    cleaned['skills'][template_key] = skill_items
                else:
                    cleaned['skills'][template_key] = [self._clean_text(str(skill_value))]
        
        # Additional template sections
        cleaned['achievements'] = self._filter_valid_entries(
            data.get('achievements', []), 
            required_fields=['title']
        )
        
        cleaned['publications'] = self._filter_valid_entries(
            data.get('publications', []), 
            required_fields=['title']
        )
        
        cleaned['languages'] = self._filter_valid_entries(
            data.get('languages', []), 
            required_fields=['language']
        )
        
        return cleaned
    
    def _clean_text(self, text: str) -> str:
        """Enhanced text cleaning"""
        if not text:
            return ""
        text = str(text).strip()
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def _filter_valid_entries(self, entries: List[Dict], required_fields: List[str]) -> List[Dict]:
        """Filter entries that have all required fields with meaningful content"""
        valid_entries = []
        for entry in entries:
            if all(entry.get(field) and str(entry.get(field)).strip() for field in required_fields):
                cleaned_entry = {}
                for key, value in entry.items():
                    if value:
                        cleaned_entry[key] = self._clean_text(str(value))
                valid_entries.append(cleaned_entry)
        return valid_entries
    
    def escape_latex_premium(self, text: str) -> str:
        """Premium LaTeX escaping for Anubhav Singh template"""
        if not text:
            return ""
        
        text = str(text)
        escape_map = {
            '\\': r'\textbackslash{}',
            '{': r'\{',
            '}': r'\}',
            '$': r'\$',
            '&': r'\&',
            '%': r'\%',
            '#': r'\#',
            '^': r'\textasciicircum{}',
            '_': r'\_',
            '~': r'\textasciitilde{}',
        }
        
        for char, escaped in escape_map.items():
            text = text.replace(char, escaped)
        return text
    
    def format_bullet_points(self, text: str) -> List[str]:
        """Smart bullet point formatting for template"""
        if not text:
            return []
        
        bullet_patterns = [
            r'^\s*[•\-\*]\s+',
            r'^\s*\d+\.\s+',
            r'^\s*[a-zA-Z]\)\s+'
        ]
        
        lines = text.split('\n')
        formatted_items = []
        current_item = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            is_new_bullet = any(re.match(pattern, line) for pattern in bullet_patterns)
            
            if is_new_bullet:
                if current_item:
                    formatted_items.append(current_item)
                for pattern in bullet_patterns:
                    line = re.sub(pattern, '', line)
                current_item = line
            else:
                if current_item:
                    current_item += " " + line
                else:
                    current_item = line
        
        if current_item:
            formatted_items.append(current_item)
        
        return formatted_items
