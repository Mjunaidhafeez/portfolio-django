from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def projects(request):
    return render(request, 'projects.html')     

def contact(request):
    return render(request, 'contact.html')

def skills(request):
    return render(request, 'skills.html')   

def education(request):
    return render(request, 'education.html')

def experience(request):
    return render(request, 'experience.html')   

def certifications(request):
    return render(request, 'certifications.html')

def resume(request):
    return render(request, 'resume.html')

@csrf_exempt
def contact_view(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            
            if not all([name, email, subject, message]):
                return JsonResponse({
                    'status': 'error',
                    'message': 'All fields are required.'
                })
            
            # Send email
            email_message = f"""
            Name: {name}
            Email: {email}
            Subject: {subject}
            
            Message:
            {message}
            """
            
            send_mail(
                subject=f'Portfolio Contact Form: {subject}',
                message=email_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Your message has been sent successfully!'
            })
            
        except Exception as e:
            print(f"Email sending error: {str(e)}")  # For debugging
            return JsonResponse({
                'status': 'error',
                'message': 'There was an error sending your message. Please try again later.'
            })
    
    return render(request, 'contact.html')

# Contact Information
contact_info = [
    ("Email", "junaidhafeez.cs@gmail.com"),
    ("Phone", "+92 306 9287947"),
    ("Address", "402B City Tower, Gulberg, Lahore"),
    ("LinkedIn", "linkedin.com/in/junadhafeezcs"),
    ("Website", "www.paksoft.com")
]

def generate_pdf(request):
    # Create the PDF object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Junaid_Hafeez_Resume.pdf"'
    
    # Create the PDF
    p = canvas.Canvas(response)
    width, height = letter
    
    # Add header with blue background
    p.setFillColorRGB(0.2, 0.6, 0.8)  # Blue color
    p.rect(0, height - 100, width, 100, fill=1)
    
    # Add name and title in white
    p.setFillColorRGB(1, 1, 1)  # White color
    p.setFont("Helvetica-Bold", 24)
    p.drawString(50, height - 50, "JUNAID HAFEEZ")
    
    p.setFont("Helvetica", 14)
    p.drawString(50, height - 80, "Quality Automation Engineer")
    
    # Add contact information
    p.setFillColorRGB(0, 0, 0)  # Black color
    p.setFont("Helvetica", 10)
    y = height - 120
    for label, value in contact_info:
        p.drawString(50, y, f"{label}: {value}")
        y -= 20
    
    # Professional Summary
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y - 20, "PROFESSIONAL SUMMARY")
    p.setFont("Helvetica", 10)
    summary = """A dedicated Quality Automation Engineer with over 5 years of experience in software testing and automation. 
Passionate about implementing robust testing strategies and developing automated solutions to ensure software quality. 
Strong background in Python, Django, and modern testing frameworks. Proven track record of improving software reliability 
and reducing testing time through automation. Committed to continuous learning and staying updated with the latest 
technologies in software testing and quality assurance."""
    textobject = p.beginText(50, y - 40)
    for line in summary.split('\n'):
        textobject.textLine(line)
    p.drawText(textobject)
    
    # Technical Skills
    y -= 120
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "TECHNICAL SKILLS")
    p.setFont("Helvetica", 10)
    
    skills = {
        "Programming Languages": ["Python", "JavaScript", "HTML/CSS", "SQL"],
        "Frameworks & Tools": ["Django", "React.js", "Selenium", "Cypress", "Jest"],
        "Testing & QA": ["Automated Testing", "CI/CD", "Agile", "TestNG"],
        "Database & Version Control": ["PostgreSQL", "MySQL", "Git", "GitHub Actions"]
    }
    
    y -= 20
    for category, items in skills.items():
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y, f"{category}:")
        p.setFont("Helvetica", 10)
        y -= 15
        p.drawString(70, y, ", ".join(items))
        y -= 20
    
    # Professional Experience
    y -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "PROFESSIONAL EXPERIENCE")
    p.setFont("Helvetica", 10)
    
    experiences = [
        {
            "title": "Quality Automation Engineer",
            "company": "AppifyTech",
            "period": "2022 - Present",
            "responsibilities": [
                "Leading quality assurance initiatives and developing automated test frameworks",
                "Implementing comprehensive testing strategies for software reliability",
                "Collaborating with development teams to ensure quality standards",
                "Mentoring junior QA engineers and conducting technical training sessions"
            ]
        },
        {
            "title": "Automation Quality Engineer",
            "company": "IT Cures",
            "period": "2021 - 2022",
            "responsibilities": [
                "Developed and maintained automated test scripts using Selenium and Cypress",
                "Implemented continuous integration testing processes",
                "Conducted performance testing and optimization",
                "Reduced testing time by 40% through automation"
            ]
        },
        {
            "title": "Software Quality Engineer",
            "company": "Pak Soft",
            "period": "2020 - 2021",
            "responsibilities": [
                "Conducted comprehensive software testing and quality assurance",
                "Identified and resolved quality issues in software applications",
                "Collaborated with development teams to implement fixes",
                "Created detailed test documentation and reports"
            ]
        }
    ]
    
    for exp in experiences:
        y -= 20
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y, f"{exp['title']}")
        p.setFont("Helvetica", 10)
        p.drawString(50, y - 15, f"{exp['company']} | {exp['period']}")
        y -= 30
        for resp in exp['responsibilities']:
            p.drawString(70, y, "• " + resp)
            y -= 15
        y -= 10
    
    # Education
    y -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "EDUCATION")
    p.setFont("Helvetica", 10)
    
    education = [
        {
            "degree": "Master's in Education",
            "institution": "University of Education",
            "year": "2023",
            "details": "Specialized in Educational Technology and Curriculum Development"
        },
        {
            "degree": "Master's in History",
            "institution": "Islamia University Bahawalpur",
            "year": "2020",
            "details": "Focus on Modern History and Research Methodologies"
        },
        {
            "degree": "BS Computer Science",
            "institution": "Islamia University Bahawalpur",
            "year": "2017",
            "details": "Major in Software Engineering, Minor in Database Systems"
        }
    ]
    
    for edu in education:
        y -= 20
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y, f"{edu['degree']}")
        p.setFont("Helvetica", 10)
        p.drawString(50, y - 15, f"{edu['institution']} | {edu['year']}")
        p.drawString(50, y - 30, edu['details'])
        y -= 40
    
    # Certifications
    y -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "CERTIFICATIONS")
    p.setFont("Helvetica", 10)
    
    certifications = [
        {"name": "ISTQB Certified", "details": "Quality Assurance Engineer", "year": "2022"},
        {"name": "Python & Django", "details": "Professional Developer", "year": "2021"},
        {"name": "Selenium", "details": "Automation Expert", "year": "2021"},
        {"name": "Cypress", "details": "Test Automation Professional", "year": "2022"}
    ]
    
    for cert in certifications:
        y -= 20
        p.drawString(50, y, f"{cert['name']} - {cert['details']} ({cert['year']})")
    
    # Save the PDF
    p.showPage()
    p.save()
    
    return response


