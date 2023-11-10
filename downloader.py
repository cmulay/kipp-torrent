import sys
import time
import logging
import libtorrent
from termcolor import colored


class Downloader:
    HEADER = 'Kipp-Torrent V1.0'
    DISCLAIMER = 'Developed for Educational Purpose Only'
    SIZE_CONVERT = 1024 * 1024 * 1024

    def __init__(self, session, torrent_info, save_path, libtorrent, is_magnet):
        self._session = session
        self._torrent_info = torrent_info
        self._save_path = save_path
        self._file = None
        self._status = None
        self._name = ''
        self._state = ''
        self._lt = libtorrent
        self._add_torrent_params = None
        self._is_magnet = is_magnet
        self._logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def print_header(self):
        self._logger.info(colored(f'{self.HEADER}', 'yellow'))
        self._logger.info(colored(f'{self.DISCLAIMER}', 'yellow'))

    def display_progress(self):
        try:
            while not self._status.is_seeding:
                s = self.status()

                if not self._is_magnet:
                    total_size = self._torrent_info.total_size() / self.SIZE_CONVERT
                else:
                    total_size = s.total_wanted / self.SIZE_CONVERT if s.total_wanted > 0 else 0

                progress = s.progress * 100
                download_speed = s.download_rate / 1000
                upload_speed = s.upload_rate / 1000
                connected_peers = s.num_peers
                download_state = s.state

                sys.stdout.write(
                    f'\r[{"=" * int(progress / 2)}{" " * (50 - int(progress / 2))}] '
                    f'{progress:.2f}% Completed ({total_size:.2f} GB, '
                    f'{colored("Down Speed:", "yellow")} {download_speed:.1f} kB/s, '
                    f'{colored("Up Speed:", "yellow")} {upload_speed:.1f} kB/s, '
                    f'{colored("Connected Peers:", "yellow")} {connected_peers}, '
                    f'{colored("State:", "yellow")} {download_state}'
                )
                sys.stdout.flush()

                time.sleep(1)
        except (RuntimeError, libtorrent.error) as e:
            self._logger.error(f"An error occurred during download: {e}")

    def print_completion_message(self):
        self._logger.info('\nDownload complete for: ' + colored(self.name, 'green'))

    def status(self):
        try:
            if not self._is_magnet:
                self._file = self._session.add_torrent({'ti': self._torrent_info, 'save_path': f'{self._save_path}'})
                self._status = self._file.status()
            else:
                self._add_torrent_params = self._torrent_info
                self._add_torrent_params.save_path = self._save_path
                self._file = self._session.add_torrent(self._add_torrent_params)
                self._status = self._file.status()
            return self._status
        except (RuntimeError, libtorrent.error) as e:
            self._logger.error(f"An error occurred while getting torrent status: {e}")
            raise

    @property
    def name(self):
        try:
            self._name = self.status().name
            return self._name
        except (RuntimeError, libtorrent.error) as e:
            self._logger.error(f"An error occurred while getting torrent name: {e}")
            return "Unknown"

    def download(self):
        self.print_header()

        confirmation = input("Press Enter to start the download or 'Q' to quit: ")
        if confirmation.lower() == 'q':
            self._logger.info("Download aborted.")
            return

        try:
            self._logger.info(f'\nNow Downloading: {colored(self.name, "cyan")}')
            self.display_progress()
            self.print_completion_message()
        except (RuntimeError, libtorrent.error) as e:
            self._logger.error(f"An error occurred during download: {e}")