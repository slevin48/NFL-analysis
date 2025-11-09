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

## Compute the TV Clutch Factor Leaderboard

Once the clutch dataset has been generated, aggregate quarterback performance into a
TV Clutch Factor score:

```bash
python scripts/compute_tv_clutch_factor.py --input data/pbp_last_25_seasons_clutch.parquet \
    --output data/tv_clutch_factor.parquet --top 15
```

The script expects the clutch dataset created by `download_pbp.py`. It computes, for
each quarterback, clutch passing attempts, completions, touchdowns, interceptions,
and total yards. Completion percentage, yards per attempt, touchdown rate, and
interception rate are combined through the traditional NFL passer rating formula.
The resulting rating is scaled by `1 + log1p(clutch_attempts)` to account for volume,
yielding the **TV Clutch Factor**. Scores are then ranked from highest to lowest.
