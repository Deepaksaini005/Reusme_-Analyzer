"""
Comprehensive Industry Database with Real Market Data
Contains job profiles, salary benchmarks, company data, and industry standards
Updated for 2024-2026 accuracy
"""

# ============================================================================
# SKILL TAXONOMY - COMPREHENSIVE & INDUSTRY-STANDARD
# ============================================================================

TECHNICAL_SKILLS = {
    # Programming Languages (High Demand)
    'Python': {'category': 'Language', 'demand': 'High', 'growth': 15},
    'JavaScript': {'category': 'Language', 'demand': 'High', 'growth': 12},
    'Java': {'category': 'Language', 'demand': 'High', 'growth': 8},
    'TypeScript': {'category': 'Language', 'demand': 'High', 'growth': 18},
    'SQL': {'category': 'Database', 'demand': 'Critical', 'growth': 5},
    'C++': {'category': 'Language', 'demand': 'Medium', 'growth': 6},
    'C#': {'category': 'Language', 'demand': 'High', 'growth': 9},
    'Go': {'category': 'Language', 'demand': 'High', 'growth': 20},
    'Rust': {'category': 'Language', 'demand': 'High', 'growth': 25},
    
    # Frontend Technologies
    'React': {'category': 'Frontend', 'demand': 'Critical', 'growth': 14},
    'Vue': {'category': 'Frontend', 'demand': 'Medium', 'growth': 12},
    'Angular': {'category': 'Frontend', 'demand': 'High', 'growth': 8},
    'HTML': {'category': 'Frontend', 'demand': 'Critical', 'growth': 3},
    'CSS': {'category': 'Frontend', 'demand': 'Critical', 'growth': 4},
    'Tailwind CSS': {'category': 'Frontend', 'demand': 'High', 'growth': 22},
    'Next.js': {'category': 'Frontend', 'demand': 'High', 'growth': 28},
    
    # Backend & Databases
    'Node.js': {'category': 'Backend', 'demand': 'High', 'growth': 13},
    'Django': {'category': 'Backend', 'demand': 'High', 'growth': 9},
    'Flask': {'category': 'Backend', 'demand': 'Medium', 'growth': 11},
    'Spring Boot': {'category': 'Backend', 'demand': 'High', 'growth': 7},
    'FastAPI': {'category': 'Backend', 'demand': 'High', 'growth': 35},
    'MongoDB': {'category': 'Database', 'demand': 'High', 'growth': 10},
    'PostgreSQL': {'category': 'Database', 'demand': 'High', 'growth': 8},
    'MySQL': {'category': 'Database', 'demand': 'High', 'growth': 5},
    'Redis': {'category': 'Cache', 'demand': 'High', 'growth': 12},
    
    # Cloud & DevOps (Critical Skills in 2024)
    'AWS': {'category': 'Cloud', 'demand': 'Critical', 'growth': 18},
    'Azure': {'category': 'Cloud', 'demand': 'Critical', 'growth': 20},
    'Google Cloud': {'category': 'Cloud', 'demand': 'Critical', 'growth': 16},
    'Docker': {'category': 'DevOps', 'demand': 'Critical', 'growth': 15},
    'Kubernetes': {'category': 'DevOps', 'demand': 'Critical', 'growth': 22},
    'Terraform': {'category': 'IaC', 'demand': 'High', 'growth': 24},
    'Ansible': {'category': 'DevOps', 'demand': 'High', 'growth': 10},
    'Jenkins': {'category': 'CI/CD', 'demand': 'High', 'growth': 9},
    'GitLab': {'category': 'DevOps', 'demand': 'High', 'growth': 11},
    'GitHub': {'category': 'Version Control', 'demand': 'Critical', 'growth': 7},
    
    # AI/ML (Rapidly Growing)
    'Machine Learning': {'category': 'AI/ML', 'demand': 'Critical', 'growth': 35},
    'Deep Learning': {'category': 'AI/ML', 'demand': 'High', 'growth': 42},
    'TensorFlow': {'category': 'AI/ML', 'demand': 'High', 'growth': 28},
    'PyTorch': {'category': 'AI/ML', 'demand': 'High', 'growth': 32},
    'LLM': {'category': 'AI/ML', 'demand': 'Critical', 'growth': 65},
    'Generative AI': {'category': 'AI/ML', 'demand': 'Critical', 'growth': 70},
    'Computer Vision': {'category': 'AI/ML', 'demand': 'High', 'growth': 25},
    'NLP': {'category': 'AI/ML', 'demand': 'High', 'growth': 28},
    
    # Data Engineering
    'Pandas': {'category': 'Data', 'demand': 'High', 'growth': 12},
    'NumPy': {'category': 'Data', 'demand': 'High', 'growth': 10},
    'Spark': {'category': 'Big Data', 'demand': 'High', 'growth': 11},
    'Hadoop': {'category': 'Big Data', 'demand': 'Medium', 'growth': 2},
    'Airflow': {'category': 'Orchestration', 'demand': 'High', 'growth': 24},
    'Kafka': {'category': 'Streaming', 'demand': 'High', 'growth': 18},
    'dbt': {'category': 'Data', 'demand': 'High', 'growth': 40},
    
    # Other Technical
    'Git': {'category': 'Version Control', 'demand': 'Critical', 'growth': 6},
    'REST API': {'category': 'API', 'demand': 'Critical', 'growth': 4},
    'GraphQL': {'category': 'API', 'demand': 'High', 'growth': 20},
    'Microservices': {'category': 'Architecture', 'demand': 'High', 'growth': 16},
    'System Design': {'category': 'Architecture', 'demand': 'High', 'growth': 14},
    # Mobile & more
    'Swift': {'category': 'Language', 'demand': 'High', 'growth': 12},
    'Kotlin': {'category': 'Language', 'demand': 'High', 'growth': 18},
    'Agile': {'category': 'Process', 'demand': 'High', 'growth': 8},
    'iOS': {'category': 'Platform', 'demand': 'High', 'growth': 10},
    'Android': {'category': 'Platform', 'demand': 'High', 'growth': 10},
}

SOFT_SKILLS = {
    'Communication': {'type': 'Leadership', 'importance': 0.9},
    'Leadership': {'type': 'Leadership', 'importance': 0.85},
    'Problem Solving': {'type': 'Cognitive', 'importance': 0.9},
    'Teamwork': {'type': 'Interpersonal', 'importance': 0.85},
    'Project Management': {'type': 'Management', 'importance': 0.8},
    'Critical Thinking': {'type': 'Cognitive', 'importance': 0.85},
    'Adaptability': {'type': 'Behavioral', 'importance': 0.8},
    'Creativity': {'type': 'Cognitive', 'importance': 0.75},
    'Time Management': {'type': 'Management', 'importance': 0.8},
    'Mentoring': {'type': 'Leadership', 'importance': 0.7},
    'Negotiation': {'type': 'Interpersonal', 'importance': 0.65},
    'Strategic Thinking': {'type': 'Management', 'importance': 0.8},
}

# Creative, design, video, marketing - for non-tech job descriptions
CREATIVE_SKILLS = {
    'Premiere Pro': {'category': 'Video', 'demand': 'High', 'growth': 12},
    'After Effects': {'category': 'Video', 'demand': 'High', 'growth': 14},
    'DaVinci Resolve': {'category': 'Video', 'demand': 'High', 'growth': 18},
    'Final Cut Pro': {'category': 'Video', 'demand': 'Medium', 'growth': 8},
    'Video Editing': {'category': 'Video', 'demand': 'High', 'growth': 15},
    'Motion Graphics': {'category': 'Video', 'demand': 'High', 'growth': 16},
    'Color Grading': {'category': 'Video', 'demand': 'Medium', 'growth': 10},
    'Photoshop': {'category': 'Design', 'demand': 'Critical', 'growth': 8},
    'Illustrator': {'category': 'Design', 'demand': 'High', 'growth': 10},
    'Figma': {'category': 'Design', 'demand': 'Critical', 'growth': 25},
    'Adobe XD': {'category': 'Design', 'demand': 'Medium', 'growth': 6},
    'Canva': {'category': 'Design', 'demand': 'High', 'growth': 20},
    'Graphic Design': {'category': 'Design', 'demand': 'High', 'growth': 12},
    'UI Design': {'category': 'Design', 'demand': 'High', 'growth': 14},
    'UX Design': {'category': 'Design', 'demand': 'High', 'growth': 18},
    'Content Writing': {'category': 'Content', 'demand': 'High', 'growth': 12},
    'Copywriting': {'category': 'Content', 'demand': 'High', 'growth': 10},
    'SEO': {'category': 'Marketing', 'demand': 'High', 'growth': 14},
    'Google Analytics': {'category': 'Marketing', 'demand': 'High', 'growth': 12},
    'Social Media Marketing': {'category': 'Marketing', 'demand': 'High', 'growth': 16},
    'Digital Marketing': {'category': 'Marketing', 'demand': 'High', 'growth': 12},
    'Email Marketing': {'category': 'Marketing', 'demand': 'Medium', 'growth': 8},
    'Video Production': {'category': 'Video', 'demand': 'High', 'growth': 14},
    'Cinematography': {'category': 'Video', 'demand': 'Medium', 'growth': 8},
    'Sound Design': {'category': 'Audio', 'demand': 'Medium', 'growth': 10},
    '3D Modeling': {'category': 'Design', 'demand': 'High', 'growth': 14},
    'Blender': {'category': 'Design', 'demand': 'High', 'growth': 22},
    'Documentation': {'category': 'Content', 'demand': 'High', 'growth': 10},
    'Technical Writing': {'category': 'Content', 'demand': 'High', 'growth': 12},
}

CERTIFICATIONS_BY_INDUSTRY = {
    'Cloud': {
        'AWS': ['AWS Solutions Architect Professional', 
                'AWS DevOps Engineer Professional',
                'AWS Security Specialty',
                'AWS Data Analytics Specialty'],
        'Azure': ['Azure Administrator',
                  'Azure Solutions Architect',
                  'Azure DevOps Engineer Expert',
                  'Azure Security Engineer'],
        'GoogleCloud': ['GCP Associate Cloud Engineer',
                        'GCP Professional Cloud Architect',
                        'GCP Professional Data Engineer']
    },
    'Kubernetes': {
        'CKA': 'Certified Kubernetes Administrator',
        'CKAD': 'Certified Kubernetes Application Developer',
        'CKS': 'Certified Kubernetes Security Specialist'
    },
    'DevOps': {
        'Docker': 'Docker Certified Associate',
        'HashiCorp': 'Terraform Associate Certified',
        'Jenkins': 'Jenkins Certified Engineer'
    },
    'DataScience': {
        'Google': 'Google Data Analytics Professional Certificate',
        'AWS': 'AWS Data Engineer Associate',
        'Databricks': 'Databricks Certified Associate Data Engineer'
    },
    'Security': {
        'CISSP': 'Certified Information Systems Security Professional',
        'CEH': 'Certified Ethical Hacker',
        'Security+': 'CompTIA Security+ Certification'
    }
}

# ============================================================================
# JOB PROFILES - INDUSTRY STANDARDS (2024-2026)
# ============================================================================

JOB_PROFILES = {
    'Full Stack Developer': {
        'required_skills': {
            'critical': ['JavaScript', 'React', 'Node.js', 'SQL', 'Git', 'REST API'],
            'required': ['HTML', 'CSS', 'Database Design', 'Problem Solving', 'Communication'],
            'preferred': ['TypeScript', 'Docker', 'AWS', 'Testing', 'CI/CD']
        },
        'min_experience': 1,
        'typical_experience': 3,
        'education': 'Bachelor',
        'salary_2024': {'min': 95, 'avg': 130, 'max': 180},
    },
    
    'Frontend Developer': {
        'required_skills': {
            'critical': ['JavaScript', 'React', 'HTML', 'CSS', 'Problem Solving'],
            'required': ['REST API', 'Git', 'Responsive Design', 'Communication'],
            'preferred': ['TypeScript', 'Next.js', 'Testing', 'Performance Optimization']
        },
        'min_experience': 1,
        'typical_experience': 3,
        'education': 'Bachelor',
        'salary_2024': {'min': 85, 'avg': 120, 'max': 160},
    },
    
    'Backend Developer': {
        'required_skills': {
            'critical': ['Python', 'SQL', 'Database Design', 'REST API', 'Problem Solving'],
            'required': ['Git', 'Backend Framework', 'Server Architecture', 'Communication'],
            'preferred': ['Docker', 'Microservices', 'Cloud (AWS/Azure)', 'Testing']
        },
        'min_experience': 1,
        'typical_experience': 3,
        'education': 'Bachelor',
        'salary_2024': {'min': 95, 'avg': 135, 'max': 190},
    },
    
    'Data Scientist': {
        'required_skills': {
            'critical': ['Python', 'SQL', 'Machine Learning', 'Data Analysis', 'Statistics'],
            'required': ['Pandas', 'NumPy', 'Visualization', 'Problem Solving', 'Communication'],
            'preferred': ['TensorFlow', 'Deep Learning', 'Spark', 'Cloud']
        },
        'min_experience': 2,
        'typical_experience': 4,
        'education': 'Master',
        'salary_2024': {'min': 120, 'avg': 165, 'max': 240},
    },
    
    'DevOps Engineer': {
        'required_skills': {
            'critical': ['Docker', 'Kubernetes', 'AWS', 'Linux', 'Git', 'CI/CD'],
            'required': ['Infrastructure as Code', 'Monitoring', 'Shell Scripting', 'Problem Solving'],
            'preferred': ['Terraform', 'Python', 'Azure', 'Security']
        },
        'min_experience': 2,
        'typical_experience': 4,
        'education': 'Bachelor',
        'salary_2024': {'min': 130, 'avg': 170, 'max': 240},
    },
    
    'Cloud Architect': {
        'required_skills': {
            'critical': ['AWS', 'System Design', 'Architecture', 'Security', 'Leadership'],
            'required': ['Azure or GCP', 'Docker', 'Kubernetes', 'Cost Optimization'],
            'preferred': ['Terraform', 'Multiple Cloud Platforms', 'Compliance', 'Advanced Certifications']
        },
        'min_experience': 5,
        'typical_experience': 8,
        'education': 'Bachelor',
        'salary_2024': {'min': 180, 'avg': 240, 'max': 350},
    },
    
    'ML Engineer': {
        'required_skills': {
            'critical': ['Python', 'Machine Learning', 'Deep Learning', 'TensorFlow/PyTorch', 'Statistics'],
            'required': ['Data Processing', 'Model Deployment', 'Git', 'Communication'],
            'preferred': ['MLOps', 'Kubernetes', 'Cloud', 'SQL', 'System Design']
        },
        'min_experience': 2,
        'typical_experience': 4,
        'education': 'Master',
        'salary_2024': {'min': 140, 'avg': 190, 'max': 280},
    },
    
    'Senior Software Engineer': {
        'required_skills': {
            'critical': ['System Design', 'Architecture', 'Leadership', 'Problem Solving', 'Code Review'],
            'required': ['Multiple Languages', 'Mentoring', 'Project Management', 'Communication'],
            'preferred': ['Open Source', 'Patents', 'Strategic Thinking', 'Business Acumen']
        },
        'min_experience': 5,
        'typical_experience': 8,
        'education': 'Bachelor',
        'salary_2024': {'min': 160, 'avg': 220, 'max': 320},
    },

    'Solutions Architect': {
        'required_skills': {
            'critical': ['System Design', 'Architecture', 'Cloud', 'Communication', 'Leadership'],
            'required': ['Technical Depth', 'Business Understanding', 'Problem Solving', 'Documentation'],
            'preferred': ['Multiple Cloud Platforms', 'Certifications', 'Domain Expertise']
        },
        'min_experience': 5,
        'typical_experience': 8,
        'education': 'Bachelor',
        'salary_2024': {'min': 170, 'avg': 230, 'max': 330},
    },
}

# ============================================================================
# INDUSTRY SALARY BENCHMARKS - 2024-2026 (USA Market)
# ============================================================================

INDUSTRY_SALARY_DATA = {
    'Tech': {
        'Entry Level': {'min': 65, 'avg': 85, 'max': 110, 'locations': {'SF': 1.5, 'NYC': 1.4, 'Seattle': 1.3}},
        'Junior': {'min': 95, 'avg': 130, 'max': 170, 'locations': {'SF': 1.5, 'NYC': 1.4, 'Seattle': 1.3}},
        'Mid-Level': {'min': 140, 'avg': 180, 'max': 240, 'locations': {'SF': 1.5, 'NYC': 1.4, 'Seattle': 1.3}},
        'Senior': {'min': 190, 'avg': 260, 'max': 380, 'locations': {'SF': 1.5, 'NYC': 1.4, 'Seattle': 1.3}},
        'Staff+': {'min': 300, 'avg': 400, 'max': 600, 'locations': {'SF': 1.5, 'NYC': 1.4, 'Seattle': 1.3}},
    },
    'Finance': {
        'Entry Level': {'min': 75, 'avg': 95, 'max': 120},
        'Junior': {'min': 120, 'avg': 160, 'max': 210},
        'Mid-Level': {'min': 170, 'avg': 220, 'max': 300},
        'Senior': {'min': 250, 'avg': 350, 'max': 500},
    },
    'Healthcare Tech': {
        'Entry Level': {'min': 60, 'avg': 78, 'max': 98},
        'Junior': {'min': 85, 'avg': 115, 'max': 150},
        'Mid-Level': {'min': 120, 'avg': 160, 'max': 210},
        'Senior': {'min': 170, 'avg': 230, 'max': 320},
    },
    'Startup': {
        'Entry Level': {'min': 70, 'avg': 90, 'max': 120},
        'Junior': {'min': 100, 'avg': 135, 'max': 180},
        'Mid-Level': {'min': 150, 'avg': 190, 'max': 260},
        'Senior': {'min': 210, 'avg': 290, 'max': 400},
    },
}

# ============================================================================
# SKILL ALIASES & VARIATIONS
# ============================================================================

SKILL_ALIASES = {
    'python': ['py', 'python3', 'python 3'],
    'javascript': ['js', 'node', 'nodejs'],
    'typescript': ['ts'],
    'c++': ['cpp', 'c plus plus'],
    'c#': ['csharp', 'c sharp'],
    'sql': ['mysql', 'postgresql', 'sqlite'],
    'react': ['reactjs', 'react.js'],
    'aws': ['amazon web services', 'amazon aws'],
    'gcp': ['google cloud', 'google cloud platform'],
    'ml': ['machine learning', 'ml/ai'],
    'nlp': ['natural language processing'],
    'cicd': ['ci/cd', 'continuous integration', 'continuous deployment'],
    'rest': ['rest api', 'restful'],
    'oop': ['object oriented programming'],
}

# ============================================================================
# SALARY MULTIPLIERS BY SKILL (Skill Premium Analysis)
# ============================================================================

SKILL_MULTIPLIERS = {
    # Critical High-Demand Skills (8-12% premium)
    'machine learning': 0.12,
    'generative ai': 0.15,
    'llm': 0.13,
    'kubernetes': 0.10,
    'aws': 0.10,
    'azure': 0.09,
    
    # High-Demand Skills (5-7% premium)
    'python': 0.08,
    'docker': 0.07,
    'go': 0.08,
    'rust': 0.08,
    'system design': 0.10,
    'architecture': 0.09,
    'leadership': 0.07,
    
    # Medium Demand (3-4% premium)
    'javascript': 0.05,
    'java': 0.05,
    'sql': 0.04,
    'react': 0.06,
    'terraform': 0.06,
    
    # Soft Skill Bonuses (2-3% premium)
    'communication': 0.03,
    'project management': 0.04,
}

# ============================================================================
# LEARNING RESOURCES & PLATFORMS
# ============================================================================

LEARNING_PATHS = {
    'Python': {
        'entry': ['Codecademy', 'Django for Beginners'],
        'intermediate': ['Real Python', 'DataCamp'],
        'advanced': ['Advanced Python', 'Open Source Contributions'],
        'timeline': '4-8 weeks'
    },
    'JavaScript': {
        'entry': ['FreeCodeCamp', 'Codecademy'],
        'intermediate': ['Udemy React Course', 'Frontend Masters'],
        'advanced': ['Advanced Patterns', 'Open Source'],
        'timeline': '4-8 weeks'
    },
    'AWS': {
        'entry': ['AWS Training Portal', 'A Cloud Guru'],
        'intermediate': ['Solutions Architect Associate'],
        'advanced': ['Solutions Architect Professional'],
        'timeline': '12-16 weeks'
    },
    'Kubernetes': {
        'entry': ['Kubernetes Basics', 'KodeKloud'],
        'intermediate': ['CKA Preparation'],
        'advanced': ['Advanced Topics', 'Production Setup'],
        'timeline': '8-12 weeks'
    },
    'Machine Learning': {
        'entry': ['Andrew Ng ML Course'],
        'intermediate': ['Deep Learning Specialization'],
        'advanced': ['Kaggle Competitions', 'Research'],
        'timeline': '16-24 weeks'
    },
}

# ============================================================================
# RESUME QUALITY SCORING RUBRIC
# ============================================================================

QUALITY_RUBRIC = {
    'length': {
        'points': 15,
        'excellent': 800,  # characters
        'good': 600,
        'acceptable': 400,
    },
    'skills_count': {
        'points': 15,
        'excellent': 12,
        'good': 8,
        'acceptable': 5,
    },
    'experience': {
        'points': 20,
        'excellent': 5,  # years
        'good': 3,
        'acceptable': 1,
    },
    'education': {
        'points': 15,
        'excellent': ['Master', 'PhD'],
        'good': ['Bachelor'],
        'acceptable': ['Diploma', 'High School'],
    },
    'contact_info': {
        'points': 10,
        'required': ['email', 'phone', 'linkedin'],
    },
    'sections': {
        'points': 10,
        'required': ['experience', 'education', 'skills'],
        'preferred': ['projects', 'certifications', 'achievements'],
    },
    'action_verbs': {
        'points': 10,
        'verbs': ['Led', 'Developed', 'Managed', 'Created', 'Implemented',
                  'Designed', 'Built', 'Improved', 'Achieved', 'Optimized']
    },
    'quantification': {
        'points': 5,
        'metric_verbs': ['increased', 'reduced', 'improved', 'grew', 'decreased', '%', '$']
    },
}

# ============================================================================
# INDUSTRY STANDARDS & BENCHMARKS
# ============================================================================

INDUSTRY_STANDARDS = {
    'resume_length': '1-2 pages for 0-5 years, 2-3 pages for 5+ years',
    'skills_count': '10-15 relevant skills recommended',
    'ats_passing_rate': '75% ATS match as minimum',
    'typical_interview_stages': 4,
    'avg_salary_increase_per_year': '3-5%',
    'promotion_timeline': '2-3 years',
}
