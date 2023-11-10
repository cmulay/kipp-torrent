from session import Session
from torrent_info import TorrentInfo
from downloader import Downloader
import libtorrent as lt


class TorrentDownloader:
    def __init__(self, file_path=None, magnet_link=None, save_path=None):
        self._file_path = file_path
        self._magnet_link = magnet_link
        self._save_path = save_path
        self._downloader = None
        self._torrent_info = None
        self._lt = lt
        self._file = None
        self._add_torrent_params = None
        self._session = Session(self._lt)

    def start_download(self):
        if self._magnet_link:
            self._add_torrent_params = self._lt.parse_magnet_uri(self._magnet_link)
            self._add_torrent_params.save_path = self._save_path
            self._downloader = Downloader(session=self._session(), torrent_info=self._add_torrent_params,
                                          save_path=self._save_path, libtorrent=lt, is_magnet=True)
        elif self._file_path:
            self._torrent_info = TorrentInfo(self._file_path, self._lt)
            self._downloader = Downloader(session=self._session(), torrent_info=self._torrent_info(),
                                          save_path=self._save_path, libtorrent=None, is_magnet=False)
        else:
            print("Error: You must provide either --file or --magnet argument.")
            return

        self._file = self._downloader
        self._file.download()
