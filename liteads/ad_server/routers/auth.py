"""Demo authentication endpoint until persistent user accounts are introduced."""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=1)


class LoginUser(BaseModel):
    id: str
    name: str
    email: str
    role: str


class LoginResponse(BaseModel):
    user: LoginUser
    token: str


_DEMO_USERS = {
    "admin@openadserver.dev": ("admin123", LoginUser(id="usr_admin", name="Platform Admin", email="admin@openadserver.dev", role="admin"), "demo-token-admin"),
    "advertiser@openadserver.dev": ("ad1234", LoginUser(id="usr_adv", name="Demo Advertiser", email="advertiser@openadserver.dev", role="advertiser"), "demo-token-advertiser"),
    "publisher@openadserver.dev": ("pub1234", LoginUser(id="usr_pub", name="Demo Publisher", email="publisher@openadserver.dev", role="publisher"), "demo-token-publisher"),
}


@router.post("/auth/login", response_model=LoginResponse)
async def login(payload: LoginRequest) -> LoginResponse:
    """Authenticate the documented demo users.

    Replace this credential store with persistent password hashes and JWTs when
    the platform user model is introduced.
    """
    record = _DEMO_USERS.get(payload.email.strip().lower())
    if record is None or record[0] != payload.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return LoginResponse(user=record[1], token=record[2])
