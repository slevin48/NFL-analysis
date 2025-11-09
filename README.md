# NFL Play-by-Play Downloader

This repository contains a small utility script that retrieves the last 25 seasons of NFL play-by-play data using [`nfl_data_py`](https://github.com/nflverse/nfl_data_py). All columns exposed by the library are preserved in the downloaded dataset.

## Prerequisites

1. Create and activate a Python 3.10+ virtual environment.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the downloader to fetch the most recent 25 completed seasons and save them to a Parquet file:

```bash
python scripts/download_pbp.py
```

You can customize the output path (supports `.parquet` and `.csv`) or change the number of seasons:

```bash
python scripts/download_pbp.py --output data/pbp.csv --span 25
```

Set `--no-cache` if you would like to bypass the local nflverse cache when downloading.
