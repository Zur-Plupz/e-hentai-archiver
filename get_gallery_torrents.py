from src.scraping.selenium import SeleniumScraper

downloads = r'C:\Users\David\Code\python\sadpanda\downloads'
scraper = SeleniumScraper(download_dir= downloads)

torrents = scraper.get_gallery_torrents(url= 'https://e-hentai.org/gallerytorrents.php?gid=2231376&t=a7584a5932',
                                        download_torrents= False)

from json import dumps

print(dumps([t._asdict() for t in torrents], indent=4, default=str))

scraper.close()