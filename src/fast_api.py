from src.db.sqlite import (
  get_connection, find_galleries, GalleryFindQueryBuilder, add_gallery
  )

from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List
import sqlite3

from src.models import Gallery, Tag, Torrent

from src.sadpanda_client import (
    Client as SadpandaClient, GalleryDataRequest, GalleryMetadataResponse, GalleryMetadata,
    Torrent as SadpandaTorrent
    )


from contextlib import asynccontextmanager

DATABASE_URL = "sadpanda.db"

db : sqlite3.Connection = None # type: ignore
sadpanda_client : SadpandaClient = None # type: ignore

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db, sadpanda_client

    db = get_connection(DATABASE_URL)
    sadpanda_client = SadpandaClient()
    yield
    db.close()


app = FastAPI(lifespan=lifespan)


class GalleryFromUrlRequest(BaseModel):
    url: str


@app.post('/galleries/from_url', response_model=Gallery, status_code=status.HTTP_201_CREATED)
def create_gallery_from_url(request: GalleryFromUrlRequest):
    gdata_request = GalleryDataRequest.from_gallery_url(request.url)

    gdata_response = sadpanda_client.get_gallery_metadata(gdata_request)

    gdata = next(iter(gdata_response.gmetadata), None)

    if not gdata:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gallery not found")
    
    torrents : list[Torrent] = []

    gallery = Gallery(
        title= gdata.title,
        gid= gdata.gid,
        token= gdata.token,
        archiver_key= gdata.archiver_key,
        category= gdata.category.value,
        thumb= gdata.thumb,
        uploader= gdata.uploader,
        posted= int(gdata.posted),
        filecount= int(gdata.filecount),
        filesize= int(gdata.filesize),
        expunged= gdata.expunged,
        rating= gdata.rating,
        torrentcount= int(gdata.torrentcount),
        torrents= torrents,
        tags= [Tag.from_string(tag) for tag in gdata.tags]
    )

    add_gallery(db, gallery)

    db.commit()

    return gallery


@app.post("/galleries", response_model=Gallery, status_code=status.HTTP_201_CREATED)
def create_gallery(gallery: Gallery):
    try:
        add_gallery(db, gallery)
        db.commit()
        return gallery
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/galleries", response_model=List[Gallery])
def read_galleries(
    gallery_id: int|None = None,
    title: str|None = None,
    gid: int|None = None,
    token: str|None = None
):
    builder = GalleryFindQueryBuilder()
    if gallery_id:
        builder.with_id(gallery_id)
    if title:
        builder.with_title(title)
    if gid:
        builder.with_gid(gid)
    if token:
        builder.with_token(token)

    galleries = list(find_galleries(db, builder))
    if not galleries:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Galleries not found")
    return galleries
