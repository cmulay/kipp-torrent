# Kipp-Torrent

Kipp-Torrent is a command-line torrent client developed in Python, based on the libtorrent library. It allows users to download torrents either from a file or a magnet link.

## Features

- Download torrents from file or magnet link
- Track download progress and display real-time statistics
- Educational and open-source

## Installation

### Prerequisites

- Python 3.10 or later
- libtorrent library

1. Clone the repository:

    ```bash
    git clone https://github.com/cmulay/kipp-torrent.git
    cd kipp-torrent
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

**Note:** This project is tested and confirmed to work on Ubuntu 22.04 LTS.

## Options
`--file`: Path to the torrent file.

`--magnet`: Magnet link for the torrent.

`--save`: Path to save the downloaded files.

## Usage

### Downloading a Torrent

To download a torrent from a file, use the following command:

  ```bash
  python main.py --file "path/to/torrent/file" --save "path/to/save/location"
  ```

To download a torrent from a magnet link, use:

  ```bash
  python main.py --magnet "magnet:url" --save "path/to/save/location"
  ```

## Contributing

Contributions are welcome! If you want to improve this project, feel free to contribute.

## License
This project is licensed under the MIT License