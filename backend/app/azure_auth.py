"""Validate Entra OAuth access tokens against tenant JWKS; never trust client-provided user ids."""
from functools import lru_cache
import jwt
from jwt import PyJWKClient
from app.services.cases import CaseError

@lru_cache(maxsize=16)
def jwks_client(tenant):
    return PyJWKClient(f'https://login.microsoftonline.com/{tenant}/discovery/v2.0/keys',cache_jwk_set=True,lifespan=300)

def validate_access_token(token,tenant,audience):
    try:
        header=jwt.get_unverified_header(token)
        if header.get('alg')!='RS256':raise ValueError()
        key=jwks_client(tenant).get_signing_key_from_jwt(token).key
        claims=jwt.decode(token,key,algorithms=['RS256'],audience=audience,
            issuer=f'https://login.microsoftonline.com/{tenant}/v2.0',options={'require':['exp','iat','aud','iss','sub']})
        if not claims.get('scp') or 'review' not in claims['scp'].split():raise ValueError()
        return claims['sub']
    except Exception:raise CaseError('Sign in required.',401) from None
