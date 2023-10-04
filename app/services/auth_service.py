import os

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

load_dotenv()

security = HTTPBearer()

ENV = os.environ.get("ENV", "dev")
SUPABASE_JWT_SECRET = os.environ.get("SUPABASE_JWT_SECRET", "")


class AuthService:
    @staticmethod
    def decode_token(token: str) -> dict:
        print("decoding token")
        if ENV == "dev":
            return {"sub": "mock_user_id"}

        try:
            payload = jwt.decode(
                token,
                SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                audience="authenticated",
            )
            return payload
        except Exception:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )

    @staticmethod
    def get_current_user(
        authorization: HTTPAuthorizationCredentials = Depends(security),
    ):
        print("calling get_current_user")
        payload = AuthService.decode_token(authorization.credentials)
        return payload

    @staticmethod
    def authorize_user(payload: dict, user_id: str):
        if ENV == "dev":
            return

        if payload.get("sub") != user_id:  # Assuming 'sub' is user_id in the JWT token
            raise HTTPException(status_code=403, detail="Not authorized")
