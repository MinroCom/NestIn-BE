from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import decodeJWT


class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error : bool = True):
        super(jwtBearer, self).__init__(auto_eror=auto_Error)
        
        async def __call__(seld, request : Request):
            credentials : HTTPAuthorizationCredentials = await super(jwtBearer, seld).__call__(request)
            if credentials:
                if not credentials.schema == "Bearer":
                    raise HTTPException(status_code = 403, details = "Invalid or Expired Token!")
                return credentials.credentials
            else:
                raise HTTPException(status_code = 403, details = "Invalid or Expired Token!")
    def verify_jwt(self, jwtoken : str):
        
        isTokenValid : bool = False
        payload = decodeJWT(jwtoken)
        if payload:
            isTokenValid = True
        return isTokenValid