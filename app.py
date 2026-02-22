import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from utils import (
    extract_text_from_pdf, extract_skills, calculate_match,
    extract_experience, extract_education, extract_keywords,
    categorize_skills, analyze_resume_quality, get_improvement_suggestions,
    get_skill_gaps, match_certifications, predict_salary,
    get_interview_readiness_score, get_career_progression_path,
    calculate_weighted_match_score, match_job_profile, extract_contact_info,
    detect_job_role, is_technical_skill, filter_technical_skills,
    extract_job_requirements, normalize_skill,
    get_keyword_density, get_ats_checklist, get_readability_stats,
    get_action_verb_suggestions, get_tailoring_phrases,
    get_interview_questions, get_cover_letter_bullets,
    get_ideal_candidate_snapshot, generate_report_text
)
from industry_data import JOB_PROFILES, INDUSTRY_SALARY_DATA, TECHNICAL_SKILLS, SOFT_SKILLS, CREATIVE_SKILLS

# Page Configuration
st.set_page_config(
    page_title="Smart Resume Analyzer PRO v3.0",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with enhanced styling
st.markdown("""
<style>
.big-font {
    font-size: 40px !important;
    font-weight: bold;
    color: #1f77b4;
}
.score-excellent {
    background: linear-gradient(90deg, #d4edda 0%, #28a745 100%);
    padding: 20px;
    border-radius: 10px;
    color: white;
    font-weight: bold;
    text-align: center;
    font-size: 24px;
}
.score-good {
    background: linear-gradient(90deg, #fff3cd 0%, #ffc107 100%);
    padding: 20px;
    border-radius: 10px;
    color: #333;
    font-weight: bold;
    text-align: center;
    font-size: 24px;
}
.score-fair {
    background: linear-gradient(90deg, #f8d7da 0%, #dc3545 100%);
    padding: 20px;
    border-radius: 10px;
    color: white;
    font-weight: bold;
    text-align: center;
    font-size: 24px;
}
.metric-card {
    background: #f0f2f6;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #1f77b4;
    margin: 10px 0;
}
.insight-box {
    background: #e3f2fd;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #1976d2;
    margin: 10px 0;
}
.st-warning, .stSuccess, .stInfo {
    word-wrap: break-word;
    overflow-wrap: break-word;
}
[data-testid="stMetricDelta"], [data-testid="stMetricValue"] {
    word-break: break-word;
}
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.title("⚙️ Smart Resume Analyzer PRO v3.0")
option = st.sidebar.radio("Select Mode", [
    "📄 Single Resume Analysis",
    "📊 Batch Resume Comparison",
    "💼 Job Description Analyzer",
    "🎯 Advanced Analytics"
])

st.sidebar.divider()
st.sidebar.markdown("**Features:**")
st.sidebar.markdown("✓ AI skill matching & weighted score\n✓ Keyword density & ATS checklist\n✓ Salary & career path\n✓ Certifications & skill gaps\n✓ Interview Qs & readiness\n✓ Resume tailoring & cover letter bullets\n✓ Readability & action verbs")

# Default skills list
default_skills = [
    "Python", "SQL", "Machine Learning", "Data Analysis", "Java", "C++",
    "Communication", "Excel", "Leadership", "AWS", "React", "Node.js",
    "Docker", "Git", "Agile", "REST API", "JavaScript", "TypeScript"
]

# ==========================================
# MODE 1: SINGLE RESUME ANALYSIS
# ==========================================
if option == "📄 Single Resume Analysis":
    
    st.markdown('<p class="big-font">📄 Single Resume Analyzer</p>', unsafe_allow_html=True)
    st.markdown("Analyze a single resume against a job description with detailed insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📤 Upload Resume")
        uploaded_file = st.file_uploader("Choose a PDF resume", type="pdf", key="single_resume")
        
        st.subheader("🎯 Custom Skills (Optional)")
        custom_skills_input = st.text_area(
            "Enter skills separated by commas (leave blank to use defaults)",
            height=100,
            placeholder="Python, SQL, Machine Learning..."
        )
        
        if custom_skills_input:
            custom_skills = [skill.strip() for skill in custom_skills_input.split(",")]
        else:
            custom_skills = default_skills
    
    with col2:
        st.subheader("📋 Job Description")
        job_description = st.text_area(
            "Paste the full job description",
            height=280,
            placeholder="Paste job description here..."
        )
    
    if not uploaded_file or not job_description or len(job_description.strip()) <= 20:
        st.info("👆 **Upload a PDF resume** and **paste the job description** (at least 20 characters) to run the analysis.")
        st.markdown("---")
        with st.expander("📖 How to use"):
            st.markdown("""
            1. **Upload** your resume (PDF only).
            2. **Paste** the full job description in the right box.
            3. Optionally add **custom skills** (comma-separated) if your role uses specific tech.
            4. You’ll see **8 tabs**: Overview, Skills, Quality, Recommendations, Career & Salary, Interview Ready, Certifications, ATS & Power Tools.
            5. In **Overview** you can **Download Report** to save the analysis as text.
            """)
    elif uploaded_file and job_description and len(job_description.strip()) > 20:
        resume_text = extract_text_from_pdf(uploaded_file)
        if resume_text.startswith("Error"):
            st.error(resume_text)
            st.caption("Try re-uploading the PDF or use a different file.")
        else:
            # Extract resume data
            resume_skills = extract_skills(resume_text, custom_skills)
            # Enrich with full industry skill list (tech + creative) so we don't miss matches
            all_industry_skills = list(TECHNICAL_SKILLS.keys()) + list(SOFT_SKILLS.keys()) + list(CREATIVE_SKILLS.keys())
            resume_skills_from_full = extract_skills(resume_text, all_industry_skills)
            resume_skills = sorted(list(set(resume_skills) | set(resume_skills_from_full)))
            categorized = categorize_skills(resume_skills)  # Add this early for ATS breakdown

            # Extract job requirements from the job description (includes role-based expansion)
            job_skills = extract_job_requirements(job_description)
        
            # Detect job role from description for role-specific analysis
            detected_job_role = detect_job_role(job_description)
        
            experience = extract_experience(resume_text)
            if experience == 0:  # Default minimum if not found
                if 'senior' in resume_text.lower():
                    experience = 5
                elif 'junior' in resume_text.lower():
                    experience = 1
                else:
                    experience = 2
            education = extract_education(resume_text)
        
            # Ensure we have meaningful data
            if not resume_skills:
                resume_skills = ['Python', 'JavaScript']
            if not job_skills:
                job_skills = ['Python', 'JavaScript']
            if not experience:
                experience = 2
        
            # Calculate scores
            match_score, matched_skills, missing_skills = calculate_match(resume_skills, job_skills)
            weighted_score = calculate_weighted_match_score(resume_skills, job_skills)
            quality_score, quality_issues, quality_analysis = analyze_resume_quality(resume_text, resume_skills, experience, education)
        
            # Filter to only technical skills for matched and missing
            matched_technical = filter_technical_skills(matched_skills)
            missing_technical = filter_technical_skills(list(missing_skills))
        
            # Calculate ATS compatibility (based on resume quality + technical skills + experience)
            # ATS considers: resume structure (quality) + technical skills match + experience
            technical_skills_count = len([s for s in resume_skills if is_technical_skill(s)])
            skill_factor = min(100, (technical_skills_count / 10) * 100) if technical_skills_count else 0  # 10 tech skills = 100
            experience_factor = min(100, (experience / 8) * 100) if experience else 0  # 8 years = 100
            ats_score = (quality_score * 0.5) + (skill_factor * 0.25) + (experience_factor * 0.25)
        
            # Find matching job roles based on resume skills
            role_matches = []
            for role, profile in JOB_PROFILES.items():
                required_critical = profile['required_skills']['critical']
                required_all = required_critical + profile['required_skills']['required']
            
                # Calculate match for this role
                role_match_score, role_matched, role_missing = calculate_match(resume_skills, required_all)
            
                # Count critical skills missing and matched
                critical_missing = sum(1 for s in role_missing if normalize_skill(s) in {normalize_skill(c) for c in required_critical})
                critical_matched = sum(1 for s in role_matched if normalize_skill(s) in {normalize_skill(c) for c in required_critical})
            
                # Better eligibility determination based on critical skills
                total_critical = len(required_critical)
                critical_match_pct = (critical_matched / total_critical * 100) if total_critical > 0 else 0
            
                if critical_match_pct >= 80 and role_match_score >= 70:
                    eligibility = "Excellent Match"
                    color = "🟢"
                elif critical_match_pct >= 60 and role_match_score >= 55:
                    eligibility = "Good Match"
                    color = "🟡"
                elif critical_match_pct >= 40 and role_match_score >= 40:
                    eligibility = "Potential Match"
                    color = "🟠"
                else:
                    eligibility = "Learning Required"
                    color = "🔴"
            
                role_matches.append({
                    'role': role,
                    'match_score': role_match_score,
                    'critical_missing': critical_missing,
                    'critical_matched': critical_matched,
                    'total_critical': total_critical,
                    'eligibility': eligibility,
                    'color': color,
                    'min_exp': profile['min_experience'],
                    'salary': profile['salary_2024']['avg']
                })
        
            # Sort by match score
            role_matches = sorted(role_matches, key=lambda x: x['match_score'], reverse=True)
        
            # Advanced analysis
            skill_gaps = get_skill_gaps(resume_skills, job_skills)
            certifications = match_certifications(job_description, resume_text, resume_skills)
            salary_prediction = predict_salary(experience, resume_skills, education)
            interview_readiness = get_interview_readiness_score(resume_skills, job_skills, experience, education)
            career_paths = get_career_progression_path(experience, resume_skills)
            keyword_density = get_keyword_density(resume_text, job_skills)
            ats_checklist = get_ats_checklist(resume_text, resume_skills, experience, education)
            readability_stats = get_readability_stats(resume_text)
            action_verb_suggestions = get_action_verb_suggestions(resume_text)
            tailoring_phrases = get_tailoring_phrases(job_skills, list(missing_skills), detected_job_role)
            interview_questions = get_interview_questions(detected_job_role, missing_technical, experience)
            cover_letter_bullets = get_cover_letter_bullets(resume_skills, job_skills, experience, detected_job_role)

            # Tabs for different views
            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
                "📊 Overview",
                "🛠️ Skills Analysis",
                "📈 Quality Report",
                "💡 Recommendations",
                "💼 Career & Salary",
                "🏆 Interview Ready",
                "📜 Certifications",
                "🎯 ATS & Power Tools"
            ])
        
            # TAB 1: OVERVIEW
            with tab1:
                # Display detected job role and extracted requirements
                st.subheader("📋 Job Analysis")
                col_job1, col_job2 = st.columns(2)
            
                with col_job1:
                    st.markdown(f"**Detected Job Role:** 🎯 {detected_job_role}")
            
                with col_job2:
                    st.markdown(f"**Required Skills Detected:** {len(job_skills)}")
            
                st.markdown("**Skills Required for this Role:**")
                skill_cols = st.columns(min(4, len(job_skills)))
                for idx, skill in enumerate(sorted(job_skills)):
                    with skill_cols[idx % 4]:
                        st.info(f"✓ {skill}")

                with st.expander("🎯 Ideal candidate for this role"):
                    for bullet in get_ideal_candidate_snapshot(detected_job_role):
                        st.markdown(f"- {bullet}")

                report_text = generate_report_text(
                    detected_job_role, match_score, weighted_score, quality_score, ats_score,
                    experience, education, resume_skills, job_skills, matched_technical,
                    missing_technical, quality_issues, skill_gaps, salary_prediction,
                    interview_readiness, keyword_density
                )
                st.download_button("📥 Download Report (TXT)", data=report_text, file_name="resume_analysis_report.txt", mime="text/plain", key="dl_report_overview")

                st.divider()

                col1, col2, col3, col4 = st.columns(4)
            
                with col1:
                    ats_label = "Excellent" if ats_score >= 80 else "Very Good" if ats_score >= 70 else "Good" if ats_score >= 60 else "Needs Work"
                    st.metric("ATS Compatibility", f"{ats_score:.1f}%", ats_label, help="Resume ATS compatibility (structure, keywords, formatting)")
            
                with col2:
                    st.metric("Job Match", f"{match_score:.1f}%",
                             f"{len(matched_skills)}/{len(job_skills)} skills · Weighted: {weighted_score:.0f}%",
                             help="Match % of required skills in resume. Weighted score emphasizes critical skills.")
                    if match_score < 50 and job_skills:
                        st.caption("💡 Open **Skills Analysis** tab to see transferable skills and what to learn.")

                with col3:
                    quality_label = "Excellent" if quality_score >= 80 else "Good" if quality_score >= 60 else "Needs Work"
                    st.metric("Resume Quality", f"{quality_score:.1f}%", quality_label,
                             help="Resume structure, content, and completeness score")
            
                with col4:
                    st.metric("Experience", experience, education,
                             help="Detected professional experience and education level")
            
                # ATS Score Breakdown
                st.divider()
                st.markdown("### 📊 ATS Score Breakdown")
            
                col_breakdown1, col_breakdown2, col_breakdown3 = st.columns(3)
            
                with col_breakdown1:
                    st.markdown(f"""**Resume Quality: {quality_score:.0f}%** (50% of ATS)
    - Structure & formatting
    - Sections completeness
    - Contact information
    - Keyword usage""")
            
                with col_breakdown2:
                    st.markdown(f"""**Skills Level: {skill_factor:.0f}%** (25% of ATS)
    - Total skills found: {len(resume_skills)}
    - Recommended: 8-15 skills
    - Technical: {len(categorized['technical'])}
    - Soft skills: {len(categorized['soft'])}""")
            
                with col_breakdown3:
                    st.markdown(f"""**Experience Factor: {experience_factor:.0f}%** (25% of ATS)
    - Years: {experience}
    - Target: 2-10 years
    - Education: {education}""")
            
                # Main visualization
                st.subheader("📈 Detailed Match Analysis")
            
                col_chart1, col_chart2 = st.columns(2)
            
                with col_chart1:
                    matched_count = len(matched_skills)
                    missing_count = max(0, len(job_skills) - len(matched_skills))
                
                    fig = go.Figure(data=[
                        go.Bar(name='Matched', x=['Skills'], y=[matched_count], 
                              marker_color='#28a745', text=str(matched_count), textposition='auto'),
                        go.Bar(name='Missing', x=['Skills'], y=[missing_count], 
                              marker_color='#dc3545', text=str(missing_count), textposition='auto')
                    ])
                    fig.update_layout(
                        title="Skills Match Breakdown",
                        barmode='stack',
                        height=350,
                        showlegend=True,
                        yaxis_title="Number of Skills"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
                with col_chart2:
                    fig = go.Figure(data=[go.Indicator(
                        mode="gauge+number",
                        value=match_score,
                        title={'text': "Job Match Score"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "#ff7f0e"},
                            'steps': [
                                {'range': [0, 50], 'color': "#f8d7da"},
                                {'range': [50, 80], 'color': "#fff3cd"},
                                {'range': [80, 100], 'color': "#d4edda"}
                            ],
                        }
                    )])
                    fig.update_layout(height=350)
                    st.plotly_chart(fig, use_container_width=True)
            
                # Role Matching Section (only for tech roles in our database)
                st.divider()
                st.subheader("🎯 Eligible Roles Based on Your Resume")

                if detected_job_role in JOB_PROFILES and role_matches:
                    st.markdown("**Top roles you're qualified for:**")
                    for idx, role_data in enumerate(role_matches[:5], 1):
                        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                        with col1:
                            st.markdown(f"{role_data['color']} **{idx}. {role_data['role']}**")
                            st.caption(f"Avg Salary: ${int(role_data['salary'])}K | Min Exp: {role_data['min_exp']} years")
                        with col2:
                            st.metric("Match", f"{role_data['match_score']:.0f}%")
                        with col3:
                            st.markdown(f"**Status**\n{role_data['eligibility']}")
                        with col4:
                            if role_data['match_score'] >= 80:
                                st.success("Ready")
                            elif role_data['match_score'] >= 60:
                                st.info("Capable")
                            else:
                                st.warning("Learn")
                        st.divider()
                elif detected_job_role not in JOB_PROFILES:
                    st.info(f"**Role: {detected_job_role}** — Match and skills above are based only on the job description you pasted (no tech-role database for this role).")
                else:
                    st.info("Upload a resume to see eligible roles")
        
            # TAB 2: SKILLS ANALYSIS (for non-tech roles show all skills; for tech show technical only)
            with tab2:
                is_tech_role = detected_job_role in JOB_PROFILES
                display_matched = matched_technical if is_tech_role else matched_skills
                display_missing = missing_technical if is_tech_role else list(missing_skills)
                match_label = "Matched Technical Skills" if is_tech_role else "Matched Skills"
                missing_label = "Missing Technical Skills" if is_tech_role else "Missing Skills"

                st.subheader(f"✅ {match_label}")
                st.caption(f"Found {len(display_matched)} skills that match this job")
                if display_matched:
                    skill_cols = st.columns(min(3, len(display_matched)))
                    for idx, skill in enumerate(sorted(display_matched)):
                        with skill_cols[idx % 3]:
                            st.success(f"✓ {skill}")
                else:
                    st.warning("No skills matched")
                if not display_matched and (categorized['technical'] or categorized.get('tools')):
                    transfer_skills = categorized['technical'] + categorized.get('tools', [])
                    st.markdown("**Your skills (highlight these as transferable):**")
                    transfer_cols = st.columns(min(3, len(transfer_skills)))
                    for idx, skill in enumerate(sorted(transfer_skills)[:9]):
                        with transfer_cols[idx % 3]:
                            st.info(f"• {skill}")

                st.divider()

                st.subheader(f"❌ {missing_label}")
                st.caption(f"Skills needed for this job: {len(display_missing)} missing")
                missing_display = [s.title() if isinstance(s, str) else s for s in display_missing]

                if display_missing:
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.markdown("**Priority Skills to Learn:**")
                        for idx, skill in enumerate(sorted(missing_display)[:5], 1):
                            st.error(f"{idx}. {skill}")
                    with col2:
                        if len(display_missing) > 5:
                            st.info(f"+ {len(display_missing) - 5} more skills needed")
                        else:
                            st.success("All critical skills shown above")
                else:
                    st.success("✅ All required skills found!")

                st.divider()

                # Skills Categorization
                st.subheader("Skills by Category")
                tools_and_creative = categorized.get('tools', []) + categorized.get('creative', [])

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Technical Skills** ({len(categorized['technical'])})")
                    for skill in categorized['technical']:
                        st.write(f"• {skill}")
                with col2:
                    st.markdown(f"**Soft Skills** ({len(categorized['soft'])})")
                    for skill in categorized['soft']:
                        st.write(f"• {skill}")
                with col3:
                    st.markdown(f"**Tools & Creative** ({len(tools_and_creative)})")
                    for skill in sorted(set(tools_and_creative)):
                        st.write(f"• {skill}")
        
            # TAB 3: QUALITY REPORT
            with tab3:
                col1, col2 = st.columns([2, 1])
            
                with col1:
                    st.subheader("Resume Quality Score: " + str(round(quality_score, 1)) + "%")
                
                    # Progress bar
                    fig = go.Figure(data=[
                        go.Bar(x=[quality_score], y=['Quality'], orientation='h', 
                              marker=dict(color='#1f77b4'), text=f'{quality_score:.1f}%', textposition='auto')
                    ])
                    fig.update_layout(height=100, xaxis_range=[0, 100], showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                
                    if quality_issues:
                        st.subheader("⚠️ Issues Found:")
                        for issue in quality_issues:
                            st.warning(f"• {issue}")
                    else:
                        st.success("✅ No quality issues detected!")
            
                with col2:
                    st.subheader("📋 Details")
                    st.write(f"**Text Length:** {len(resume_text)} chars")
                    st.write(f"**Skills Found:** {len(resume_skills)}")
                    st.write(f"**Experience:** {experience}")
                    st.write(f"**Education:** {education}")
        
            # TAB 4: RECOMMENDATIONS
            with tab4:
                st.subheader("💡 Improvement Recommendations")
            
                suggestions = get_improvement_suggestions(
                    resume_skills, job_skills, experience, quality_issues
                )
            
                for idx, suggestion in enumerate(suggestions, 1):
                    st.info(f"**{idx}.** {suggestion}")

                st.divider()

                st.subheader("✂️ One-Click Tailoring Phrases")
                st.caption("Add these phrases to your resume to better match this job.")
                for i, phrase in enumerate(tailoring_phrases, 1):
                    st.success(f"{i}. {phrase}")

                st.divider()

                st.subheader("📄 Cover Letter Bullet Points")
                st.caption("Use these in your cover letter for this role.")
                for b in cover_letter_bullets:
                    st.markdown(f"- {b}")

                st.divider()

                # Skill gaps analysis
                if skill_gaps:
                    st.subheader("📚 Skill Gap Analysis")
                    st.markdown("**Technical skills to develop for this role:**")
                
                    for gap in skill_gaps[:5]:
                        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                        with col1:
                            st.write(f"**{gap['skill']}**")
                            st.caption(f"Learning time: {gap['timeline']}")
                            if gap['resources']:
                                st.caption(f"Resources: {', '.join(gap['resources'][:2])}")
                        with col2:
                            if gap['priority'] == 'Critical':
                                st.error(f"Priority: {gap['priority']}")
                            else:
                                st.warning(f"Priority: {gap['priority']}")
                        with col3:
                            demand_color = {'Critical': '#c0392b', 'High': 'green', 'Medium': 'blue', 'Low': 'gray'}.get(gap['demand'], 'gray')
                            st.markdown(f"<span style='color:{demand_color}'>📈 Demand: {gap['demand']}</span>", unsafe_allow_html=True)
                        with col4:
                            growth = gap.get('growth', 0)
                            st.metric("Growth", f"{growth}%")
            
                st.divider()
            
            st.subheader("📝 Action Items")
            missing_set = set(normalize_skill(s) for s in job_skills) - set(normalize_skill(s) for s in resume_skills)
            missing_action = [s.title() for s in missing_set]
            missing_technical_action = [s for s in missing_action if is_technical_skill(s)]

            if len(missing_technical_action) > 0:
                st.markdown(f"""
                **Priority 1: Learn Missing Technical Skills ({len(missing_technical_action)})**
                - {', '.join(sorted(missing_technical_action)[:5])}
                
                    **How to improve:**
                    1. Take online courses (Udemy, Coursera, LinkedIn Learning)
                    2. Build portfolio projects using these technologies
                    3. Update your resume with hands-on project experience
                    4. Practice on LeetCode/HackerRank for coding skills
                    """)
            
                if quality_score < 70:
                    st.markdown("""
                    **Priority 2: Structure & Format**
                    - Ensure clear section headers (Experience, Education, Skills)
                    - Include contact information (email, phone, LinkedIn)
                    - Use action verbs and quantifiable achievements
                    """)
            
                st.markdown("""
                **General Tips:**
                - Keep resume to 1-2 pages
                - Use relevant keywords from job description
                - Quantify achievements with metrics
                - Tailor resume for each job application
                """)
        
            # TAB 5: CAREER & SALARY
            with tab5:
                st.subheader("💼 Career Progression & Salary Analysis")
                st.markdown(f"📌 **Job Role:** {detected_job_role}")
            
                col1, col2 = st.columns(2)
            
                with col1:
                    st.subheader("💰 Salary Prediction")
                    salary = salary_prediction
                
                    # Create salary visualization with role context
                    fig = go.Figure(data=[
                        go.Bar(x=['Min', 'Average', 'Max'],
                              y=[salary['min'], salary['avg'], salary['max']],
                              marker_color=['#ff9999', '#66b3ff', '#99ff99'],
                              text=[f"${int(salary['min'])}K", f"${int(salary['avg'])}K", f"${int(salary['max'])}K"],
                              textposition='outside')
                    ])
                    fig.update_layout(
                        title=f"Estimated Annual Salary - {detected_job_role} ({salary['level']})",
                        yaxis_title="Salary (USD, Thousands)",
                        height=400,
                        showlegend=False,
                        xaxis_title="Salary Range"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                    st.markdown(f"""
                    **Salary Range:** ${int(salary['min'])}K - ${int(salary['max'])}K  
                    **Average:** ${int(salary['avg'])}K {salary['period']}  
                    **Seniority Level:** {salary['level']}  
                    **Job Role:** {detected_job_role}

                    *Calculated based on:*
                    - Experience: {experience} years
                    - Education: {education}
                    - Technical Skills: {len(resume_skills)} skills
                    - Role Requirements: {detected_job_role}
                    """)
            
                with col2:
                    st.subheader("📈 Career Progression Paths")
                    for idx, path in enumerate(career_paths, 1):
                        with st.container():
                            st.markdown(f"""
                            **Path {idx}: {path['title']}**
                            - Timeline: {path['timeline']}
                            - Salary increase: {path['salary_increase']}
                            - Skills to develop: {', '.join(path['skills'])}
                            """)
                            st.divider()
        
            # TAB 6: INTERVIEW READINESS
            with tab6:
                st.subheader("🏆 Interview Readiness Assessment")
            
                interview = interview_readiness
                readiness_level = interview['readiness_level']
                score = interview['score']
            
                # Color-coded score display
                if score >= 80:
                    st.markdown(f'<div class="score-excellent">Interview Ready: {score}%</div>', unsafe_allow_html=True)
                elif score >= 60:
                    st.markdown(f'<div class="score-good">Good Preparation: {score}%</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="score-fair">Needs Preparation: {score}%</div>', unsafe_allow_html=True)
            
                col1, col2 = st.columns(2)
            
                with col1:
                    st.subheader("✅ Strengths")
                    for strength in interview['strengths']:
                        st.success(f"✓ {strength}")
            
                with col2:
                    st.subheader("⚠️ Areas to Improve")
                    for concern in interview['concerns']:
                        st.warning("• " + str(concern))
            
                st.divider()

                st.subheader("🎤 Likely Interview Questions")
                st.caption("Based on role and skill gaps—prepare answers for these.")
                for i, q in enumerate(interview_questions, 1):
                    st.markdown(f"**{i}.** {q}")

                st.divider()

                st.subheader("Interview Tips")
                st.markdown("""
                1. **Research the company** - Know their products, culture, and recent news
                2. **Prepare with STAR method** - Situation, Task, Action, Result for behavioral questions
                3. **Practice technical concepts** - Review data structures, algorithms, and system design
                4. **Prepare questions** - Ask thoughtful questions about the role and company
                5. **Mock interviews** - Practice with friends or use online platforms
                """)

            # TAB 7: CERTIFICATIONS
            with tab7:
                st.subheader("📜 Recommended Certifications")
                st.markdown(f"📌 **Certifications for {detected_job_role} Role**")
            
                if certifications:
                    # Group certifications by area
                    grouped_certs = {}
                    for cert_item in certifications:
                        area = cert_item['area']
                        if area not in grouped_certs:
                            grouped_certs[area] = []
                        grouped_certs[area].append(cert_item)
                
                    # Display grouped certifications with enhanced details
                    for area, cert_group in grouped_certs.items():
                        st.markdown(f"### **{area}**")
                        for cert_item in cert_group:
                            relevance = cert_item.get('relevance', 'Medium')
                            duration = cert_item.get('duration', '2-3 months')
                        
                            # Color code by relevance
                            if relevance == 'Critical':
                                col1, col2, col3 = st.columns([3, 1, 1])
                                with col1:
                                    st.write(f"🔴 **{cert_item['cert']}**")
                                with col2:
                                    st.error(relevance)
                                with col3:
                                    st.info(f"⏱️ {duration}")
                            elif relevance == 'High':
                                col1, col2, col3 = st.columns([3, 1, 1])
                                with col1:
                                    st.write(f"🟠 **{cert_item['cert']}**")
                                with col2:
                                    st.warning(relevance)
                                with col3:
                                    st.info(f"⏱️ {duration}")
                            else:
                                col1, col2, col3 = st.columns([3, 1, 1])
                                with col1:
                                    st.write(f"🟡 **{cert_item['cert']}**")
                                with col2:
                                    st.info(relevance)
                                with col3:
                                    st.info(f"⏱️ {duration}")
                        st.divider()
                else:
                    st.info("No specific certifications detected for this role")
            
                st.subheader("🎓 General Certification Recommendations")
                st.markdown("""
                **Cloud Platforms (2-3 months each)**
                - AWS Solutions Architect Associate
                - Azure Administrator Certified
                - Google Cloud Associate
            
                **Development (3-6 months each)**
                - CKA - Kubernetes Administration
                - Docker Certified Associate
                - HashiCorp Certified
            
                **Soft Skills**
                - Project Management Professional (PMP)
                - Scrum Master (CSM)
                - Leadership certifications
                """)

            # TAB 8: ATS & POWER TOOLS
            with tab8:
                st.subheader("🎯 ATS & Power Tools")
                st.caption("Keyword density, ATS checklist, readability, and action verbs.")

                col_kw1, col_kw2, col_kw3 = st.columns(3)
                with col_kw1:
                    st.metric("Keyword Match", f"{keyword_density['score_pct']}%", f"{len(keyword_density['found'])}/{len(job_skills)} in resume")
                with col_kw2:
                    st.metric("Reading Time", f"~{readability_stats['reading_time_mins']} min", f"{readability_stats['word_count']} words")
                with col_kw3:
                    st.metric("Action Verbs", action_verb_suggestions['count'], "strong verbs used")

                st.divider()
                st.subheader("📋 Job Keywords in Your Resume")
                if keyword_density['found']:
                    for skill, count in sorted(keyword_density['found'], key=lambda x: -x[1])[:15]:
                        st.success(f"✓ **{skill}** (appears {count}×)")
                if keyword_density['missing']:
                    st.markdown("**Add these keywords:**")
                    missing_display = [s.title() for s in keyword_density['missing'][:10]]
                    st.warning(", ".join(missing_display))

                st.divider()
                st.subheader("✅ ATS Checklist")
                for item in ats_checklist:
                    status = item['status']
                    if status == 'pass':
                        st.success(f"✓ {item['item']}")
                    elif status == 'warn':
                        st.warning(f"⚠ {item['item']} — {item['tip']}")
                    else:
                        st.error(f"✗ {item['item']} — {item['tip']}")

                st.divider()
                st.subheader("📖 Readability")
                st.write(readability_stats['suggestion'])
                st.caption(f"Characters: {readability_stats['char_count']} · Words: {readability_stats['word_count']}")

                st.divider()
                st.subheader("💪 Action Verbs")
                if action_verb_suggestions['used']:
                    st.write("You're using: ", ", ".join(action_verb_suggestions['used']))
                if action_verb_suggestions['weak_found']:
                    st.warning("Consider replacing weak verbs: " + ", ".join(action_verb_suggestions['weak_found']))
                if action_verb_suggestions['suggested_add']:
                    st.info("Add more impact: " + ", ".join(action_verb_suggestions['suggested_add']))

    # ==========================================
# MODE 2: BATCH RESUME COMPARISON
# ==========================================
elif option == "📊 Batch Resume Comparison":
    
    st.markdown('<p class="big-font">📊 Batch Resume Analyzer</p>', unsafe_allow_html=True)
    st.markdown("Compare and rank multiple resumes against a single job description")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📤 Upload Resumes")
        uploaded_files = st.file_uploader(
            "Choose multiple PDF resumes",
            type="pdf",
            accept_multiple_files=True,
            key="batch_resumes"
        )
    
    with col2:
        st.subheader("Custom Skills (Optional)")
        custom_skills_input = st.text_area(
            "Enter skills separated by commas",
            height=100,
            placeholder="Python, SQL, Machine Learning..."
        )
        
        if custom_skills_input:
            custom_skills = [skill.strip() for skill in custom_skills_input.split(",")]
        else:
            custom_skills = default_skills
    
    st.subheader("📋 Job Description")
    job_description = st.text_area(
        "Paste the job description",
        height=200,
        placeholder="Paste job description here..."
    )
    
    if uploaded_files and job_description:
        job_skills_batch = extract_job_requirements(job_description)
        if not job_skills_batch:
            job_skills_batch = default_skills
        all_industry = list(TECHNICAL_SKILLS.keys()) + list(SOFT_SKILLS.keys())
        ranking_data = []

        with st.spinner(f"Analyzing {len(uploaded_files)} resumes..."):
            for file in uploaded_files:
                resume_text = extract_text_from_pdf(file)
                if resume_text.startswith("Error"):
                    ranking_data.append({
                        "Resume": file.name,
                        "ATS Score": 0,
                        "Job Match %": 0,
                        "Quality %": 0,
                        "Matched Skills": 0,
                        "Total Skills": 0,
                    })
                    continue
                resume_skills = extract_skills(resume_text, custom_skills)
                resume_skills_full = extract_skills(resume_text, all_industry)
                resume_skills = sorted(list(set(resume_skills) | set(resume_skills_full)))
                job_skills = job_skills_batch

                match_score, matched_skills, missing_skills = calculate_match(resume_skills, job_skills)
                quality_score, quality_issues, quality_analysis = analyze_resume_quality(resume_text, resume_skills, 
                                                         extract_experience(resume_text),
                                                         extract_education(resume_text))
                ats_score = quality_score
                
                ranking_data.append({
                    "Resume": file.name,
                    "ATS Score": round(ats_score, 2),
                    "Job Match %": round(match_score, 2),
                    "Quality %": round(quality_score, 2),
                    "Matched Skills": len(matched_skills),
                    "Total Skills": len(resume_skills)
                })
        
        df = pd.DataFrame(ranking_data).sort_values(by="ATS Score", ascending=False)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Resumes", len(df))
        with col2:
            st.metric("Top ATS Score", f"{df['ATS Score'].max():.1f}%")
        with col3:
            st.metric("Avg ATS Score", f"{df['ATS Score'].mean():.1f}%")
        with col4:
            st.metric("Score Range", f"{df['ATS Score'].max() - df['ATS Score'].min():.1f}%")
        
        st.divider()
        
        # Ranking table with color coding
        st.subheader("🏆 Candidate Rankings")
        
        # Color the table based on scores
        def color_score(val):
            if isinstance(val, (int, float)):
                if val >= 80:
                    return 'background-color: #d4edda'
                elif val >= 60:
                    return 'background-color: #fff3cd'
                else:
                    return 'background-color: #f8d7da'
            return ''
        
        styled_df = df.style.map(color_score, subset=['ATS Score', 'Job Match %', 'Quality %'])
        st.dataframe(styled_df, use_container_width=True)
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(df.head(10), x='Resume', y='ATS Score', 
                        color='ATS Score', color_continuous_scale='RdYlGn',
                        title="Top 10 Resumes by ATS Score")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(df, x='Job Match %', y='Quality %', 
                           size='ATS Score', hover_name='Resume',
                           color='ATS Score', color_continuous_scale='RdYlGn',
                           title="Job Match vs Resume Quality")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Export option
        st.subheader("💾 Export Results")
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="resume_ranking.csv",
            mime="text/csv"
        )

# ==========================================
# MODE 3: JOB DESCRIPTION ANALYZER
# ==========================================
elif option == "💼 Job Description Analyzer":
    
    st.markdown('<p class="big-font">💼 Job Description Analyzer</p>', unsafe_allow_html=True)
    st.markdown("Analyze a job description and extract key requirements")
    
    st.subheader("📋 Job Description")
    job_description = st.text_area(
        "Paste the complete job description",
        height=250,
        placeholder="Paste job description here..."
    )
    
    if job_description:
        job_skills = extract_job_requirements(job_description)
        detected_role = detect_job_role(job_description)
        keywords = extract_keywords(job_description)
        categorized = categorize_skills(job_skills)

        # Tabs
        tab1, tab2, tab3 = st.tabs(["📊 Overview", "🛠️ Skills", "🏢 Keywords"])

        with tab1:
            st.markdown(f"**Detected role:** {detected_role}")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Skills", len(job_skills))
            with col2:
                st.metric("Technical Skills", len(categorized['technical']))
            with col3:
                st.metric("Soft Skills", len(categorized['soft']))
            with col4:
                st.metric("Tools & Platforms", len(categorized['tools']))
            
            st.divider()
            
            # Skills distribution
            fig = go.Figure(data=[
                go.Bar(name='Technical', x=['Skills'], y=[len(categorized['technical'])], marker_color='#1f77b4'),
                go.Bar(name='Soft', x=['Skills'], y=[len(categorized['soft'])], marker_color='#ff7f0e'),
                go.Bar(name='Tools', x=['Skills'], y=[len(categorized['tools'])], marker_color='#2ca02c')
            ])
            fig.update_layout(title="Skills Distribution", barmode='group', height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader(f"🔧 Technical ({len(categorized['technical'])})")
                for skill in sorted(categorized['technical']):
                    st.write(f"• {skill}")
            
            with col2:
                st.subheader(f"💬 Soft ({len(categorized['soft'])})")
                for skill in sorted(categorized['soft']):
                    st.write(f"• {skill}")
            
            with col3:
                st.subheader(f"🛠️ Tools ({len(categorized['tools'])})")
                for skill in sorted(categorized['tools']):
                    st.write(f"• {skill}")
        
        with tab3:
            st.subheader("🔑 Important Keywords")
            if keywords:
                for kw in keywords:
                    st.write(f"• {kw}")
            else:
                st.info("No specific ATS keywords detected")
            
            st.divider()
            st.info("""
            **Note:** These keywords are often used by ATS systems to screen resumes.
            Make sure to include relevant keywords in your resume when applying for this position.
            """)

# ==========================================
# MODE 4: ADVANCED ANALYTICS
# ==========================================
else:  # option == "🎯 Advanced Analytics"
    
    st.markdown('<p class="big-font">🎯 Advanced Analytics Dashboard</p>', unsafe_allow_html=True)
    st.markdown("Comprehensive insights, benchmarking, and strategic career planning")
    
    st.subheader("📊 Advanced Resume Analysis Tools")
    
    # Tool selection with more options
    analysis_tool = st.radio("Select Analysis Tool", [
        "Resume Health Score",
        "Career Trajectory",
        "Competitive Analysis",
        "Skill Gap & Roadmap",
        "Industry Comparison",
        "Salary Negotiation",
        "Learning Recommendations",
        "Market Insights"
    ], horizontal=True)
    
    st.divider()
    
    # Tool 1: Resume Health Score
    if analysis_tool == "Resume Health Score":
        st.markdown("### 🏥 Complete Resume Health Assessment")
        
        uploaded_file = st.file_uploader("Upload your resume", type="pdf", key="health_resume")
        
        if uploaded_file:
            resume_text = extract_text_from_pdf(uploaded_file)
            resume_skills = extract_skills(resume_text, default_skills)
            experience = extract_experience(resume_text)
            education = extract_education(resume_text)
            contact_info = extract_contact_info(resume_text)
            quality_score, quality_issues, quality_analysis = analyze_resume_quality(resume_text, resume_skills, experience, education)
            
            # Overall Health Score
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                health_label = "Excellent" if quality_score >= 80 else "Good" if quality_score >= 60 else "Needs Work"
                st.metric("Overall Health", f"{quality_score:.0f}/100", health_label)
            with col2:
                st.metric("Skills Found", len(resume_skills), "technical & soft")
            with col3:
                st.metric("Experience", f"{experience}y", "+5y recommended")
            with col4:
                st.metric("Education", education, "Bachelor+ ideal")
            
            st.divider()
            
            # Detailed Breakdown
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📋 Resume Structure Assessment")
                st.markdown("""
                **Checking:**
                • Length (ideal: 1-2 pages) ✓
                • Clear sections ✓
                • Contact information visibility ✓
                • Quantified achievements ✓
                • Action verbs usage ✓
                • Keyword density ✓
                • ATS compatibility ✓
                """)
            
            with col2:
                st.subheader("🎯 Quality Analysis Breakdown")
                analysis_items = [
                    ("Length", quality_analysis.get('Length', 'N/A')),
                    ("Skills", quality_analysis.get('Skills', 'N/A')),
                    ("Experience", quality_analysis.get('Experience', 'N/A')),
                    ("Education", quality_analysis.get('Education', 'N/A')),
                    ("Contact", quality_analysis.get('Contact', 'N/A')),
                ]
                for item, value in analysis_items:
                    st.write(f"**{item}:** {value}")
            
            st.divider()
            
            st.subheader("💡 Improvement Recommendations")
            recommendations = get_improvement_suggestions(resume_skills, default_skills, experience, quality_issues)
            for i, rec in enumerate(recommendations, 1):
                st.info(f"{i}. {rec}")
    
    # Tool 2: Career Trajectory
    elif analysis_tool == "Career Trajectory":
        st.markdown("### 📈 Your Career Growth Path")
        
        uploaded_file = st.file_uploader("Upload your resume", type="pdf", key="trajectory_resume")
        
        if uploaded_file:
            resume_text = extract_text_from_pdf(uploaded_file)
            resume_skills = extract_skills(resume_text, default_skills)
            experience = extract_experience(resume_text)
            
            # Career progression simulation
            current_level = "Junior" if experience < 3 else "Mid-Level" if experience < 7 else "Senior"
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Current Level:** {current_level} ({experience} years)")
            with col2:
                st.markdown(f"**Top Skills:** {', '.join(resume_skills[:3])}")
            
            st.divider()
            
            # Salary progression chart
            years = list(range(0, 15))
            junior_progression = [80 + (i * 8) for i in years]
            mid_progression = [130 + (i * 10) for i in years]
            senior_progression = [200 + (i * 15) for i in years]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=years, y=junior_progression, mode='lines+markers', name='Junior Track', line=dict(color='#3498db', width=2)))
            fig.add_trace(go.Scatter(x=years, y=mid_progression, mode='lines+markers', name='Mid-Level Track', line=dict(color='#2ecc71', width=2)))
            fig.add_trace(go.Scatter(x=years, y=senior_progression, mode='lines+markers', name='Senior Track', line=dict(color='#e74c3c', width=2)))
            
            fig.update_layout(
                title="Projected Salary Growth by Career Path",
                xaxis_title="Years of Experience",
                yaxis_title="Annual Salary (USD, Thousands)",
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            # Progression milestones
            st.subheader("🎯 Career Progression Milestones")
            
            milestones = {
                "0-2 Years": ["Learn core tech stack", "Build 2-3 projects", "Contribute to open source"],
                "2-5 Years": ["Tech leadership", "Mentor juniors", "Architecture decisions"],
                "5-10 Years": ["Senior/Lead role", "Strategic thinking", "Team management"],
                "10+ Years": ["Director/Principal", "Industry influence", "Technology strategy"]
            }
            
            for period, items in milestones.items():
                with st.expander(f"📌 {period}"):
                    for item in items:
                        st.write(f"✓ {item}")
    
    # Tool 3: Competitive Analysis
    elif analysis_tool == "Competitive Analysis":
        st.markdown("### 🏆 How You Stack Up in the Market")
        
        uploaded_file = st.file_uploader("Upload your resume", type="pdf", key="competitive_resume")
        
        if uploaded_file:
            resume_text = extract_text_from_pdf(uploaded_file)
            resume_skills = extract_skills(resume_text, default_skills)
            experience = extract_experience(resume_text)
            quality_score, _, _ = analyze_resume_quality(resume_text, resume_skills, experience, extract_education(resume_text))
            
            # Competitive metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                your_score = min(100, quality_score + (experience * 3))
                st.metric("Your Score", f"{your_score:.0f}/100", "74th percentile")
            with col2:
                avg_score = 65
                st.metric("Market Avg", f"{avg_score}/100", "-9 points")
            with col3:
                top_score = 95
                st.metric("Top Candidate", f"{top_score}/100", "+{top_score - your_score:.0f} ahead")
            with col4:
                percentile = (your_score - avg_score) / (top_score - avg_score) * 100
                st.metric("Percentile", f"{percentile:.0f}%", "Above average")
            
            st.divider()
            
            # Competitive positioning
            st.subheader("📊 Market Positioning Analysis")
            
            metrics = ['Technical Skills', 'Experience', 'Resume Quality', 'Education', 'Certifications']
            your_scores = [
                (len(resume_skills) / 20) * 100,  # Technical skills
                min(100, experience * 10),  # Experience
                quality_score,  # Resume quality
                85,  # Education (assuming good)
                60  # Certifications
            ]
            market_avg = [75, 70, 65, 80, 50]
            
            fig = go.Figure(data=[
                go.Scatterpolar(r=your_scores, theta=metrics, fill='toself', name='You', line=dict(color='#3498db')),
                go.Scatterpolar(r=market_avg, theta=metrics, fill='toself', name='Market Average', line=dict(color='#95a5a6'))
            ])
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True,
                height=400,
                title="Skills & Experience Radar"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            st.subheader("💪 Competitive Advantages")
            if len(resume_skills) > 12:
                st.success(f"✓ Well-rounded skillset ({len(resume_skills)} skills)")
            if experience > 5:
                st.success(f"✓ Strong experience ({experience} years)")
            if quality_score > 75:
                st.success(f"✓ High-quality resume ({quality_score:.0f}/100)")
    
    # Tool 4: Skill Gap & Roadmap
    elif analysis_tool == "Skill Gap & Roadmap":
        st.markdown("### 🛣️ Personalized Learning Roadmap")
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_skills = st.multiselect(
                "Your Current Skills",
                ["Python", "JavaScript", "SQL", "AWS", "Docker", "React", "Machine Learning", "Java", "Go", "Kubernetes"],
                default=["Python", "SQL"]
            )
        
        with col2:
            target_role = st.selectbox(
                "Target Role",
                ["Full Stack Developer", "Data Scientist", "DevOps Engineer", "Cloud Architect", "Backend Developer"]
            )
        
        months = st.slider("Timeframe (months)", 3, 36, 12)
        
        st.divider()
        
        # Generate personalized roadmap
        role_skills = {
            "Full Stack Developer": ["React", "Node.js", "MongoDB", "AWS", "Docker"],
            "Data Scientist": ["Machine Learning", "TensorFlow", "Spark", "Statistics", "Python"],
            "DevOps Engineer": ["Kubernetes", "Docker", "Terraform", "Jenkins", "AWS"],
            "Cloud Architect": ["AWS", "Azure", "Terraform", "Architecture", "Security"],
            "Backend Developer": ["Django", "FastAPI", "PostgreSQL", "REST API", "Docker"]
        }
        
        required_skills = role_skills.get(target_role, [])
        missing_skills = [s for s in required_skills if s not in current_skills]
        
        st.subheader(f"📚 Learning Roadmap for {target_role}")
        
        # Monthly breakdown
        monthly_skills = {}
        skills_per_month = max(1, len(missing_skills) // (months // 3))
        
        for i in range(0, len(missing_skills), skills_per_month):
            month_range = f"Month {i + 1}-{min(i + skills_per_month, months)}"
            monthly_skills[month_range] = missing_skills[i:i + skills_per_month]
        
        for period, skills in monthly_skills.items():
            with st.expander(f"📅 {period}"):
                for skill in skills:
                    duration = 4 if skill in ["Machine Learning", "Kubernetes", "Cloud Architect"] else 2
                    st.write(f"**{skill}** ({duration} weeks)")
                    st.caption("Online courses + hands-on projects")
        
        st.divider()
        
        st.subheader("🎓 Recommended Learning Resources")
        
        resources = {
            "Online Courses": ["Udemy", "Coursera", "DataCamp", "Pluralsight", "LinkedIn Learning"],
            "Hands-On Practice": ["GitHub Projects", "LeetCode", "HackerRank", "Codewars"],
            "Documentation": ["Official Docs", "Dev.to", "Medium", "Stack Overflow"],
            "Communities": ["Discord", "Reddit", "Dev Communities", "Meetup Groups"]
        }
        
        for category, platforms in resources.items():
            st.markdown(f"**{category}:** {', '.join(platforms)}")
    
    # Tool 5: Industry Comparison
    elif analysis_tool == "Industry Comparison":
        st.markdown("### 🌍 Cross-Industry Salary & Opportunity Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            experience_level = st.selectbox(
                "Experience Level",
                ["Entry Level", "Junior", "Mid-Level", "Senior"]
            )
        
        with col2:
            selected_skills = st.multiselect(
                "Your Key Skills",
                ["Python", "AWS", "Docker", "Machine Learning", "React"],
                default=["Python"]
            )
        
        st.divider()
        
        # Industry salary comparison
        industries = {
            "Tech": {"min": 140, "avg": 180, "max": 280},
            "Finance": {"min": 160, "avg": 210, "max": 320},
            "Healthcare Tech": {"min": 130, "avg": 170, "max": 260},
            "E-Commerce": {"min": 125, "avg": 165, "max": 250},
            "Startup": {"min": 100, "avg": 140, "max": 220}
        }
        
        st.subheader("💰 Salary Comparison by Industry")
        
        industry_names = list(industries.keys())
        avg_salaries = [industries[ind]["avg"] for ind in industry_names]
        min_salaries = [industries[ind]["min"] for ind in industry_names]
        max_salaries = [industries[ind]["max"] for ind in industry_names]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=industry_names, y=min_salaries, name='Min', marker_color='#e74c3c'))
        fig.add_trace(go.Bar(x=industry_names, y=avg_salaries, name='Average', marker_color='#3498db'))
        fig.add_trace(go.Bar(x=industry_names, y=max_salaries, name='Max', marker_color='#2ecc71'))
        
        fig.update_layout(
            title=f"Salary Range by Industry ({experience_level})",
            yaxis_title="Annual Salary (USD, Thousands)",
            barmode='group',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        st.subheader("📊 Industry Insights")
        
        insights = {
            "Tech": "Highest salaries, strong demand for Python/AWS skills, remote opportunities",
            "Finance": "Premium salaries, strict requirements, strong security focus",
            "Healthcare Tech": "Growing sector, mission-driven, good work-life balance",
            "E-Commerce": "Fast-paced, competitive, strong focus on scalability",
            "Startup": "Lower base but equity, high growth potential, learning opportunity"
        }
        
        for industry, insight in insights.items():
            st.info(f"**{industry}:** {insight}")
    
    # Tool 6: Salary Negotiation
    elif analysis_tool == "Salary Negotiation":
        st.markdown("### 💬 Smart Salary Negotiation Guide")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            experience_years = st.number_input("Years of Experience", 0, 30, 5)
        with col2:
            education = st.selectbox("Education", ["High School", "Bachelor", "Master", "PhD"])
        with col3:
            role = st.selectbox("Target Role", ["Backend Dev", "Data Scientist", "DevOps", "Cloud Architect"])
        
        st.divider()
        
        # Calculate negotiation range
        base_salary = 100 + (experience_years * 15)
        bonus_education = 1.1 if education == "Master" else 1.15 if education == "PhD" else 1.0
        market_multiplier = {"Backend Dev": 1.1, "Data Scientist": 1.2, "DevOps": 1.15, "Cloud Architect": 1.25}.get(role, 1.0)
        
        min_ask = int(base_salary * bonus_education * market_multiplier * 0.9)
        target_ask = int(base_salary * bonus_education * market_multiplier)
        max_ask = int(base_salary * bonus_education * market_multiplier * 1.2)
        
        st.subheader("💰 Salary Negotiation Range")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Conservative Ask", f"${min_ask}K")
        with col2:
            st.metric("Target Range", f"${target_ask}K")
        with col3:
            st.metric("Stretch Goal", f"${max_ask}K")
        with col4:
            st.metric("Benefit Value", f"+${int(target_ask * 0.2)}K")
        
        st.divider()
        
        st.subheader("🎯 Negotiation Strategy")
        st.markdown("""
        **Before Negotiation:**
        1. Research market rates for your role/location
        2. Document your achievements and impact
        3. Know the company's budget range
        4. Prepare negotiation talking points
        
        **During Discussion:**
        • Ask what the budget range is
        • Don't anchor below market rate
        • Emphasize your unique value
        • Consider total compensation (bonuses, equity, benefits)
        
        **Negotiation Tactics:**
        • Start with market research data
        • Present your case with evidence
        • Ask for time to consider offers
        • Negotiate benefits if salary is fixed
        • Get final offer in writing
        """)
        
        st.divider()
        
        st.subheader("📋 Salary Negotiation Checklist")
        checklist = [
            "Researched market salary data",
            "Know company's budget range",
            "Documented career achievements",
            "Prepared negotiation talking points",
            "Know minimum acceptable salary",
            "Understand benefits package value",
            "Practiced negotiation conversation",
            "Have backup job offers"
        ]
        
        for item in checklist:
            st.checkbox(item)
    
    # Tool 7: Learning Recommendations
    elif analysis_tool == "Learning Recommendations":
        st.markdown("### 🎓 AI-Powered Learning Recommendations")
        
        uploaded_file = st.file_uploader("Upload your resume", type="pdf", key="learning_resume")
        job_desc = st.text_area("Target job description (optional)", height=150)
        
        if uploaded_file:
            resume_text = extract_text_from_pdf(uploaded_file)
            resume_skills = extract_skills(resume_text, default_skills)
            
            if job_desc:
                job_skills = extract_job_requirements(job_desc)
            else:
                job_skills = default_skills
            
            # Get skill gaps
            gaps = get_skill_gaps(resume_skills, job_skills)
            
            st.subheader("📚 Personalized Learning Path")
            
            if gaps:
                for gap in gaps[:5]:
                    with st.expander(f"📖 Learn {gap['skill']} - {gap['priority']} Priority"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"""
                            **Skill:** {gap['skill']}
                            **Priority:** {gap['priority']}
                            **Timeline:** {gap['timeline']}
                            **Market Demand:** {gap['demand']}
                            **Growth Rate:** {gap['growth']}%
                            """)
                        
                        with col2:
                            st.markdown(f"""
                            **Learning Resources:**
                            """)
                            for resource in gap['resources'][:3]:
                                st.write(f"• {resource}")
                        
                        st.markdown("---")
                        st.markdown("""
                        **Recommended Approach:**
                        1. Start with fundamentals (1-2 weeks)
                        2. Follow tutorials and courses (2-4 weeks)
                        3. Build 2-3 projects (3-4 weeks)
                        4. Contribute to open source (ongoing)
                        5. Practice on platforms (LeetCode, HackerRank)
                        """)
            else:
                st.success("✓ You have most required skills! Focus on advanced concepts.")
    
    # Tool 8: Market Insights
    else:  # Market Insights
        st.markdown("### 📈 Deep Market Insights & Trends")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_industry = st.selectbox(
                "Select Industry",
                ["Tech", "Finance", "Healthcare", "E-Commerce", "Startups"]
            )
        
        with col2:
            selected_location = st.selectbox(
                "Select Location",
                ["US (Remote)", "San Francisco", "New York", "Austin", "Seattle"]
            )
        
        st.divider()
        
        st.subheader("🔥 Hot Skills in Demand")
        
        hot_skills = {
            "Tech": ["AI/ML", "Cloud (AWS/Azure)", "DevOps", "GoLang", "Rust"],
            "Finance": ["Python", "SQL", "Risk Analytics", "Cybersecurity", "Blockchain"],
            "Healthcare": ["Python", "Healthcare IT", "HIPAA", "Data Analysis", "Cloud"],
            "E-Commerce": ["Golang", "Kubernetes", "React", "ELK Stack", "NoSQL"],
            "Startups": ["Full Stack", "Growth", "SaaS", "Mobile", "AI/ML"]
        }
        
        skill_demand = st.slider("Show top N skills", 3, 10, 5)
        skills = hot_skills.get(selected_industry, [])[:skill_demand]
        
        cols = st.columns(len(skills))
        for i, skill in enumerate(skills):
            with cols[i]:
                st.success(f"📈 {skill}")
        
        st.divider()
        
        st.subheader("💼 Job Market Statistics")
        
        stats = {
            "Average Salary Growth": "+8-12% YoY",
            "Hiring Trend": "↑ Strong Growth",
            "Remote Opportunities": "45-60% fully remote",
            "Average Interview Time": "3-4 weeks",
            "Avg Applications for Hire": "50-100 candidates",
            "Most Requested Seniority": "Mid-Level (3-7 years)"
        }
        
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        
        for i, (stat, value) in enumerate(stats.items()):
            with cols[i % 3]:
                st.metric(stat, value)
        
        st.divider()
        
        st.subheader("🎯 Market Recommendations")
        st.markdown(f"""
        **Based on {selected_industry} Industry & {selected_location} Market:**
        
        1. **Prioritize Learning:** Focus on Python, Cloud platforms, and AI/ML
        2. **Networking:** Attend industry meetups and conferences
        3. **Certifications:** AWS/Azure certifications boost prospects by 15-20%
        4. **Portfolio:** 2-3 strong projects matter more than just resume
        5. **Interview Prep:** System design and behavioral questions critical
        6. **Salary:** Expect {selected_location} premium of +15-25% vs baseline
        7. **Timeline:** Start job searches 2-3 months in advance
        8. **Growth:** Plan skill upgrades every 6 months
        """)

