from django.shortcuts import render

# Dummy profile data — baad me asli details se replace kar dena.
PROFILE = {
    "name": "Ankur Sharma",
    "title": "DevOps Engineer",
    "tagline": "Linux, Docker aur CI/CD ke saath scalable infra banata hoon.",
    "location": "Jaipur, India",
    "email": "ankur@example.com",
    "phone": "+91 98765 43210",
    "github": "https://github.com/ankur-dummy",
    "linkedin": "https://linkedin.com/in/ankur-dummy",
    "about": (
        "Main ek DevOps engineer hoon jise servers, automation aur "
        "deployment pipelines banane me maza aata hai. Abhi Linux, "
        "Docker, Nginx aur cloud infra par kaam kar raha hoon."
    ),
    "skills": [
        "Python / Django",
        "Linux (Ubuntu)",
        "Git & GitHub",
        "Docker",
        "Nginx & Gunicorn",
        "CI/CD (GitHub Actions)",
        "AWS / DigitalOcean",
        "Bash Scripting",
    ],
    "experience": [
        {
            "role": "DevOps Engineer",
            "company": "Dummy Tech Pvt. Ltd.",
            "period": "2024 - Present",
            "description": "Deployment automate kiya, Docker par services migrate ki, "
            "aur monitoring setup kiya.",
        },
        {
            "role": "Junior Backend Developer",
            "company": "Sample Solutions",
            "period": "2022 - 2024",
            "description": "Django REST APIs banayi aur PostgreSQL queries optimize ki.",
        },
    ],
    "projects": [
        {
            "name": "Server Monitoring Dashboard",
            "description": "CPU, RAM aur disk usage dikhane wala simple dashboard.",
            "tech": "Django, Chart.js, psutil",
        },
        {
            "name": "Auto Deploy Script",
            "description": "Ek command me code pull, migrate aur service restart.",
            "tech": "Bash, systemd, Git",
        },
    ],
    "education": {
        "degree": "B.Tech, Computer Science",
        "college": "Dummy Institute of Technology",
        "year": "2018 - 2022",
    },
}


def index(request):
    return render(request, "portfolio/index.html", {"profile": PROFILE})
