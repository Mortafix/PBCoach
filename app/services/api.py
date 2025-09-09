from os import getenv, path
from shutil import copyfile

from app.database.players import get_all_players
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

load_dotenv()

security = HTTPBearer()


class EndpointException(Exception):
    ...


# ---- security


async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != getenv("endpoint-token"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token non valido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


# ---- endpoints


async def test_token(token: str = Depends(verify_token)):
    return {"response": "Ok, authenticated."}


async def update_players_avatar(token: str = Depends(verify_token)):
    count = 0
    for player in get_all_players(parse=True):
        if path.exists(f"assets/players/{player.id}.jpg"):
            continue
        avatar_filename = "N-0.jpg"
        if player.gender and player.gender != "Non specificato":
            avatar_filename = f"{player.gender[0]}-{player.id % 3}.jpg"
        copyfile(
            f"assets/images/avatars/{avatar_filename}",
            f"assets/players/{player.id}.jpg",
        )
        count += 1
    for i in range(1, 5):
        copyfile("assets/images/avatars/U-0.jpg", f"assets/players/-{i}.jpg")
    return {"response": f"Ok, updated {count} players avatar."}
