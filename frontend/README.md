# PlacementPro Frontend (Vite + React)

## Overview

Refactored from a single monolithic `App.js` into a modular Vite + React project with separated concerns:

- `src/pages/*` individual page views
- `src/layouts/DashboardLayout.jsx` shared layout
- `src/context/AuthContext.jsx` auth state
- `src/components/*` reusable helpers (ProtectedRoute, SessionHandler)
- `src/services/*` API & auth services
- `src/config/constants.js` environment-based config

## Getting Started

### 1. Install dependencies

```bash
npm install
```

### 2. Environment variables

Create a `.env` file in the frontend root:

```
VITE_BACKEND_URL=http://localhost:8001
```

(Adjust port/host to match your running backend.)

### 3. Run development server

```bash
npm run dev
```

Visit: http://localhost:5173

### 4. Build for production

```bash
npm run build
```

Then preview locally:

```bash
npm run preview
```

## Folder Structure

```
frontend/
  index.html
  vite.config.js
  package.json
  src/
    main.jsx
    App.jsx
    App.css
    config/constants.js
    context/AuthContext.jsx
    services/api.js
    services/authService.js
    layouts/DashboardLayout.jsx
    components/ProtectedRoute.jsx
    components/SessionHandler.jsx
    pages/
      LandingPage.jsx
      Dashboard.jsx
      PlacementDrives.jsx
      MyApplications.jsx
      MockTests.jsx
      Resources.jsx
      Profile.jsx
      AdminPanel.jsx
```

## Notes

- Replace any previous `REACT_APP_BACKEND_URL` usage with `import.meta.env.VITE_BACKEND_URL`.
- Axios instance handles `withCredentials` for auth cookies.
- Session handling logic moved to `SessionHandler` component.

## Next Ideas

- Add error boundary component.
- Implement code-splitting via dynamic imports for routes.
- Add unit tests (React Testing Library + Vitest).

Enjoy building! 🚀
