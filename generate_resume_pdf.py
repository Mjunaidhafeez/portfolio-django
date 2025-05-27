from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from PIL import Image as PILImage, ImageDraw
import io

def create_circular_image(image_path, size):
    # Open the image
    img = PILImage.open(image_path)
    
    # Create a circular mask
    mask = PILImage.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img.size, fill=255)
    
    # Apply the mask
    output = PILImage.new('RGBA', img.size, (255, 255, 255, 0))
    output.paste(img, mask=mask)
    
    # Resize the image
    output = output.resize((size, size), PILImage.LANCZOS)
    
    # Save to bytes
    img_byte_arr = io.BytesIO()
    output.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return img_byte_arr

def create_resume_pdf():
    # Create PDF directory if it doesn't exist
    pdf_dir = os.path.join('resume', 'static', 'pdf')
    os.makedirs(pdf_dir, exist_ok=True)
    
    # Create PDF file
    doc = SimpleDocTemplate(
        os.path.join(pdf_dir, "Junaid_Hafeez_Resume.pdf"),
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )
    
    # Create styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=20,
        textColor=colors.HexColor('#2c3e50'),
        fontName='Helvetica-Bold'
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        textColor=colors.HexColor('#2c3e50'),
        fontName='Helvetica-Bold'
    )
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=8,
        fontName='Helvetica'
    )
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=15,
        textColor=colors.HexColor('#3498db'),
        fontName='Helvetica-Bold'
    )
    
    # Create content
    content = []
    
    # Header with Circular Image
    image_path = os.path.join('resume', 'static', 'images', 'junaid.jpg')
    circular_image = create_circular_image(image_path, 200)  # 200 pixels size
    
    header_data = [
        [
            Image(circular_image, width=2*inch, height=2*inch),
            [
                [Paragraph("JUNAID HAFEEZ", title_style)],
                [Paragraph("Quality Automation Engineer", heading_style)],
                [Paragraph("Email: junaid.hafeez.cs@gmail.com", normal_style)],
                [Paragraph("Phone: +92 306 9287947", normal_style)],
                [Paragraph("Address: 402B City Tower, Gulberg, Lahore", normal_style)],
                [Paragraph("LinkedIn: linkedin.com/in/junadhafeezcs", normal_style)],
                [Paragraph("Website: www.paksoft.com", normal_style)]
            ]
        ]
    ]
    
    header_table = Table(header_data, colWidths=[2.5*inch, 4*inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
    ]))
    content.append(header_table)
    
    # Personal Profile
    content.append(Paragraph("PERSONAL PROFILE", section_style))
    about_text = """
    A dedicated Quality Automation Engineer with over 5 years of experience in software testing and automation. 
    Passionate about implementing robust testing strategies and developing automated solutions to ensure software quality. 
    Strong background in Python, Django, and modern testing frameworks. Proven track record of improving software reliability 
    and reducing testing time through automation. Committed to continuous learning and staying updated with the latest 
    technologies in software testing and quality assurance.
    """
    content.append(Paragraph(about_text, normal_style))
    content.append(Spacer(1, 20))
    
    # Professional Experience
    content.append(Paragraph("WORK EXPERIENCE", section_style))
    
    experience_data = [
        [
            "2022 - Present",
            [
                ["Quality Automation Engineer", "AppifyTech"],
                ["• Leading quality assurance initiatives and developing automated test frameworks"],
                ["• Implementing comprehensive testing strategies for software reliability"],
                ["• Collaborating with development teams to ensure quality standards"],
                ["• Mentoring junior QA engineers and conducting technical training sessions"]
            ]
        ],
        [
            "2021 - 2022",
            [
                ["Automation Quality Engineer", "IT Cures"],
                ["• Developed and maintained automated test scripts using Selenium and Cypress"],
                ["• Implemented continuous integration testing processes"],
                ["• Conducted performance testing and optimization"],
                ["• Reduced testing time by 40% through automation"]
            ]
        ],
        [
            "2020 - 2021",
            [
                ["Software Quality Engineer", "Pak Soft"],
                ["• Conducted comprehensive software testing and quality assurance"],
                ["• Identified and resolved quality issues in software applications"],
                ["• Collaborated with development teams to implement fixes"],
                ["• Created detailed test documentation and reports"]
            ]
        ]
    ]
    
    for exp in experience_data:
        exp_table = Table([
            [Paragraph(exp[0], heading_style), Paragraph(exp[1][0][0], heading_style)],
            ['', Paragraph(exp[1][0][1], normal_style)]
        ], colWidths=[1.5*inch, 4*inch])
        
        exp_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        content.append(exp_table)
        
        for bullet in exp[1][1:]:
            content.append(Paragraph(bullet[0], normal_style))
        
        content.append(Spacer(1, 10))
    
    content.append(Spacer(1, 20))
    
    # Education
    content.append(Paragraph("EDUCATION AND TRAINING", section_style))
    
    education_data = [
        [
            "2023",
            [
                ["Master's in Education", "University of Education"],
                ["Specialized in Educational Technology and Curriculum Development"]
            ]
        ],
        [
            "2020",
            [
                ["Master's in History", "Islamia University Bahawalpur"],
                ["Focus on Modern History and Research Methodologies"]
            ]
        ],
        [
            "2017",
            [
                ["BS Computer Science", "Islamia University Bahawalpur"],
                ["Major in Software Engineering, Minor in Database Systems"]
            ]
        ]
    ]
    
    for edu in education_data:
        edu_table = Table([
            [Paragraph(edu[0], heading_style), Paragraph(edu[1][0][0], heading_style)],
            ['', Paragraph(edu[1][0][1], normal_style)],
            ['', Paragraph(edu[1][1][0], normal_style)]
        ], colWidths=[1.5*inch, 4*inch])
        
        edu_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        content.append(edu_table)
        content.append(Spacer(1, 10))
    
    content.append(Spacer(1, 20))
    
    # Skills
    content.append(Paragraph("SKILLS AND COMPETENCES", section_style))
    
    skills_data = [
        ["Programming Languages", "Python, JavaScript, HTML/CSS, SQL"],
        ["Frameworks & Tools", "Django, React.js, Selenium, Cypress, Jest"],
        ["Testing & QA", "Automated Testing, CI/CD, Agile Methodologies, TestNG"],
        ["Database & Version Control", "PostgreSQL, MySQL, Git, GitHub Actions"]
    ]
    
    skills_table = Table(skills_data, colWidths=[2*inch, 3.5*inch])
    skills_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    content.append(skills_table)
    content.append(Spacer(1, 20))
    
    # Interests
    content.append(Paragraph("INTERESTS", section_style))
    
    interests_data = [
        ["Technology Trends", "Staying updated with latest developments in software testing and automation"],
        ["Reading", "Technical books and industry publications"],
        ["Cooking", "Experimenting with new recipes and cooking techniques"],
        ["Outdoor Activities", "Exploring nature and engaging in outdoor sports"]
    ]
    
    interests_table = Table(interests_data, colWidths=[2*inch, 3.5*inch])
    interests_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    content.append(interests_table)
    content.append(Spacer(1, 20))
    
    # Hobbies
    content.append(Paragraph("HOBBIES", section_style))
    
    hobbies_data = [
        ["Cooking", "Passionate about experimenting with new recipes and cooking techniques"],
        ["Reading", "Enjoy reading technical books and staying updated with latest technologies"],
        ["Outdoor Activities", "Love exploring nature and engaging in outdoor sports"]
    ]
    
    hobbies_table = Table(hobbies_data, colWidths=[2*inch, 3.5*inch])
    hobbies_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    content.append(hobbies_table)
    content.append(Spacer(1, 20))
    
    # Certifications
    content.append(Paragraph("CERTIFICATIONS", section_style))
    
    certs = [
        "• ISTQB Certified Quality Assurance Engineer (2022)",
        "• Python & Django Professional Developer (2021)",
        "• Selenium Automation Expert (2021)",
        "• Cypress Test Automation Professional (2022)",
        "• Certified Scrum Master (2022)",
        "• AWS Certified Cloud Practitioner (2023)"
    ]
    
    for cert in certs:
        content.append(Paragraph(cert, normal_style))
    
    # Build PDF
    doc.build(content)

if __name__ == "__main__":
    create_resume_pdf() 