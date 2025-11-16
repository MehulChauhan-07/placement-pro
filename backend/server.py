from fastapi import FastAPI, APIRouter, HTTPException, Header, Response, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
import httpx

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

# Models
class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    email: str
    name: str
    picture: Optional[str] = None
    role: str = "student"  # student, admin, recruiter
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserSession(BaseModel):
    model_config = ConfigDict(extra="ignore")
    user_id: str
    session_token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StudentProfile(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    phone: Optional[str] = None
    college: Optional[str] = None
    degree: Optional[str] = None
    graduation_year: Optional[int] = None
    skills: List[str] = []
    resume_url: Optional[str] = None
    cgpa: Optional[float] = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PlacementDrive(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    company_name: str
    company_logo: Optional[str] = None
    role: str
    description: str
    eligibility: str
    ctc: str
    location: str
    application_deadline: datetime
    interview_date: Optional[datetime] = None
    skills_required: List[str] = []
    process_steps: List[str] = []
    status: str = "active"  # active, closed
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Application(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    drive_id: str
    user_id: str
    status: str = "applied"  # applied, shortlisted, rejected, selected
    applied_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MockTest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    category: str  # aptitude, technical, coding
    questions: List[dict]  # {question, options, correct_answer}
    duration: int  # minutes
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TestAttempt(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    test_id: str
    user_id: str
    score: int
    total: int
    answers: List[dict]
    attempted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Resource(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    category: str
    type: str  # pdf, video, link
    url: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Announcement(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    priority: str = "normal"  # high, normal, low
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Request Models
class SessionDataRequest(BaseModel):
    session_id: str

class ProfileUpdateRequest(BaseModel):
    phone: Optional[str] = None
    college: Optional[str] = None
    degree: Optional[str] = None
    graduation_year: Optional[int] = None
    skills: Optional[List[str]] = None
    cgpa: Optional[float] = None

class DriveCreateRequest(BaseModel):
    company_name: str
    company_logo: Optional[str] = None
    role: str
    description: str
    eligibility: str
    ctc: str
    location: str
    application_deadline: datetime
    interview_date: Optional[datetime] = None
    skills_required: List[str] = []
    process_steps: List[str] = []

class ApplicationStatusUpdate(BaseModel):
    status: str

class TestSubmission(BaseModel):
    test_id: str
    answers: List[dict]

class ResourceCreateRequest(BaseModel):
    title: str
    description: str
    category: str
    type: str
    url: str

class AnnouncementCreateRequest(BaseModel):
    title: str
    content: str
    priority: str = "normal"

# Auth Helper
async def get_current_user(authorization: Optional[str] = Header(None), request: Request = None) -> User:
    session_token = None
    
    # Try to get token from cookie first
    if request and request.cookies.get("session_token"):
        session_token = request.cookies.get("session_token")
    # Fallback to Authorization header
    elif authorization and authorization.startswith("Bearer "):
        session_token = authorization.replace("Bearer ", "")
    
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Check session in database
    session = await db.user_sessions.find_one({"session_token": session_token})
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    # Check if session expired
    if isinstance(session["expires_at"], str):
        expires_at = datetime.fromisoformat(session["expires_at"])
    else:
        expires_at = session["expires_at"]
    
    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Session expired")
    
    # Get user
    user = await db.users.find_one({"id": session["user_id"]}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return User(**user)

# Auth Routes
@api_router.post("/auth/session")
async def create_session(session_id: str = Header(None, alias="X-Session-ID"), response: Response = None):
    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID required")
    
    # Get session data from Emergent Auth
    async with httpx.AsyncClient() as client:
        try:
            auth_response = await client.get(
                "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data",
                headers={"X-Session-ID": session_id}
            )
            auth_response.raise_for_status()
            session_data = auth_response.json()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to get session data: {str(e)}")
    
    # Create or update user
    user_data = {
        "id": session_data["id"],
        "email": session_data["email"],
        "name": session_data["name"],
        "picture": session_data.get("picture"),
        "role": "student",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    existing_user = await db.users.find_one({"email": session_data["email"]})
    if not existing_user:
        await db.users.insert_one(user_data)
        # Create student profile
        profile_data = {
            "id": str(uuid.uuid4()),
            "user_id": session_data["id"],
            "skills": [],
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        await db.student_profiles.insert_one(profile_data)
    
    # Store session
    session_token = session_data["session_token"]
    session_doc = {
        "user_id": session_data["id"],
        "session_token": session_token,
        "expires_at": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.user_sessions.insert_one(session_doc)
    
    # Set cookie
    if response:
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            secure=True,
            samesite="none",
            max_age=7 * 24 * 60 * 60,
            path="/"
        )
    
    return {"user": user_data, "session_token": session_token}

@api_router.get("/auth/me")
async def get_me(authorization: Optional[str] = Header(None), request: Request = None):
    user = await get_current_user(authorization, request)
    return user

@api_router.post("/auth/logout")
async def logout(authorization: Optional[str] = Header(None), request: Request = None, response: Response = None):
    user = await get_current_user(authorization, request)
    
    # Delete session
    session_token = None
    if request and request.cookies.get("session_token"):
        session_token = request.cookies.get("session_token")
    elif authorization and authorization.startswith("Bearer "):
        session_token = authorization.replace("Bearer ", "")
    
    if session_token:
        await db.user_sessions.delete_one({"session_token": session_token})
    
    # Clear cookie
    if response:
        response.delete_cookie("session_token", path="/")
    
    return {"message": "Logged out successfully"}

# Profile Routes
@api_router.get("/profile")
async def get_profile(authorization: Optional[str] = Header(None), request: Request = None):
    user = await get_current_user(authorization, request)
    profile = await db.student_profiles.find_one({"user_id": user.id}, {"_id": 0})
    return {"user": user, "profile": profile}

@api_router.put("/profile")
async def update_profile(profile_update: ProfileUpdateRequest, authorization: Optional[str] = Header(None), request: Request = None):
    user = await get_current_user(authorization, request)
    
    update_data = profile_update.model_dump(exclude_none=True)
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    await db.student_profiles.update_one(
        {"user_id": user.id},
        {"$set": update_data}
    )
    
    profile = await db.student_profiles.find_one({"user_id": user.id}, {"_id": 0})
    return profile

# Placement Drives Routes
@api_router.get("/drives")
async def get_drives():
    drives = await db.placement_drives.find({"status": "active"}, {"_id": 0}).sort("created_at", -1).to_list(100)
    for drive in drives:
        if isinstance(drive.get("application_deadline"), str):
            drive["application_deadline"] = datetime.fromisoformat(drive["application_deadline"]).isoformat()
        if drive.get("interview_date") and isinstance(drive["interview_date"], str):
            drive["interview_date"] = datetime.fromisoformat(drive["interview_date"]).isoformat()
    return drives

@api_router.get("/drives/{drive_id}")
async def get_drive(drive_id: str):
    drive = await db.placement_drives.find_one({"id": drive_id}, {"_id": 0})
    if not drive:
        raise HTTPException(status_code=404, detail="Drive not found")
    return drive

@api_router.post("/drives")
async def create_drive(drive_data: DriveCreateRequest, authorization: Optional[str] = Header(None), request: Request = None):
    user = await get_current_user(authorization, request)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    drive = PlacementDrive(**drive_data.model_dump())
    drive_dict = drive.model_dump()
    drive_dict["created_at"] = drive_dict["created_at"].isoformat()
    drive_dict["application_deadline"] = drive_dict["application_deadline"].isoformat()
    if drive_dict.get("interview_date"):
        drive_dict["interview_date"] = drive_dict["interview_date"].isoformat()
    
    await db.placement_drives.insert_one(drive_dict)
    return drive

@api_router.put("/drives/{drive_id}")
async def update_drive(drive_id: str, drive_data: DriveCreateRequest, authorization: Optional[str] = Header(None), request: Request = None):
    user = await get_current_user(authorization, request)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    update_data = drive_data.model_dump()
    update_data["application_deadline"] = update_data["application_deadline"].isoformat()
    if update_data.get("interview_date"):
        update_data["interview_date"] = update_data["interview_date"].isoformat()
    
    result = await db.placement_drives.update_one(
        {"id": drive_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Drive not found")
    
    return {"message": "Drive updated successfully"}

@api_router.delete("/drives/{drive_id}")
async def delete_drive(drive_id: str, authorization: Optional[str] = Header(None), request: Request = None):
    user = await get_current_user(authorization, request)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    result = await db.placement_drives.delete_one({"id": drive_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Drive not found")
    
    return {"message": "Drive deleted successfully"}

# Application Routes
@api_router.post("/applications")
async def apply_to_drive(drive_id: str, authorization: Optional[str] = Header(None), request: Request = None):
    user = await get_current_user(authorization, request)
    
    # Check if already applied
    existing = await db.applications.find_one({"drive_id": drive_id, "user_id": user.id})
    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this drive")
    
    application = Application(drive_id=drive_id, user_id=user.id)
    app_dict = application.model_dump()
    app_dict["applied_at"] = app_dict["applied_at"].isoformat()
    app_dict["updated_at"] = app_dict["updated_at"].isoformat()
    
    await db.applications.insert_one(app_dict)
    return application

@api_router.get("/applications/my")
async def get_my_applications(authorization: Optional[str] = Header(None), request: Request = None):
    user = await get_current_user(authorization, request)
    applications = await db.applications.find({"user_id": user.id}, {"_id": 0}).to_list(100)
    
    # Enrich with drive data
    for app in applications:
        drive = await db.placement_drives.find_one({"id": app["drive_id"]}, {"_id": 0})
        app["drive"] = drive
    
    return applications

@api_router.get("/applications/drive/{drive_id}")
async def get_drive_applications(drive_id: str, authorization: Optional[str] = Header(None), request: Request = None):
    user = await get_current_user(authorization, request)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    applications = await db.applications.find({"drive_id": drive_id}, {"_id": 0}).to_list(1000)
    
    # Enrich with user data
    for app in applications:
        user_data = await db.users.find_one({"id": app["user_id"]}, {"_id": 0})
        profile = await db.student_profiles.find_one({"user_id": app["user_id"]}, {"_id": 0})
        app["user"] = user_data
        app["profile"] = profile
    
    return applications

@api_router.put("/applications/{application_id}/status")
async def update_application_status(application_id: str, status_update: ApplicationStatusUpdate, authorization: Optional[str] = Header(None), request: Request = None):
    user = await get_current_user(authorization, request)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    result = await db.applications.update_one(
        {"id": application_id},
        {"$set": {"status": status_update.status, "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return {"message": "Status updated successfully"}

# Mock Test Routes
@api_router.get("/tests")
async def get_tests():
    tests = await db.mock_tests.find({}, {"_id": 0, "questions": 0}).to_list(100)
    return tests

@api_router.get("/tests/{test_id}")
async def get_test(test_id: str, authorization: Optional[str] = Header(None), request: Request = None):
    user = await get_current_user(authorization, request)
    test = await db.mock_tests.find_one({"id": test_id}, {"_id": 0})
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    # Remove correct answers for students
    for question in test["questions"]:
        question.pop("correct_answer", None)
    
    return test

@api_router.post("/tests/submit")
async def submit_test(submission: TestSubmission, authorization: Optional[str] = Header(None), request: Request = None):
    user = await get_current_user(authorization, request)
    
    # Get test with correct answers
    test = await db.mock_tests.find_one({"id": submission.test_id}, {"_id": 0})
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    # Calculate score
    score = 0
    total = len(test["questions"])
    for i, answer in enumerate(submission.answers):
        if i < len(test["questions"]) and answer.get("answer") == test["questions"][i].get("correct_answer"):
            score += 1
    
    # Save attempt
    attempt = TestAttempt(
        test_id=submission.test_id,
        user_id=user.id,
        score=score,
        total=total,
        answers=submission.answers
    )
    attempt_dict = attempt.model_dump()
    attempt_dict["attempted_at"] = attempt_dict["attempted_at"].isoformat()
    
    await db.test_attempts.insert_one(attempt_dict)
    return {"score": score, "total": total, "percentage": round((score / total) * 100, 2)}

@api_router.get("/tests/attempts/my")
async def get_my_attempts(authorization: Optional[str] = Header(None), request: Request = None):
    user = await get_current_user(authorization, request)
    attempts = await db.test_attempts.find({"user_id": user.id}, {"_id": 0}).sort("attempted_at", -1).to_list(100)
    
    # Enrich with test data
    for attempt in attempts:
        test = await db.mock_tests.find_one({"id": attempt["test_id"]}, {"_id": 0, "questions": 0})
        attempt["test"] = test
    
    return attempts

# Resources Routes
@api_router.get("/resources")
async def get_resources():
    resources = await db.resources.find({}, {"_id": 0}).sort("created_at", -1).to_list(100)
    return resources

@api_router.post("/resources")
async def create_resource(resource_data: ResourceCreateRequest, authorization: Optional[str] = Header(None), request: Request = None):
    user = await get_current_user(authorization, request)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    resource = Resource(**resource_data.model_dump())
    resource_dict = resource.model_dump()
    resource_dict["created_at"] = resource_dict["created_at"].isoformat()
    
    await db.resources.insert_one(resource_dict)
    return resource

@api_router.delete("/resources/{resource_id}")
async def delete_resource(resource_id: str, authorization: Optional[str] = Header(None), request: Request = None):
    user = await get_current_user(authorization, request)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    result = await db.resources.delete_one({"id": resource_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    return {"message": "Resource deleted successfully"}

# Announcements Routes
@api_router.get("/announcements")
async def get_announcements():
    announcements = await db.announcements.find({}, {"_id": 0}).sort("created_at", -1).limit(10).to_list(10)
    return announcements

@api_router.post("/announcements")
async def create_announcement(announcement_data: AnnouncementCreateRequest, authorization: Optional[str] = Header(None), request: Request = None):
    user = await get_current_user(authorization, request)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    announcement = Announcement(**announcement_data.model_dump())
    ann_dict = announcement.model_dump()
    ann_dict["created_at"] = ann_dict["created_at"].isoformat()
    
    await db.announcements.insert_one(ann_dict)
    return announcement

# Admin Stats
@api_router.get("/admin/stats")
async def get_admin_stats(authorization: Optional[str] = Header(None), request: Request = None):
    user = await get_current_user(authorization, request)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    total_students = await db.users.count_documents({"role": "student"})
    total_drives = await db.placement_drives.count_documents({})
    total_applications = await db.applications.count_documents({})
    placed_students = await db.applications.count_documents({"status": "selected"})
    
    # Applications by status
    pipeline = [
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
    status_stats = await db.applications.aggregate(pipeline).to_list(100)
    
    return {
        "total_students": total_students,
        "total_drives": total_drives,
        "total_applications": total_applications,
        "placed_students": placed_students,
        "status_breakdown": status_stats
    }

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
