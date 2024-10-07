from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import time
import spacy
from spacy.matcher import PhraseMatcher

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load pre-trained NLP model
nlp = spacy.load("en_core_web_sm")

# Define a list of common skills
skills = [
    # Programming Languages
    "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "PHP", "Ruby", 
    "Swift", "Kotlin", "Rust", "Go", "SQL", "R", "MATLAB", "Scala", "Perl", 
    "Bash", "Shell scripting", "HTML", "CSS", "SASS", "SCSS",
    
    # Web Development
    "React.js", "Angular", "Vue.js", "Next.js", "Node.js", "Express.js", 
    "Django", "Flask", "Laravel", "Spring Boot", "Ruby on Rails", "ASP.NET", 
    "GraphQL", "RESTful APIs", "WebSocket", "jQuery", "Bootstrap", 
    "Tailwind CSS", "WordPress", "Magento", "Shopify",

    # Data Science & Machine Learning
    "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "Keras", 
    "Matplotlib", "Seaborn", "Plotly", "D3.js", "Data Visualization", 
    "Data Wrangling", "Data Analysis", "Machine Learning", "Deep Learning", 
    "Neural Networks", "Natural Language Processing", "NLP", "Computer Vision", 
    "Time Series Analysis", "Statistical Modeling", "Data Mining", 
    "AI/ML Algorithms", "Reinforcement Learning", "Generative Adversarial Networks", "GANs",

    # Cloud Computing & DevOps
    "Amazon Web Services", "AWS", "Microsoft Azure", "Google Cloud Platform", 
    "GCP", "Docker", "Kubernetes", "Terraform", "Jenkins", "CI/CD", 
    "Ansible", "Puppet", "Chef", "Vagrant", "OpenShift", "NGINX", 
    "Load Balancing", "Monitoring", "Prometheus", "Grafana", "Serverless Architecture", 
    "Microservices", "CloudFormation", "ElasticSearch",

    # Databases
    "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra", "SQLite", 
    "DynamoDB", "MariaDB", "Oracle Database", "Microsoft SQL Server", 
    "Couchbase", "Neo4j", "Graph Databases", "Firebase", "Elasticsearch",

    # Operating Systems
    "Linux", "Windows", "macOS", "Unix", "Android", "iOS", "Red Hat", 
    "CentOS", "Ubuntu", "FreeBSD", "Docker",

    # Version Control & Collaboration Tools
    "Git", "GitHub", "GitLab", "Bitbucket", "Mercurial", "Subversion", 
    "SVN", "JIRA", "Trello", "Asana", "Slack", "Confluence",

    # Mobile Development
    "Android SDK", "iOS SDK", "React Native", "Flutter", "Xamarin", 
    "SwiftUI", "Kotlin Multiplatform", "Firebase", "Ionic",

    # Cybersecurity
    "Information Security", "Network Security", "Application Security", 
    "Cloud Security", "Penetration Testing", "Vulnerability Assessment", 
    "OWASP", "Encryption", "Firewalls", "VPN", 
    "Security Information and Event Management", "SIEM", 
    "Identity and Access Management", "IAM", "Intrusion Detection Systems", "IDS", 
    "Data Loss Prevention", "DLP",

    # Soft Skills
    "Problem-solving", "Communication", "Teamwork", "Leadership", 
    "Time Management", "Critical Thinking", "Project Management", 
    "Agile Methodologies", "Scrum", "Kanban", "Collaboration",

    # Business Intelligence & Analytics Tools
    "Power BI", "Tableau", "Looker", "QlikView", "Google Data Studio", 
 "SAP Analytics Cloud", "Apache Hadoop", "Apache Spark", "Hive", 
    "Pig", "Presto", "Microsoft Excel", "Advanced Excel", 
    "Business Intelligence", "BI", "ETL", "Extract, Transform, Load",

    # Networking
    "TCP/IP", "DNS", "DHCP", "VPN", "LAN", "WAN", "Network Protocols", 
    "Wireless Networks", "Routing and Switching", "Firewall Configuration", 
    "Virtual LAN", "VLAN", "Load Balancing",

    # Other Technical Skills
    "API Development", "Microservices Architecture", "Performance Tuning", 
    "High Availability", "Load Testing", "Scalability", "SQL Optimization", 
    "Automated Testing", "Unit Testing", "Integration Testing", 
    "User Interface", "UI Design", "User Experience", "UX Design", 
    "Cross-platform Development", "Event-driven Architecture", 
    "Blockchain", "Internet of Things", "IoT", "Web Scraping", 
    "WebRTC", "Augmented Reality", "AR", "Virtual Reality", "VR", 
    "Robotics", "Game Development", "3D Modeling", "Embedded Systems", 
    "Autonomous Systems",

    # Design and Multimedia
    "Adobe Photoshop", "Adobe Illustrator", "Adobe Premiere Pro", 
    "Adobe After Effects", "Figma", "Sketch", "Adobe XD", 
    "Blender", "Unity", "Unreal Engine", "Final Cut Pro", 
    "3D Rendering", "Animation"
]

matcher = PhraseMatcher(nlp.vocab)
patterns = [nlp(skill.lower()) for skill in skills]
matcher.add("SKILLS", patterns)

def extract_skills(text):
    doc = nlp(text.lower())  # Process the text with the NLP model
    matches = matcher(doc)   # Find matches in the text
    extracted_skills = [doc[start:end].text for match_id, start, end in matches]
    
    return list(set(extracted_skills))  # Return unique skills

def fetchJobDecription(job_description_url):
    try:
        desc_response = requests.get(job_description_url)
        if desc_response.status_code == 200:
            page_content = desc_response.content
        elif desc_response.status_code == 429:
            return 429
        else:
            raise Exception("Failed to retrieve the webpage")
    except Exception as e:
        raise Exception("Failed to retrieve the webpage")

    soup = BeautifulSoup(page_content, "html.parser")
    job_criteria = soup.find("ul", class_="description__job-criteria-list")
    job_apply_description = soup.select_one("div.description__text.description__text--rich > section > div").get_text(separator = ' ', strip=True)
    skills_required = extract_skills(job_apply_description)
    
    d = {
        
        "skills required": skills_required,
        "seniority level": job_criteria.select_one("li:nth-child(1) > span").get_text(strip=True) if job_criteria.select_one("li:nth-child(1) > span") else "NA",
        "employment type": job_criteria.select_one("li:nth-child(2) > span").get_text(strip=True) if job_criteria.select_one("li:nth-child(2) > span") else "NA",
        "job function": job_criteria.select_one("li:nth-child(3) > span").get_text(strip=True) if job_criteria.select_one("li:nth-child(3) > span") else "NA",
        "industries": job_criteria.select_one("li:nth-child(4) > span").get_text(strip=True) if job_criteria.select_one("li:nth-child(4) > span") else "NA"

    } 
    return d

def fetchJobs(role: str,location: str, start: int):
    try:
        role = role.replace(" ", "%20")
        location = location.replace(" ", "%20")

        url = f"https://in.linkedin.com/jobs/search?keywords={role}&location={location}&geoId=&position=1&pageNum=0&start={start}"
        response = requests.get(url)

        if response.status_code == 200:
            page_content = response.content
        elif response.status_code == 429:
            return 429
        else:
            raise Exception("Failed to retrieve the webpage")
    except Exception as e:
        raise Exception("Failed to retrieve the webpage")

    soup = BeautifulSoup(page_content, "html.parser")
    
    all_jobs = []
    job_list = soup.select("ul > li > div.base-search-card")
    for i in job_list:
        d = {
            "title": i.find('h3', class_='base-search-card__title').get_text(strip=True),
            "company": i.select_one('div.base-search-card__info > h4 > a').get_text (strip=True),
            "link": i.select_one('a').get('href'),
            "location": i.select_one('div.base-search-card__info > div > span').get_text(strip=True),
            "list_date": i.select_one('div > time').get_text(strip=True)
        }
        all_jobs.append(d)

    return all_jobs

@app.get("/api/jobs")
async def getJobs(role: str, location: str, page: int):
    try:
        start = (page-1)*25
        jobs = []
        count = 0
        while True:
            data = fetchJobs(role,location, start)
            if count == 20:
                break
            elif data == 429:
                count+=1 
                continue
            elif data == -1:
                break
            else:
                jobs += data
                break
        return JSONResponse(content=jobs, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/api/jobs/description")
async def getJobDescription(url: str):
    try:
        data = {}
        count = 0
        while True:
            data = fetchJobDecription(url)
            if count == 20:
                break
            elif data == 429:
                count+=1 
                continue
            elif data == -1:
                break
            else:
                break
        return JSONResponse(content=data, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")