import jwt
from app.config import SUPABASE_JWT_SECRET

def decode_jwt_token(token: str) -> dict:
    return jwt.decode(token, 
                      SUPABASE_JWT_SECRET, 
                      algorithms=["HS256"],  
                      audience="authenticated")