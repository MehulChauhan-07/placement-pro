export const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8001';
export const AUTH_REDIRECT_URL = `${window.location.origin}/dashboard`;
export const EMERGENT_AUTH_URL = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(AUTH_REDIRECT_URL)}`;
