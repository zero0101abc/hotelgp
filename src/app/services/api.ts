const API_BASE = import.meta.env.VITE_API_URL || '';

class ApiService {
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      credentials: 'include',
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
      throw new Error(error.detail || 'Request failed');
    }

    if (response.status === 204) {
      return {} as T;
    }

    return response.json();
  }

  async login(email: string, password: string) {
    return this.request<{ message: string; user: any }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async register(email: string, password: string, name: string, phone?: string) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, name, phone }),
    });
  }

  async logout() {
    return this.request('/auth/logout', { method: 'POST' });
  }

  async getMe() {
    return this.request('/auth/me');
  }

  async checkAuth() {
    return this.request<{ authenticated: boolean; user?: any }>('/auth/check');
  }

  async getRooms(filters?: { type?: string; status?: string; featured?: boolean; children?: number }) {
    const params = new URLSearchParams();
    if (filters?.type) params.append('type', filters.type);
    if (filters?.status) params.append('status', filters.status);
    if (filters?.featured !== undefined) params.append('featured', String(filters.featured));
    if (filters?.children !== undefined && filters.children > 0) params.append('children', String(filters.children));
    
    const query = params.toString() ? `?${params.toString()}` : '';
    return this.request(`/rooms${query}`);
  }

  async getRoom(id: number) {
    return this.request(`/rooms/${id}`);
  }

  async getRoomPackages(roomId: number) {
    return this.request(`/rooms/${roomId}/packages`);
  }

  async getRoomReviews(roomId: number) {
    return this.request(`/rooms/${roomId}/reviews`);
  }

  async getBookings() {
    return this.request('/bookings');
  }

  async createBooking(booking: {
    room_id: number;
    check_in: string;
    check_out: string;
    package_id?: number;
  }) {
    return this.request('/bookings', {
      method: 'POST',
      body: JSON.stringify(booking),
    });
  }

  async cancelBooking(bookingId: string) {
    return this.request(`/bookings/${bookingId}/cancel`, {
      method: 'POST',
    });
  }

  async getAllBookings() {
    return this.request('/bookings/all');
  }

  async updateBookingStatus(bookingId: string, status: string) {
    return this.request(`/bookings/${bookingId}`, {
      method: 'PUT',
      body: JSON.stringify({ status }),
    });
  }

  async getAmenities() {
    return this.request('/amenities');
  }
}

export const api = new ApiService();
