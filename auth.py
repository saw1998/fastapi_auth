# auth.py
from fastapi_users.authentication import JWTStrategy, BearerTransport, AuthenticationBackend
from models import User
from typing import Dict, Any
# Remove duplicate import

SECRET = "SUPER_SECRET_CHANGE_ME"

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

# Custom JWTStrategy that adds "role" to the JWT
class RoleJWTStrategy(JWTStrategy):
    async def get_extra_claims(self, user: User) -> Dict[str, Any]:
        # This will be included in the JWT payload
        return {"role": user.role}
    
    async def write_token(self, user: User) -> str:
        # Call the parent method to generate the token with extra claims
        extra_claims = await self.get_extra_claims(user)
        
        # Create the payload manually to include the role
        from datetime import datetime, timedelta
        import jwt
        
        now = datetime.utcnow()
        expire = now + timedelta(seconds=self.lifetime_seconds or 3600)
        
        data = {
            "sub": str(user.id),
            "aud": self.token_audience,
            "exp": expire.timestamp(),
            **extra_claims  # Include the extra claims (including role)
        }
        
        return jwt.encode(data, str(self.secret), algorithm=self.algorithm)

def get_jwt_strategy() -> RoleJWTStrategy:
    return RoleJWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
