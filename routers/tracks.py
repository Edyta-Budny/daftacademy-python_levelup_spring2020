import aiosqlite
from fastapi import APIRouter

router = APIRouter()


@router.on_event("startup")
async def startup():
    router.db_connection = await aiosqlite.connect('chinook.db')
    router.db_connection.row_factory = aiosqlite.Row


@router.on_event("shutdown")
async def shutdown():
    await router.db_connection.close()


@router.get('/tracks')
async def tracks_list(page: int = 0, per_page: int = 10):
    cursor = await router.db_connection.execute(
        "SELECT * FROM tracks ORDER BY TrackId LIMIT :per_page OFFSET :per_page*:page",
        {"page": page, "per_page": per_page})
    tracks = await cursor.fetchall()
    return tracks
