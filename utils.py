"""
Advanced Resume Analyzer - Core Engine
Industry-accurate skill matching, salary prediction, and analysis
Updated 2024-2026 with real market data
"""

import re
from PyPDF2 import PdfReader
from io import BytesIO
from industry_data import (
    TECHNICAL_SKILLS, SOFT_SKILLS, CREATIVE_SKILLS, JOB_PROFILES,
    INDUSTRY_SALARY_DATA, SKILL_ALIASES, SKILL_MULTIPLIERS,
    LEARNING_PATHS, QUALITY_RUBRIC, CERTIFICATIONS_BY_INDUSTRY
)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF with robust error handling."""
    try:
        if isinstance(pdf_file, bytes):
            pdf_reader = PdfReader(BytesIO(pdf_file))
        else:
            pdf_reader = PdfReader(pdf_file)
        
        if len(pdf_reader.pages) == 0:
            return "Error: PDF has no pages"
        
        text = ""
        for page in pdf_reader.pages:
            try:
                text += page.extract_text() + "\n"
            except Exception:
                continue
        
        return text.strip() if text.strip() else "Error: Could not extract text"
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"


def normalize_skill(skill):
    """Normalize skill name for comparison."""
    return skill.lower().strip()


def is_technical_skill(skill):
    """Check if a skill is technical (not soft skill)."""
    skill_norm = normalize_skill(skill)
    
    # Check if it's in technical skills database
    for tech_skill in TECHNICAL_SKILLS.keys():
        if normalize_skill(tech_skill) == skill_norm:
            return True
    
    # Check against soft skills - if it's in soft skills, it's not technical
    for soft_skill in SOFT_SKILLS.keys():
        if normalize_skill(soft_skill) == skill_norm:
            return False
    
    # Heuristic: common soft skills to exclude
    soft_skill_keywords = {
        'communication', 'leadership', 'teamwork', 'collaboration',
        'problem solving', 'project management', 'time management',
        'critical thinking', 'negotiation', 'presentation', 'mentoring',
        'adaptability', 'creativity', 'emotional intelligence'
    }
    
    return skill_norm not in soft_skill_keywords


def filter_technical_skills(skills):
    """Filter a list to only include technical skills."""
    return [skill for skill in skills if is_technical_skill(skill)]


def expand_skill_with_aliases(skill):
    """Expand skill with all known aliases."""
    skill_norm = normalize_skill(skill)
    
    # Check if exact match in aliases
    if skill_norm in SKILL_ALIASES:
        return [skill_norm] + SKILL_ALIASES[skill_norm]
    
    # Check if this skill is an alias of something else
    for main_skill, aliases in SKILL_ALIASES.items():
        if skill_norm in aliases:
            return [main_skill] + aliases
    
    return [skill_norm]


def extract_skills(text, skills=None):
    """
    Extract skills with intelligent matching including aliases.
    Uses industry-based skill database for accuracy.
    """
    if not text or not isinstance(text, str):
        return []
    
    # Use all technical + soft skills if not specified
    if skills is None:
        all_skills = list(TECHNICAL_SKILLS.keys()) + list(SOFT_SKILLS.keys())
    else:
        all_skills = list(skills)
    
    text_lower = text.lower()
    detected_skills = set()
    
    for skill in all_skills:
        skill_norm = normalize_skill(skill)
        
        # Check direct match
        if skill_norm in text_lower:
            detected_skills.add(skill)
        
        # Check with aliases
        for alias in expand_skill_with_aliases(skill_norm):
            if alias != skill_norm and f' {alias} ' in f' {text_lower} ':
                detected_skills.add(skill)
            elif f' {alias}' in text_lower or text_lower.startswith(alias):
                detected_skills.add(skill)
            elif text_lower.endswith(f' {alias}'):
                detected_skills.add(skill)
    
    return sorted(list(detected_skills))


def extract_experience(text):
    """Extract years of experience with accuracy and fallback logic."""
    patterns = [
        r'(\d+)\s+(?:years?|yrs?)',
        r'(\d+)\+\s+(?:years?|yrs?)',
        r'(?:since|from)\s+(?:20\d{2}|19\d{2})',  # Extract from year
    ]
    
    matches = []
    for pattern in patterns:
        found = re.findall(pattern, text, re.IGNORECASE)
        for item in found:
            try:
                # If it's a year, calculate experience
                if len(str(item)) == 4:
                    year = int(item)
                    exp = 2026 - year
                    if 0 < exp <= 60:  # Reasonable experience range
                        matches.append(exp)
                else:
                    matches.append(int(item))
            except:
                continue
    
    if matches:
        exp_val = max(matches)
        return min(exp_val, 50)  # Cap at 50 years
    return 0


def extract_education(text):
    """Extract education level with industry standards."""
    education_mapping = {
        'PhD': ['phd', 'doctorate', 'doctor of philosophy', 'postdoctoral'],
        'Master': ['master\'?s?', 'ms', 'm.s', 'mba', 'mtech', 'm.tech'],
        'Bachelor': ['bachelor\'?s?', 'bs', 'b.s', 'b.tech', 'btech', 'bsc', 'b.sc'],
        'Diploma': ['diploma', 'associate', 'a.s'],
        'High School': ['high school', 'secondary', 'h.s', 'hs'],
    }
    
    text_lower = text.lower()
    
    for degree, patterns in education_mapping.items():
        for pattern in patterns:
            if re.search(r'\b' + pattern + r'\b', text_lower):
                return degree
    
    return "Not Mentioned"


def extract_contact_info(text):
    """Extract and validate contact information."""
    info = {
        'email': None,
        'phone': None,
        'linkedin': None,
    }
    
    # Email pattern
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    if email_match:
        info['email'] = email_match.group(0)
    
    # Phone pattern
    phone_match = re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)
    if phone_match:
        info['phone'] = phone_match.group(0)
    
    # LinkedIn
    linkedin_match = re.search(r'linkedin\.com/in/[A-Za-z0-9-]+', text, re.IGNORECASE)
    if linkedin_match:
        info['linkedin'] = linkedin_match.group(0)
    
    return info


def categorize_skills(skills):
    """Categorize skills into technical, soft, creative, and tools (case-insensitive)."""
    technical = []
    soft = []
    creative = []
    tools = []
    tech_norm_to_name = {normalize_skill(k): k for k in TECHNICAL_SKILLS}
    soft_norm_to_name = {normalize_skill(k): k for k in SOFT_SKILLS}
    creative_norm_to_name = {normalize_skill(k): k for k in CREATIVE_SKILLS}

    for skill in skills:
        sn = normalize_skill(skill)
        if sn in tech_norm_to_name:
            technical.append(tech_norm_to_name[sn])
        elif sn in soft_norm_to_name:
            soft.append(soft_norm_to_name[sn])
        elif sn in creative_norm_to_name:
            creative.append(creative_norm_to_name[sn])
        else:
            tools.append(skill)

    return {
        'technical': sorted(set(technical)),
        'soft': sorted(set(soft)),
        'creative': sorted(set(creative)),
        'tools': sorted(set(tools)),
        'total': len(skills)
    }


def extract_keywords(text):
    """Extract important keywords from text."""
    keywords = []
    text_lower = text.lower()
    
    ats_keywords = {
        'experience', 'responsibility', 'skill', 'requirement', 'qualification',
        'lead', 'manage', 'develop', 'design', 'implement', 'bachelor', 'master'
    }
    
    for keyword in ats_keywords:
        if keyword in text_lower:
            keywords.append(keyword.title())
    
    return list(set(keywords))


def extract_job_requirements(job_description):
    """Extract skills from job description. Uses JD-only skills for non-tech roles (Video Editor, etc.)."""
    if not job_description or len(job_description.strip()) < 10:
        return []

    # Include creative/design/video skills so we detect Premiere Pro, After Effects, etc.
    all_skills = list(TECHNICAL_SKILLS.keys()) + list(SOFT_SKILLS.keys()) + list(CREATIVE_SKILLS.keys())

    job_lower = job_description.lower()
    detected_skills = set()

    # First pass: explicit requirement sections
    requirement_patterns = [
        'required skills:', 'must have:', 'should have:', 'preferred skills:',
        'looking for:', 'we need:', 'seeking:', 'responsibilities:', 'qualifications:',
        'required:', 'preferred:', 'must:', 'skills needed:', 'technical skills:',
        'you should have:', 'you will need:', 'requirement', 'key skills:', 'tools:'
    ]
    requirement_sections = []
    for pattern in requirement_patterns:
        if pattern in job_lower:
            idx = job_lower.find(pattern)
            start = idx + len(pattern)
            end = min(start + 500, len(job_description))
            requirement_sections.append(job_description[start:end])

    for section in requirement_sections:
        detected_skills.update(extract_skills(section, all_skills))

    if not detected_skills:
        detected_skills.update(extract_skills(job_description, all_skills))

    if len(detected_skills) < 5:
        skill_indicators = [
            'experience with', 'knowledge of', 'fluent in', 'skilled in',
            'proficiency', 'familiar with', 'expertise in', 'work with', 'proficient in'
        ]
        for indicator in skill_indicators:
            parts = job_lower.split(indicator)
            for i in range(1, len(parts)):
                detected_skills.update(extract_skills(parts[i][:150], all_skills))

    detected_role = detect_job_role(job_description)

    # Only merge role defaults when this role is in our list. Non-tech roles get ONLY JD-extracted skills.
    role_defaults = {
        'Backend Developer': ['Python', 'Django', 'REST API', 'PostgreSQL', 'AWS', 'SQL', 'Git'],
        'Frontend Developer': ['React', 'JavaScript', 'HTML', 'CSS', 'TypeScript', 'REST API', 'Git'],
        'Full Stack Developer': ['React', 'Node.js', 'Python', 'SQL', 'AWS', 'Git', 'REST API', 'HTML', 'CSS'],
        'DevOps Engineer': ['Docker', 'Kubernetes', 'AWS', 'Jenkins', 'Terraform', 'Linux', 'Git', 'CI/CD'],
        'Cloud Architect': ['AWS', 'Azure', 'Google Cloud', 'Terraform', 'System Design', 'Security', 'Docker'],
        'Data Scientist': ['Python', 'Machine Learning', 'SQL', 'TensorFlow', 'Pandas', 'Statistics', 'NumPy', 'Data Analysis'],
        'Data Engineer': ['Python', 'SQL', 'Spark', 'Hadoop', 'AWS', 'ETL', 'Data Pipelines'],
        'Data Analyst': ['SQL', 'Excel', 'Tableau', 'Python', 'Power BI', 'Data Analysis', 'Statistics'],
        'QA Engineer': ['TestNG', 'Selenium', 'Automation', 'Java', 'Testing', 'Git', 'CI/CD'],
        'Security Engineer': ['Linux', 'Cybersecurity', 'AWS', 'Encryption', 'Penetration Testing', 'Security'],
        'Machine Learning Engineer': ['Python', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'SQL', 'Git'],
        'ML Engineer': ['Python', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'SQL'],
        'Software Engineer': ['Python', 'JavaScript', 'SQL', 'Git', 'REST API', 'Problem Solving'],
        'Video Editor': ['Premiere Pro', 'After Effects', 'Video Editing', 'Motion Graphics', 'DaVinci Resolve', 'Color Grading'],
        'Graphic Designer': ['Photoshop', 'Illustrator', 'Graphic Design', 'Figma', 'Canva', 'UI Design'],
        'Content Writer': ['Content Writing', 'Copywriting', 'SEO', 'Communication'],
        'Digital Marketing': ['Digital Marketing', 'SEO', 'Social Media Marketing', 'Content Writing', 'Google Analytics', 'Email Marketing'],
        'Social Media Manager': ['Social Media Marketing', 'Content Writing', 'Communication', 'Canva'],
        'Product Manager': ['Project Management', 'Communication', 'Problem Solving', 'SQL', 'Data Analysis', 'Agile'],
        'Project Manager': ['Project Management', 'Communication', 'Leadership', 'Agile', 'Problem Solving'],
        'Business Analyst': ['SQL', 'Excel', 'Data Analysis', 'Communication', 'Problem Solving'],
        'Scrum Master': ['Agile', 'Project Management', 'Communication', 'Leadership'],
        'iOS Developer': ['Swift', 'iOS', 'Git', 'REST API', 'Problem Solving'],
        'Android Developer': ['Kotlin', 'Java', 'Git', 'REST API', 'Problem Solving'],
        '.NET Developer': ['C#', 'SQL', 'REST API', 'Git', 'Problem Solving'],
        'Technical Writer': ['Content Writing', 'Communication', 'Documentation', 'Technical Writing'],
        'UX Designer': ['UX Design', 'Figma', 'User Research', 'Wireframing', 'Prototyping'],
        'UI Designer': ['UI Design', 'Figma', 'Photoshop', 'Illustrator', 'Design Systems'],
        'Motion Graphics Designer': ['After Effects', 'Motion Graphics', 'Premiere Pro', 'Cinematography'],
        'Video Producer': ['Video Production', 'Premiere Pro', 'Video Editing', 'Project Management'],
    }

    if detected_role in role_defaults and len(detected_skills) < 6:
        # Known role and few skills from JD: add that role's defaults so we have a fuller list
        for s in role_defaults[detected_role]:
            detected_skills.add(s)
    elif detected_role not in role_defaults:
        # Other Role / extracted title: do NOT add tech skills. Use only what we extracted.
        if not detected_skills and detected_role != 'Other Role':
            detected_skills.add(detected_role)

    return sorted(list(detected_skills))


# ============================================================================
# MATCHING & SCORING FUNCTIONS
# ============================================================================

def calculate_match(resume_skills, job_requirements):
    """
    Calculate precise skill match percentage.
    Returns (match_percentage, matched_skills_list, missing_skills_list)
    """
    if isinstance(job_requirements, str):
        required_skills = extract_skills(job_requirements)
    else:
        required_skills = list(job_requirements)
    
    if not required_skills:
        return 0, [], []
    
    resume_set = set(normalize_skill(s) for s in resume_skills)
    required_set = set(normalize_skill(s) for s in required_skills)
    
    matched = resume_set & required_set
    missing = required_set - resume_set
    
    match_percentage = (len(matched) / len(required_set)) * 100 if required_set else 0
    
    # Return with original casing
    matched_with_case = [s for s in resume_skills if normalize_skill(s) in matched]
    
    return round(match_percentage, 2), matched_with_case, list(missing)


def calculate_weighted_match_score(resume_skills, job_requirements):
    """
    Calculate weighted match using skill importance from industry data.
    More accurate for real job matching.
    """
    if isinstance(job_requirements, str):
        required_skills = extract_skills(job_requirements)
    else:
        required_skills = list(job_requirements)
    
    if not required_skills:
        return 0
    
    resume_norm = {normalize_skill(s): s for s in resume_skills}
    total_weight = 0
    matched_weight = 0
    
    for req_skill in required_skills:
        req_norm = normalize_skill(req_skill)
        
        # Get multiplier for this skill
        multiplier = SKILL_MULTIPLIERS.get(req_norm, 1.0)
        weight = (1.0 + multiplier) * 10  # Base 10 points + multiplier
        
        total_weight += weight
        
        if req_norm in resume_norm:
            matched_weight += weight
    
    if total_weight == 0:
        return 0
    
    return round((matched_weight / total_weight) * 100, 2)


# ============================================================================
# RESUME QUALITY ANALYSIS
# ============================================================================

def analyze_resume_quality(resume_text, resume_skills, experience, education):
    """
    Comprehensive resume quality scoring using industry rubric.
    Returns (score, detailed_issues_list, detailed_analysis_dict)
    """
    if not resume_text or not isinstance(resume_text, str):
        return 0, ["Resume text is empty"], {}
    
    total_score = 0
    issues = []
    analysis = {}
    
    # 1. TEXT LENGTH QUALITY (15 points)
    char_count = len(resume_text)
    rubric = QUALITY_RUBRIC['length']
    if char_count >= rubric['excellent']:
        total_score += rubric['points']
        analysis['Length'] = f"Excellent ({char_count} characters)"
    elif char_count >= rubric['good']:
        total_score += 12
        analysis['Length'] = f"Good ({char_count} characters)"
    elif char_count >= rubric['acceptable']:
        total_score += 8
        analysis['Length'] = f"Acceptable ({char_count} characters)"
        issues.append(f"Resume text is short ({char_count} chars, 800+ recommended)")
    else:
        analysis['Length'] = f"Too short ({char_count} characters)"
        issues.append(f"Resume is too brief ({char_count} chars, minimum 400 required)")
    
    # 2. SKILLS QUALITY (15 points)
    skill_count = len(resume_skills)
    rubric = QUALITY_RUBRIC['skills_count']
    if skill_count >= rubric['excellent']:
        total_score += rubric['points']
        analysis['Skills'] = f"Excellent ({skill_count} skills)"
    elif skill_count >= rubric['good']:
        total_score += 12
        analysis['Skills'] = f"Good ({skill_count} skills)"
    elif skill_count >= rubric['acceptable']:
        total_score += 8
        analysis['Skills'] = f"Acceptable ({skill_count} skills)"
    else:
        analysis['Skills'] = f"Limited ({skill_count} skills)"
        issues.append(f"Too few skills ({skill_count}, 8+ recommended)")
    
    # 3. EXPERIENCE QUALITY (20 points)
    exp_rubric = QUALITY_RUBRIC['experience']
    if experience >= exp_rubric['excellent']:
        total_score += exp_rubric['points']
        analysis['Experience'] = f"Excellent ({experience}+ years)"
    elif experience >= exp_rubric['good']:
        total_score += 15
        analysis['Experience'] = f"Good ({experience} years)"
    elif experience >= exp_rubric['acceptable']:
        total_score += 10
        analysis['Experience'] = f"Entry level ({experience} year)"
    else:
        analysis['Experience'] = "No experience found"
        issues.append("Include years of professional experience")
    
    # 4. EDUCATION QUALITY (15 points)
    edu_rubric = QUALITY_RUBRIC['education']
    if education in edu_rubric['excellent']:
        total_score += edu_rubric['points']
        analysis['Education'] = f"Excellent ({education})"
    elif education in edu_rubric['good']:
        total_score += 12
        analysis['Education'] = f"Good ({education})"
    elif education in edu_rubric['acceptable']:
        total_score += 8
        analysis['Education'] = f"Basic ({education})"
    else:
        analysis['Education'] = "Not mentioned"
        issues.append("Mention your educational background")
    
    # 5. CONTACT INFORMATION (10 points)
    contact_info = extract_contact_info(resume_text)
    contact_found = sum(1 for v in contact_info.values() if v)
    
    if contact_found >= 3:
        total_score += 10
        analysis['Contact'] = "Perfect (all info included)"
    elif contact_found >= 2:
        total_score += 8
        analysis['Contact'] = "Good (email + phone or LinkedIn)"
    elif contact_found >= 1:
        total_score += 5
        analysis['Contact'] = "Partial (at least one item)"
        issues.append("Add more contact information (email, phone, LinkedIn)")
    else:
        analysis['Contact'] = "Missing"
        issues.append("Add contact information: email, phone, LinkedIn")
    
    # 6. RESUME SECTIONS (10 points)
    required_sections = QUALITY_RUBRIC['sections']['required']
    found_sections = []
    for section in required_sections:
        if section.lower() in resume_text.lower():
            found_sections.append(section)
    
    if len(found_sections) >= 3:
        total_score += 10
        analysis['Sections'] = f"Perfect ({', '.join(found_sections)})"
    elif len(found_sections) >= 2:
        total_score += 7
        analysis['Sections'] = f"Good ({', '.join(found_sections)})"
        missing = [s for s in required_sections if s not in found_sections]
        issues.append(f"Add {missing[0].lower()} section")
    else:
        total_score += 3
        analysis['Sections'] = f"Incomplete ({', '.join(found_sections)})"
        issues.append("Include Experience, Education, and Skills sections")
    
    # 7. ACTION VERBS (10 points)
    verbs = QUALITY_RUBRIC['action_verbs']['verbs']
    verb_count = sum(resume_text.lower().count(verb.lower()) for verb in verbs)
    
    if verb_count >= 8:
        total_score += 10
        analysis['Action Verbs'] = f"Excellent ({verb_count} verbs)"
    elif verb_count >= 5:
        total_score += 7
        analysis['Action Verbs'] = f"Good ({verb_count} verbs)"
    elif verb_count >= 2:
        total_score += 4
        analysis['Action Verbs'] = f"Some ({verb_count} verbs)"
        issues.append("Use more action verbs (led, developed, managed, created, etc.)")
    else:
        analysis['Action Verbs'] = "Needs improvement"
        issues.append("Start bullet points with strong action verbs")
    
    # 8. QUANTIFICATION (5 points)
    metric_keywords = QUALITY_RUBRIC['quantification']['metric_verbs']
    metrics_found = sum(resume_text.count(keyword) for keyword in metric_keywords)
    
    if metrics_found >= 5:
        total_score += 5
        analysis['Metrics'] = f"Excellent ({metrics_found} metrics)"
    elif metrics_found >= 2:
        total_score += 3
        analysis['Metrics'] = f"Good ({metrics_found} metrics)"
    else:
        analysis['Metrics'] = "Needs more quantification"
        issues.append("Add metrics/numbers to achievements (e.g., 20% improvement)")
    
    # Final score
    final_score = min(100, total_score)
    
    return round(final_score, 1), issues, analysis


# ============================================================================
# SALARY PREDICTION
# ============================================================================

def predict_salary(experience_years, resume_skills, education, industry='Tech'):
    """
    Predict salary based on industry data with accuracy.
    Considers experience, skills, education, and industry.
    """
    try:
        if isinstance(experience_years, int):
            exp = experience_years
        else:
            match = re.search(r'\d+', str(experience_years))
            exp = int(match.group(0)) if match else 0
    except:
        exp = 0
    
    exp = min(exp, 30)  # Cap at 30 years for realistic calculation
    
    # Get industry salary data
    industry_data = INDUSTRY_SALARY_DATA.get(industry, INDUSTRY_SALARY_DATA['Tech'])
    
    # Determine level
    if exp < 2:
        level = 'Entry Level'
    elif exp < 5:
        level = 'Junior'
    elif exp < 10:
        level = 'Mid-Level'
    elif exp < 15:
        level = 'Senior'
    else:
        level = 'Staff+'
    
    base_salary = industry_data.get(level, industry_data['Mid-Level'])
    
    # Calculate skill multiplier
    skill_multiplier = 1.0
    resume_norm = {normalize_skill(s) for s in resume_skills}
    
    for skill, premium in SKILL_MULTIPLIERS.items():
        if skill in resume_norm:
            skill_multiplier += premium
    
    skill_multiplier = min(2.0, skill_multiplier)  # Cap at 2x
    
    # Education multiplier
    education_mult = 1.0
    if education == 'PhD':
        education_mult = 1.15
    elif education == 'Master':
        education_mult = 1.10
    elif education == 'Bachelor':
        education_mult = 1.05
    
    # Experience increment
    exp_mult = 1.0 + (min(exp, 20) * 0.02)  # 2% per year
    
    # Calculate final salary
    total_mult = skill_multiplier * education_mult * exp_mult
    
    min_sal = base_salary['min'] * total_mult
    avg_sal = base_salary['avg'] * total_mult
    max_sal = base_salary['max'] * total_mult
    
    return {
        'min': round(max(35, min_sal), 0),
        'avg': round(max(50, avg_sal), 0),
        'max': round(max(70, max_sal), 0),
        'level': level,
        'currency': 'USD',
        'period': 'annual (2024-2026)',
    }


# ============================================================================
# CAREER INSIGHTS
# ============================================================================

def get_skill_gaps(resume_skills, job_requirements):
    """Identify technical skill gaps with learning resources."""
    if isinstance(job_requirements, str):
        required = extract_skills(job_requirements)
    else:
        required = list(job_requirements)

    resume_norm = {normalize_skill(s) for s in resume_skills}
    required_norm = {normalize_skill(s) for s in required}
    missing = required_norm - resume_norm
    tech_norm = {normalize_skill(s) for s in TECHNICAL_SKILLS.keys()}
    default_resources = ['Udemy', 'Coursera', 'Official documentation', 'Hands-on projects']

    gaps = []
    for skill in sorted(missing):
        display_name = skill.title()
        path = LEARNING_PATHS.get(display_name, {})
        skill_data = TECHNICAL_SKILLS.get(display_name, {})

        if skill in tech_norm:
            priority = 'Critical' if skill in SKILL_MULTIPLIERS else 'High'
            timeline = path.get('timeline', '6-12 weeks')
            resources = path.get('entry', []) or default_resources
            demand = skill_data.get('demand', 'Medium')
            growth = skill_data.get('growth', 0)
        else:
            # Missing skill not in TECHNICAL_SKILLS (e.g. "Database Design") - still show as gap
            priority = 'High'
            timeline = '6-12 weeks'
            resources = default_resources
            demand = 'Medium'
            growth = 0

        gaps.append({
            'skill': display_name,
            'priority': priority,
            'timeline': timeline,
            'resources': resources,
            'demand': demand,
            'growth': growth
        })

    return gaps[:8]


def get_interview_readiness_score(resume_skills, job_requirements, experience, education):
    """Calculate interview readiness score."""
    match_pct, matched, missing = calculate_match(resume_skills, job_requirements)
    
    score = 0
    strengths = []
    concerns = []
    
    # Experience factor (30 pts)
    if experience >= 5:
        score += 30
        strengths.append(f"Strong experience ({experience}+ years)")
    elif experience >= 2:
        score += 20
        strengths.append(f"Relevant experience ({experience} years)")
    elif experience >= 1:
        score += 10
        concerns.append("Limited experience - prepare examples")
    else:
        concerns.append("Entry-level position - emphasize learning")
    
    # Skills match (40 pts)
    if match_pct >= 90:
        score += 40
        strengths.append(f"Expert match ({match_pct}% of required skills)")
    elif match_pct >= 70:
        score += 30
        strengths.append(f"Good match ({match_pct}% of required skills)")
    elif match_pct >= 50:
        score += 20
        concerns.append("Moderate skill gaps—prepare a learning plan.")
    else:
        score += 10
        concerns.append("Highlight transferable skills to offset gaps.")
    
    # Education (15 pts)
    if education in ['Master', 'PhD']:
        score += 15
        strengths.append(f"Advanced degree ({education})")
    elif education == 'Bachelor':
        score += 10
    
    # Technical depth (15 pts)
    tech_skills = [s for s in resume_skills if s in TECHNICAL_SKILLS]
    if len(tech_skills) >= 10:
        score += 15
        strengths.append("Strong technical depth")
    elif len(tech_skills) >= 5:
        score += 10
    
    return {
        'score': min(100, score),
        'strengths': strengths[:3],
        'concerns': concerns[:3],
        'readiness_level': 'Excellent' if score >= 85 else 'Very Good' if score >= 75 else 'Good' if score >= 60 else 'Fair'
    }


def get_career_progression_path(experience_years, resume_skills, job_description=''):
    """Suggest realistic IT industry career progression paths based on current skills."""
    try:
        if isinstance(experience_years, int):
            exp = experience_years
        else:
            match = re.search(r'\d+', str(experience_years))
            exp = int(match.group(0)) if match else 0
    except:
        exp = 0
    
    paths = []
    resume_norm = {normalize_skill(s) for s in resume_skills}
    
    # Python/Backend Developer Path
    if any(s in resume_norm for s in ['python', 'java', 'javascript', 'node.js']):
        if exp < 2:
            paths.append({
                'title': 'Mid-Level Developer',
                'timeline': '1-2 years',
                'salary_increase': '15-25%',
                'skills': ['System Design', 'SQL Optimization', 'API Design', 'Code Architecture']
            })
        elif exp < 5:
            paths.append({
                'title': 'Senior Developer',
                'timeline': '2-3 years',
                'salary_increase': '25-40%',
                'skills': ['System Architecture', 'Performance Tuning', 'Security Practices', 'Tech Leadership']
            })
        else:
            paths.append({
                'title': 'Tech Lead / Engineering Manager',
                'timeline': '3-5 years',
                'salary_increase': '35-60%',
                'skills': ['Team Leadership', 'Strategic Planning', 'Mentoring', 'Project Management']
            })
    
    # Cloud/DevOps Path
    if any(s in resume_norm for s in ['aws', 'azure', 'docker', 'kubernetes']):
        if exp < 2:
            paths.append({
                'title': 'Cloud Engineer',
                'timeline': '1-2 years',
                'salary_increase': '20-30%',
                'skills': ['Container Orchestration', 'Infrastructure as Code', 'CI/CD', 'Cloud Security']
            })
        elif exp < 5:
            paths.append({
                'title': 'Senior DevOps/Cloud Engineer',
                'timeline': '2-3 years',
                'salary_increase': '30-45%',
                'skills': ['Multi-Cloud Architecture', 'Kubernetes Mastery', 'Terraform', 'Cost Optimization']
            })
        else:
            paths.append({
                'title': 'Cloud Architect',
                'timeline': '2-4 years',
                'salary_increase': '40-70%',
                'skills': ['Enterprise Architecture', 'Compliance & Security', 'Disaster Recovery', 'Cost Strategy']
            })
    
    # Data/ML Path
    if any(s in resume_norm for s in ['machine learning', 'deep learning', 'python']):
        if exp < 3:
            paths.append({
                'title': 'ML Engineer',
                'timeline': '2-3 years',
                'salary_increase': '25-35%',
                'skills': ['Deep Learning Frameworks', 'Model Optimization', 'Feature Engineering', 'MLOps']
            })
        else:
            paths.append({
                'title': 'Senior ML Engineer / ML Architect',
                'timeline': '3-4 years',
                'salary_increase': '40-60%',
                'skills': ['Advanced ML Architectures', 'Distributed ML', 'Research', 'Production ML Systems']
            })
    
    # Default if no specific path matched
    if not paths:
        paths.append({
            'title': 'Senior Specialist',
            'timeline': '2-3 years',
            'salary_increase': '20-30%',
            'skills': ['Advanced Expertise', 'Leadership', 'Specialization', 'Innovation']
        })
    
    return paths[:3]


# ============================================================================
# RECOMMENDATIONS & ANALYSIS
# ============================================================================

def get_improvement_suggestions(resume_skills, job_requirements, experience, quality_issues):
    """Generate actionable recommendations."""
    recommendations = []

    if quality_issues:
        recommendations.extend(quality_issues[:3])

    _, _, missing = calculate_match(resume_skills, job_requirements)
    if missing:
        display_skills = [s.title() for s in list(missing)[:3]]
        recommendations.append(f"Learn in-demand skills: {', '.join(display_skills)}")

    if not recommendations:
        recommendations.append("✓ Resume and skills look great! Focus on interview preparation.")

    return recommendations[:5]


def analyze_skill_gaps(resume_skills, job_requirements):
    """Analyze skill gaps with learning time estimates."""
    gaps = get_skill_gaps(resume_skills, job_requirements)
    return gaps


def detect_job_role(job_description):
    """Detect the job role/title from job description. Non-tech roles checked first."""
    if not job_description or not isinstance(job_description, str):
        return 'Software Engineer'

    # Normalize: single spaces, no extra newlines – so "digital  marketing" / "digital\nmarketing" match
    job_lower = re.sub(r'\s+', ' ', job_description.lower().strip())

    # Non-tech / creative roles FIRST – strong phrases so wrong tech role na aaye
    exact_phrases_non_tech = {
        'Digital Marketing': [
            'digital marketing', 'digital marketer', 'digital markiting', 'digital markting',
            'marketing specialist', 'performance marketing', 'growth marketing', 'online marketing',
            'digital marketing manager', 'dm manager', 'seo specialist', 'ppc specialist',
            'we are hiring for digital marketing', 'job for digital marketing', 'role: digital marketing',
        ],
        'Video Editor': [
            'video editor', 'video editing', 'video edit', 'we are hiring video editor', 'looking for video editor',
        ],
        'Graphic Designer': ['graphic designer', 'graphic design', 'visual designer'],
        'Content Writer': ['content writer', 'content writing', 'content creator', 'copywriter'],
        'Social Media Manager': [
            'social media manager', 'social media specialist', 'smm ', 'social media marketing',
            'social media coordinator', 'community manager',
        ],
        'UX Designer': ['ux designer', 'ux design', 'user experience designer'],
        'UI Designer': ['ui designer', 'ui design', 'user interface designer'],
        'Motion Graphics Designer': ['motion graphics', 'motion designer', 'motion graphics designer'],
        'Video Producer': ['video producer', 'video production'],
    }
    for role, phrases in exact_phrases_non_tech.items():
        for phrase in phrases:
            if phrase.strip() in job_lower:
                return role

    # Tech roles – exact phrase matching (order matters for clarity)
    exact_phrases_tech = {
        'Product Manager': ['product manager', 'product management', 'pm role', 'technical product manager'],
        'Project Manager': ['project manager', 'project management', 'it project manager'],
        'Business Analyst': ['business analyst', 'ba role', 'business analysis'],
        'Scrum Master': ['scrum master', 'agile coach', 'scrum master role'],
        'DevOps Engineer': ['devops engineer', 'dev ops engineer'],
        'Cloud Architect': ['cloud architect', 'solutions architect'],
        'Data Scientist': ['data scientist'],
        'Data Engineer': ['data engineer'],
        'Data Analyst': ['data analyst', 'bi analyst', 'business intelligence analyst'],
        'Backend Developer': ['backend developer', 'back-end developer', 'backend engineer'],
        'Frontend Developer': ['frontend developer', 'front-end developer', 'frontend engineer'],
        'Full Stack Developer': ['full stack developer', 'fullstack developer', 'full stack engineer'],
        'iOS Developer': ['ios developer', 'ios engineer', 'swift developer', 'apple ios'],
        'Android Developer': ['android developer', 'android engineer', 'kotlin developer', 'android app'],
        '.NET Developer': ['.net developer', '.net engineer', 'c# developer', 'asp.net developer'],
        'QA Engineer': ['qa engineer', 'quality assurance engineer', 'test engineer'],
        'Security Engineer': ['security engineer', 'cybersecurity engineer'],
        'Machine Learning Engineer': ['machine learning engineer', 'ml engineer', 'ai engineer'],
        'Technical Writer': ['technical writer', 'technical writing', 'documentation writer'],
        'Software Engineer': ['software engineer', 'software developer', 'application developer'],
    }
    for role, phrases in exact_phrases_tech.items():
        for phrase in phrases:
            if phrase in job_lower:
                return role

    # Keyword-based patterns (tech only) – use specific phrases to avoid wrong match
    role_patterns = {
        'DevOps Engineer': [
            'devops', 'dev-ops', 'infrastructure engineer', 'site reliability engineer',
            'sre ', 'kubernetes', 'docker', 'terraform', 'ci/cd', 'cicd',
            'deployment engineer', 'linux engineer'
        ],
        'Cloud Architect': [
            'cloud architect', 'cloud infrastructure', 'aws architect', 'azure architect',
            'gcp architect', 'cloud solutions'
        ],
        'Backend Developer': [
            'backend', 'back-end', 'api development', 'server-side', 'server side',
            'django developer', 'flask developer', 'nodejs developer', 'node.js developer',
            'spring developer', 'fastapi developer', 'rest api', 'microservices'
        ],
        'Frontend Developer': [
            'frontend', 'front-end', 'react developer', 'vue developer', 'angular developer',
            'javascript developer', 'typescript developer', 'web developer', 'frontend engineer'
        ],
        'Full Stack Developer': [
            'full stack', 'fullstack', 'full-stack', 'full stack engineer'
        ],
        'Machine Learning Engineer': [
            'machine learning', 'ml engineer', 'deep learning', 'neural network',
            'tensorflow', 'pytorch', 'nlp engineer', 'computer vision', 'ai/ml'
        ],
        'Data Scientist': [
            'data scientist', 'statistical analysis', 'predictive model', 'machine learning model'
        ],
        'Data Engineer': [
            'data engineer', 'etl engineer', 'data pipeline', 'big data', 'spark',
            'hadoop', 'data warehouse', 'data architecture'
        ],
        'Data Analyst': [
            'data analyst', 'bi analyst', 'business intelligence', 'tableau', 'power bi',
            'analytics engineer', 'sql analyst'
        ],
        'QA Engineer': [
            'qa engineer', 'quality assurance', 'test engineer', 'test automation',
            'automated tester', 'selenium', 'quality engineer'
        ],
        'Security Engineer': [
            'security engineer', 'cybersecurity', 'infosec', 'penetration tester', 'security architect'
        ],
        'Product Manager': [
            'product roadmap', 'product strategy', 'product owner', 'prioritization', 'user stories'
        ],
        'Project Manager': [
            'project management', 'pm certification', 'pmp', 'stakeholder management', 'project delivery'
        ],
    }
    
    # Count keyword matches for each role
    role_scores = {}
    
    for role, patterns in role_patterns.items():
        match_count = 0
        for pattern in patterns:
            if pattern in job_lower:
                match_count += 1
        if match_count > 0:
            role_scores[role] = match_count
    
    # Return role with highest match count
    if role_scores:
        detected_role = max(role_scores, key=role_scores.get)
        return detected_role

    # Extract job title from description when no known role matches (avoid forcing Software Engineer)
    title_patterns = [
        r'(?:job title|position|role|we are hiring|looking for|hiring)\s*[:\-]\s*([a-z\s]+?)(?:\s*\-|\s*\(|\.|$)',
        r'^([a-z\s]+?)\s*[\-\|]\s*(?:full time|part time|remote)',
        r'^#?\s*([a-z][a-z\s]{3,40}?)(?:\s+job|\s+position|\.)',
    ]
    for pat in title_patterns:
        m = re.search(pat, job_lower[:300], re.IGNORECASE)
        if m:
            title = m.group(1).strip()
            if len(title) >= 4 and len(title) < 50 and 'experience' not in title and 'description' not in title:
                return title.title()

    return 'Other Role'


def get_role_specific_certs(job_role, job_skills):
    """Get certifications specific to the detected job role and job requirements."""
    # Map skills to relevant certifications
    skill_cert_mapping = {
        'kubernetes': {'cert': 'CKA - Kubernetes Administrator', 'relevance': 'Critical', 'duration': '3-4 months'},
        'docker': {'cert': 'Docker Certified Associate', 'relevance': 'Critical', 'duration': '1-2 months'},
        'terraform': {'cert': 'HashiCorp Certified Terraform Associate', 'relevance': 'Critical', 'duration': '2 months'},
        'aws': {'cert': 'AWS Solutions Architect Associate', 'relevance': 'Critical', 'duration': '2-3 months'},
        'gcp': {'cert': 'Google Cloud Associate Cloud Engineer', 'relevance': 'Critical', 'duration': '2-3 months'},
        'google cloud': {'cert': 'Google Cloud Associate Cloud Engineer', 'relevance': 'Critical', 'duration': '2-3 months'},
        'azure': {'cert': 'Azure Administrator', 'relevance': 'Critical', 'duration': '2-3 months'},
        'python': {'cert': 'Google ML Engineer Certificate', 'relevance': 'High', 'duration': '3-6 months'},
        'machine learning': {'cert': 'AWS ML Specialty', 'relevance': 'Critical', 'duration': '3-4 months'},
        'ml': {'cert': 'AWS ML Specialty', 'relevance': 'Critical', 'duration': '3-4 months'},
        'data science': {'cert': 'Google ML Engineer Certificate', 'relevance': 'Critical', 'duration': '3-6 months'},
        'sql': {'cert': 'Google Cloud Data Engineer', 'relevance': 'High', 'duration': '3-4 months'},
        'spark': {'cert': 'AWS Data Analytics Specialty', 'relevance': 'Critical', 'duration': '3-4 months'},
        'tableau': {'cert': 'Tableau Public Certified Associate', 'relevance': 'Critical', 'duration': '2-3 months'},
        'power bi': {'cert': 'Microsoft Certified: Data Analyst Associate', 'relevance': 'Critical', 'duration': '3-4 months'},
        'java': {'cert': 'Oracle Certified Associate Java Programmer', 'relevance': 'High', 'duration': '2-3 months'},
        'react': {'cert': 'Google Mobile Web Specialist', 'relevance': 'High', 'duration': '1-2 months'},
        'angular': {'cert': 'Google Mobile Web Specialist', 'relevance': 'High', 'duration': '1-2 months'},
        'node.js': {'cert': 'AWS Solutions Architect Associate', 'relevance': 'High', 'duration': '2-3 months'},
        'nodejs': {'cert': 'AWS Solutions Architect Associate', 'relevance': 'High', 'duration': '2-3 months'},
        'django': {'cert': 'AWS Solutions Architect Associate', 'relevance': 'High', 'duration': '2-3 months'},
        'testing': {'cert': 'ISTQB Certified Tester', 'relevance': 'Critical', 'duration': '2-4 weeks'},
        'qa': {'cert': 'ISTQB Certified Tester', 'relevance': 'Critical', 'duration': '2-4 weeks'},
        'security': {'cert': 'AWS Security Specialty', 'relevance': 'Critical', 'duration': '2-3 months'},
        'jenkins': {'cert': 'AWS DevOps Engineer Professional', 'relevance': 'High', 'duration': '3-4 months'},
        'devops': {'cert': 'AWS DevOps Engineer Professional', 'relevance': 'Critical', 'duration': '3-4 months'},
        # Creative / Video / Design
        'premiere pro': {'cert': 'Adobe Certified Professional - Video Design', 'relevance': 'Critical', 'duration': '1-2 months'},
        'after effects': {'cert': 'Adobe Certified Professional - Visual Design', 'relevance': 'Critical', 'duration': '1-2 months'},
        'davinci resolve': {'cert': 'Blackmagic DaVinci Resolve Certified', 'relevance': 'High', 'duration': '1-2 months'},
        'video editing': {'cert': 'Adobe Certified Professional - Video Design', 'relevance': 'Critical', 'duration': '2-3 months'},
        'motion graphics': {'cert': 'Adobe Certified Professional - Visual Design', 'relevance': 'Critical', 'duration': '2-3 months'},
        'photoshop': {'cert': 'Adobe Certified Professional - Graphic Design', 'relevance': 'Critical', 'duration': '1-2 months'},
        'illustrator': {'cert': 'Adobe Certified Professional - Graphic Design', 'relevance': 'Critical', 'duration': '1-2 months'},
        'figma': {'cert': 'Figma Certified Professional', 'relevance': 'High', 'duration': '2-4 weeks'},
        'graphic design': {'cert': 'Adobe Certified Professional - Graphic Design', 'relevance': 'Critical', 'duration': '2-3 months'},
        'ui design': {'cert': 'Google UX Certificate', 'relevance': 'High', 'duration': '3-6 months'},
        'ux design': {'cert': 'Google UX Certificate', 'relevance': 'Critical', 'duration': '3-6 months'},
        'content writing': {'cert': 'HubSpot Content Marketing', 'relevance': 'High', 'duration': '1-2 months'},
        'copywriting': {'cert': 'American Writers & Artists Inc. (AWAI)', 'relevance': 'High', 'duration': '2-3 months'},
        'seo': {'cert': 'Google Analytics / SEO Certifications', 'relevance': 'Critical', 'duration': '1-2 months'},
        'digital marketing': {'cert': 'Google Digital Marketing Certificate', 'relevance': 'Critical', 'duration': '3-6 months'},
        'social media marketing': {'cert': 'Meta Blueprint Certified', 'relevance': 'High', 'duration': '1-2 months'},
        'color grading': {'cert': 'Blackmagic DaVinci Resolve Certified', 'relevance': 'Medium', 'duration': '1-2 months'},
        'video production': {'cert': 'Adobe Certified Professional - Video Design', 'relevance': 'Critical', 'duration': '2-3 months'},
        'blender': {'cert': 'Blender Certification', 'relevance': 'High', 'duration': '2-3 months'},
    }

    # Default certifications by role if no specific skills match
    default_certs_by_role = {
        'Backend Developer': [
            {'cert': 'AWS Solutions Architect Associate', 'relevance': 'Critical', 'duration': '2-3 months'},
            {'cert': 'Oracle Certified Associate Java Programmer', 'relevance': 'High', 'duration': '2-3 months'},
            {'cert': 'Microsoft Azure Developer', 'relevance': 'High', 'duration': '2-3 months'},
        ],
        'Frontend Developer': [
            {'cert': 'Google Mobile Web Specialist', 'relevance': 'Critical', 'duration': '1-2 months'},
            {'cert': 'AWS Solutions Architect Associate', 'relevance': 'High', 'duration': '2-3 months'},
            {'cert': 'Microsoft Azure Web Developer', 'relevance': 'Medium', 'duration': '2 months'},
        ],
        'Full Stack Developer': [
            {'cert': 'AWS Solutions Architect Associate', 'relevance': 'Critical', 'duration': '2-3 months'},
            {'cert': 'Google Cloud Associate Cloud Engineer', 'relevance': 'Critical', 'duration': '2-3 months'},
            {'cert': 'Azure Administrator', 'relevance': 'High', 'duration': '2-3 months'},
        ],
        'DevOps Engineer': [
            {'cert': 'CKA - Kubernetes Administrator', 'relevance': 'Critical', 'duration': '3-4 months'},
            {'cert': 'AWS DevOps Engineer Professional', 'relevance': 'Critical', 'duration': '3-4 months'},
            {'cert': 'Docker Certified Associate', 'relevance': 'Critical', 'duration': '1-2 months'},
            {'cert': 'HashiCorp Certified Terraform Associate', 'relevance': 'High', 'duration': '2 months'},
        ],
        'Cloud Architect': [
            {'cert': 'AWS Solutions Architect Professional', 'relevance': 'Critical', 'duration': '3-4 months'},
            {'cert': 'Google Cloud Architect', 'relevance': 'Critical', 'duration': '3-4 months'},
            {'cert': 'Azure Solutions Architect', 'relevance': 'Critical', 'duration': '3 months'},
        ],
        'Data Scientist': [
            {'cert': 'Google ML Engineer Certificate', 'relevance': 'Critical', 'duration': '3-6 months'},
            {'cert': 'AWS ML Specialty', 'relevance': 'Critical', 'duration': '3-4 months'},
            {'cert': 'Azure Data Scientist', 'relevance': 'High', 'duration': '3 months'},
        ],
        'Data Engineer': [
            {'cert': 'Google Cloud Data Engineer', 'relevance': 'Critical', 'duration': '3-4 months'},
            {'cert': 'AWS Data Analytics Specialty', 'relevance': 'Critical', 'duration': '3-4 months'},
            {'cert': 'Azure Data Engineer', 'relevance': 'High', 'duration': '3 months'},
        ],
        'Data Analyst': [
            {'cert': 'Google Data Analytics Certificate', 'relevance': 'Critical', 'duration': '3-6 months'},
            {'cert': 'Microsoft Certified: Data Analyst Associate', 'relevance': 'Critical', 'duration': '3-4 months'},
            {'cert': 'Tableau Public Certified Associate', 'relevance': 'High', 'duration': '2-3 months'},
        ],
        'QA Engineer': [
            {'cert': 'ISTQB Certified Tester', 'relevance': 'Critical', 'duration': '2-4 weeks'},
            {'cert': 'AWS SysOps Administrator', 'relevance': 'Medium', 'duration': '2-3 months'},
            {'cert': 'Azure Administrator', 'relevance': 'Medium', 'duration': '2-3 months'},
        ],
        'Security Engineer': [
            {'cert': 'AWS Security Specialty', 'relevance': 'Critical', 'duration': '2-3 months'},
            {'cert': 'Google Cloud Security Engineer', 'relevance': 'Critical', 'duration': '2-3 months'},
            {'cert': 'Azure Security Engineer', 'relevance': 'Critical', 'duration': '2-3 months'},
        ],
        'Software Engineer': [
            {'cert': 'AWS Solutions Architect Associate', 'relevance': 'Critical', 'duration': '2-3 months'},
            {'cert': 'Google Cloud Associate Cloud Engineer', 'relevance': 'High', 'duration': '2-3 months'},
            {'cert': 'Microsoft Azure Developer', 'relevance': 'High', 'duration': '2-3 months'},
        ],
        'Machine Learning Engineer': [
            {'cert': 'Google ML Engineer Certificate', 'relevance': 'Critical', 'duration': '3-6 months'},
            {'cert': 'AWS ML Specialty', 'relevance': 'Critical', 'duration': '3-4 months'},
            {'cert': 'Azure Data Scientist', 'relevance': 'High', 'duration': '3 months'},
        ],
        'ML Engineer': [
            {'cert': 'Google ML Engineer Certificate', 'relevance': 'Critical', 'duration': '3-6 months'},
            {'cert': 'AWS ML Specialty', 'relevance': 'Critical', 'duration': '3-4 months'},
        ],
        # Creative & non-tech roles – job ke hisaab se popular certificates
        'Video Editor': [
            {'cert': 'Adobe Certified Professional - Video Design', 'relevance': 'Critical', 'duration': '2-3 months'},
            {'cert': 'Adobe Certified Professional - Visual Design (After Effects)', 'relevance': 'Critical', 'duration': '1-2 months'},
            {'cert': 'Blackmagic DaVinci Resolve Certified', 'relevance': 'High', 'duration': '1-2 months'},
            {'cert': 'Apple Certified Pro - Final Cut Pro X', 'relevance': 'High', 'duration': '1-2 months'},
        ],
        'Graphic Designer': [
            {'cert': 'Adobe Certified Professional - Graphic Design', 'relevance': 'Critical', 'duration': '2-3 months'},
            {'cert': 'Adobe Certified Professional - Visual Design', 'relevance': 'High', 'duration': '1-2 months'},
            {'cert': 'Figma Certified Professional', 'relevance': 'High', 'duration': '2-4 weeks'},
        ],
        'Content Writer': [
            {'cert': 'HubSpot Content Marketing Certification', 'relevance': 'High', 'duration': '1-2 months'},
            {'cert': 'Google Digital Marketing Certificate', 'relevance': 'High', 'duration': '3-6 months'},
            {'cert': 'AWAI Copywriting Certifications', 'relevance': 'High', 'duration': '2-3 months'},
        ],
        'Digital Marketing': [
            {'cert': 'Google Digital Marketing Certificate', 'relevance': 'Critical', 'duration': '3-6 months'},
            {'cert': 'Google Analytics Certification', 'relevance': 'Critical', 'duration': '1-2 months'},
            {'cert': 'Meta Blueprint Certified', 'relevance': 'High', 'duration': '1-2 months'},
            {'cert': 'HubSpot Inbound Marketing', 'relevance': 'High', 'duration': '1 month'},
        ],
        'Social Media Manager': [
            {'cert': 'Meta Blueprint Certified', 'relevance': 'Critical', 'duration': '1-2 months'},
            {'cert': 'Google Digital Marketing Certificate', 'relevance': 'High', 'duration': '3-6 months'},
            {'cert': 'Hootsuite Social Marketing Certification', 'relevance': 'High', 'duration': '2-4 weeks'},
        ],
        'UX Designer': [
            {'cert': 'Google UX Certificate', 'relevance': 'Critical', 'duration': '3-6 months'},
            {'cert': 'Figma Certified Professional', 'relevance': 'High', 'duration': '2-4 weeks'},
            {'cert': 'Nielsen Norman Group UX Certification', 'relevance': 'High', 'duration': '2-3 months'},
        ],
        'UI Designer': [
            {'cert': 'Google UX Certificate', 'relevance': 'Critical', 'duration': '3-6 months'},
            {'cert': 'Figma Certified Professional', 'relevance': 'Critical', 'duration': '2-4 weeks'},
            {'cert': 'Adobe Certified Professional - Graphic Design', 'relevance': 'High', 'duration': '2-3 months'},
        ],
        'Motion Graphics Designer': [
            {'cert': 'Adobe Certified Professional - Visual Design', 'relevance': 'Critical', 'duration': '2-3 months'},
            {'cert': 'Adobe Certified Professional - Video Design', 'relevance': 'High', 'duration': '2-3 months'},
        ],
        'Video Producer': [
            {'cert': 'Adobe Certified Professional - Video Design', 'relevance': 'Critical', 'duration': '2-3 months'},
            {'cert': 'Blackmagic DaVinci Resolve Certified', 'relevance': 'High', 'duration': '1-2 months'},
        ],
        # Tech – job ke hisaab se
        'Product Manager': [
            {'cert': 'Certified Product Manager (AIPMM)', 'relevance': 'High', 'duration': '2-3 months'},
            {'cert': 'Google Project Management Certificate', 'relevance': 'High', 'duration': '3-6 months'},
            {'cert': 'Certified Scrum Product Owner (CSPO)', 'relevance': 'High', 'duration': '2-4 weeks'},
        ],
        'Project Manager': [
            {'cert': 'PMP - Project Management Professional', 'relevance': 'Critical', 'duration': '3-4 months'},
            {'cert': 'PRINCE2', 'relevance': 'High', 'duration': '2-3 months'},
            {'cert': 'Certified Scrum Master (CSM)', 'relevance': 'High', 'duration': '2-4 weeks'},
        ],
        'Business Analyst': [
            {'cert': 'ECBA / CBAP - Business Analysis', 'relevance': 'Critical', 'duration': '3-6 months'},
            {'cert': 'Google Data Analytics Certificate', 'relevance': 'High', 'duration': '3-6 months'},
        ],
        'Scrum Master': [
            {'cert': 'Certified Scrum Master (CSM)', 'relevance': 'Critical', 'duration': '2-4 weeks'},
            {'cert': 'SAFe Scrum Master', 'relevance': 'High', 'duration': '1-2 months'},
        ],
        'iOS Developer': [
            {'cert': 'Apple Certified Developer', 'relevance': 'High', 'duration': '2-3 months'},
        ],
        'Android Developer': [
            {'cert': 'Associate Android Developer Certification', 'relevance': 'Critical', 'duration': '2-3 months'},
        ],
        '.NET Developer': [
            {'cert': 'Microsoft Certified: .NET Developer', 'relevance': 'Critical', 'duration': '2-3 months'},
            {'cert': 'Microsoft Certified: Azure Developer', 'relevance': 'High', 'duration': '2-3 months'},
        ],
        'Technical Writer': [
            {'cert': 'CPTC - Certified Professional Technical Communicator', 'relevance': 'High', 'duration': '2-3 months'},
        ],
    }

    recommendations = []
    seen_certs = set()
    
    # Extract skills from job_skills (could be string or list)
    if isinstance(job_skills, str):
        job_skills_list = extract_skills(job_skills)
    else:
        job_skills_list = list(job_skills) if job_skills else []
    
    # Match certifications based on job requirements
    for skill in job_skills_list:
        skill_lower = normalize_skill(skill).lower()
        
        # Check for direct skill matches
        for skill_keyword, cert_info in skill_cert_mapping.items():
            if skill_keyword in skill_lower:
                cert_name = cert_info['cert']
                if cert_name not in seen_certs:
                    recommendations.append(cert_info)
                    seen_certs.add(cert_name)
                    break
    
    # If no specific matches, use default role-based certs (only for known roles – no tech fallback for Video Editor / Other)
    if not recommendations:
        default_certs = default_certs_by_role.get(job_role, [])
        recommendations = [c for c in default_certs if c['cert'] not in seen_certs]

    # Ensure we have at least 3-4 recommendations (only from same role)
    if len(recommendations) < 3:
        default_certs = default_certs_by_role.get(job_role, [])
        for cert in default_certs:
            if cert['cert'] not in seen_certs and len(recommendations) < 4:
                recommendations.append(cert)
                seen_certs.add(cert['cert'])
    
    return recommendations[:6]


def match_certifications(job_description, resume_text, resume_skills=None):
    """Recommend certifications based on job requirements and detected job role."""
    if resume_skills is None:
        resume_skills = []
    
    # Detect job role from description
    job_role = detect_job_role(job_description)
    
    # Get job requirements/skills
    job_requirements = extract_job_requirements(job_description)
    
    # Get role-specific certifications that match job requirements
    role_certs = get_role_specific_certs(job_role, job_requirements)
    
    recommendations = []
    for cert in role_certs:
        recommendations.append({
            'area': job_role,
            'cert': cert['cert'],
            'relevance': cert['relevance'],
            'duration': cert['duration']
        })
    
    # Ensure minimum recommendations
    if len(recommendations) < 3:
        default_certs = {
            'Backend Developer': [
                {'cert': 'AWS Solutions Architect Associate', 'relevance': 'Critical', 'duration': '2-3 months'},
                {'cert': 'Oracle Certified Associate Java Programmer', 'relevance': 'High', 'duration': '2-3 months'},
            ],
            'Frontend Developer': [
                {'cert': 'Google Mobile Web Specialist', 'relevance': 'Critical', 'duration': '1-2 months'},
                {'cert': 'AWS Solutions Architect Associate', 'relevance': 'High', 'duration': '2-3 months'},
            ],
            'DevOps Engineer': [
                {'cert': 'CKA - Kubernetes Administrator', 'relevance': 'Critical', 'duration': '3-4 months'},
                {'cert': 'AWS DevOps Engineer Professional', 'relevance': 'Critical', 'duration': '3-4 months'},
            ],
            'Data Analyst': [
                {'cert': 'Microsoft Certified: Data Analyst Associate', 'relevance': 'Critical', 'duration': '3-4 months'},
                {'cert': 'Google Data Analytics Certificate', 'relevance': 'Critical', 'duration': '3-6 months'},
            ],
            'Data Scientist': [
                {'cert': 'AWS ML Specialty', 'relevance': 'Critical', 'duration': '3-4 months'},
                {'cert': 'Google ML Engineer Certificate', 'relevance': 'Critical', 'duration': '3-6 months'},
            ],
        }
        
        additional_certs = default_certs.get(job_role, [])
        existing_cert_names = {r['cert'] for r in recommendations}
        
        for cert in additional_certs:
            if cert['cert'] not in existing_cert_names and len(recommendations) < 5:
                recommendations.append({
                    'area': job_role,
                    'cert': cert['cert'],
                    'relevance': cert['relevance'],
                    'duration': cert['duration']
                })
    
    return recommendations[:6]


def match_job_profile(resume_skills, job_description):
    """Match resume to closest job profile."""
    best_match = None
    best_score = 0

    for role, profile in JOB_PROFILES.items():
        required = profile['required_skills']['critical'] + profile['required_skills']['required']
        score, _, _ = calculate_match(resume_skills, required)

        if score > best_score:
            best_score = score
            best_match = role

    return best_match or 'Unclassified Role', best_score


# ============================================================================
# POWER FEATURES: KEYWORD DENSITY, ATS, READABILITY, TAILORING, INTERVIEW Qs
# ============================================================================

def get_keyword_density(resume_text, job_skills):
    """Analyze how many job keywords appear in resume. Returns found (with count), missing, and score %."""
    if not resume_text or not job_skills:
        return {'found': [], 'missing': list(job_skills), 'score_pct': 0}
    text_lower = resume_text.lower()
    found = []
    missing = []
    for skill in job_skills:
        sn = normalize_skill(skill)
        count = text_lower.count(sn) + sum(text_lower.count(a) for a in expand_skill_with_aliases(skill) if a != sn)
        if count > 0:
            found.append((skill, count))
        else:
            missing.append(skill)
    score_pct = round((len(found) / len(job_skills)) * 100, 1) if job_skills else 0
    return {'found': found, 'missing': missing, 'score_pct': score_pct}


def get_ats_checklist(resume_text, resume_skills, experience, education):
    """Return ATS-friendly checklist: item, status (pass/warn/fail), tip."""
    contact = extract_contact_info(resume_text)
    contact_count = sum(1 for v in contact.values() if v)
    sections_required = ['experience', 'education', 'skills']
    found_sections = [s for s in sections_required if s in resume_text.lower()]
    verbs = QUALITY_RUBRIC['action_verbs']['verbs']
    verb_count = sum(resume_text.lower().count(v.lower()) for v in verbs)
    char_count = len(resume_text)
    word_count = len(resume_text.split())

    checklist = [
        {'item': 'Contact info (email, phone, LinkedIn)', 'status': 'pass' if contact_count >= 2 else 'warn' if contact_count >= 1 else 'fail', 'tip': 'Add email, phone, and LinkedIn URL.'},
        {'item': 'Experience section', 'status': 'pass' if 'experience' in resume_text.lower() else 'fail', 'tip': 'Include a clear Experience or Work History section.'},
        {'item': 'Education section', 'status': 'pass' if 'education' in resume_text.lower() else 'fail', 'tip': 'Include Education with degree and institution.'},
        {'item': 'Skills section', 'status': 'pass' if 'skills' in resume_text.lower() else 'fail', 'tip': 'List technical and soft skills clearly.'},
        {'item': 'Length (400–1500 words)', 'status': 'pass' if 400 <= word_count <= 1500 else 'warn' if 200 <= word_count < 400 or word_count > 2000 else 'fail', 'tip': 'Ideal: 1–2 pages, 400–800 words.'},
        {'item': 'Action verbs (5+)', 'status': 'pass' if verb_count >= 5 else 'warn' if verb_count >= 2 else 'fail', 'tip': 'Start bullets with Led, Developed, Implemented, etc.'},
        {'item': 'Skills count (8+)', 'status': 'pass' if len(resume_skills) >= 8 else 'warn' if len(resume_skills) >= 5 else 'fail', 'tip': 'List 8–15 relevant skills.'},
        {'item': 'Experience years mentioned', 'status': 'pass' if experience and experience > 0 else 'fail', 'tip': 'Mention years of experience explicitly.'},
    ]
    return checklist


def get_readability_stats(resume_text):
    """Word count, reading time, length recommendation."""
    if not resume_text:
        return {'word_count': 0, 'char_count': 0, 'reading_time_mins': 0, 'length_ok': False, 'suggestion': 'Add resume content.'}
    words = resume_text.split()
    word_count = len(words)
    char_count = len(resume_text)
    reading_time_mins = max(1, round(word_count / 200.0))  # ~200 wpm
    length_ok = 400 <= word_count <= 1200
    if word_count < 400:
        suggestion = 'Resume is too short. Add more bullet points and achievements (target 400–800 words).'
    elif word_count > 1200:
        suggestion = 'Resume is long. Consider trimming to 1–2 pages (under 800 words) for ATS.'
    else:
        suggestion = 'Length is good for ATS and recruiters.'
    return {'word_count': word_count, 'char_count': char_count, 'reading_time_mins': reading_time_mins, 'length_ok': length_ok, 'suggestion': suggestion}


def get_action_verb_suggestions(resume_text):
    """Count action verbs and suggest stronger alternatives."""
    verbs_strong = ['Led', 'Developed', 'Managed', 'Created', 'Implemented', 'Designed', 'Built', 'Improved', 'Achieved', 'Optimized', 'Launched', 'Established', 'Reduced', 'Increased', 'Automated']
    weak = ['did', 'made', 'worked', 'helped', 'used', 'responsible for', 'handled']
    text_lower = resume_text.lower()
    used = [v for v in verbs_strong if v.lower() in text_lower]
    weak_found = [w for w in weak if w in text_lower]
    suggested = ['Led', 'Developed', 'Implemented', 'Designed', 'Achieved', 'Optimized'] if not used else []
    return {'count': len(used), 'used': used[:10], 'weak_found': weak_found, 'suggested_add': suggested[:5]}


def get_tailoring_phrases(job_skills, missing_skills, job_role):
    """Suggest exact phrases to add to resume for this job."""
    phrases = []
    for skill in missing_skills[:5]:
        skill_display = skill.title() if isinstance(skill, str) else skill
        phrases.append(f"Experience with {skill_display} in production environments")
        phrases.append(f"Proficient in {skill_display} for building scalable solutions")
    phrases.append(f"Strong fit for {job_role} role with hands-on technical delivery")
    return phrases[:8]


def get_interview_questions(job_role, missing_skills, experience):
    """Generate likely interview questions based on role and gaps."""
    questions = []
    role_lower = job_role.lower()
    if 'data' in role_lower or 'ml' in role_lower or 'scientist' in role_lower:
        questions.append("Walk me through a data or ML project from problem to deployment.")
        questions.append("How do you handle imbalanced datasets or missing data?")
    if 'engineer' in role_lower or 'developer' in role_lower:
        questions.append("Describe a technical challenge you solved and the approach you took.")
        questions.append("How do you balance code quality with delivery deadlines?")
    if 'devops' in role_lower or 'cloud' in role_lower:
        questions.append("Describe your experience with CI/CD and production deployments.")
        questions.append("How do you approach incident response and post-mortems?")
    for skill in (missing_skills or [])[:3]:
        sk = (skill.title() if isinstance(skill, str) else skill)
        questions.append(f"What is your hands-on experience with {sk}?")
    questions.append("Why do you want to join our team and what will you contribute in the first 90 days?")
    return questions[:8]


def get_cover_letter_bullets(resume_skills, job_skills, experience, job_role):
    """Generate 3–5 bullet points for cover letter."""
    match_pct, matched, _ = calculate_match(resume_skills, job_skills)
    bullets = []
    bullets.append(f"Over {experience} years of experience in software development and delivery.")
    top_matched = sorted(matched, key=lambda s: (s in TECHNICAL_SKILLS, s))[:5]
    if top_matched:
        bullets.append(f"Proficient in {', '.join(top_matched[:3])} and related technologies.")
    bullets.append(f"Eager to contribute to {job_role} responsibilities and team goals.")
    bullets.append(f"Strong match to role requirements ({match_pct:.0f}% skill alignment) with focus on quality and impact.")
    return bullets[:5]


def get_ideal_candidate_snapshot(job_role):
    """Return short bullet list of what an ideal resume has for this role."""
    profile = JOB_PROFILES.get(job_role)
    if not profile:
        return ["Strong technical skills matching the job description", "Clear experience section", "Relevant education and certifications"]
    critical = profile['required_skills']['critical'][:5]
    required = profile['required_skills']['required'][:3]
    min_exp = profile['min_experience']
    edu = profile.get('education', 'Bachelor')
    bullets = [f"Key skills: {', '.join(critical)}"]
    bullets.append(f"Also: {', '.join(required)}")
    bullets.append(f"Experience: {min_exp}+ years")
    bullets.append(f"Education: {edu} or equivalent")
    return bullets


def generate_report_text(detected_job_role, match_score, weighted_score, quality_score, ats_score,
                         experience, education, resume_skills, job_skills, matched_technical,
                         missing_technical, quality_issues, skill_gaps, salary_prediction,
                         interview_readiness, keyword_density):
    """Generate a plain-text summary report for download."""
    lines = [
        "RESUME ANALYSIS REPORT",
        "======================",
        f"Job Role: {detected_job_role}",
        f"Match: {match_score:.1f}% | Weighted: {weighted_score:.0f}% | Quality: {quality_score:.1f}% | ATS: {ats_score:.1f}%",
        f"Experience: {experience} years | Education: {education}",
        "",
        "YOUR SKILLS (" + str(len(resume_skills)) + ")",
        ", ".join(sorted(resume_skills)[:20]) + ("..." if len(resume_skills) > 20 else ""),
        "",
        "MATCHED: " + ", ".join(sorted(matched_technical)[:15]) if matched_technical else "MATCHED: None",
        "MISSING: " + ", ".join(s.title() for s in sorted(missing_technical)[:15]) if missing_technical else "MISSING: None",
        "",
        "QUALITY ISSUES: " + ("; ".join(quality_issues) if quality_issues else "None"),
        "",
        "SALARY RANGE: ${:.0f}K - ${:.0f}K (avg ${:.0f}K)".format(
            salary_prediction['min'], salary_prediction['max'], salary_prediction['avg']),
        "",
        "INTERVIEW READINESS: " + str(interview_readiness['score']) + "% - " + interview_readiness['readiness_level'],
        "",
        "KEYWORD MATCH: " + str(keyword_density['score_pct']) + "% (" + str(len(keyword_density['found'])) + "/" + str(max(1, len(keyword_density['found']) + len(keyword_density['missing']))) + " in resume)",
    ]
    if skill_gaps:
        lines.append("")
        lines.append("SKILL GAPS TO LEARN:")
        for g in skill_gaps[:5]:
            lines.append(f"  - {g['skill']} ({g['timeline']}, {g['priority']})")
    return "\n".join(lines)
