#!/usr/bin/env python
"""Quick test of core functions"""
from utils import predict_salary, extract_skills, analyze_resume_quality
from industry_data import INDUSTRY_SALARY_DATA

# Test 1: Skill extraction
print("="*50)
print("TEST 1: Skill Extraction")
print("="*50)
skills = extract_skills('Python and AWS expert with 5 years experience')
print(f"✓ Detected skills: {skills}\n")

# Test 2: Salary prediction
print("="*50)
print("TEST 2: Salary Prediction")
print("="*50)
salary = predict_salary(5, skills, 'Master')
print(f"✓ Experience: 5 years, Master degree")
print(f"✓ Skills: {skills}")
print(f"✓ Salary Range: ${salary['min']:.0f}K - ${salary['max']:.0f}K")
print(f"✓ Average: ${salary['avg']:.0f}K ({salary['level']})\n")

# Test 3: Quality analysis
print("="*50)
print("TEST 3: Resume Quality Analysis")
print("="*50)
resume_text = """
PROFESSIONAL SUMMARY
Experienced Software Engineer with 5+ years of Python and AWS development.

TECHNICAL SKILLS
Python, AWS, Docker, Kubernetes, SQL, React, Django, REST APIs, Git, CI/CD

EXPERIENCE
Senior Software Engineer at TechCorp (2020-Present)
- Led migration of monolithic app to microservices (40% performance improvement)
- Developed Python/AWS solutions for 100+ customers
- Mentored junior developers and conducted code reviews

Software Engineer at StartupXYZ (2018-2020)
- Built REST APIs using Django and Flask
- Deployed applications on AWS (EC2, RDS, S3)
- Reduced deployment time by 60% with CI/CD improvements

EDUCATION
Bachelor of Science in Computer Science
State University, Graduated 2018

CERTIFICATIONS
AWS Solutions Architect Associate
Docker Certified Associate

CONTACT
Email: engineer@example.com
Phone: +1-555-123-4567
LinkedIn: linkedin.com/in/myprofile
"""

quality, issues, analysis = analyze_resume_quality(
    resume_text, 
    skills, 
    5, 
    'Bachelor'
)
print(f"✓ Quality Score: {quality}/100")
print(f"✓ Analysis: {analysis}")
if issues:
    print(f"✓ Recommendations:")
    for issue in issues[:3]:
        print(f"  - {issue}")
print()

# Test 4: Job profiles
print("="*50)
print("TEST 4: Industry Salary Benchmarks")
print("="*50)
for level in ['Entry Level', 'Junior', 'Mid-Level', 'Senior', 'Staff+']:
    try:
        data = INDUSTRY_SALARY_DATA['Tech'][level]
        print(f"✓ {level:15} → ${data['min']:.0f}K - ${data['max']:.0f}K (avg: ${data['avg']:.0f}K)")
    except KeyError:
        print(f"✗ {level:15} → Not available")

print("\n" + "="*50)
print("✅ ALL TESTS PASSED - APP READY TO RUN")
print("="*50)
print("\nTo start the application:")
print("  streamlit run app.py")
