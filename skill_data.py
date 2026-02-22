# Predefined skill sets for different job roles
JOB_PROFILES = {
    "Full Stack Developer": [
        "Python", "JavaScript", "React", "Node.js", "SQL", "MongoDB",
        "Git", "Docker", "AWS", "REST API", "HTML", "CSS", "TypeScript",
        "Express", "Problem Solving", "Communication", "Teamwork"
    ],
    
    "Data Scientist": [
        "Python", "SQL", "Machine Learning", "TensorFlow", "PyTorch",
        "Pandas", "NumPy", "Scikit-learn", "Data Analysis", "Statistics",
        "Tableau", "Power BI", "Deep Learning", "AI", "Communication"
    ],
    
    "DevOps Engineer": [
        "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Linux", "Git",
        "Jenkins", "CI/CD", "Bash", "Python", "Terraform", "Ansible",
        "Problem Solving", "Leadership", "Communication"
    ],
    
    "Frontend Developer": [
        "JavaScript", "React", "Vue", "Angular", "HTML", "CSS", "TypeScript",
        "Git", "REST API", "Webpack", "npm", "Communication", "Teamwork",
        "Problem Solving", "UI/UX", "Design Patterns"
    ],
    
    "Backend Developer": [
        "Python", "Java", "Node.js", "SQL", "REST API", "Django", "Flask",
        "Spring Boot", "Git", "Docker", "Microservices", "Communication",
        "Problem Solving", "Database Design"
    ],
    
    "Software Engineer": [
        "Java", "C++", "Python", "SQL", "Git", "Agile", "Problem Solving",
        "Data Structures", "Algorithms", "Leadership", "Communication",
        "Code Review", "Testing", "Scrum"
    ],
    
    "Cloud Architect": [
        "AWS", "Azure", "GCP", "Cloud", "Docker", "Kubernetes", "Linux",
        "Terraform", "Security", "Design Patterns", "Leadership",
        "Communication", "Problem Solving", "DevOps"
    ],
    
    "QA Engineer": [
        "Testing", "Automation", "Python", "JavaScript", "Selenium", "JIRA",
        "Problem Solving", "Communication", "Attention to Detail",
        "Test Planning", "SQL", "Git", "DevOps", "CI/CD"
    ],
    
    "Product Manager": [
        "Leadership", "Communication", "Project Management", "Agile",
        "Stakeholder Management", "Data Analysis", "Product Strategy",
        "Problem Solving", "Critical Thinking", "Analytics", "Tableau"
    ],
    
    "Data Engineer": [
        "Python", "SQL", "Spark", "Hadoop", "Kafka", "AWS", "Data Warehousing",
        "ETL", "Scala", "Git", "Docker", "Problem Solving", "Communication",
        "Airflow", "NoSQL"
    ]
}

# Industry-specific keywords
INDUSTRY_KEYWORDS = {
    "Finance": ["Investment", "Trading", "Financial Analysis", "Compliance", "Risk", "Audit", "Banking"],
    "Healthcare": ["HIPAA", "Patient Care", "Clinical", "Pharmaceutical", "Medical Records", "Healthcare IT"],
    "E-commerce": ["Customer Experience", "Conversion", "Sales", "Inventory", "Logistics", "Marketing"],
    "Manufacturing": ["Supply Chain", "Quality Control", "Production", "Lean", "Six Sigma", "Operations"],
    "Startup": ["MVP", "Agile", "Growth Hacking", "Startup Culture", "Innovation", "Fast-paced"]
}

# Seniority levels and their typical skill counts
SENIORITY_LEVELS = {
    "Entry Level (0-2 years)": {
        "min_years": 0,
        "max_years": 2,
        "min_skills": 5,
        "max_quality_score": 70
    },
    "Junior (2-5 years)": {
        "min_years": 2,
        "max_years": 5,
        "min_skills": 8,
        "max_quality_score": 80
    },
    "Mid-Level (5-8 years)": {
        "min_years": 5,
        "max_years": 8,
        "min_skills": 10,
        "max_quality_score": 85
    },
    "Senior (8+ years)": {
        "min_years": 8,
        "max_years": 50,
        "min_skills": 12,
        "max_quality_score": 90
    }
}

def get_job_profile_skills(job_title):
    """Get predefined skills for a job title."""
    return JOB_PROFILES.get(job_title, [])

def get_all_job_profiles():
    """Get all available job profiles."""
    return list(JOB_PROFILES.keys())

def get_industry_keywords(industry):
    """Get keywords for a specific industry."""
    return INDUSTRY_KEYWORDS.get(industry, [])

def get_seniority_requirements(seniority_level):
    """Get requirements for a seniority level."""
    return SENIORITY_LEVELS.get(seniority_level, {})
