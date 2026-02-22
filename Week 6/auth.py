import os
import requests
from jose import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
ALGORITHMS = [os.getenv("AUTH0_ALGORITHMS", "RS256")]


security = HTTPBearer()
_jwks_cache = None

def _get_jwks():
    global _jwks_cache
    if _jwks_cache is None:
        _jwks_cache = requests.get(
            f"https://{AUTH0_DOMAIN}/.well-known/jwks.json",
            timeout=10
        ).json()
    return _jwks_cache

def require_auth(creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials

    jwks = _get_jwks()
    header = jwt.get_unverified_header(token)

    key = next((k for k in jwks["keys"] if k["kid"] == header["kid"]), None)
    if not key:
        raise HTTPException(status_code=401, detail="Invalid token (kid)")

    try:
        return jwt.decode(
            token,
            key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/",
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
