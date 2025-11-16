import { api } from './api';

export const authService = {
  me: async () => {
    const { data } = await api.get('/auth/me');
    return data;
  },
  logout: async () => {
    await api.post('/auth/logout');
  },
  establishSession: async (sessionId) => {
    await api.post('/auth/session', {}, { headers: { 'X-Session-ID': sessionId } });
  },
};
