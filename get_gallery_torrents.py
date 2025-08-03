from src.scraping.selenium import SeleniumScraper
from src.models import Torrent, Gallery
from src.torrents.q_bittorrent import get_client_session

from src.db.sqlite import (
  get_connection, find_galleries, add_gallery_torrent, GalleryFindQueryBuilder)


def get_gallery_torrents(base_url:str, gl: Gallery, scraper: SeleniumScraper) -> list[Torrent]:
  if not gl.id:
    raise ValueError('Gallery id is not set')

  url = base_url + '/gallerytorrents.php?gid=' + str(gl.gid) + '&t=' + gl.token

  torrents = scraper.get_gallery_torrents(url, download_torrents= True)

  new_torrents = []

  for t in torrents:
    # https://ehtracker.org/get/2043548/25198ccc3cd88393897aa5c630eb95d5ec4f695e.torrent
    _hash = t.redist_url.split('/')[-1].split('.')[0]

    new_torrents.append(Torrent(
      gallery_id= gl.id,
      hash= _hash,
      name= t.title,
      size= t.size,
      seeds= int(t.seeds),
      peers= int(t.peers),
      downloads= int(t.downloads),
      uploader= t.uploader,
      redist_url= t.redist_url,
      torrent_path= t.fpath
    ))

  return new_torrents


downloads = r'C:\Users\David\Code\python\sadpanda\downloads'
scraper = SeleniumScraper(download_dir= downloads)

builder = GalleryFindQueryBuilder()
conn = get_connection('sadpanda.db')

torrent_client = get_client_session('http://localhost:8080/', 'admin', 'adminadmin')

base_url = 'https://e-hentai.org'

for gl in find_galleries(conn, builder):
  torrents = get_gallery_torrents(base_url, gl, scraper)

  files :list[str] = []

  for t in torrents:
    add_gallery_torrent(conn, t)

    if t.torrent_path:
      files.append(t.torrent_path)

  scraper.close()

  torrent_client.torrents_add(torrent_files= files,
                              save_path= downloads)