import os
import tempfile
import subprocess
import logging
from typing import Dict, Any, Optional, List
from .latex_processor import LaTeXDataProcessor

logger = logging.getLogger(__name__)

class ProfessionalLaTeXHandler:
    """Professional LaTeX handler using EXACT Anubhav Singh template"""
    
    def __init__(self):
        logger.info("Professional LaTeX Handler initialized with Anubhav Singh template")
        self.processor = LaTeXDataProcessor()
    
    def generate_resume_pdf(self, data: Dict[str, Any]) -> Optional[bytes]:
        """Generate PDF using EXACT Anubhav Singh template"""
        try:
            logger.info("Generating resume with Anubhav Singh template")
            
            # Clean and validate data
            cleaned_data = self.processor.clean_and_validate_data(data)
            
            # Generate LaTeX content with exact template
            latex_content = self._generate_anubhav_latex(cleaned_data)
            
            # Compile to PDF
            pdf_bytes = self._compile_latex_premium(latex_content)
            
            logger.info("Premium resume PDF generated successfully")
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Resume generation failed: {str(e)}")
            raise Exception(f"Failed to generate PDF: {str(e)}")
    
    def _generate_header_section(self, personal: Dict) -> str:
        """Generate header exactly like Anubhav Singh template"""
        name = self.processor.escape_latex_premium(personal['full_name'])
        email = self.processor.escape_latex_premium(personal.get('email', ''))
        phone = self.processor.escape_latex_premium(personal.get('phone', ''))
        website = self.processor.escape_latex_premium(personal.get('website', ''))
        github = self.processor.escape_latex_premium(personal.get('github', ''))
        
        return f"""\\begin{{tabular*}}{{\\textwidth}}{{l@{{\\extracolsep{{\\fill}}}}r}}
  \\textbf{{{{\\LARGE {name}}}}} & Email: {email}\\\\
  Portfolio: {website} & Mobile:~~~{phone} \\\\
  Github: ~~{github} \\\\
\\end{{tabular*}}"""
    
    def _generate_education_section(self, education_data: List[Dict]) -> str:
        """Generate education section exactly like template"""
        if not education_data:
            return ""
        
        section_content = "%-----------EDUCATION-----------------\n\\section{~~Education}\n  \\resumeSubHeadingListStart\n"
        
        for edu in education_data:
            institution = self.processor.escape_latex_premium(edu.get('school', ''))
            location = self.processor.escape_latex_premium(edu.get('location', ''))
            degree = self.processor.escape_latex_premium(edu.get('degree', ''))
            gpa = edu.get('gpa', '')
            
            # Format dates
            graduation_date = edu.get('graduation_date', '')
            start_date = edu.get('start_date', '')
            end_date = edu.get('end_date', '')
            
            if graduation_date:
                date_str = graduation_date
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
            if edu.get('relevant_coursework'):
                courses = self.processor.escape_latex_premium(edu['relevant_coursework'])
                section_content += f"""
      {{\\scriptsize \\textit{{ \\footnotesize{{\\newline{{}}\\textbf{{Courses:}} {courses}}}}}}}"""
            
            section_content += "\n"
        
        section_content += "    \\resumeSubHeadingListEnd\n    \n"
        return section_content
    
    def _generate_skills_section(self, skills_data: Dict) -> str:
        """Generate skills section exactly like template"""
        if not skills_data:
            return ""
        
        section_content = "\\vspace{-5pt}\n\\section{Skills Summary}\n\\resumeSubHeadingListStart\n"
        
        # Template skill order and spacing
        skill_template = {
            'Languages': ('Languages', '~~~~~~'),
            'Frameworks': ('Frameworks', '~~~~'),
            'Tools': ('Tools', '~~~~~~~~~~~~~~'),
            'Platforms': ('Platforms', '~~~~~~~'),
            'Soft Skills': ('Soft Skills', '~~~~~~~')
        }
        
        for key, (label, spacing) in skill_template.items():
            if skills_data.get(key):
                skill_value = skills_data[key]
                
                if isinstance(skill_value, list):
                    skills_list = ', '.join([self.processor.escape_latex_premium(skill) for skill in skill_value if skill])
                else:
                    skills_list = self.processor.escape_latex_premium(str(skill_value))
                
                if skills_list:
                    section_content += f"\\resumeSubItem{{{label}}}{{{spacing}{skills_list}}}\n"
        
        section_content += "\n\\resumeSubHeadingListEnd\n"
        return section_content
    
    def _generate_experience_section(self, experience_data: List[Dict]) -> str:
        """Generate experience section with FIXED description formatting and increased spacing"""
        if not experience_data:
            return ""
        
        section_content = "\\vspace{-5pt}\n\\section{Experience}\n  \\resumeSubHeadingListStart\n"
        
        for i, exp in enumerate(experience_data):
            if i > 0:
                section_content += "\\vspace{30pt}\n"  # INCREASED spacing between entries
            
            job_title = self.processor.escape_latex_premium(exp.get('job_title', ''))
            company = self.processor.escape_latex_premium(exp.get('company', ''))
            location = self.processor.escape_latex_premium(exp.get('location', ''))
            
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
            
            # FIXED: Add description WITHOUT "Achievement" title - just display the description
            if exp.get('description'):
                section_content += "\n    \\resumeItemListStart\n"
                bullet_items = self.processor.format_bullet_points(exp['description'])
                
                for item in bullet_items:
                    if item.strip():
                        # CHANGED: Use resumeItemWithoutTitle to display only the description
                        section_content += f"        \\resumeItemWithoutTitle{{{self.processor.escape_latex_premium(item.strip())}}}\n"
                
                section_content += "      \\resumeItemListEnd\n"
            
            section_content += "\\vspace{20pt}\n"  # INCREASED spacing after each entry
        
        section_content += "\n\\resumeSubHeadingListEnd\n"
        return section_content
    
    def _generate_projects_section(self, projects_data: List[Dict]) -> str:
        """Generate projects section with increased spacing"""
        if not projects_data:
            return ""
        
        section_content = "%-----------PROJECTS-----------------\n\\vspace{-5pt}\n\\section{Projects}\n\\resumeSubHeadingListStart\n"
        
        for i, project in enumerate(projects_data):
            if i > 0:
                section_content += "\\vspace{20pt}\n"  # INCREASED spacing between projects
            
            name = self.processor.escape_latex_premium(project.get('name', ''))
            technologies = self.processor.escape_latex_premium(project.get('technologies', ''))
            description = self.processor.escape_latex_premium(project.get('description', ''))
            
            # Format dates
            date = project.get('date', '')
            
            # Template format for projects
            project_title = f"{name} ({technologies})" if technologies else name
            project_desc = f"{description} ({date})" if date else description
            
            section_content += f"\\resumeSubItem{{{project_title}}}{{{project_desc}}}\n"
        
        section_content += "\\resumeSubHeadingListEnd\n"
        return section_content
    
    def _generate_publications_section(self, publications_data: List[Dict]) -> str:
        """Generate publications section exactly like template"""
        if not publications_data:
            return ""
        
        section_content = "\\vspace{-5pt}\n\\section{Publications}\n\\resumeSubHeadingListStart\n"
        
        for i, pub in enumerate(publications_data):
            if i > 0:
                section_content += "\\vspace{2pt}\n"
            
            title = self.processor.escape_latex_premium(pub.get('title', ''))
            journal = self.processor.escape_latex_premium(pub.get('journal', ''))
            date = pub.get('date', '')
            
            pub_title = f"{title} ({journal})" if journal else title
            pub_desc = f"Published in {date}" if date else ""
            
            section_content += f"\\resumeSubItem{{{pub_title}}}{{{pub_desc}}}\n"
        
        section_content += "\\resumeSubHeadingListEnd\n"
        return section_content
    
    def _generate_achievements_section(self, achievements_data: List[Dict]) -> str:
        """Generate achievements section exactly like template"""
        if not achievements_data:
            return ""
        
        section_content = "\\vspace{-5pt}\n%-----------Awards-----------------\n\\section{Honors and Awards}\n\\begin{description}[font=$\\bullet$]\n"
        
        for achievement in achievements_data:
            title = self.processor.escape_latex_premium(achievement.get('title', ''))
            date = achievement.get('date', '')
            
            achievement_line = f"{title} - {date}" if date else title
            section_content += f"\\item {{{achievement_line}}}\n\\vspace{{-5pt}}\n"
        
        section_content += "\n\\end{description}\n"
        return section_content
    
    def _generate_anubhav_latex(self, data: Dict[str, Any]) -> str:
        """Generate complete LaTeX document using EXACT Anubhav Singh template"""
        personal = data['personal']
        
        # Header content
        header_info = self._generate_header_section(personal)
        
        # Generate sections in template order
        sections = []
        
        # Education
        if data['education']:
            sections.append(self._generate_education_section(data['education']))
        
        # Skills
        if data['skills']:
            sections.append(self._generate_skills_section(data['skills']))
        
        # Experience
        if data['experience']:
            sections.append(self._generate_experience_section(data['experience']))
        
        # Projects
        if data['projects']:
            sections.append(self._generate_projects_section(data['projects']))
        
        # Publications
        if data['publications']:
            sections.append(self._generate_publications_section(data['publications']))
        
        # Achievements
        if data['achievements']:
            sections.append(self._generate_achievements_section(data['achievements']))
        
        # Combine all sections
        all_sections = "".join(sections)
        
        # Complete LaTeX document - EXACT template
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
\\usepackage[pdftex]{{hyperref}}
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
