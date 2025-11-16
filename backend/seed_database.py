#!/usr/bin/env python3
"""
Database Seeding Script for PlacementPro
Creates sample data for placement drives, mock tests, resources, and announcements
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone, timedelta
import uuid
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
db_name = os.environ.get('DB_NAME', 'placement_manager_db')

client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

# Sample Placement Drives
placement_drives = [
    {
        "id": str(uuid.uuid4()),
        "company_name": "Google",
        "company_logo": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
        "role": "Software Engineer",
        "description": "Join Google as a Software Engineer and work on cutting-edge technologies that impact billions of users worldwide.",
        "eligibility": "B.Tech/M.Tech in CS/IT with CGPA >= 7.5",
        "ctc": "₹25-30 LPA",
        "location": "Bangalore, India",
        "application_deadline": (datetime.now(timezone.utc) + timedelta(days=15)).isoformat(),
        "interview_date": (datetime.now(timezone.utc) + timedelta(days=25)).isoformat(),
        "skills_required": ["Java", "Python", "Data Structures", "Algorithms", "System Design"],
        "process_steps": ["Online Test", "Technical Interview 1", "Technical Interview 2", "HR Interview"],
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "company_name": "Microsoft",
        "role": "Software Development Engineer",
        "description": "Microsoft is looking for talented developers to join our Azure team and build cloud solutions.",
        "eligibility": "B.Tech/M.Tech in CS/IT/ECE with CGPA >= 7.0",
        "ctc": "₹22-28 LPA",
        "location": "Hyderabad, India",
        "application_deadline": (datetime.now(timezone.utc) + timedelta(days=20)).isoformat(),
        "interview_date": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
        "skills_required": ["C++", "C#", ".NET", "Azure", "Problem Solving"],
        "process_steps": ["Aptitude Test", "Coding Round", "Technical Interview", "Manager Round"],
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "company_name": "Amazon",
        "role": "SDE-1",
        "description": "Amazon Web Services is hiring fresh graduates for SDE-1 positions in our cloud computing division.",
        "eligibility": "B.Tech in CS/IT with CGPA >= 7.0, Strong coding skills",
        "ctc": "₹28-35 LPA",
        "location": "Bangalore/Hyderabad",
        "application_deadline": (datetime.now(timezone.utc) + timedelta(days=12)).isoformat(),
        "interview_date": (datetime.now(timezone.utc) + timedelta(days=22)).isoformat(),
        "skills_required": ["Java", "Python", "AWS", "Data Structures", "OOP"],
        "process_steps": ["Online Assessment", "Technical Round 1", "Technical Round 2", "Bar Raiser"],
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "company_name": "Goldman Sachs",
        "role": "Technology Analyst",
        "description": "Join Goldman Sachs as a Technology Analyst and work on high-performance trading systems.",
        "eligibility": "B.Tech/M.Tech in CS/IT/Mathematics with CGPA >= 8.0",
        "ctc": "₹20-25 LPA",
        "location": "Bangalore",
        "application_deadline": (datetime.now(timezone.utc) + timedelta(days=18)).isoformat(),
        "interview_date": (datetime.now(timezone.utc) + timedelta(days=28)).isoformat(),
        "skills_required": ["Java", "C++", "Database", "Algorithms", "Problem Solving"],
        "process_steps": ["HackerRank Test", "Technical Interview 1", "Technical Interview 2", "HR Round"],
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "company_name": "Flipkart",
        "role": "Software Development Engineer",
        "description": "Flipkart is hiring SDEs to work on e-commerce platforms serving millions of customers.",
        "eligibility": "B.Tech in CS/IT with CGPA >= 7.5",
        "ctc": "₹18-24 LPA",
        "location": "Bangalore",
        "application_deadline": (datetime.now(timezone.utc) + timedelta(days=10)).isoformat(),
        "interview_date": (datetime.now(timezone.utc) + timedelta(days=20)).isoformat(),
        "skills_required": ["Java", "Spring Boot", "Microservices", "SQL", "NoSQL"],
        "process_steps": ["Coding Test", "Technical Round 1", "Technical Round 2", "Hiring Manager"],
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
]

# Sample Mock Tests
mock_tests = [
    {
        "id": str(uuid.uuid4()),
        "title": "Quantitative Aptitude Test",
        "category": "aptitude",
        "duration": 60,
        "questions": [
            {
                "question": "If a train travels 180 km in 3 hours, what is its speed in km/h?",
                "options": ["50", "60", "70", "80"],
                "correct_answer": "60"
            },
            {
                "question": "What is 15% of 200?",
                "options": ["20", "25", "30", "35"],
                "correct_answer": "30"
            },
            {
                "question": "If the ratio of boys to girls is 3:2 and there are 50 students, how many are boys?",
                "options": ["20", "25", "30", "35"],
                "correct_answer": "30"
            },
            {
                "question": "What is the next number in the series: 2, 6, 12, 20, ?",
                "options": ["28", "30", "32", "34"],
                "correct_answer": "30"
            },
            {
                "question": "A sum of money doubles in 5 years at simple interest. In how many years will it triple?",
                "options": ["10", "12", "15", "20"],
                "correct_answer": "10"
            }
        ],
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Logical Reasoning Test",
        "category": "aptitude",
        "duration": 45,
        "questions": [
            {
                "question": "All roses are flowers. Some flowers fade quickly. Therefore:",
                "options": [
                    "All roses fade quickly",
                    "Some roses fade quickly",
                    "No roses fade quickly",
                    "Cannot be determined"
                ],
                "correct_answer": "Cannot be determined"
            },
            {
                "question": "If BOOK is coded as CPPL, how is PENCIL coded?",
                "options": ["QFODJM", "QFODKM", "QFODJL", "PFNDJM"],
                "correct_answer": "QFODJM"
            },
            {
                "question": "Find the odd one out: 3, 5, 7, 12, 13, 17, 19",
                "options": ["3", "12", "13", "19"],
                "correct_answer": "12"
            }
        ],
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Data Structures Basics",
        "category": "technical",
        "duration": 90,
        "questions": [
            {
                "question": "What is the time complexity of searching in a balanced BST?",
                "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
                "correct_answer": "O(log n)"
            },
            {
                "question": "Which data structure uses LIFO principle?",
                "options": ["Queue", "Stack", "Tree", "Graph"],
                "correct_answer": "Stack"
            },
            {
                "question": "What is the best case time complexity of Quick Sort?",
                "options": ["O(n)", "O(n log n)", "O(n²)", "O(log n)"],
                "correct_answer": "O(n log n)"
            },
            {
                "question": "Which data structure is used for BFS traversal?",
                "options": ["Stack", "Queue", "Heap", "Array"],
                "correct_answer": "Queue"
            }
        ],
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Python Programming Test",
        "category": "coding",
        "duration": 120,
        "questions": [
            {
                "question": "What does the 'lambda' keyword do in Python?",
                "options": [
                    "Creates a loop",
                    "Creates an anonymous function",
                    "Imports a module",
                    "Defines a class"
                ],
                "correct_answer": "Creates an anonymous function"
            },
            {
                "question": "What is the output of: print(type([]) == list)",
                "options": ["True", "False", "list", "Error"],
                "correct_answer": "True"
            },
            {
                "question": "Which method is used to add an element at the end of a list?",
                "options": ["add()", "append()", "insert()", "push()"],
                "correct_answer": "append()"
            }
        ],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
]

# Sample Resources
resources = [
    {
        "id": str(uuid.uuid4()),
        "title": "Data Structures and Algorithms Complete Guide",
        "description": "Comprehensive guide covering all important DSA topics with practice problems",
        "category": "Technical",
        "type": "pdf",
        "url": "https://example.com/dsa-guide.pdf",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "System Design Interview Preparation",
        "description": "Learn how to approach system design interviews with real-world examples",
        "category": "Technical",
        "type": "video",
        "url": "https://www.youtube.com/watch?v=example",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Resume Building Tips for Tech Jobs",
        "description": "Expert tips on crafting a resume that stands out to recruiters",
        "category": "Career",
        "type": "link",
        "url": "https://example.com/resume-tips",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Behavioral Interview Questions",
        "description": "Common behavioral questions and how to answer them effectively",
        "category": "Interview",
        "type": "pdf",
        "url": "https://example.com/behavioral-questions.pdf",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Aptitude Test Practice Papers",
        "description": "100+ aptitude questions with solutions for placement preparation",
        "category": "Aptitude",
        "type": "pdf",
        "url": "https://example.com/aptitude-papers.pdf",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "LeetCode Top 100 Problems",
        "description": "Most frequently asked coding problems in technical interviews",
        "category": "Technical",
        "type": "link",
        "url": "https://leetcode.com/problemset/top-100-liked/",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
]

# Sample Announcements
announcements = [
    {
        "id": str(uuid.uuid4()),
        "title": "🎉 Google On-Campus Drive Scheduled for Next Month",
        "content": "Google will be conducting on-campus recruitment. Eligible students, please apply before the deadline.",
        "priority": "high",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "📚 New Mock Test Series Added - Practice Now!",
        "content": "We've added new aptitude and technical mock tests. Start practicing to improve your scores.",
        "priority": "normal",
        "created_at": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "⚠️ Resume Submission Deadline Extended",
        "content": "The deadline for resume submission has been extended by 3 days. Update your profiles.",
        "priority": "high",
        "created_at": (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "💼 Career Counseling Session This Friday",
        "content": "Join us for a career counseling session with industry experts. Register in the resources section.",
        "priority": "normal",
        "created_at": (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()
    }
]

async def seed_database():
    print("🌱 Starting database seeding...\n")
    
    try:
        # Clear existing data
        print("🗑️  Clearing existing data...")
        await db.placement_drives.delete_many({})
        await db.mock_tests.delete_many({})
        await db.resources.delete_many({})
        await db.announcements.delete_many({})
        print("✓ Existing data cleared\n")
        
        # Insert placement drives
        print("💼 Inserting placement drives...")
        await db.placement_drives.insert_many(placement_drives)
        print(f"✓ Added {len(placement_drives)} placement drives\n")
        
        # Insert mock tests
        print("🎯 Inserting mock tests...")
        await db.mock_tests.insert_many(mock_tests)
        print(f"✓ Added {len(mock_tests)} mock tests\n")
        
        # Insert resources
        print("📚 Inserting learning resources...")
        await db.resources.insert_many(resources)
        print(f"✓ Added {len(resources)} resources\n")
        
        # Insert announcements
        print("📢 Inserting announcements...")
        await db.announcements.insert_many(announcements)
        print(f"✓ Added {len(announcements)} announcements\n")
        
        print("✨ Database seeding completed successfully!")
        print("\n📊 Summary:")
        print(f"   - Placement Drives: {len(placement_drives)}")
        print(f"   - Mock Tests: {len(mock_tests)}")
        print(f"   - Resources: {len(resources)}")
        print(f"   - Announcements: {len(announcements)}")
        print("\n🚀 You can now start the application and explore the features!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
