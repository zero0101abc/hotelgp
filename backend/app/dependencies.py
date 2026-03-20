from typing import Optional
from fastapi import Depends, HTTPException, status, Request as FastAPIRequest
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.session import get_current_session

def get_current_user_from_session(
    request: FastAPIRequest,
    db: Session = Depends(get_db)
) -> User:
    session_data = get_current_session(request)
    user_id = session_data.get('user_id')
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


def get_current_user(
    db: Session = Depends(get_db),
    request: FastAPIRequest = None
) -> User:
    return get_current_user_from_session(request, db)


def get_current_staff(
    current_user: User = Depends(get_current_user_from_session)
) -> User:
    role_value = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if role_value != 'staff':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
