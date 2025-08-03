from typing import Any
from datetime import datetime

import sqlite3

from src.models import Gallery, Tag, Torrent


class GalleryFindQueryBuilder:
  def __init__(self) -> None:
    self._id :int|None = None
    self._title :str|None = None
    self._gid :int|None = None
    self._token :str|None = None
    self._credits :int|None = None
    self._gp :int|None = None
    self._favorited :str|None = None
    self._archived :int|None = None
    self._archive_path :str|None = None
    self._archiver_key :str|None = None
    self._category :str|None = None
    self._uploader :str|None = None
    self._filecount :int|None = None
    self._filesize :int|None = None
    self._expunged :bool|None = None
    self._torrentcount :int|None = None

  def with_id(self, Id:int):
    self._id = Id
    return self

  def with_title(self, title:str):
    self._title = title
    return self

  def with_gid(self, gid:int):
    self._gid = gid
    return self

  def with_token(self, token:str):
    self._token = token
    return self

  def with_credits(self, credits:int):
    self._credits = credits
    return self

  def with_gp(self, gp:int):
    self._gp = gp
    return self

  def with_favorited(self, favorited:str):
    self._favorited = favorited
    return self

  def with_archived(self, archived:int):
    self._archived = archived
    return self

  def with_archive_path(self, archive_path:str):
    self._archive_path = archive_path
    return self

  def with_archiver_key(self, archiver_key:str):
    self._archiver_key = archiver_key
    return self

  def with_category(self, category:str):
    self._category = category
    return self

  def with_uploader(self, uploader:str):
    self._uploader = uploader
    return self

  def with_filecount(self, filecount:int):
    self._filecount = filecount
    return self

  def with_filesize(self, filesize:int):
    self._filesize = filesize
    return self

  def is_expunged(self, expunged:bool):
    self._expunged = expunged
    return self

  def with_torrentcount(self, torrentcount:int):
    self._torrentcount = torrentcount
    return self
  
  def with_fields(self, map_columns_values: dict[str, Any]):
    self._id = map_columns_values.get('id', None)
    self._title = map_columns_values.get('title', None)
    self._gid = map_columns_values.get('gid', None)
    self._token = map_columns_values.get('token', None)
    self._credits = map_columns_values.get('credits', None)
    self._gp = map_columns_values.get('gp', None)
    self._favorited = map_columns_values.get('favorited', None)
    self._archived = map_columns_values.get('archived', None)
    self._archive_path = map_columns_values.get('archive_path', None)
    self._archiver_key = map_columns_values.get('archiver_key', None)
    self._category = map_columns_values.get('category', None)
    self._uploader = map_columns_values.get('uploader', None)
    self._filecount = map_columns_values.get('filecount', None)
    self._filesize = map_columns_values.get('filesize', None)
    self._expunged = map_columns_values.get('expunged', None)
    self._torrentcount = map_columns_values.get('torrentcount', None)
    return self
  
  def build(self):
    sql = 'SELECT * FROM galleries'

    map_columns_values :dict[str, Any] = {
      'id': self._id,
      'title': self._title,
      'gid': self._gid,
      'token': self._token,
      'credits': self._credits,
      'gp': self._gp,
      'favorited': self._favorited,
      'archived': self._archived,
      'archive_path': self._archive_path,
      'archiver_key': self._archiver_key,
      'category': self._category,
      'uploader': self._uploader,
      'filecount': self._filecount,
      'filesize': self._filesize,
      'expunged': self._expunged,
      'torrentcount': self._torrentcount,
    }

    wherelist :list[str] = []
    bindings :list[Any] = []

    for column, value in map_columns_values.items():
      if value is not None:
        s = f" WHERE {column} = ?"

        wherelist.append(s)

        bindings.append(value)

    sql = sql + ''.join(wherelist)

    return sql, bindings
  

def get_connection(database:str, timeout:float= 15):
  conn= sqlite3.connect(
    database= database,
    check_same_thread=False
  )

  conn.row_factory = sqlite3.Row

  return conn


def find_galleries(conn: sqlite3.Connection, builder: GalleryFindQueryBuilder):
  sql, bindings = builder.build()

  cursor = conn.cursor()
  cursor.execute(sql, bindings)  # type: ignore

  rows = cursor.fetchall() # type: ignore

  for row in rows:
    gl = Gallery(**row)

    for tag in find_gallery_tags(conn, gl.id): # type: ignore
      gl.tags.append(tag)

    for torrent in find_gallery_torrents(conn, gl.id): # type: ignore
      gl.torrents.append(torrent)

    yield gl


def add_tag(conn: sqlite3.Connection, tag: Tag) -> None:
  now = datetime.now()

  sql = """
  INSERT INTO tags (
    namespace,
    name,
    created_at
  ) VALUES (?, ?, ?)
  """

  bindings = (
    tag.namespace,
    tag.name,
    now.isoformat()
  )

  cursor = conn.cursor() # type: ignore
  cursor.execute(sql, bindings) # type: ignore

  _id = cursor.lastrowid # type: ignore

  tag.id = _id
  tag.created_at = now


def find_tag(conn: sqlite3.Connection, namespace:str, name:str):
  sql = """
  SELECT * FROM tags WHERE namespace = ? AND name = ?
  """

  bindings = (
    namespace,
    name
  )

  cursor = conn.cursor() # type: ignore
  cursor.execute(sql, bindings) # type: ignore

  row :sqlite3.Row = cursor.fetchone() # type: ignore

  return Tag(**row) if row else None


def tag_first_or_create(conn: sqlite3.Connection, namespace:str, name:str):
  tag = find_tag(conn, namespace, name)

  if not tag:
    tag = Tag(namespace=namespace, name=name)
    add_tag(conn, tag)

  return tag


def find_gallery_tags(conn: sqlite3.Connection, gallery_id:int):
  sql = """
  SELECT tag.* FROM tags tag
  INNER JOIN gallery_taggings gtag ON gtag.tag_id = tag.id
  WHERE gtag.gallery_id = ?
  """

  bindings = (
    gallery_id,
  )

  cursor= conn.cursor() # type: ignore
  cursor.execute(sql, bindings) # type: ignore

  rows = cursor.fetchall() # type: ignore

  for row in rows:
    yield Tag(**row)


def find_gallery_torrents(conn: sqlite3.Connection, gallery_id:int):
  sql = """
  SELECT * FROM torrents WHERE gallery_id = ?
  """

  bindings = (
    gallery_id,
  )

  cursor = conn.cursor()
  cursor.execute(sql, bindings)

  rows = cursor.fetchall() # type: ignore

  for row in rows:
    yield Torrent(**row) # type: ignore


def add_gallery(conn: sqlite3.Connection, gl: Gallery) -> None:
  # Check if a gallery with the given gid already exists
  sql_check_exists = "SELECT 1 FROM galleries WHERE gid = ?"
  
  cursor = conn.cursor()
  cursor.execute(sql_check_exists, (gl.gid,))
  exists = cursor.fetchone()

  if exists:
    raise ValueError(f'Gallery with gid {gl.gid} already exists.')

  now = datetime.now()

  sql = """
  INSERT INTO galleries (
    title,
    gid,
    token,
    credits,
    gp,
    favorited,
    archived,
    archive_path,
    archiver_key,
    category,
    thumb,
    uploader,
    posted,
    filecount,
    filesize,
    expunged,
    rating,
    torrentcount,
    created_at
  ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  """

  bindings = (
    gl.title,
    gl.gid,
    gl.token,
    gl.credits,
    gl.gp,
    gl.favorited,
    gl.archived,
    gl.archive_path,
    gl.archiver_key,
    gl.category,
    gl.thumb,
    gl.uploader,
    gl.posted,
    gl.filecount,
    gl.filesize,
    gl.expunged,
    gl.rating,
    gl.torrentcount,
    now.isoformat()
  )

  cursor = conn.cursor()
  cursor.execute(sql, bindings) # type: ignore

  _id = cursor.lastrowid # type: ignore

  gl.id = _id
  gl.created_at = now

  for tag in gl.tags:
    new_tag = tag_first_or_create(conn, tag.namespace, tag.name)

    sql = 'INSERT INTO gallery_taggings (gallery_id, tag_id) VALUES (?, ?)'

    bindings = (gl.id, new_tag.id) # type: ignore

    cursor.execute(sql, bindings) # type: ignore

    tag.id = new_tag.id
    tag.created_at = new_tag.created_at


def add_gallery_torrent(conn: sqlite3.Connection, torrent: Torrent) -> None:
  now = datetime.now()

  sql = """
  INSERT INTO torrents (
    gallery_id,
    hash,
    name,
    size,
    seeds,
    peers,
    downloads,
    uploader,
    redist_url,
    torrent_path,
    created_at
  ) VALUES (%s)
  """

  bindings = (
    torrent.gallery_id,
    torrent.hash,
    torrent.name,
    torrent.size,
    torrent.seeds,
    torrent.peers,
    torrent.downloads,
    torrent.uploader,
    torrent.redist_url,
    torrent.torrent_path,
    now.isoformat()
  )

  cursor = conn.cursor()

  cursor.execute(sql, bindings) # type: ignore

  _id = cursor.lastrowid # type: ignore

  torrent.id = _id
  torrent.created_at = now