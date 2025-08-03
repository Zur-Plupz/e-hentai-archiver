from pydantic import BaseModel, Field
from typing import List, Tuple, Optional, Literal, Any
from enum import StrEnum
import requests 

from src.logger import logger

class GalleryDataRequest(BaseModel):
    '''
    {
      "method": "gdata",
      "gidlist": [
          [2231376,"a7584a5932"]
      ],
      "namespace": 1
    }
    '''
    method: Literal['gdata'] = 'gdata'
    gidlist: List[Tuple[int, str]] = Field(default_factory=list) # type: ignore
    namespace: Optional[int] = 1

    @classmethod
    def from_gallery_url(cls, url:str, method: Literal['gdata']='gdata'):
        parts = url.strip().strip('/').split('/')

        gallery_token :str = parts[-1]
        gallery_id = int(parts[-2])

        return cls(
            method= method,
            gidlist= [(gallery_id, gallery_token)]
        )
    
    def add_gallery_url(self, url:str, method: Literal['gdata']='gdata'):
        if len(self.gidlist) >= 25:
            raise RuntimeError('only 25 entries per request')

        parts = url.strip().strip('/').split('/')

        gallery_token :str = parts[-1]
        gallery_id = int(parts[-2])

        self.gidlist.append((gallery_id, gallery_token))


class Torrent(BaseModel):
    hash: str
    added: str
    name: str
    tsize: str
    fsize: str


class Category(StrEnum):
    Doujinshi = "Doujinshi"
    Manga = "Manga"
    ArtistCG = "Artist CG"
    GameCG = "Game CG"
    Western = "Western"
    ImageSet = "Image Set"
    NonH = "Non-H"
    Cosplay = "Cosplay"
    AsianPorn = "Asian Porn"
    Misc = "Misc"
    Private = "Private"


class GalleryMetadata(BaseModel):
    gid: int
    token: str
    title: str
    title_jpn: str
    category: Category
    thumb: str
    uploader: str
    posted: str
    filecount: str
    filesize: int
    expunged: bool
    rating: str
    torrentcount: str
    torrents: List[Torrent]
    tags: List[str]
    archiver_key: Optional[str] = None
    parent_gid: Optional[str] = None
    parent_key: Optional[str] = None
    first_gid: Optional[str] = None
    first_key: Optional[str] = None
    last_gid: Optional[str] = None
    last_key: Optional[str] = None



class GalleryMetadataResponse(BaseModel):
    gmetadata: List[GalleryMetadata]


class GalleryMetadataError(BaseModel):
    gid: str
    error: str


class Client:
    def __init__(self, url:str= 'https://api.e-hentai.org/api.php') -> None:
        self._URL = url

    def get_gallery_metadata(self, req: GalleryDataRequest):
        r = requests.post(url= self._URL, json= req.model_dump(mode='json'))

        r.raise_for_status()

        logger.debug(r.text)

        data = r.json()

        gmedatalist :list[dict[str, Any]] = data['gmetadata']

        response = GalleryMetadataResponse(gmetadata=[])

        for gmjson in gmedatalist:
            gm = GalleryMetadata.model_validate(gmjson)

            response.gmetadata.append(gm)

        return response

