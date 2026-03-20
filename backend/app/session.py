import os
import json
import uuid
from datetime import datetime, timedelta
from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi import Request as FastAPIRequest
from app.config import settings

COOKIES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'cookies')
os.makedirs(COOKIES_DIR, exist_ok=True)

SESSION_FILE_MAX_AGE = settings.SESSION_COOKIE_MAX_AGE


class SessionManager:
    def __init__(self):
        self.sessions = {}
    
    def _get_session_file(self, session_id: str) -> str:
        return os.path.join(COOKIES_DIR, f"{session_id}.json")
    
    def _load_session(self, session_id: str) -> dict:
        session_file = self._get_session_file(session_id)
        if os.path.exists(session_file):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if 'created_at' in data:
                    created = datetime.fromisoformat(data['created_at'])
                    if (datetime.now() - created).total_seconds() > SESSION_FILE_MAX_AGE:
                        os.remove(session_file)
                        return {}
                return data
            except (json.JSONDecodeError, KeyError):
                return {}
        return {}
    
    def _save_session(self, session_id: str, data: dict) -> None:
        data['created_at'] = datetime.now().isoformat()
        session_file = self._get_session_file(session_id)
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    
    def _delete_session(self, session_id: str) -> None:
        session_file = self._get_session_file(session_id)
        if os.path.exists(session_file):
            os.remove(session_file)
    
    def get_session(self, session_id: str) -> dict:
        return self._load_session(session_id)
    
    def set_session(self, session_id: str, data: dict) -> None:
        self._save_session(session_id, data)
    
    def delete_session(self, session_id: str) -> None:
        self._delete_session(session_id)
    
    def cleanup_expired_sessions(self) -> None:
        now = datetime.now()
        for filename in os.listdir(COOKIES_DIR):
            if filename.endswith('.json'):
                filepath = os.path.join(COOKIES_DIR, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    if 'created_at' in data:
                        created = datetime.fromisoformat(data['created_at'])
                        if (now - created).total_seconds() > SESSION_FILE_MAX_AGE:
                            os.remove(filepath)
                except (json.JSONDecodeError, KeyError, ValueError):
                    pass


session_manager = SessionManager()


def get_session_id(request: FastAPIRequest) -> Optional[str]:
    return request.cookies.get(settings.SESSION_COOKIE_NAME)


def get_current_session(request: FastAPIRequest) -> dict:
    session_id = get_session_id(request)
    if session_id:
        return session_manager.get_session(session_id)
    return {}


def create_session(response: Response, user_id: int, user_data: dict) -> str:
    session_id = str(uuid.uuid4())
    session_data = {
        'user_id': user_id,
        'email': user_data.get('email'),
        'name': user_data.get('name'),
        'role': user_data.get('role', 'customer'),
    }
    session_manager.set_session(session_id, session_data)
    
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=session_id,
        max_age=settings.SESSION_COOKIE_MAX_AGE,
        httponly=True,
        samesite='lax',
        path='/'
    )
    return session_id


def destroy_session(response: Response, request: FastAPIRequest) -> None:
    session_id = get_session_id(request)
    if session_id:
        session_manager.delete_session(session_id)
    
    response.delete_cookie(
        key=settings.SESSION_COOKIE_NAME,
        path='/'
    )
