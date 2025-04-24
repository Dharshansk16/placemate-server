import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
api_key:str = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash-001")

def fetch_company_data(company_name):
    prompt = f"""
    Provide detailed structured data in JSON format for a company named '{company_name}'.
    The JSON should be structured exactly like the example below (no commentary or extra explanation), and include the following fields:

    - name (string)
    - description (string)
    - tech_stack (list of technology names used by the company)
    - headquarters (string)
    - founded_year (integer)
    - employee_count (integer)
    - industry (string)
    - website (string - URL)
    - average_ctc (float - average CTC for freshers in LPA)
    - work_culture (string - short paragraph)

    - roles (list of dictionaries):
        - title (string)
        - description (string)
        - tech_stack (list of technologies)
        - average_ctc (float - in LPA)
        - job_location (string)
        - openings_per_year (integer)

    - interview_tips (list of general tips or advice)
    
    - interview_experiences (list of dictionaries):
        - role_title (string)
        - experience (string)
        - outcome (string - one of: "selected", "rejected")
        - difficulty (string - one of: "easy", "medium", "hard")
        - tech_stack (list of technologies)

    - reviews (list of dictionaries):
        - reviewer_name (string or null)
        - rating (float - out of 5)
        - review_text (string)
        - pros (string or null)
        - cons (string or null)
        - work_life_balance (integer - out of 10)
        - culture (integer - out of 10)

    Example format:

    {{
        "name": "ExampleCorp",
        "description": "A leading provider of example solutions.",
        "tech_stack": ["Python", "Django", "React"],
        "headquarters": "New York, USA",
        "founded_year": 2010,
        "employee_count": 500,
        "industry": "Software Development",
        "website": "https://example.com",
        "average_ctc": 10.5,
        "work_culture": "Collaborative and innovation-focused environment.",
        "roles": [
            {{
                "title": "Software Engineer",
                "description": "Develop and maintain web applications.",
                "tech_stack": ["Python", "Django", "React"],
                "average_ctc": 12.0,
                "job_location": "Bangalore",
                "openings_per_year": 20
            }}
        ],
        "interview_tips": [
            "Focus on data structures and algorithms.",
            "Prepare for system design interviews."
        ],
        "interview_experiences": [
            {{
                "role_title": "Software Engineer",
                "experience": "Interview had three rounds including DSA, System Design, and HR.",
                "outcome": "selected",
                "difficulty": "medium",
                "tech_stack": ["Python", "Django"]
            }}
        ],
        "reviews": [
            {{
                "reviewer_name": "John Doe",
                "rating": 4.5,
                "review_text": "Great company culture and learning opportunities.",
                "pros": "Supportive teams, flexible hours.",
                "cons": "Fast-paced can be overwhelming.",
                "work_life_balance": 8,
                "culture": 9
            }}
        ]
    }}
    """

    response = model.generate_content(prompt)
    try:
        return response.text
    except Exception as e:
        return str(e)
