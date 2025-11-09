# NFL Play-by-Play Downloader

This repository contains a small utility script that retrieves the last 25 seasons of NFL play-by-play data using [`nfl_data_py`](https://github.com/nflverse/nfl_data_py). The script filters the results to **clutch** plays, defined as snaps where:

- The score differential is within 7.5 points (one possession), and
- The play occurs in the final 7.5 minutes of the fourth quarter or during any overtime period.

All columns exposed by the library are preserved for the remaining plays.

## Prerequisites

1. Create and activate a Python 3.10+ virtual environment.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the downloader to fetch the most recent 25 completed seasons and save the clutch plays to a Parquet file:

```bash
python scripts/download_pbp.py
```

You can customize the output path (supports `.parquet` and `.csv`) or change the number of seasons:

```bash
python scripts/download_pbp.py --output data/pbp.csv --span 25
```

Set `--no-cache` if you would like to bypass the local nflverse cache when downloading.
