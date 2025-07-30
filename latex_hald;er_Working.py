import os
import tempfile
import subprocess
from typing import Dict, Any, Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProfessionalLaTeXHandler:
    """Complete LaTeX handler with robust error handling"""
    
    def __init__(self):
        self.supported_templates = ['jake', 'deedy', 'rendercv']
        logger.info("Professional LaTeX Handler initialized")
    
    def generate_resume_pdf(self, data: Dict[str, Any], template_name: str) -> Optional[bytes]:
        """Generate PDF with comprehensive error handling"""
        try:
            logger.info(f"Generating resume with template: {template_name}")
            
            # Validate template
            if template_name not in self.supported_templates:
                template_name = 'jake'  # Default fallback
            
            # Clean and validate data
            cleaned_data = self._clean_data(data)
            
            # Generate LaTeX content
            latex_content = self._get_template_content(template_name, cleaned_data)
            
            # Debug: Log the generated LaTeX content
            logger.info(f"Generated LaTeX content length: {len(latex_content)}")
            
            # Compile to PDF
            pdf_bytes = self._compile_latex(latex_content)
            
            logger.info("Resume PDF generated successfully")
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Resume generation failed: {str(e)}")
            raise Exception(f"Failed to generate PDF: {str(e)}")
    
    def _clean_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and validate all data"""
        cleaned = {}
        
        # Personal info with safe defaults
        personal = data.get('personal', {})
        cleaned['personal'] = {
            'full_name': str(personal.get('full_name', 'John Doe')),
            'email': str(personal.get('email', 'john.doe@example.com')),
            'phone': str(personal.get('phone', '+1 (555) 123-4567')),
            'linkedin': str(personal.get('linkedin', 'linkedin.com/in/johndoe')),
            'github': str(personal.get('github', 'github.com/johndoe')),
            'website': str(personal.get('website', 'johndoe.com')),
            'address': str(personal.get('address', 'San Francisco, CA')),
            'summary': str(personal.get('summary', 'Professional summary here'))
        }
        
        # Clean sections - only keep valid entries
        cleaned['education'] = [
            edu for edu in data.get('education', [])
            if edu.get('degree') and edu.get('institution')
        ]
        
        cleaned['experience'] = [
            exp for exp in data.get('experience', [])
            if exp.get('job_title') and exp.get('company')
        ]
        
        cleaned['projects'] = [
            proj for proj in data.get('projects', [])
            if proj.get('name')
        ]
        
        # Handle skills properly
        skills = data.get('skills', {})
        cleaned['skills'] = {}
        for key, value in skills.items():
            if value:
                if isinstance(value, list):
                    cleaned['skills'][key] = [str(v) for v in value if v]
                else:
                    cleaned['skills'][key] = str(value)
        
        # Other sections with safe defaults
        cleaned['achievements'] = [
            ach for ach in data.get('achievements', [])
            if ach.get('title')
        ]
        
        cleaned['publications'] = [
            pub for pub in data.get('publications', [])
            if pub.get('title')
        ]
        
        cleaned['certifications'] = [
            cert for cert in data.get('certifications', [])
            if cert.get('name')
        ]
        
        cleaned['languages'] = [
            lang for lang in data.get('languages', [])
            if lang.get('language')
        ]
        
        interests = data.get('interests', [])
        cleaned['interests'] = [str(i) for i in interests if i] if interests else []
        
        return cleaned
    
    def _escape_latex(self, text: str) -> str:
        """Comprehensive LaTeX character escaping"""
        if not text:
            return ""
        
        text = str(text)
        
        # LaTeX special characters - order matters!
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
            '|': r'\textbar{}',
            '<': r'\textless{}',
            '>': r'\textgreater{}',
        }
        
        for char, escaped in escape_map.items():
            text = text.replace(char, escaped)
        
        return text
    
    def _format_education(self, education_data: List[Dict]) -> str:
        """Format education section"""
        if not education_data:
            return "% No education entries\\resumeSubheading{Sample University}{2024}{Bachelor of Science}{City, State}"
        
        entries = []
        for edu in education_data:
            entry = f"\\resumeSubheading{{{self._escape_latex(edu['institution'])}}}" \
                   f"{{{self._escape_latex(edu.get('graduation_year', ''))}}}" \
                   f"{{{self._escape_latex(edu['degree'])}}}" \
                   f"{{{self._escape_latex(edu.get('location', ''))}}}"
            
            details = []
            if edu.get('gpa'):
                details.append(f"GPA: {self._escape_latex(edu['gpa'])}")
            if edu.get('relevant_courses'):
                details.append(f"Relevant Courses: {self._escape_latex(edu['relevant_courses'])}")
            
            if details:
                entry += "\n\\resumeItemListStart\n"
                for detail in details:
                    entry += f"\\resumeItem{{{detail}}}\n"
                entry += "\\resumeItemListEnd"
            
            entries.append(entry)
        
        return "\n".join(entries)
    
    def _format_experience(self, experience_data: List[Dict]) -> str:
        """Format experience section"""
        if not experience_data:
            return "% No experience entries\\resumeSubheading{Sample Position}{2023 -- Present}{Sample Company}{City, State}"
        
        entries = []
        for exp in experience_data:
            dates = f"{self._escape_latex(exp.get('start_date', ''))} -- {self._escape_latex(exp.get('end_date', ''))}"
            
            entry = f"\\resumeSubheading{{{self._escape_latex(exp['job_title'])}}}" \
                   f"{{{dates}}}" \
                   f"{{{self._escape_latex(exp['company'])}}}" \
                   f"{{{self._escape_latex(exp.get('location', ''))}}}"
            
            if exp.get('description'):
                entry += "\n\\resumeItemListStart\n"
                # Split description into lines and process each
                descriptions = str(exp['description']).split('\n')
                for desc in descriptions:
                    if desc.strip():
                        entry += f"\\resumeItem{{{self._escape_latex(desc.strip())}}}\n"
                entry += "\\resumeItemListEnd"
            
            entries.append(entry)
        
        return "\n".join(entries)
    
    def _format_projects(self, projects_data: List[Dict]) -> str:
        """Format projects section"""
        if not projects_data:
            return "% No projects\\resumeSubheading{Sample Project}{2023 -- 2024}{React, Node.js}{github.com/sample}"
        
        entries = []
        for project in projects_data:
            dates = f"{self._escape_latex(project.get('start_date', ''))} -- {self._escape_latex(project.get('end_date', ''))}"
            
            entry = f"\\resumeSubheading{{{self._escape_latex(project['name'])}}}" \
                   f"{{{dates}}}" \
                   f"{{{self._escape_latex(project.get('technologies', ''))}}}" \
                   f"{{{self._escape_latex(project.get('github_link', ''))}}}"
            
            if project.get('description'):
                entry += "\n\\resumeItemListStart\n"
                descriptions = str(project['description']).split('\n')
                for desc in descriptions:
                    if desc.strip():
                        entry += f"\\resumeItem{{{self._escape_latex(desc.strip())}}}\n"
                entry += "\\resumeItemListEnd"
            
            entries.append(entry)
        
        return "\n".join(entries)
    
    def _format_skills(self, skills_data: Dict) -> str:
        """Format skills section"""
        if not skills_data:
            return "\\textbf{Programming Languages:} Python, JavaScript, Java \\\\ \\textbf{Frameworks:} React, Node.js, Django"
        
        skill_lines = []
        skill_categories = {
            'languages': 'Programming Languages',
            'frameworks': 'Frameworks',
            'databases': 'Databases',
            'tools': 'Tools',
            'technical_skills': 'Technical Skills',
            'soft_skills': 'Soft Skills'
        }
        
        for key, label in skill_categories.items():
            if skills_data.get(key):
                if isinstance(skills_data[key], list):
                    skills_list = ', '.join([self._escape_latex(skill) for skill in skills_data[key]])
                else:
                    skills_list = self._escape_latex(str(skills_data[key]))
                
                if skills_list:
                    skill_lines.append(f"\\textbf{{{label}:}} {skills_list}")
        
        return " \\\\ ".join(skill_lines) if skill_lines else "\\textbf{Skills:} Various technical and soft skills"
    
    def _format_other_sections(self, data: List[Dict], section_type: str) -> str:
        """Format other sections (achievements, publications, etc.)"""
        if not data:
            return f"% No {section_type} entries"
        
        entries = []
        for item in data:
            if section_type == 'achievements':
                entry = f"\\resumeSubheading{{{self._escape_latex(item.get('title', ''))}}}" \
                       f"{{{self._escape_latex(item.get('date', ''))}}}" \
                       f"{{{self._escape_latex(item.get('organization', ''))}}}" \
                       f"{{}}"
            elif section_type == 'publications':
                entry = f"\\resumeSubheading{{{self._escape_latex(item.get('title', ''))}}}" \
                       f"{{{self._escape_latex(item.get('year', ''))}}}" \
                       f"{{{self._escape_latex(item.get('venue', ''))}}}" \
                       f"{{{self._escape_latex(item.get('authors', ''))}}}"
            elif section_type == 'certifications':
                entry = f"\\resumeSubheading{{{self._escape_latex(item.get('name', ''))}}}" \
                       f"{{{self._escape_latex(item.get('date', ''))}}}" \
                       f"{{{self._escape_latex(item.get('issuer', ''))}}}" \
                       f"{{{self._escape_latex(item.get('credential_id', ''))}}}"
            else:
                continue
                
            if item.get('description'):
                entry += "\n\\resumeItemListStart\n"
                entry += f"\\resumeItem{{{self._escape_latex(item['description'])}}}\n"
                entry += "\\resumeItemListEnd"
            
            entries.append(entry)
        
        return "\n".join(entries) if entries else f"% No {section_type}"
    
    def _format_languages(self, languages_data: List[Dict]) -> str:
        """Format languages section"""
        if not languages_data:
            return "English (Native), Spanish (Conversational)"
        
        language_entries = []
        for lang in languages_data:
            if lang.get('language'):
                proficiency = lang.get('proficiency', 'Basic')
                language_entries.append(f"{self._escape_latex(lang['language'])} ({self._escape_latex(proficiency)})")
        
        return ', '.join(language_entries) if language_entries else "English (Native)"
    
    def _format_interests(self, interests_data: List[str]) -> str:
        """Format interests section"""
        if not interests_data:
            return "Technology, Photography, Travel"
        
        return ', '.join([self._escape_latex(interest) for interest in interests_data])
    
    def _get_template_content(self, template_name: str, data: Dict[str, Any]) -> str:
        """Get template content with data filled in"""
        template = self._get_template(template_name)
        
        # Replace placeholders
        personal = data['personal']
        template = template.replace('{{name}}', self._escape_latex(personal['full_name']))
        template = template.replace('{{email}}', self._escape_latex(personal['email']))
        template = template.replace('{{phone}}', self._escape_latex(personal['phone']))
        template = template.replace('{{linkedin}}', self._escape_latex(personal['linkedin']))
        template = template.replace('{{github}}', self._escape_latex(personal['github']))
        template = template.replace('{{website}}', self._escape_latex(personal['website']))
        template = template.replace('{{address}}', self._escape_latex(personal['address']))
        template = template.replace('{{summary}}', self._escape_latex(personal['summary']))
        
        # Replace sections
        template = template.replace('{{education}}', self._format_education(data['education']))
        template = template.replace('{{experience}}', self._format_experience(data['experience']))
        template = template.replace('{{projects}}', self._format_projects(data['projects']))
        template = template.replace('{{skills}}', self._format_skills(data['skills']))
        template = template.replace('{{achievements}}', self._format_other_sections(data['achievements'], 'achievements'))
        template = template.replace('{{publications}}', self._format_other_sections(data['publications'], 'publications'))
        template = template.replace('{{certifications}}', self._format_other_sections(data['certifications'], 'certifications'))
        template = template.replace('{{languages}}', self._format_languages(data['languages']))
        template = template.replace('{{interests}}', self._format_interests(data['interests']))
        
        return template
    
    def _compile_latex(self, latex_content: str) -> bytes:
        """Compile LaTeX to PDF with enhanced error handling"""
        with tempfile.TemporaryDirectory() as temp_dir:
            tex_file = os.path.join(temp_dir, 'resume.tex')
            
            # Write LaTeX file with proper encoding
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            try:
                # First pass compilation
                result = subprocess.run([
                    'pdflatex', 
                    '-interaction=nonstopmode',
                    '-output-directory', temp_dir,
                    tex_file
                ], capture_output=True, text=True, timeout=120)
                
                # Check for successful compilation
                pdf_file = os.path.join(temp_dir, 'resume.pdf')
                if os.path.exists(pdf_file) and os.path.getsize(pdf_file) > 0:
                    with open(pdf_file, 'rb') as f:
                        return f.read()
                else:
                    # Parse and report the actual error
                    error_details = self._parse_latex_error(result.stderr, result.stdout)
                    raise Exception(f"LaTeX compilation failed: {error_details}")
                    
            except subprocess.TimeoutExpired:
                raise Exception("LaTeX compilation timed out (120 seconds)")
            except FileNotFoundError:
                raise Exception("pdflatex not found - LaTeX not installed properly")
    
    def _parse_latex_error(self, stderr: str, stdout: str) -> str:
        """Parse detailed LaTeX error information"""
        error_text = stderr + stdout
        
        # Look for specific error patterns
        if "! LaTeX Error" in error_text:
            lines = error_text.split('\n')
            for i, line in enumerate(lines):
                if "! LaTeX Error" in line:
                    error_line = line.strip()
                    # Get the next few lines for context
                    context = []
                    for j in range(i+1, min(i+4, len(lines))):
                        if lines[j].strip():
                            context.append(lines[j].strip())
                    return f"{error_line} | Context: {' '.join(context)}"
        
        # Look for other common errors
        if "! Undefined control sequence" in error_text:
            return "Undefined control sequence - check LaTeX commands"
        elif "! Missing $ inserted" in error_text:
            return "Missing $ inserted - math mode error"
        elif "! Extra alignment tab" in error_text:
            return "Extra alignment tab - table formatting error"
        elif "! Package" in error_text and "Error" in error_text:
            return "Package error - missing or incompatible package"
        
        # Return first few lines of error output
        lines = error_text.split('\n')[:10]
        return f"LaTeX error: {' '.join(line.strip() for line in lines if line.strip())}"
    
    def _get_template(self, template_name: str) -> str:
        """Get LaTeX template - simplified and tested"""
        if template_name == 'jake':
            return self._get_jake_template()
        elif template_name == 'deedy':
            return self._get_deedy_template()
        elif template_name == 'rendercv':
            return self._get_rendercv_template()
        else:
            return self._get_jake_template()
    
    def _get_jake_template(self) -> str:
        """Simplified Jake template - guaranteed to work"""
        return r"""
\documentclass[letterpaper,11pt]{article}

\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage[usenames,dvipsnames]{color}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage[english]{babel}
\usepackage{tabularx}

\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}
\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

\begin{document}

\begin{center}
    \textbf{\Huge \scshape {{name}}} \\ \vspace{1pt}
    \small {{phone}} $|$ \href{mailto:{{email}}}{\underline{ {{email}} }} $|$ 
    \href{https://{{linkedin}}}{\underline{ {{linkedin}} }} $|$
    \href{https://{{github}}}{\underline{ {{github}} }}
\end{center}

\section{Education}
\resumeSubHeadingListStart
{{education}}
\resumeSubHeadingListEnd

\section{Experience}
\resumeSubHeadingListStart
{{experience}}
\resumeSubHeadingListEnd

\section{Projects}
\resumeSubHeadingListStart
{{projects}}
\resumeSubHeadingListEnd

\section{Technical Skills}
\begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
     {{skills}}
    }}
\end{itemize}

\section{Achievements}
\resumeSubHeadingListStart
{{achievements}}
\resumeSubHeadingListEnd

\section{Publications}
\resumeSubHeadingListStart
{{publications}}
\resumeSubHeadingListEnd

\section{Certifications}
\resumeSubHeadingListStart
{{certifications}}
\resumeSubHeadingListEnd

\section{Languages}
\begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
     {{languages}}
    }}
\end{itemize}

\section{Interests}
\begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
     {{interests}}
    }}
\end{itemize}

\end{document}
"""
    
    def _get_deedy_template(self) -> str:
        """Simplified Deedy template"""
        return r"""
\documentclass[letterpaper,11pt]{article}

\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage[usenames,dvipsnames]{color}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage[english]{babel}
\usepackage{tabularx}
\usepackage{multicol}

\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large\color{blue}
}{}{0em}{}[\color{blue}\titlerule \vspace{-5pt}]

\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

\begin{document}

\begin{center}
    \textbf{\Huge \scshape {{name}}} \\ \vspace{1pt}
    \small {{phone}} $|$ \href{mailto:{{email}}}{\underline{ {{email}} }} $|$ 
    \href{https://{{linkedin}}}{\underline{ {{linkedin}} }} $|$
    \href{https://{{github}}}{\underline{ {{github}} }}
\end{center}

\begin{multicols}{2}

\section{Experience}
\resumeSubHeadingListStart
{{experience}}
\resumeSubHeadingListEnd

\section{Projects}
\resumeSubHeadingListStart
{{projects}}
\resumeSubHeadingListEnd

\columnbreak

\section{Education}
\resumeSubHeadingListStart
{{education}}
\resumeSubHeadingListEnd

\section{Skills}
\begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
     {{skills}}
    }}
\end{itemize}

\section{Achievements}
\resumeSubHeadingListStart
{{achievements}}
\resumeSubHeadingListEnd

\end{multicols}

\end{document}
"""
    
    def _get_rendercv_template(self) -> str:
        """Simplified RenderCV template"""
        return r"""
\documentclass[10pt, letterpaper]{article}

\usepackage[
    top=2 cm,
    bottom=2 cm,
    left=2 cm,
    right=2 cm,
]{geometry}
\usepackage{titlesec}
\usepackage{tabularx}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}

\raggedright
\setcounter{secnumdepth}{0}
\setlength{\parindent}{0pt}
\pagenumbering{gobble}

\titleformat{\section}{\bfseries\large}{}{0pt}{}[\vspace{1pt}\titlerule]

\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

\begin{document}

\begin{center}
    \fontsize{24 pt}{24 pt}\selectfont {{name}}

    \vspace{5 pt}

    \normalsize
    {{address}} | \href{mailto:{{email}}}{ {{email}} } | {{phone}} | 
    \href{https://{{linkedin}}}{ {{linkedin}} } | \href{https://{{github}}}{ {{github}} }
\end{center}

\vspace{5 pt}

\section{Education}
\resumeSubHeadingListStart
{{education}}
\resumeSubHeadingListEnd

\section{Experience}
\resumeSubHeadingListStart
{{experience}}
\resumeSubHeadingListEnd

\section{Projects}
\resumeSubHeadingListStart
{{projects}}
\resumeSubHeadingListEnd

\section{Skills}
\begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
     {{skills}}
    }}
\end{itemize}

\section{Achievements}
\resumeSubHeadingListStart
{{achievements}}
\resumeSubHeadingListEnd

\end{document}
"""

# For compatibility
FreePDFHandler = ProfessionalLaTeXHandler
DockerLaTeXHandler = ProfessionalLaTeXHandler
