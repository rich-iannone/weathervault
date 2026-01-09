#!/usr/bin/env python
"""Download sample data for documentation examples.

This script downloads weather data files that are bundled with the package
to enable documentation examples to run without network access.

Buffer years (±1) are included because when converting to local time,
data from adjacent years may be needed to ensure complete coverage at
year boundaries.

Usage:
    python scripts/download_sample_data.py
"""

from pathlib import Path

import httpx

BASE_URL = "https://www.ncei.noaa.gov/pub/data/noaa"

# Stations and years used in documentation examples
# Format: (station_id, [years]) - buffer years (±1) are automatically added
EXAMPLE_STATIONS = [
    ("744860-94789", [2023]),  # JFK Airport (get_weather_data basic example)
    ("725030-14732", [2022, 2023]),  # LaGuardia Airport (multi-year, cache, incl_stn_info)
    ("724050-13743", [2023]),  # Washington Reagan Airport (make_hourly example)
]


def _get_years_with_buffers(years: list[int]) -> list[int]:
    """Add buffer years (±1) to handle timezone conversion at year boundaries."""
    all_years = set(years)
    for year in years:
        all_years.add(year - 1)
        all_years.add(year + 1)
    return sorted(all_years)


def download_sample_data():
    """Download sample data files to the package data directory."""
    data_dir = Path(__file__).parent.parent / "weathervault" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Build full list with buffer years
    sample_data = []
    for station_id, years in EXAMPLE_STATIONS:
        for year in _get_years_with_buffers(years):
            sample_data.append((station_id, year))

    print(f"Downloading sample data to: {data_dir}")
    print("(includes buffer years for timezone handling)")
    print()

    with httpx.Client(timeout=120.0, follow_redirects=True) as client:
        for station_id, year in sample_data:
            filename = f"{station_id}-{year}.gz"
            filepath = data_dir / filename
            url = f"{BASE_URL}/{year}/{filename}"

            if filepath.exists():
                print(f"  ✓ {filename} (already exists)")
                continue

            print(f"  ↓ Downloading {filename}...", end=" ", flush=True)
            try:
                response = client.get(url)
                response.raise_for_status()
                filepath.write_bytes(response.content)
                size_kb = len(response.content) / 1024
                print(f"({size_kb:.1f} KB)")
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    print("(not available - OK for buffer year)")
                else:
                    print(f"FAILED: {e}")
            except httpx.HTTPError as e:
                print(f"FAILED: {e}")

    print()
    print("Done! Sample data is ready for documentation builds.")


if __name__ == "__main__":
    download_sample_data()
