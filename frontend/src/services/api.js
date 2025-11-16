import axios from 'axios';
import { BACKEND_URL } from '@/config/constants';

export const api = axios.create({
  baseURL: `${BACKEND_URL}/api`,
  withCredentials: true,
});

api.interceptors.response.use(
  (res) => res,
  (error) => {
    // Optional global error handling
    return Promise.reject(error);
  }
);
