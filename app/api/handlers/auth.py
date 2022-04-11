from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordRequestForm
from core.auth import Token, create_access_token
from database.models.user import User
from core.utils import get_db_session
from sqlalchemy.orm import Session
from core.config import settings
from datetime import timedelta
import api.service as service

router = APIRouter()


@router.post("/", response_model=Token)
def authenticate_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_session),
):
    user = service.user.authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    scopes = []
    for role in user.roles:
        for permission in role.permissions:
            scopes.append(permission.name)
    
    access_token = create_access_token(
        data={"sub": user.email, "scopes": scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
