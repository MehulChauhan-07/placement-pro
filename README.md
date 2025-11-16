# PlacementPro - Placement Management System

> A comprehensive, modern placement management platform for college students with mock tests, placement drives, and application tracking.

![PlacementPro](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![React](https://img.shields.io/badge/React-19.0-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)
![MongoDB](https://img.shields.io/badge/MongoDB-Latest-success)

## 🚀 Features

- **🔐 Google OAuth Authentication** - Secure login via Emergent Auth
- **📊 Student Dashboard** - Profile management, quick actions, announcements
- **💼 Placement Drives** - Browse, search, and apply to company opportunities
- **📝 Application Tracking** - Monitor status (applied, shortlisted, selected, rejected)
- **🎯 Mock Tests** - Practice tests with scoring and progress tracking
- **📚 Learning Resources** - Study materials, videos, and guides
- **👨‍💼 Admin Panel** - Manage drives, students, applications, and analytics
- **📱 Fully Responsive** - Works seamlessly on desktop, tablet, and mobile

## 🛠 Tech Stack

**Frontend:**

- React 19
- React Router v7
- Axios for API calls
- Lucide React icons
- Custom CSS with glassmorphism design

**Backend:**

- FastAPI (Python)
- Motor (Async MongoDB driver)
- JWT authentication
- Pydantic for data validation

**Database:**

- MongoDB

## 📋 Prerequisites

Before installation, ensure you have:

- **Node.js** (v18 or higher) - [Download](https://nodejs.org/)
- **Python** (v3.10 or higher) - [Download](https://www.python.org/)
- **MongoDB** (v5.0 or higher) - [Download](https://www.mongodb.com/try/download/community)
- **Yarn** package manager - Install via `npm install -g yarn`
- **Git** - [Download](https://git-scm.com/)

## 🔧 Installation Guide

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd placement-manager
```

### Step 2: MongoDB Setup

**Option A: Local MongoDB**

```bash
# Start MongoDB service
# On macOS:
brew services start mongodb-community

# On Windows (Run as Administrator):
net start MongoDB

# On Linux:
sudo systemctl start mongod
```

**Option B: MongoDB Atlas (Cloud)**

1. Create free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a cluster
3. Get connection string (replace `<password>` with your password)
4. Use this string in `.env` file

### Step 3: Backend Setup

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env file with your configuration
# For local MongoDB:
MONGO_URL="mongodb://localhost:27017"
DB_NAME="placement_manager_db"
CORS_ORIGINS="http://localhost:3000"
```

### Step 4: Frontend Setup

```bash
# Navigate to frontend folder (from root)
cd frontend

# Install dependencies
yarn install

# Create .env file
cp .env.example .env.local

# Edit .env.local with your backend URL
REACT_APP_BACKEND_URL=http://localhost:8001
```

### Step 5: Seed Database (Optional - Sample Data)

```bash
# From backend folder with activated venv
python seed_database.py
```

This will create:

- Sample placement drives
- Mock tests
- Learning resources
- Announcements

## 🚀 Running the Application

### Method 1: Manual Start (Development)

**Terminal 1 - Backend:**

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

**Terminal 2 - Frontend:**

```bash
cd frontend
yarn start
```

Access the app at: **http://localhost:3000**

### Method 2: Using Setup Scripts

**On macOS/Linux:**

```bash
chmod +x start.sh
./start.sh
```

**On Windows:**

```bash
start.bat
```

## 🔑 Authentication Setup

This app uses **Emergent Auth** for Google OAuth. The authentication flow is pre-configured:

1. Click "Sign In" or "Get Started"
2. You'll be redirected to Google OAuth
3. After successful login, you'll be redirected back to dashboard
4. Session persists for 7 days

**Note:** For production deployment, you'll need to update the redirect URL in the code.

## 👨‍💼 Admin Access

To make a user admin:

```bash
# Connect to MongoDB
mongo

# Switch to your database
use placement_manager_db

# Update user role
db.users.updateOne(
  { email: "your-email@example.com" },
  { $set: { role: "admin" } }
)
```

Admin features:

- Create/edit/delete placement drives
- View all applications
- Update application status
- Add resources and announcements
- View analytics dashboard

## 📁 Project Structure

```
placement-manager/
├── backend/
│   ├── server.py          # FastAPI application
│   ├── requirements.txt   # Python dependencies
│   ├── seed_database.py   # Database seeding script
│   └── .env              # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.js        # Main React component
│   │   ├── App.css       # Styling
│   │   └── index.js      # Entry point
│   ├── package.json      # Node dependencies
│   └── .env.local        # Frontend env variables
├── setup.sh              # Unix setup script
├── setup.bat             # Windows setup script
├── start.sh              # Unix start script
├── start.bat             # Windows start script
└── README.md             # This file
```

## 🌐 API Documentation

Once the backend is running, visit:

- **Swagger UI:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc

### Key API Endpoints

**Authentication:**

- `POST /api/auth/session` - Create session from Emergent Auth
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout

**Placement Drives:**

- `GET /api/drives` - List all drives
- `GET /api/drives/{id}` - Get drive details
- `POST /api/drives` - Create drive (admin only)
- `PUT /api/drives/{id}` - Update drive (admin only)
- `DELETE /api/drives/{id}` - Delete drive (admin only)

**Applications:**

- `POST /api/applications?drive_id={id}` - Apply to drive
- `GET /api/applications/my` - Get my applications
- `GET /api/applications/drive/{id}` - Get drive applications (admin)
- `PUT /api/applications/{id}/status` - Update status (admin)

**Tests:**

- `GET /api/tests` - List tests
- `GET /api/tests/{id}` - Get test details
- `POST /api/tests/submit` - Submit test
- `GET /api/tests/attempts/my` - Get my attempts

**Profile:**

- `GET /api/profile` - Get profile
- `PUT /api/profile` - Update profile

**Resources:**

- `GET /api/resources` - List resources
- `POST /api/resources` - Add resource (admin)
- `DELETE /api/resources/{id}` - Delete resource (admin)

**Announcements:**

- `GET /api/announcements` - List announcements
- `POST /api/announcements` - Create announcement (admin)

**Admin:**

- `GET /api/admin/stats` - Get statistics (admin)

## 🐛 Troubleshooting

### Backend won't start

**Issue:** `ModuleNotFoundError`

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Issue:** MongoDB connection error

```bash
# Check if MongoDB is running
mongo --eval "db.adminCommand('ping')"

# If not running, start MongoDB service
```

### Frontend won't start

**Issue:** `node-sass` or dependency errors

```bash
# Clear cache and reinstall
rm -rf node_modules yarn.lock
yarn install
```

**Issue:** Port 3000 already in use

```bash
# Kill process on port 3000
# macOS/Linux:
lsof -ti:3000 | xargs kill -9

# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### CORS Issues

Ensure backend `.env` has correct CORS_ORIGINS:

```
CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
```

## 🚢 Production Deployment

### Environment Variables

**Backend (.env):**

```bash
MONGO_URL="your-production-mongodb-url"
DB_NAME="placement_manager_prod"
CORS_ORIGINS="https://yourdomain.com"
```

**Frontend (.env.local):**

```bash
REACT_APP_BACKEND_URL=https://api.yourdomain.com
```

### Build Frontend

```bash
cd frontend
yarn build
```

This creates optimized production build in `build/` folder.

### Deploy Backend

**Using Gunicorn:**

```bash
cd backend
gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001
```

### Recommended Platforms

- **Backend:** Railway, Render, DigitalOcean, AWS EC2
- **Frontend:** Vercel, Netlify, AWS S3 + CloudFront
- **Database:** MongoDB Atlas, AWS DocumentDB

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 💬 Support

For issues and questions:

- Create an issue on GitHub
- Email: support@placementpro.com

## 🙏 Acknowledgments

- Built with [Emergent Auth](https://emergent.sh) for authentication
- Icons by [Lucide](https://lucide.dev)
- UI inspired by modern SaaS platforms

---

**Happy Coding! 🚀**
