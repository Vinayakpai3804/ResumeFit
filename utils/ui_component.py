import streamlit as st
import plotly.graph_objects as go
from typing import Dict, List
import json
from datetime import datetime

class UIComponents:
    """Dynamic UI components that adapt to real AI analysis results"""
    
    def display_overview(self, feedback_data: Dict):
        """Display dynamic overview based on real AI analysis"""
        st.markdown("### 📊 AI-Powered Resume Analysis")
        st.markdown("*Real-time analysis using advanced AI models*")
        
        # Dynamic metrics based on actual analysis
        col1, col2 = st.columns(2)
        
        with col1:
            # Dynamic gauge chart
            overall_score = feedback_data.get('overall_score', 5)
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=overall_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "AI Assessment Score", 'font': {'size': 18, 'color': '#f0f6fc'}},
                delta={'reference': 7, 'increasing': {'color': "#22c55e"}, 'decreasing': {'color': "#ef4444"}},
                gauge={
                    'axis': {'range': [None, 10], 'tickcolor': "#8b949e", 'tickfont': {'color': '#f0f6fc'}},
                    'bar': {'color': "#58a6ff"},
                    'bgcolor': "#21262d",
                    'borderwidth': 2,
                    'bordercolor': "#30363d",
                    'steps': [
                        {'range': [0, 4], 'color': "#7f1d1d"},
                        {'range': [4, 6], 'color': "#92400e"},
                        {'range': [6, 8], 'color': "#1e40af"},
                        {'range': [8, 10], 'color': "#064e3b"}
                    ]
                }
            ))
            fig.update_layout(height=250, font={'color': "#f0f6fc"}, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Dynamic match visualization
            match_pct = feedback_data.get('match_percentage', 0)
            colors = ['#58a6ff', '#30363d'] if match_pct >= 70 else ['#ef4444', '#30363d'] if match_pct < 50 else ['#f59e0b', '#30363d']
            
            fig = go.Figure(data=[go.Pie(
                labels=['Match', 'Gap'],
                values=[match_pct, 100 - match_pct],
                hole=.7,
                marker_colors=colors,
                textinfo='none'
            )])
            
            fig.update_layout(
                title={'text': "Role Alignment", 'x': 0.5, 'font': {'size': 18, 'color': '#f0f6fc'}},
                height=250,
                showlegend=False,
                annotations=[dict(text=f"<b>{match_pct}%</b>", x=0.5, y=0.5, font_size=24, font_color='#f0f6fc', showarrow=False)],
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # AI-generated summary
        st.markdown("### 🤖 AI Analysis Summary")
        summary = feedback_data.get('summary', 'Analysis in progress...')
        st.info(f"**AI Insight:** {summary}")
        
        # Dynamic metrics
        col_a, col_b, col_c, col_d = st.columns(4)
        
        with col_a:
            st.metric("Skills Found", len(feedback_data.get('found_skills', [])))
        with col_b:
            st.metric("Missing Skills", len(feedback_data.get('missing_skills', [])))
        with col_c:
            st.metric("Improvement Areas", len(feedback_data.get('suggestions', [])))
        with col_d:
            ats_score = feedback_data.get('ats_compatibility', {}).get('score', 0)
            st.metric("ATS Score", f"{ats_score}/10")
    
    def display_strengths(self, feedback_data: Dict):
        """Display AI-identified strengths dynamically"""
        st.markdown("### 💪 AI-Identified Strengths")
        st.markdown("*Based on real-time analysis of your resume content*")
        
        strengths = feedback_data.get('strengths', [])
        
        if not strengths:
            st.warning("⚠️ AI analysis in progress. Strengths will appear here once analysis is complete.")
            return
        
        # Display each strength dynamically
        for i, strength in enumerate(strengths, 1):
            if strength and strength.strip():
                st.success(f"✅ **Strength {i}:** {strength}")
        
        # Dynamic skills display
        st.markdown("### 🎯 Skills Identified by AI")
        found_skills = feedback_data.get('found_skills', [])
        
        if found_skills:
            st.markdown("**AI found these skills in your resume:**")
            
            # Create dynamic skill display
            cols = st.columns(min(len(found_skills), 4))
            for i, skill in enumerate(found_skills):
                if skill and skill.strip():
                    with cols[i % 4]:
                        st.button(f"🔹 {skill}", disabled=True, key=f"skill_{i}")
            
            # Alternative display for many skills
            if len(found_skills) > 8:
                with st.expander("View all identified skills"):
                    skill_text = " • ".join(found_skills)
                    st.markdown(f"🏷️ {skill_text}")
        else:
            st.info("🔍 AI is analyzing your resume for skills. Results will appear here.")
    
    def display_improvements(self, feedback_data: Dict, weak_sections: List[str]):
        """Display AI-powered improvement recommendations"""
        st.markdown("### ⚠️ AI-Powered Improvement Recommendations")
        st.markdown("*Personalized suggestions based on your specific resume and target role*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔧 Priority Improvements")
            weaknesses = feedback_data.get('weaknesses', [])
            
            if weaknesses:
                for i, weakness in enumerate(weaknesses, 1):
                    if weakness and weakness.strip():
                        priority = "🔴 HIGH" if i <= 2 else "🟡 MEDIUM"
                        st.error(f"{priority} **Area {i}:** {weakness}")
            else:
                st.success("🎉 AI found no major weaknesses in your resume!")
        
        with col2:
            st.markdown("#### 🎯 Missing Skills (AI Analysis)")
            missing_skills = feedback_data.get('missing_skills', [])
            
            if missing_skills:
                for skill in missing_skills:
                    if skill and skill.strip():
                        st.warning(f"🔴 **{skill}** - Important for your target role")
            else:
                st.success("✅ AI found good skill coverage for your target role!")
            
            # AI-suggested keywords
            st.markdown("#### 🔑 AI-Recommended Keywords")
            keywords = feedback_data.get('suggested_keywords', [])
            
            if keywords:
                st.markdown("**AI suggests these keywords:**")
                keyword_text = " • ".join(keywords)
                st.markdown(f"🏷️ {keyword_text}")
            else:
                st.info("💡 AI analysis for keywords in progress...")
        
        # AI suggestions
        st.markdown("### 🚀 AI Action Plan")
        suggestions = feedback_data.get('suggestions', [])
        
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                if suggestion and suggestion.strip():
                    st.info(f"**AI Recommendation {i}:** {suggestion}")
        else:
            st.info("📝 AI is generating personalized recommendations...")
    
    def display_download_options(self, feedback_data: Dict, resume_text: str, job_role: str, pdf_generator):
        """Display download options for AI analysis"""
        st.markdown("### 📥 Export AI Analysis")
        st.markdown("*Download your personalized AI-powered resume analysis*")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Generate AI Report", type="primary"):
                try:
                    pdf_data = pdf_generator.generate_analysis_pdf(feedback_data, resume_text, job_role)
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=pdf_data,
                        file_name=f"ai_resume_analysis_{job_role.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
                    st.success("✅ AI analysis report generated!")
                except Exception as e:
                    st.error(f"Report generation failed: {str(e)}")
        
        with col2:
            if st.button("📝 Markdown Summary"):
                try:
                    markdown_content = pdf_generator.generate_markdown_report(feedback_data, job_role)
                    st.download_button(
                        label="⬇️ Download Markdown",
                        data=markdown_content,
                        file_name=f"ai_analysis_{job_role.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d')}.md",
                        mime="text/markdown"
                    )
                    st.success("✅ Markdown report ready!")
                except Exception as e:
                    st.error(f"Markdown generation failed: {str(e)}")
        
        with col3:
            if st.button("📊 Raw AI Data"):
                enhanced_data = {
                    "metadata": {
                        "generated_at": datetime.now().isoformat(),
                        "job_role": job_role,
                        "analysis_type": "Real-time AI Analysis",
                        "ai_model": "Advanced Language Model"
                    },
                    "ai_analysis_results": feedback_data
                }
                
                st.download_button(
                    label="⬇️ Download JSON",
                    data=json.dumps(enhanced_data, indent=2),
                    file_name=f"ai_data_{job_role.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
                st.success("✅ AI data export ready!")
        
        # Dynamic analysis metrics
        with st.expander("📊 AI Analysis Metrics", expanded=False):
            col_a, col_b, col_c, col_d = st.columns(4)
            
            with col_a:
                st.metric("AI Match Score", f"{feedback_data.get('match_percentage', 0)}%")
            with col_b:
                st.metric("AI Rating", f"{feedback_data.get('overall_score', 0)}/10")
            with col_c:
                st.metric("Skills Found", len(feedback_data.get('found_skills', [])))
            with col_d:
                st.metric("AI Suggestions", len(feedback_data.get('suggestions', [])))
            
            # Additional AI insights
            st.markdown("---")
            st.markdown("**🤖 AI Analysis Details:**")
            
            content_insights = feedback_data.get('content_insights', {})
            if content_insights:
                st.write(f"• **Experience Detected:** {content_insights.get('years_experience', 0)} years")
                st.write(f"• **Quantified Achievements:** {len(content_insights.get('quantified_achievements', []))}")
                st.write(f"• **Resume Word Count:** {content_insights.get('word_count', 0)}")
                st.write(f"• **Contact Info:** {'✅ Complete' if content_insights.get('has_contact_info') else '❌ Missing'}")
            
            ats_data = feedback_data.get('ats_compatibility', {})
            st.write(f"• **ATS Compatibility:** {ats_data.get('score', 0)}/10")
            
            if ats_data.get('issues'):
                st.write(f"• **ATS Issues:** {len(ats_data['issues'])} identified")
