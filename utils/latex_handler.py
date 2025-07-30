import os
import tempfile
import subprocess
from typing import Dict, Any, Optional, List
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProfessionalLaTeXHandler:
    """Premium LaTeX handler using Anubhav Singh's template"""
    
    def __init__(self):
        logger.info("Professional LaTeX Handler initialized with Anubhav Singh template")
    
    def generate_resume_pdf(self, data: Dict[str, Any]) -> Optional[bytes]:
        """Generate premium quality PDF with Anubhav Singh's template"""
        try:
            logger.info("Generating resume with Anubhav Singh template")
            
            # Clean and validate data
            cleaned_data = self._clean_and_validate_data(data)
            
            # Generate LaTeX content with smart section handling
            latex_content = self._generate_anubhav_latex(cleaned_data)
            
            # Compile to PDF
            pdf_bytes = self._compile_latex_premium(latex_content)
            
            logger.info("Premium resume PDF generated successfully")
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Resume generation failed: {str(e)}")
            raise Exception(f"Failed to generate PDF: {str(e)}")
    
    def _clean_and_validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced data cleaning with smart validation"""
        cleaned = {}
        
        # Personal info with enhanced validation
        personal = data.get('personal', {})
        cleaned['personal'] = {
            'full_name': self._clean_text(personal.get('full_name', '')),
            'email': self._clean_text(personal.get('email', '')),
            'phone': self._clean_text(personal.get('phone', '')),
            'linkedin': self._clean_text(personal.get('linkedin', '')),
            'github': self._clean_text(personal.get('github', '')),
            'website': self._clean_text(personal.get('website', '')),
            'location': self._clean_text(personal.get('location', '')),
            'summary': self._clean_text(personal.get('summary', ''))
        }
        
        # Only include sections that have meaningful content
        cleaned['education'] = self._filter_valid_entries(
            data.get('education', []), 
            required_fields=['degree', 'institution']
        )
        
        cleaned['experience'] = self._filter_valid_entries(
            data.get('experience', []), 
            required_fields=['job_title', 'company']
        )
        
        cleaned['projects'] = self._filter_valid_entries(
            data.get('projects', []), 
            required_fields=['name']
        )
        
        # Handle skills with smart filtering
        skills = data.get('skills', {})
        cleaned['skills'] = {}
        for key, value in skills.items():
            if value:
                if isinstance(value, list):
                    skill_list = [self._clean_text(str(v)) for v in value if v]
                    if skill_list:
                        cleaned['skills'][key] = skill_list
                else:
                    clean_value = self._clean_text(str(value))
                    if clean_value:
                        cleaned['skills'][key] = clean_value
        
        # Other sections - only include if they have content
        cleaned['achievements'] = self._filter_valid_entries(
            data.get('achievements', []), 
            required_fields=['title']
        )
        
        cleaned['publications'] = self._filter_valid_entries(
            data.get('publications', []), 
            required_fields=['title']
        )
        
        cleaned['certifications'] = self._filter_valid_entries(
            data.get('certifications', []), 
            required_fields=['name']
        )
        
        cleaned['languages'] = self._filter_valid_entries(
            data.get('languages', []), 
            required_fields=['language']
        )
        
        interests = data.get('interests', [])
        cleaned['interests'] = [self._clean_text(str(i)) for i in interests if i and str(i).strip()]
        
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
    
    def _escape_latex_premium(self, text: str) -> str:
        """Premium LaTeX escaping"""
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
    
    def _format_bullet_points(self, text: str) -> List[str]:
        """Smart bullet point formatting"""
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
    
    def _generate_header_section(self, personal: Dict) -> str:
        """Generate the header section - NO LINKS"""
        name = self._escape_latex_premium(personal['full_name'])
        email = self._escape_latex_premium(personal.get('email', ''))
        phone = self._escape_latex_premium(personal.get('phone', ''))
        website = self._escape_latex_premium(personal.get('website', ''))
        github = self._escape_latex_premium(personal.get('github', ''))
        
        # NO LINKS - just display text
        return f"""\\begin{{tabular*}}{{\\textwidth}}{{l@{{\\extracolsep{{\\fill}}}}r}}
  \\textbf{{{{\\LARGE {name}}}}} & Email: {email}\\\\
  Portfolio: {website} & Mobile:~~~{phone} \\\\
  Github: ~~{github} \\\\
\\end{{tabular*}}"""
    
    def _generate_education_section(self, education_data: List[Dict]) -> str:
        """Generate education section"""
        if not education_data:
            return ""
        
        section_content = "\\section{~~Education}\n  \\resumeSubHeadingListStart\n"
        
        for edu in education_data:
            institution = self._escape_latex_premium(edu['institution'])
            location = self._escape_latex_premium(edu.get('location', ''))
            degree = self._escape_latex_premium(edu['degree'])
            gpa = self._escape_latex_premium(edu.get('gpa', ''))
            
            # Format dates
            start_date = edu.get('start_date', '')
            end_date = edu.get('end_date', '')
            graduation_year = edu.get('graduation_year', '')
            
            if graduation_year:
                date_str = graduation_year
            elif start_date and end_date:
                date_str = f"{start_date} - {end_date}"
            elif start_date:
                date_str = f"{start_date} - Present"
            else:
                date_str = ""
            
            degree_line = degree
            if gpa:
                degree_line += f";  GPA: {gpa}"
            
            section_content += f"""    \\resumeSubheading
      {{{institution}}}{{{location}}}
      {{{degree_line}}}{{{date_str}}}"""
            
            # Add relevant courses if available
            if edu.get('relevant_courses'):
                courses = self._escape_latex_premium(edu['relevant_courses'])
                section_content += f"""
      {{\\scriptsize \\textit{{ \\footnotesize{{\\newline{{}}\\textbf{{Courses:}} {courses}}}}}}}"""
            
            section_content += "\n"
        
        section_content += "    \\resumeSubHeadingListEnd\n\n"
        return section_content
    
    def _generate_skills_section(self, skills_data: Dict) -> str:
        """Generate skills section with FIXED ALIGNMENT"""
        if not skills_data:
            return ""
        
        section_content = "\\vspace{-5pt}\n\\section{Skills Summary}\n\t\\resumeSubHeadingListStart\n"
        
        skill_mapping = {
            'languages': ('Languages', '~~~~~~'),
            'frameworks': ('Frameworks', '~~~~'),
            'tools': ('Tools', '~~~~~~~~~~~~~~'),  # Fixed alignment for Tools
            'databases': ('Platforms', '~~~~~~~'),
            'technical_skills': ('Technical', '~~~~~~~'),
            'soft_skills': ('Soft Skills', '~~~~~~~')
        }
        
        for key, (label, spacing) in skill_mapping.items():
            if skills_data.get(key):
                if isinstance(skills_data[key], list):
                    skills_list = ', '.join([self._escape_latex_premium(skill) for skill in skills_data[key]])
                else:
                    skills_list = self._escape_latex_premium(str(skills_data[key]))
                
                if skills_list:
                    section_content += f"\t\\resumeSubItem{{{label}}}{{{spacing}{skills_list}}}\n"
        
        section_content += "\n\\resumeSubHeadingListEnd\n"
        return section_content
    
    def _generate_experience_section(self, experience_data: List[Dict]) -> str:
        """Generate experience section with proper spacing between entries"""
        if not experience_data:
            return ""
        
        section_content = "\\vspace{-5pt}\n\\section{Experience}\n  \\resumeSubHeadingListStart\n"
        
        for i, exp in enumerate(experience_data):
            # Add proper spacing between entries (not too close)
            if i > 0:
                section_content += "\\vspace{10pt}\n"  # Increased from -5pt to 10pt for better spacing
            
            job_title = self._escape_latex_premium(exp['job_title'])
            company = self._escape_latex_premium(exp['company'])
            location = self._escape_latex_premium(exp.get('location', ''))
            
            # Format dates
            start_date = exp.get('start_date', '')
            end_date = exp.get('end_date', '')
            
            if start_date and end_date:
                date_str = f"{start_date} - {end_date}"
            elif start_date:
                date_str = f"{start_date} - Present"
            else:
                date_str = ""
            
            section_content += f"""    \\resumeSubheading{{{company}}}{{{location}}}
    {{{job_title}}}{{{date_str}}}"""
            
            # Add description with ATS-friendly bullet points
            if exp.get('description'):
                section_content += "\n    \\resumeItemListStart\n"
                bullet_items = self._format_bullet_points(exp['description'])
                
                for item in bullet_items:
                    if item.strip():
                        # Use resumeItemWithoutTitle for clean ATS-friendly bullets
                        section_content += f"        \\resumeItemWithoutTitle{{{self._escape_latex_premium(item.strip())}}}\n"
                
                section_content += "      \\resumeItemListEnd\n"
            
            section_content += "\n"
        
        section_content += "\\resumeSubHeadingListEnd\n\n"
        return section_content
    
    def _generate_projects_section(self, projects_data: List[Dict]) -> str:
        """Generate projects section with proper spacing between entries - NO LINKS"""
        if not projects_data:
            return ""
        
        section_content = "\\vspace{-5pt}\n\\section{Projects}\n\\resumeSubHeadingListStart\n"
        
        for i, project in enumerate(projects_data):
            # Add proper spacing between entries
            if i > 0:
                section_content += "\\vspace{10pt}\n"  # Increased from 2pt to 10pt for consistency
            
            name = self._escape_latex_premium(project['name'])
            technologies = self._escape_latex_premium(project.get('technologies', ''))
            
            # Format dates
            start_date = project.get('start_date', '')
            end_date = project.get('end_date', '')
            
            if start_date and end_date:
                date_str = f"{start_date} - {end_date}"
            elif start_date:
                date_str = f"{start_date} - Present"
            else:
                date_str = ""
            
            # Use the standard resumeSubheading format like experience
            section_content += f"""    \\resumeSubheading{{{name}}}{{{date_str}}}
    {{Technologies: {technologies}}}{{}}"""
            
            # Add description with ATS-friendly bullet points
            if project.get('description'):
                section_content += "\n    \\resumeItemListStart\n"
                bullet_items = self._format_bullet_points(project['description'])
                
                for item in bullet_items:
                    if item.strip():
                        # Use resumeItemWithoutTitle for clean ATS-friendly bullets
                        section_content += f"        \\resumeItemWithoutTitle{{{self._escape_latex_premium(item.strip())}}}\n"
                
                section_content += "      \\resumeItemListEnd\n"
            
            section_content += "\n"
        
        section_content += "\\resumeSubHeadingListEnd\n\n"
        return section_content
    
    def _generate_publications_section(self, publications_data: List[Dict]) -> str:
        """Generate publications section"""
        if not publications_data:
            return ""
        
        section_content = "\\vspace{-5pt}\n\\section{Publications}\n\\resumeSubHeadingListStart\n"
        
        for i, pub in enumerate(publications_data):
            if i > 0:
                section_content += "\\vspace{8pt}\n"  # Consistent spacing for publications
            
            title = self._escape_latex_premium(pub['title'])
            description = ""
            
            # Build description
            if pub.get('venue'):
                description += f"Published in {self._escape_latex_premium(pub['venue'])}"
            
            if pub.get('year'):
                if description:
                    description += f", {pub['year']}"
                else:
                    description += f"Published in {pub['year']}"
            
            if pub.get('authors'):
                if description:
                    description += f". Authors: {self._escape_latex_premium(pub['authors'])}"
                else:
                    description += f"Authors: {self._escape_latex_premium(pub['authors'])}"
            
            section_content += f"\\resumeSubItem{{{title}}}{{{description}}}\n"
        
        section_content += "\\resumeSubHeadingListEnd\n"
        return section_content
    
    def _generate_achievements_section(self, achievements_data: List[Dict]) -> str:
        """Generate achievements section"""
        if not achievements_data:
            return ""
        
        section_content = "\\vspace{-5pt}\n\\section{Honors and Awards}\n\\begin{description}[font=$\\bullet$]\n"
        
        for achievement in achievements_data:
            title = self._escape_latex_premium(achievement['title'])
            date = achievement.get('date', '')
            organization = achievement.get('organization', '')
            
            # Build achievement line
            achievement_line = title
            if organization:
                achievement_line += f" at {self._escape_latex_premium(organization)}"
            if date:
                achievement_line += f" - {date}"
            
            section_content += f"\\item {{{achievement_line}}}\n\\vspace{{-5pt}}\n"
        
        section_content += "\\end{description}\n\n"
        return section_content
    
    def _generate_certifications_section(self, certifications_data: List[Dict]) -> str:
        """Generate certifications section"""
        if not certifications_data:
            return ""
        
        section_content = "\\vspace{-5pt}\n\\section{Certifications}\n\\resumeSubHeadingListStart\n"
        
        for i, cert in enumerate(certifications_data):
            if i > 0:
                section_content += "\\vspace{8pt}\n"  # Consistent spacing for certifications
            
            name = self._escape_latex_premium(cert['name'])
            issuer = self._escape_latex_premium(cert.get('issuer', ''))
            date = cert.get('date', '')
            
            description = ""
            if issuer:
                description += f"Issued by {issuer}"
            if date:
                if description:
                    description += f", {date}"
                else:
                    description += f"Issued in {date}"
            
            section_content += f"\\resumeSubItem{{{name}}}{{{description}}}\n"
        
        section_content += "\\resumeSubHeadingListEnd\n"
        return section_content
    
    def _generate_languages_section(self, languages_data: List[Dict]) -> str:
        """Generate languages section as part of skills"""
        if not languages_data:
            return ""
        
        language_entries = []
        for lang in languages_data:
            language = self._escape_latex_premium(lang['language'])
            proficiency = self._escape_latex_premium(lang.get('proficiency', 'Conversational'))
            language_entries.append(f"{language} ({proficiency})")
        
        if language_entries:
            languages_text = ', '.join(language_entries)
            return f"\t\\resumeSubItem{{Languages}}{{~~~~~~{languages_text}}}\n"
        
        return ""
    
    def _generate_anubhav_latex(self, data: Dict[str, Any]) -> str:
        """Generate the complete LaTeX document using Anubhav Singh's template"""
        personal = data['personal']
        
        # Header content - NO LINKS
        header_info = self._generate_header_section(personal)
        
        # Generate sections only if they have content
        sections = []
        
        # ADD PROFESSIONAL SUMMARY SECTION - THIS WAS MISSING
        if personal.get('summary') and personal['summary'].strip():
            summary_section = f"""
\\section{{Professional Summary}}
{self._escape_latex_premium(personal['summary'])}

"""
            sections.append(summary_section)
        
        if data['education']:
            sections.append(self._generate_education_section(data['education']))
        
        # Skills section (including languages) - FIXED ALIGNMENT
        skills_section = ""
        if data['skills'] or data['languages']:
            skills_section = self._generate_skills_section(data['skills'])
            # Add languages to skills section if available
            if data['languages']:
                lang_line = self._generate_languages_section(data['languages'])
                if lang_line:
                    skills_section = skills_section.replace("\\resumeSubHeadingListEnd", lang_line + "\n\\resumeSubHeadingListEnd")
            sections.append(skills_section)
        
        if data['experience']:
            sections.append(self._generate_experience_section(data['experience']))
        
        if data['projects']:
            sections.append(self._generate_projects_section(data['projects']))
        
        if data['publications']:
            sections.append(self._generate_publications_section(data['publications']))
        
        if data['achievements']:
            sections.append(self._generate_achievements_section(data['achievements']))
        
        if data['certifications']:
            sections.append(self._generate_certifications_section(data['certifications']))
        
        # Combine all sections
        all_sections = "".join(sections)
        
        # Complete LaTeX document using Anubhav Singh's template
        return f"""%------------------------
% Resume Template
% Author : Anubhav Singh
% Github : https://github.com/xprilion
% License : MIT
%------------------------

\\documentclass[a4paper,20pt]{{article}}

\\usepackage{{latexsym}}
\\usepackage[empty]{{fullpage}}
\\usepackage{{titlesec}}
\\usepackage{{marvosym}}
\\usepackage[usenames,dvipsnames]{{color}}
\\usepackage{{verbatim}}
\\usepackage{{enumitem}}
\\usepackage[hidelinks]{{hyperref}}
\\usepackage{{fancyhdr}}

\\pagestyle{{fancy}}
\\fancyhf{{}} % clear all header and footer fields
\\fancyfoot{{}}
\\renewcommand{{\\headrulewidth}}{{0pt}}
\\renewcommand{{\\footrulewidth}}{{0pt}}

% Adjust margins
\\addtolength{{\\oddsidemargin}}{{-0.530in}}
\\addtolength{{\\evensidemargin}}{{-0.375in}}
\\addtolength{{\\textwidth}}{{1in}}
\\addtolength{{\\topmargin}}{{-.45in}}
\\addtolength{{\\textheight}}{{1in}}

\\urlstyle{{rm}}

\\raggedbottom
\\raggedright
\\setlength{{\\tabcolsep}}{{0in}}

% Sections formatting
\\titleformat{{\\section}}{{
  \\vspace{{-10pt}}\\scshape\\raggedright\\large
}}{{}}{{0em}}{{}}[\\color{{black}}\\titlerule \\vspace{{-6pt}}]

%-------------------------
% Custom commands
\\newcommand{{\\resumeItem}}[2]{{
  \\item\\small{{
    \\textbf{{#1}}{{: #2 \\vspace{{-2pt}}}}
  }}
}}

\\newcommand{{\\resumeItemWithoutTitle}}[1]{{
  \\item\\small{{
    {{#1 \\vspace{{-2pt}}}}
  }}
}}

\\newcommand{{\\resumeSubheading}}[4]{{
  \\vspace{{-1pt}}\\item
    \\begin{{tabular*}}{{0.97\\textwidth}}{{l@{{\\extracolsep{{\\fill}}}}r}}
      \\textbf{{#1}} & #2 \\\\
      \\textit{{#3}} & \\textit{{#4}} \\\\
    \\end{{tabular*}}\\vspace{{-5pt}}
}}

\\newcommand{{\\resumeSubItem}}[2]{{\\resumeItem{{#1}}{{#2}}\\vspace{{-3pt}}}}

\\renewcommand{{\\labelitemii}}{{$\\circ$}}

\\newcommand{{\\resumeSubHeadingListStart}}{{\\begin{{itemize}}[leftmargin=*]}}
\\newcommand{{\\resumeSubHeadingListEnd}}{{\\end{{itemize}}}}
\\newcommand{{\\resumeItemListStart}}{{\\begin{{itemize}}}}
\\newcommand{{\\resumeItemListEnd}}{{\\end{{itemize}}\\vspace{{-5pt}}}}

%-----------------------------
%%%%%%  CV STARTS HERE  %%%%%%

\\begin{{document}}

%----------HEADING-----------------
{header_info}

%-----------SECTIONS-----------------
{all_sections}
\\end{{document}}"""
    
    def _compile_latex_premium(self, latex_content: str) -> bytes:
        """Premium LaTeX compilation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            tex_file = os.path.join(temp_dir, 'resume.tex')
            
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            try:
                # Two-pass compilation for better results
                for pass_num in range(2):
                    result = subprocess.run([
                        'pdflatex', 
                        '-interaction=nonstopmode',
                        '-output-directory', temp_dir,
                        tex_file
                    ], capture_output=True, text=True, timeout=120)
                
                pdf_file = os.path.join(temp_dir, 'resume.pdf')
                if os.path.exists(pdf_file) and os.path.getsize(pdf_file) > 0:
                    with open(pdf_file, 'rb') as f:
                        return f.read()
                else:
                    error_details = self._parse_latex_errors(result.stderr, result.stdout)
                    raise Exception(f"LaTeX compilation failed: {error_details}")
                    
            except subprocess.TimeoutExpired:
                raise Exception("LaTeX compilation timed out")
            except FileNotFoundError:
                raise Exception("pdflatex not found")
    
    def _parse_latex_errors(self, stderr: str, stdout: str) -> str:
        """Enhanced LaTeX error parsing"""
        error_text = stderr + stdout
        
        if "! LaTeX Error" in error_text:
            import re
            matches = re.findall(r'! LaTeX Error: (.+)', error_text)
            if matches:
                return matches[0]
        
        if "! Undefined control sequence" in error_text:
            return "Undefined control sequence - check LaTeX syntax"
        
        lines = error_text.split('\n')
        for line in lines:
            if line.strip() and ('error' in line.lower() or '!' in line):
                return line.strip()
        
        return "Unknown LaTeX compilation error"

# For compatibility
FreePDFHandler = ProfessionalLaTeXHandler
