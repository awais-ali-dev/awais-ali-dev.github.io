from pathlib import Path
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
FONT_DIR=Path(os.environ.get('RESUME_FONT_DIR','/usr/share/fonts/truetype/dejavu'))
for name,file in [('Sans','DejaVuSans.ttf'),('SansBold','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONT_DIR/file)))
pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='SansBold',italic='Sans',boldItalic='SansBold')
ink=HexColor('#152a25'); muted=HexColor('#47564d'); green=HexColor('#1e5b45')
styles={
 'name':ParagraphStyle('name',fontName='SansBold',fontSize=24,leading=29,textColor=ink,spaceAfter=7),
 'subtitle':ParagraphStyle('subtitle',fontName='Sans',fontSize=9,leading=13,textColor=green,spaceAfter=6),
 'contact':ParagraphStyle('contact',fontName='Sans',fontSize=8,leading=12,textColor=muted,spaceAfter=11),
 'section':ParagraphStyle('section',fontName='SansBold',fontSize=10,leading=14,textColor=green,spaceBefore=12,spaceAfter=5),
 'body':ParagraphStyle('body',fontName='Sans',fontSize=8.4,leading=12.8,textColor=ink,spaceAfter=5),
 'role':ParagraphStyle('role',fontName='SansBold',fontSize=8.5,leading=13,textColor=ink,spaceAfter=3),
 'small':ParagraphStyle('small',fontName='Sans',fontSize=7.5,leading=11,textColor=muted,spaceAfter=4)
}
out=ROOT/'dist/downloads/Awais-Ali-Resume.pdf'
doc=SimpleDocTemplate(str(out),pagesize=(595.28,841.89),leftMargin=43,rightMargin=43,topMargin=35,bottomMargin=32,title='Awais Ali Lashari - Professional Resume',author='Awais Ali Lashari',subject='Cybersecurity, software development, and applied AI')
story=[]
def p(text,style='body'):story.append(Paragraph(text,styles[style]))
p('AWAIS ALI LASHARI','name')
p('CYBERSECURITY  /  SOFTWARE DEVELOPMENT  /  APPLIED AI','subtitle')
p('Sukkur, Sindh, Pakistan  |  <link href="mailto:aliawais4413@gmail.com">aliawais4413@gmail.com</link><br/><link href="https://github.com/awais-ali-dev">github.com/awais-ali-dev</link>  |  <link href="https://www.linkedin.com/in/awais-ali-lashari-/">linkedin.com/in/awais-ali-lashari-/</link>','contact')
p('PROFILE','section')
p('Computer Science graduate with completed internships in cybersecurity, network management, and machine learning. Hands-on project work in endpoint monitoring, authorized web-security testing, cloud controls, authentication, and encrypted file sharing. Seeking an early-career role that combines careful implementation with clear technical documentation.')
p('EXPERIENCE','section')
p('Cyber Security Intern | Internee.pk | Remote | Aug-Oct 2026','role')
p('Built and documented Wazuh monitoring, a local OWASP Juice Shop audit, and a non-production Azure security demonstration. Developed OAuth 2.0/TOTP and encrypted file-sharing prototypes; prepared incident-response and awareness materials.')
p('Machine Learning Intern | Ezitech Software House | Remote | Jun-Aug 2026','role')
p('Completed a two-month machine learning internship; role and completion supported by formal internship documentation.')
p('Network Management Intern | Khairpur Defence City-2 | Jun-Jul 2026','role')
p('Supported office network infrastructure, connectivity, and network operations for Project 2 during a full-time, paid internship.')
p('SELECTED PROJECTS','section')
for title,desc in [
 ('Wazuh endpoint security lab','Configured file-integrity monitoring, failed-SSH-login detection, MITRE ATT&CK mappings, and Postfix alerts in an Ubuntu virtual lab.'),
 ('Secure file sharing and authentication','Built browser-side AES-256-GCM sharing with S3 signed URLs, and a Node.js/Express OAuth 2.0 and TOTP prototype.'),
 ('Disaster SOS Pakistan','Solo-built a Kotlin/Jetpack Compose offline communication proof of concept using Nearby Connections; tested on two Android devices.'),
 ('Medical imaging final-year project','Co-developed a ResNet-50/U-Net research prototype with Grad-CAM explanations, a Flask API, and a React interface in a team of three.')]:
 p('<b>'+title+'.</b> '+desc)
p('EDUCATION','section')
p('<b>BS Computer Science | Sukkur IBA University | 2022-2026 | Completed</b><br/>CGPA: 3.05/4.00. Coursework includes information security, computer networks, software engineering, artificial intelligence, deep learning, and computer vision.')
p('TECHNICAL TOOLKIT','section')
p('<b>Security &amp; systems:</b> Wazuh, OWASP ZAP, Linux, Azure IAM/RBAC, WAF labs, MITRE ATT&amp;CK.<br/><b>Development &amp; data:</b> Python, JavaScript, React, Node.js, Express, Kotlin, SQL, MongoDB, Git, Docker.<br/><b>Applied AI:</b> TensorFlow/Keras, OpenCV, computer vision, Grad-CAM, Flask.')
p('CREDENTIALS & SERVICE','section')
p('Completed: Google AI Professional Certificate, Google AI Essentials, Google Prompting Essentials; Cisco Introduction to Cybersecurity; selected Google/Microsoft security courses; MongoDB University and Kaggle Learn courses.<br/>In progress: Google Cybersecurity (4/9 courses) and Microsoft Cybersecurity Analyst (3/9 courses).<br/>TCF Alumni Ambassador, 2024-2025. Languages: Sindhi, Urdu, English.')
p('Awais Ali Lashari | Professional profile updated 27 October 2026','small')
doc.build(story)
print(out)
