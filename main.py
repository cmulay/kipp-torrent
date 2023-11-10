import argparse
from torrent_downloader import TorrentDownloader


def parse_arguments():
    parser = argparse.ArgumentParser(description='Torrent Downloader CLI')
    parser.add_argument('--file', help='Path to the torrent file')
    parser.add_argument('--magnet', help='Magnet link for the torrent')
    parser.add_argument('--save', help='Path to save the downloaded files')
    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.file:
        downloader = TorrentDownloader(file_path=args.file, save_path=args.save)
    elif args.magnet:
        downloader = TorrentDownloader(magnet_link=args.magnet, save_path=args.save)
    else:
        print("Error: You must provide either --file or --magnet argument.")
        return

    downloader.start_download()


if __name__ == "__main__":
    main()
