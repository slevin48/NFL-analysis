#!/usr/bin/env python3
"""Download clutch NFL play-by-play data using nfl_data_py."""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
from typing import Iterable, List

import pandas as pd
from nfl_data_py import import_pbp_data


def determine_seasons(today: dt.date | None = None, *, span: int = 25) -> List[int]:
    """Return the list of seasons to download.

    nfl_data_py labels play-by-play data by season year. When the current date is
    within the first few months of the calendar year, the prior season is still the
    most recent completed one. To avoid requesting a season that is still in
    progress (and possibly unavailable), this helper only includes the current year
    if we are in or after March.
    """

    if today is None:
        today = dt.date.today()

    end_year = today.year if today.month >= 3 else today.year - 1
    start_year = end_year - span + 1
    return list(range(start_year, end_year + 1))


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Download the last 25 seasons of NFL play-by-play data using nfl_data_py. "
            "Only clutch plays—defined as those within a one-score margin during the "
            "final half of the fourth quarter or any overtime period—are retained."
        )
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=pathlib.Path("data/pbp_last_25_seasons_clutch.parquet"),
        help=(
            "Path to write the downloaded data. The format is inferred from the file "
            "extension; supported extensions are .parquet and .csv. (default: %(default)s)"
        ),
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable nfl_data_py caching when fetching play-by-play data.",
    )
    parser.add_argument(
        "--span",
        type=int,
        default=25,
        help="Number of seasons to include counting backwards from the most recent.",
    )
    return parser.parse_args(argv)


CLUTCH_SCORE_MARGIN = 7.5
FOURTH_QUARTER = 4
HALF_QUARTER_SECONDS = 450


def filter_clutch_plays(pbp: pd.DataFrame) -> pd.DataFrame:
    """Return only the plays that meet the "clutch" criteria."""

    required_columns = {"score_differential", "qtr", "quarter_seconds_remaining"}
    missing_columns = required_columns - set(pbp.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise KeyError(f"Play-by-play data is missing required columns: {missing}")

    score_close = pbp["score_differential"].abs() <= CLUTCH_SCORE_MARGIN
    last_half_fourth = (pbp["qtr"] == FOURTH_QUARTER) & (
        pbp["quarter_seconds_remaining"] <= HALF_QUARTER_SECONDS
    )
    overtime = pbp["qtr"] >= FOURTH_QUARTER + 1
    clutch_mask = score_close & (last_half_fourth | overtime)
    return pbp.loc[clutch_mask].copy()


def download_play_by_play(output_path: pathlib.Path, seasons: Iterable[int], *, use_cache: bool = True) -> None:
    """Download play-by-play data for the requested seasons and write it to disk."""
    seasons = list(seasons)
    if not seasons:
        raise ValueError("At least one season must be requested")

    print(f"Requesting play-by-play data for seasons: {seasons[0]}-{seasons[-1]}")

    pbp = import_pbp_data(seasons=seasons, downcast=False, cache=use_cache)
    print(f"Fetched {len(pbp):,} rows across {pbp['season'].nunique()} seasons")

    pbp = filter_clutch_plays(pbp)
    print(f"Filtered to {len(pbp):,} clutch plays")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix.lower() == ".parquet":
        pbp.to_parquet(output_path, index=False)
    elif output_path.suffix.lower() == ".csv":
        pbp.to_csv(output_path, index=False)
    else:
        raise ValueError("Unsupported output format. Use a .parquet or .csv extension.")

    print(f"Saved play-by-play data to {output_path.resolve()}")


def main(argv: Iterable[str] | None = None) -> None:
    args = parse_args(argv)
    seasons = determine_seasons(span=args.span)
    download_play_by_play(args.output, seasons, use_cache=not args.no_cache)


if __name__ == "__main__":
    main()
