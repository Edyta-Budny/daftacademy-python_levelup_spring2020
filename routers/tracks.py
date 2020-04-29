import aiosqlite
from fastapi import APIRouter, Response, status

router = APIRouter()


@router.on_event("startup")
async def startup():
    router.db_connection = await aiosqlite.connect('chinook.db')


@router.on_event("shutdown")
async def shutdown():
    await router.db_connection.close()


@router.get("/tracks")
async def get_tracks(page: int = 0, per_page: int = 10):
    router.db_connection.row_factory = aiosqlite.Row
    cursor = await router.db_connection.execute(
        "SELECT * FROM tracks ORDER BY TrackId LIMIT :per_page OFFSET :per_page*:page",
        {"page": page, "per_page": per_page})
    tracks = await cursor.fetchall()
    return tracks


@router.get("/tracks/composers/")
async def get_composer(response: Response, composer_name: str):
    router.db_connection.row_factory = lambda cursor, x: x[0]
    cursor = await router.db_connection.execute(
        "SELECT Name FROM tracks WHERE composer = ? ORDER BY Name",
        (composer_name, ))
    tracks_list = await cursor.fetchall()
    if not tracks_list:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": {"error": "No such composer was found!"}}
    return tracks_list
