import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key: str = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash-001")

def fetch_company_data(company_name):
    prompt = f"""
    Provide detailed structured data in JSON format for an Indian company or a company operating in India named '{company_name}'.
    The data should reflect the Indian job market context, especially for freshers and early-career professionals.
    The JSON must match the structure exactly like the example below (no commentary or extra explanation), and include the following fields:

    - name (string)
    - description (string)
    - tech_stack (list of technology names used by the company)
    - headquarters (string)
    - founded_year (integer)
    - employee_count (integer)
    - industry (string)
    - website (string - URL)
    - average_ctc (float - average CTC for freshers in LPA)
    - work_culture (string - short paragraph relevant to Indian context)

    - roles (list of dictionaries):
        - title (string)
        - description (string)
        - tech_stack (list of technologies)
        - average_ctc (float - in LPA)
        - job_location (string - Indian cities preferred)
        - openings_per_year (integer)

    - interview_tips (list of general tips or advice relevant to Indian placement and recruitment)

    - interview_experiences (list of dictionaries):
        - role_title (string)
        - experience (string)
        - outcome (string - one of: "selected", "rejected", "on hold", "internship offer")
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
        "name": "ExampleTech India",
        "description": "A rapidly growing IT services and product company in India.",
        "tech_stack": ["Java", "Spring Boot", "Angular", "MySQL"],
        "headquarters": "Bangalore, India",
        "founded_year": 2012,
        "employee_count": 2000,
        "industry": "IT Services",
        "website": "https://exampletech.in",
        "average_ctc": 6.5,
        "work_culture": "Fast-paced, learning-oriented with a focus on mentorship and career growth.",
        "roles": [
            {{
                "title": "Backend Developer",
                "description": "Work on microservices and REST APIs using Java stack.",
                "tech_stack": ["Java", "Spring Boot", "PostgreSQL"],
                "average_ctc": 7.2,
                "job_location": "Pune",
                "openings_per_year": 15
            }}
        ],
        "interview_tips": [
            "Revise DSA topics commonly asked in Indian service and product-based companies.",
            "Prepare projects and be ready to explain your contributions clearly.",
            "Practice coding on platforms like GeeksforGeeks and LeetCode.",
            "Brush up on CS fundamentals (DBMS, OS, OOP, CN)."
        ],
        "interview_experiences": [
            {{
                "role_title": "Backend Developer",
                "experience": "Online test, followed by technical and HR rounds. Focused on Java, DB queries, and problem-solving.",
                "outcome": "selected",
                "difficulty": "medium",
                "tech_stack": ["Java", "SQL"]
            }}
        ],
        "reviews": [
            {{
                "reviewer_name": "Ananya",
                "rating": 4.2,
                "review_text": "Great place for freshers. Good mentorship and tech exposure.",
                "pros": "Supportive teams, flexible timing.",
                "cons": "Can be a bit hectic during release cycles.",
                "work_life_balance": 7,
                "culture": 8
            }}
        ]
    }}
    """
    response = model.generate_content(prompt)
    try:
        return response.text
    except Exception as e:
        return str(e)
