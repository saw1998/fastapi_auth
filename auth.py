# auth.py
from fastapi_users.authentication import JWTStrategy, BearerTransport, AuthenticationBackend
from models import User
from typing import Dict, Any
from fastapi_users.jwt import generate_jwt
# Remove duplicate import

SECRET = "SUPER_SECRET_CHANGE_ME"

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

# Custom JWTStrategy that adds "role" to the JWT
class RoleJWTStrategy(JWTStrategy):
    
    async def write_token(self, user: User) -> str:
        data = {"sub" : str(user.id), "aud":self.token_audience, "role" : user.role, "email" : user.email}
        return generate_jwt(
            data, self.encode_key, self.lifetime_seconds, algorithm=self.algorithm
        )

def get_jwt_strategy() -> RoleJWTStrategy:
    return RoleJWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
