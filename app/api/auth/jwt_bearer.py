from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from app.api.auth.jwt_handler import decodeJWT

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid or Expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid or Expired token")
            
    
    def verify_jwt(self, jwttoken: str):
        isTokenValid: bool = False
        payload = decodeJWT(jwttoken)
        if payload:
            isTokenValid = True
        return isTokenValid
