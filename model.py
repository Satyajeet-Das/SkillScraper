import spacy
from collections import Counter

# Load pre-trained NLP model
nlp = spacy.load("en_core_web_sm")

# Define a list of common skills
skills = ["data science", "machine learning", "statistics", "python", "R", "SQL", "visualizations", "BI", "HW", "SW", "cloud engineering"]

# Function to extract skills
def extract_skills(text):
    doc = nlp(text.lower())  # Lowercase the text
    extracted_skills = []

    # Tokenize and match skills
    for token in doc:
        if token.text in skills:
            extracted_skills.append(token.text)

    return list(set(extracted_skills))  # Return unique skills

# Example text
text = """
Microsoft Silicon, Cloud Hardware, and Infrastructure Engineering (SCHIE) is the team behind Microsoft’s expanding Cloud Infrastructure and responsible for powering Microsoft’s “Intelligent Cloud” mission. SCHIE delivers the core infrastructure and foundational technologies for Microsoft's over 200 online businesses including Bing, MSN, Office 365, Xbox Live, Teams, OneDrive and the Microsoft Azure platform globally with our server and data center infrastructure, security and compliance, operations, globalization, and manageability solutions. Our focus is on smart growth, high efficiency, and delivering a trusted experience to customers and partners worldwide and we are looking for passionate, high energy engineers to help achieve that mission.

The Cloud Hardware Analytics & Tools (CHAT) Team within SCHIE develops advanced analytical and tooling solutions to support and improve the quality of Microsoft Azure. We collect and analyze data across the full Azure stack, HW & SW components, Silicon development processes, and much more. CHAT Data Science, a branch of CHAT, provides data science support, machine learning and artificial intelligence solutions, and advanced visualizations to cloud engineering and management partners. We are looking for a Data Scientist to support our custom data analytics and visualizations platform. This high-impact role combines software engineering with data science, and will have direct contributions to Azure-level projects, including working with highly visible platforms through data-driven approaches. This role closely collaborates with BI and Data Engineers, Software Engineers, other Data Scientists, Program Managers, and HW Engineering teams.

Responsibilities

Analyze large-scale Azure data to address critical business problems
Work on new software features within our advanced visualizations platform
Work on complex, mission-critical solutions that involve multiple Azure Services
Design and develop production-level code for data science
Work in collaborative environment

Qualifications

Required/Minimum Qualifications

Bachelor's Degree in Data Science, Mathematics, Statistics, Econometrics, Economics, Operations Research, Computer Science, or related field OR equivalent experience.
5 years industry experiance

Additional Or Preferred Qualifications

Master's Degree in Data Science, Mathematics, Statistics, Econometrics, Economics, Operations Research, Computer Science, or related field
OR Bachelor's Degree in Data Science, Mathematics, Statistics, Econometrics, Economics, Operations Research, Computer Science, or related field AND 1+ years data-science experience (e.g., managing structured and unstructured data, applying statistical techniques and reporting results)
OR equivalent experience.
1 year experience working with R
1 year experience working with visualizations and / or reporting
1 year experience working with SQL

Microsoft is an equal opportunity employer. Consistent with applicable law, all qualified applicants will receive consideration for employment without regard to age, ancestry, citizenship, color, family or medical care leave, gender identity or expression, genetic information, immigration status, marital status, medical condition, national origin, physical or mental disability, political affiliation, protected veteran or military status, race, ethnicity, religion, sex (including pregnancy), sexual orientation, or any other characteristic protected by applicable local laws, regulations and ordinances. If you need assistance and/or a reasonable accommodation due to a disability during the application process, read more about requesting accommodations.
"""

# Call the function
skills_required = extract_skills(text)
print(skills_required)
