import pdfplumber
import json
from typing import Dict

def parse_resume(pdf_path: str) -> Dict:
    """Extract text and structured data from PDF resume using pdfplumber."""
    data = {
        'full_text': '',
        'skills': [],
        'experience': [],
        'education': [],
        'contact': {}
    }

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                data['full_text'] += page.extract_text() or ''
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return data

    # Basic extraction heuristics
    lines = data['full_text'].split('\n')
    current_section = None

    for line in lines:
        line_lower = line.lower().strip()

        # Section detection
        if 'skill' in line_lower:
            current_section = 'skills'
        elif 'experience' in line_lower or 'employment' in line_lower:
            current_section = 'experience'
        elif 'education' in line_lower:
            current_section = 'education'
        elif 'contact' in line_lower or 'email' in line_lower or 'phone' in line_lower:
            current_section = 'contact'

        # Extract content
        if current_section == 'skills' and line.strip() and not any(x in line_lower for x in ['skill', 'experience', 'education', 'contact']):
            data['skills'].extend([s.strip() for s in line.split(',') if s.strip()])
        elif current_section == 'experience' and line.strip() and not any(x in line_lower for x in ['experience', 'education', 'contact', 'skill']):
            if len(line.strip()) > 10:
                data['experience'].append(line.strip())
        elif current_section == 'education' and line.strip() and not any(x in line_lower for x in ['education', 'contact', 'skill', 'experience']):
            if len(line.strip()) > 10:
                data['education'].append(line.strip())

    # Deduplicate and clean
    data['skills'] = list(set([s.lower() for s in data['skills'] if s]))
    data['experience'] = list(set(data['experience']))
    data['education'] = list(set(data['education']))

    return data
