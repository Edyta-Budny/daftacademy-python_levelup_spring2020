import aiosqlite
from fastapi import APIRouter, Response, status
from pydantic import BaseModel


class Album(BaseModel):
    title: str
    artist_id: int


class Customer(BaseModel):
    company: str = None
    address: str = None
    city: str = None
    state: str = None
    country: str = None
    postalcode: str = None
    fax: str = None


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


@router.get("/tracks/composers")
async def get_composer(response: Response, composer_name: str):
    router.db_connection.row_factory = lambda cursor, x: x[0]
    cursor = await router.db_connection.execute(
        "SELECT Name FROM tracks WHERE composer = ? ORDER BY Name", (composer_name,)
    )
    tracks_list = await cursor.fetchall()
    if not tracks_list:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": {"error": "No such composer was found!"}}
    return tracks_list


@router.post("/albums")
async def add_album(response: Response, album: Album, status_code=201):
    cursor = await router.db_connection.execute("SELECT ArtistId FROM artists WHERE ArtistId = ?",
                                                (album.artist_id,))
    artist_id = await cursor.fetchall()
    if not artist_id:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": {"error": "No artist found with the given artist_id!"}}
    cursor = await router.db_connection.execute(
        "INSERT INTO albums (Title, ArtistId) VALUES (?, ?)", (album.title, album.artist_id)
    )
    await router.db_connection.commit()
    response.status_code = status.HTTP_201_CREATED
    return {
        "AlbumId": cursor.lastrowid,
        "Title": album.title,
        "ArtistId": album.artist_id
    }


@router.get("/albums/{album_id}")
async def get_album(album_id: int):
    router.db_connection.row_factory = aiosqlite.Row
    cursor = await router.db_connection.execute(
        "SELECT * FROM albums WHERE AlbumId = ?", (album_id,)
    )
    album = await cursor.fetchone()
    return album


@router.put("/customers/{customer_id}")
async def update_customer(response: Response, customer_id: int, customer: Customer):
    cursor = await router.db_connection.execute(
        "SELECT CustomerId FROM customers WHERE CustomerId = ?", (customer_id, )
    )
    customer_row = await cursor.fetchone()
    if not customer_row:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": {"error": "No customer found with the given customer_id!"}}
    update_date = customer.dict(exclude_unset=True)
    if update_date:
        sql = "UPDATE customers SET "
        for key, value in update_date.items():
            if key == "postalcode":
                key = "PostalCode"
            key = key.capitalize()
            sql += f"{key} = '{value}', "
        sql = sql[:-2] + f" WHERE CustomerId = ?"
        cursor = await router.db_connection.execute(sql, (customer_id, ))
        await router.db_connection.commit()
    router.db_connection.row_factory = aiosqlite.Row
    cursor = await router.db_connection.execute(
        "SELECT * FROM customers WHERE CustomerId = ?", (customer_id, )
    )
    customer = await cursor.fetchone()
    return customer
