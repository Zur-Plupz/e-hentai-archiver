from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep
from os import path, makedirs

from collections import namedtuple

Torrent = namedtuple('Torrent', ['title', 'size', 'seeds', 'peers', 'downloads', 'uploader', 'redist_url', 'fpath'])



class SeleniumScraper:
    def __init__(self, 
                 service: Service= Service(ChromeDriverManager().install()), 
                 download_dir='./downloads',
                 headless=False
                 ):
        self.options = Options()

        self._download_dir = download_dir

        makedirs(download_dir, exist_ok=True)

        self.options.add_experimental_option('prefs', {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        if headless:
            self.options.add_argument("--headless")

        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")

        self.service = service
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def get_page_source(self, url):
        self.driver.get(url)
        return self.driver.page_source

    def find_element(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def find_elements(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located((by, value))
        )
    
    def get_gallery_torrents(self, url:str, 
                             timeout=10, 
                             include_outdated:bool=False,
                             download_torrents:bool=True
                             ) -> list[Torrent]:
        self.driver.get(url)

        wait = WebDriverWait(self.driver, timeout)

        # #torrentinfo > div > form:nth-child(3)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#torrentinfo')))

        if not include_outdated:
            # form is before => #torrentinfo > div:nth-child(1) > p if contains "Outdated Torrents:"
            outdated_torrents_element = self.driver.find_element(By.CSS_SELECTOR, '#torrentinfo > div:nth-child(1) > p')

            torrent_forms = outdated_torrents_element.find_elements(By.XPATH, './preceding-sibling::form')
        else:
            # foreach #torrentinfo > div > form:nth-child(3)
            torrent_forms = self.driver.find_elements(By.CSS_SELECTOR, '#torrentinfo > div > form')

        torrentlist :list[Torrent] = []

        for form in torrent_forms:
            # Extract torrent information
            # Example: name, size, uploader, etc.
            # You'll need to inspect the HTML structure of the torrent forms to get the correct selectors

            size_element = form.find_element(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(1) > td:nth-child(2)')

            size = size_element.text.strip().replace('Size: ', '')

            seeds_element = form.find_element(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(1) > td:nth-child(4)')

            seeds = seeds_element.text.strip().replace('Seeds: ', '')

            peers_element = form.find_element(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(1) > td:nth-child(5)')

            peers = peers_element.text.strip().replace('Peers: ', '')

            downloads_element = form.find_element(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(1) > td:nth-child(6)')

            downloads = downloads_element.text.strip().replace('Downloads: ', '')

            # table > tbody > tr:nth-child(2) > td:nth-child(1)
            uploader_element = form.find_element(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(2) > td:nth-child(1)')

            uploader = uploader_element.text.strip().replace('Uploader: ', '')

            # table > tbody > tr:nth-child(3) > td > a

            url_element = form.find_element(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(3) > td > a')

            redist_url = url_element.get_attribute('href')

            title = url_element.text.strip()

            if download_torrents:
                url_element.click()

                sleep(1)

            prefix = '{EHT PERSONALIZED TORRENT - DO NOT REDISTRIBUTE} '

            fpath = path.join(self._download_dir, prefix + title + '.torrent')

            if not path.exists(fpath):
                fpath = path.join(self._download_dir, title + '.torrent')

            data = Torrent(title, size, seeds, peers, downloads, uploader, redist_url, fpath)

            torrentlist.append(data)

        return torrentlist


    def close(self):
        self.driver.quit()
