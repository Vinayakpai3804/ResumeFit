import json
import time
import streamlit as st
import requests
from typing import Dict, List, Tuple
import re


class LLMHandler:
    """
    Real-time AI-powered resume analysis with dynamic responses
    """
    
    def __init__(self):
        # Use multiple AI providers for reliability
        self.ai_providers = {
            'groq': {
                'url': 'https://api.groq.com/openai/v1/chat/completions',
                'model': 'llama3-8b-8192',
                'key': st.secrets["GROQ_API_KEY"]
            },
            'together': {
                'url': 'https://api.together.xyz/v1/chat/completions',
                'model': 'meta-llama/Llama-3-8b-chat-hf',
                'key': None  # Add your Together AI key if available
            }
        }
        self.current_provider = 'groq'
    
    def _make_ai_request(self, prompt: str, max_tokens: int = 1500) -> str:
        """Make real-time AI request for dynamic analysis"""
        provider = self.ai_providers[self.current_provider]
        
        headers = {
            "Authorization": f"Bearer {provider['key']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": provider['model'],
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(provider['url'], headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception("Invalid API response structure")
                
        except Exception as e:
            st.error(f"AI request failed: {str(e)}")
            raise e
    
    def analyze_resume_comprehensive(self, resume_text: str, job_role: str, **kwargs) -> Dict:
        """
        Real-time AI analysis - completely dynamic based on actual resume content
        """
        
        if not resume_text or not job_role:
            return self._get_emergency_fallback()
        
        # Create comprehensive analysis prompt
        analysis_prompt = f"""
As an expert career advisor and ATS specialist, perform a comprehensive analysis of this resume for the "{job_role}" position.

RESUME CONTENT:
{resume_text[:6000]}

TARGET ROLE: {job_role}

Provide a detailed JSON analysis with the following structure:
{{
    "match_percentage": [calculate based on role alignment, skills match, experience relevance],
    "overall_score": [1-100 rating based on resume quality and role fit],
    "summary": "[3-4 sentence personalized summary highlighting key strengths and areas for improvement specific to this resume and role]",
    "strengths": [
        "[Specific strength based on actual resume content]",
        "[Another specific strength from the resume]",
        "[Third strength highlighting unique aspects]",
        "[Fourth strength if applicable]"
    ],
    "weaknesses": [
        "[Specific weakness or gap identified in the resume]",
        "[Another area needing improvement]",
        "[Third weakness if applicable]"
    ],
    "found_skills": [
        "[List actual skills mentioned in the resume]"
    ],
    "missing_skills": [
        "[Skills needed for {job_role} but not found in resume]"
    ],
    "suggested_keywords": [
        "[Industry-specific keywords for {job_role}]"
    ],
    "weak_sections": [
        "[Specific resume sections that need improvement]"
    ],
    "suggestions": [
        "[Actionable improvement suggestion based on analysis]",
        "[Another specific recommendation]",
        "[Third suggestion for enhancement]"
    ],
    "ats_compatibility": {{
        "score": [1-100 ATS friendliness score],
        "issues": ["[Specific ATS issues found]"],
        "recommendations": ["[Specific ATS improvements needed]"]
    }}
}}

IMPORTANT: 
- Base ALL analysis on the actual resume content provided
- Make recommendations specific to the {job_role} position
- Identify real skills and experience mentioned in the resume
- Calculate match percentage based on actual alignment between resume and role requirements
- Provide actionable, specific feedback rather than generic advice
- Ensure all suggestions are tailored to this individual's background and target role

Respond with ONLY the JSON object, no additional text.
"""

        try:
            st.info("🤖 AI is performing real-time analysis of your resume...")
            
            # Get AI analysis
            ai_response = self._make_ai_request(analysis_prompt, max_tokens=2000)
            
            # Clean and parse JSON
            cleaned_response = self._clean_json_response(ai_response)
            analysis_data = json.loads(cleaned_response)
            
            # Validate and enhance the response
            analysis_data = self._validate_and_enhance_analysis(analysis_data, resume_text, job_role)
            
            st.success("✅ Real-time AI analysis completed!")
            return analysis_data
            
        except json.JSONDecodeError as e:
            st.warning("⚠️ AI response parsing issue, generating enhanced analysis...")
            return self._generate_enhanced_fallback(resume_text, job_role, ai_response if 'ai_response' in locals() else "")
        except Exception as e:
            st.error(f"❌ Real-time analysis failed: {str(e)}")
            return self._generate_enhanced_fallback(resume_text, job_role)
    
    def _clean_json_response(self, response: str) -> str:
        """Clean AI response to extract valid JSON"""
        # Remove markdown code blocks
        response = re.sub(r'``````', '', response)
        response = re.sub(r'```', '', response)
        
        # Find JSON boundaries
        start = response.find('{')
        end = response.rfind('}')
        
        if start != -1 and end != -1:
            return response[start:end+1]
        
        raise ValueError("No valid JSON found in AI response")
    
    def _validate_and_enhance_analysis(self, analysis_data: Dict, resume_text: str, job_role: str) -> Dict:
        """Validate and enhance AI analysis with additional insights"""
        
        # Ensure all required fields exist
        required_fields = {
            "match_percentage": 75,
            "overall_score": 7,
            "summary": f"Professional analysis for {job_role} position",
            "strengths": [],
            "weaknesses": [],
            "found_skills": [],
            "missing_skills": [],
            "suggested_keywords": [],
            "weak_sections": [],
            "suggestions": [],
            "ats_compatibility": {"score": 7, "issues": [], "recommendations": []}
        }
        
        for field, default in required_fields.items():
            if field not in analysis_data or not analysis_data[field]:
                analysis_data[field] = default
        
        # Enhance with additional analysis
        analysis_data = self._add_content_insights(analysis_data, resume_text, job_role)
        
        return analysis_data
    
    def _add_content_insights(self, analysis_data: Dict, resume_text: str, job_role: str) -> Dict:
        """Add additional insights based on resume content analysis"""
        
        text_lower = resume_text.lower()
        
        # Extract experience years
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)\+?\s*yrs?\s*(?:of\s*)?(?:experience|exp)'
        ]
        
        max_years = 0
        for pattern in experience_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                try:
                    years = int(match)
                    max_years = max(max_years, years)
                except:
                    continue
        
        # Find quantified achievements
        achievements = []
        percentage_matches = re.findall(r'[^.\n]*\d+%[^.\n]*', resume_text)
        achievements.extend([match.strip() for match in percentage_matches[:2]])
        
        # Add content insights to analysis
        analysis_data['content_insights'] = {
            'years_experience': max_years,
            'quantified_achievements': achievements,
            'word_count': len(resume_text.split()),
            'has_contact_info': bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text))
        }
        
        return analysis_data
    
    def chat_response(self, user_message: str, resume_text: str, job_role: str, chat_history: List[Dict], **kwargs) -> str:
        """
        Real-time AI chat responses based on actual resume analysis - FIXED to avoid job role mentions
        """
        
        if not user_message.strip():
            return "Please ask a specific question about your resume or career."
        
        # Create context-aware chat prompt - REMOVED job role mentions from responses
        chat_prompt = f"""
You are ResumeFit AI, an expert career advisor. The user has uploaded their resume and wants career advice.

RESUME SUMMARY (first 1000 chars):
{resume_text[:1000] if resume_text else "No resume uploaded"}

RECENT CONVERSATION:
{self._format_chat_history(chat_history[-4:])}

USER QUESTION: {user_message}

Provide a helpful, specific response based on the actual resume content. Be encouraging but honest and strict. Keep response under 250 words and use relevant emojis.

Focus on:
- Specific advice based on their actual resume content
- General career recommendations that apply broadly
- Actionable next steps
- Encouraging but realistic feedback
- Be strict and professional

IMPORTANT: Do NOT mention specific job titles or roles in your response unless the user explicitly asks about them. Keep advice general but personalized to their background.
Just reply what the user asks, dont reply about t he user's summary always. reply only if the user asks about it.

Respond naturally as a career advisor would.
"""

        try:
            response = self._make_ai_request(chat_prompt, max_tokens=400)
            return response.strip()
            
        except Exception as e:
            return self._generate_contextual_fallback_response(user_message)
    
    def _format_chat_history(self, history: List[Dict]) -> str:
        """Format chat history for context"""
        formatted = ""
        for entry in history:
            role = entry.get("role", "user")
            content = entry.get("content", "")[:150]
            formatted += f"{role}: {content}\n"
        return formatted
    
    def _generate_contextual_fallback_response(self, user_message: str) -> str:
        """Generate contextual fallback when AI is unavailable - FIXED to remove job role mentions"""
        message_lower = user_message.lower()
        
        if "improve" in message_lower:
            return """🚀 To improve your resume:

📈 **Key Areas:**
-  Add quantified achievements with specific numbers/percentages
-  Include relevant keywords and technologies for your field
-  Strengthen your professional summary
-  Use strong action verbs in your experience descriptions

💡 **Quick Tip:** Research job postings in your target field to identify the most common requirements and ensure your resume addresses them.

Would you like specific advice on any of these areas?"""

        elif "strong" in message_lower or "strength" in message_lower:
            return """✨ Based on your resume:

💪 **Likely Strengths:**
-  Professional experience relevant to your field
-  Educational background supporting your goals
-  Clear resume structure and presentation

📊 **To Identify Specific Strengths:**
Upload a detailed resume so I can analyze your actual achievements, skills, and experience patterns.

🎯 **Pro Tip:** Your strongest points are usually quantified achievements that show measurable impact in previous roles."""

        elif "keyword" in message_lower:
            return """🔑 For professional positions, focus on these keyword categories:

**Technical Skills:** Role-specific technologies and tools
**Soft Skills:** Leadership, communication, problem-solving
**Industry Terms:** Current trends and methodologies in your field
**Action Words:** Developed, implemented, optimized, led

💡 **Research Strategy:** Look at job postings in your target field and note the most frequently mentioned skills and requirements.

Would you like help identifying specific keywords for your industry?"""

        else:
            return """💬 I'm here to help optimize your resume for your career goals! 

🎯 **I can help with:**
-  Specific improvement recommendations
-  Keyword optimization strategies  
-  Strength identification and enhancement
-  ATS compatibility improvements

📋 **For the best advice:** Upload your complete resume so I can provide personalized, specific feedback based on your actual content and experience.

What specific aspect of your resume would you like to focus on?"""
    
    def _generate_enhanced_fallback(self, resume_text: str, job_role: str, ai_response: str = "") -> Dict:
        """Generate enhanced fallback analysis when AI parsing fails"""
        
        # Try to extract insights from the raw AI response
        insights = self._extract_insights_from_text(ai_response, resume_text, job_role)
        
        return {
            "match_percentage": insights.get('match_percentage', 75),
            "overall_score": insights.get('overall_score', 7),
            "summary": insights.get('summary', f"Resume shows potential for {job_role} position with opportunities for optimization based on role requirements and industry standards."),
            "strengths": insights.get('strengths', [
                "Professional experience in relevant field",
                "Clear resume structure and presentation",
                "Educational background supports career goals"
            ]),
            "weaknesses": insights.get('weaknesses', [
                "Could benefit from more quantified achievements",
                "Consider adding more role-specific keywords",
                "Professional summary could be more targeted"
            ]),
            "found_skills": insights.get('found_skills', []),
            "missing_skills": insights.get('missing_skills', []),
            "suggested_keywords": insights.get('suggested_keywords', [
                "results-driven", "collaborative", "innovative", "problem-solving"
            ]),
            "weak_sections": insights.get('weak_sections', [
                "Experience descriptions need more metrics",
                "Skills section could be more comprehensive"
            ]),
            "suggestions": insights.get('suggestions', [
                f"Add specific metrics to achievements relevant to {job_role}",
                f"Include more {job_role}-specific keywords throughout",
                "Strengthen professional summary with role-targeted language"
            ]),
            "ats_compatibility": {
                "score": 7,
                "issues": ["Standard formatting recommended"],
                "recommendations": ["Use clear section headers", "Include relevant keywords naturally"]
            }
        }
    
    def _extract_insights_from_text(self, ai_response: str, resume_text: str, job_role: str) -> Dict:
        """Extract insights from AI response text when JSON parsing fails"""
        insights = {}
        
        # Try to extract match percentage
        match_pattern = r'match[_\s]*percentage["\s]*:?\s*(\d+)'
        match = re.search(match_pattern, ai_response, re.IGNORECASE)
        if match:
            insights['match_percentage'] = int(match.group(1))
        
        # Try to extract overall score
        score_pattern = r'overall[_\s]*score["\s]*:?\s*(\d+)'
        match = re.search(score_pattern, ai_response, re.IGNORECASE)
        if match:
            insights['overall_score'] = int(match.group(1))
        
        # Extract summary if available
        summary_pattern = r'summary["\s]*:?\s*["\']([^"\']+)["\']'
        match = re.search(summary_pattern, ai_response, re.IGNORECASE)
        if match:
            insights['summary'] = match.group(1)
        
        return insights
    
    def _get_emergency_fallback(self) -> Dict:
        """Emergency fallback when all else fails"""
        return {
            "match_percentage": 70,
            "overall_score": 7,
            "summary": "Resume analysis requires both resume content and target job role. Please ensure both are provided for comprehensive evaluation.",
            "strengths": ["Resume format is readable", "Ready for detailed analysis"],
            "weaknesses": ["Complete analysis requires more information"],
            "found_skills": [],
            "missing_skills": [],
            "suggested_keywords": [],
            "weak_sections": [],
            "suggestions": ["Upload complete resume for personalized analysis"],
            "ats_compatibility": {"score": 7, "issues": [], "recommendations": []}
        }
    
    def test_api_connection(self) -> Dict[str, str]:
        """Test real-time AI connection"""
        try:
            test_prompt = "Respond with 'Real-time AI analysis ready' if you can process resume analysis requests."
            response = self._make_ai_request(test_prompt, max_tokens=20)
            
            if "ready" in response.lower() or "analysis" in response.lower():
                return {"status": "success", "message": "✅ Real-time AI analysis engine connected and ready!"}
            else:
                return {"status": "success", "message": f"✅ AI connected: {response}"}
                
        except Exception as e:
            return {"status": "error", "message": f"❌ Real-time AI connection failed: {str(e)}"}
