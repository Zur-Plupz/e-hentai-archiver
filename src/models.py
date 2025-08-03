from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Torrent(BaseModel):
    gallery_id: int
    hash: str
    name: str
    size: str
    id: Optional[int] = None
    seeds: Optional[int] = None
    peers: Optional[int] = None
    completed: int = 0
    downloads: int = 0
    posted_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Gallery(BaseModel):
    title: str
    gid: int
    token: str
    id: int|None = None
    credits: Optional[int] = None
    gp: Optional[int] = None
    favorited: Optional[datetime] = None
    archived: bool = False
    archive_path: Optional[str] = None
    archiver_key: Optional[str] = None
    category: Optional[str] = None
    thumb: Optional[str] = None
    uploader: Optional[str] = None
    posted: Optional[int] = None
    filecount: Optional[int] = None
    filesize: Optional[int] = None
    expunged: Optional[int] = 0
    rating: Optional[str] = None
    torrentcount: Optional[int] = None
    tags: list['Tag'] = Field(default_factory=list) # type: ignore
    torrents: list[Torrent] = Field(default_factory=list) # type: ignore
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Tag(BaseModel):
    namespace: str
    name: str
    id: int|None = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_string(cls, tag: str):
        parts = tag.split(':')

        if len(parts) != 2:
            raise ValueError('Invalid tag format')
        
        return cls(namespace=parts[0], name=parts[1])


class Group(BaseModel):
    id: int
    name: str
    galleries: list[Gallery] = Field(default_factory=list) # type: ignore
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CreditLog(BaseModel):
    id: int
    user_id: int
    credits: int
    reason: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
