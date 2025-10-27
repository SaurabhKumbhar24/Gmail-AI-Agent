export interface Email {
  id: string;
  from: string;
  subject: string;
  date: string;
}

export interface FullEmail extends Email {
  body: string;
  to?: string;
}

export interface ApiResponse<T = any> {
  status: number;
  message: string;
  data?: T;
}

export interface EmailListData {
  count: number;
  messages: Email[];
}

export interface AuthStatus {
  authenticated: boolean;
  message: string;
}
