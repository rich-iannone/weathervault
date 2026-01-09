# weathervault

[![Tests](https://github.com/rich-iannone/weathervault/actions/workflows/tests.yml/badge.svg)](https://github.com/rich-iannone/weathervault/actions/workflows/tests.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/weathervault.svg)](https://pypi.org/project/weathervault/)

Obtain Polars DataFrames of historical weather data from NOAA's National Centers for Environmental Information (NCEI) Integrated Surface Database (ISD).

## Features

- download and decode weather station data with a simple API
- get data as efficient Polars DataFrames ready for analysis
- locate met stations by name, location, and elevation
- automatic conversion from UTC to local station time
- support different temperature units (Celsius, Fahrenheit, and Kelvin)
- optional local data file caching with automatic cache detection
- access to the global ISD network of weather stations (29,000+ stations)

## Installation

```bash
pip install weathervault
```

## Quick Start

```python
import weathervault as wv

# Get weather data for LaGuardia Airport (New York) for 2024
weather = wv.get_weather_data("725030-14732", years=2024)

weather.head()
```

Output:
```
shape: (5, 10)
┌──────────────┬─────────────────────────┬───────┬───────────┬───────┬─────┬──────┬────────────┬──────────┬────────────┐
│ id           ┆ time                    ┆ temp  ┆ dew_point ┆ rh    ┆ wd  ┆ ws   ┆ atmos_pres ┆ ceil_hgt ┆ visibility │
│ ---          ┆ ---                     ┆ ---   ┆ ---       ┆ ---   ┆ --- ┆ ---  ┆ ---        ┆ ---      ┆ ---        │
│ str          ┆ datetime[μs, tz]        ┆ f64   ┆ f64       ┆ f64   ┆ i32 ┆ f64  ┆ f64        ┆ i32      ┆ i32        │
╞══════════════╪═════════════════════════╪═══════╪═══════════╪═══════╪═════╪══════╪════════════╪══════════╪════════════╡
│ 725030-14732 ┆ 2024-01-01 00:51:00 EST ┆ 12.8  ┆ 7.8       ┆ 72.1  ┆ 200 ┆ 4.6  ┆ 1016.9     ┆ 2438     ┆ 16093      │
│ 725030-14732 ┆ 2024-01-01 01:51:00 EST ┆ 12.2  ┆ 7.2       ┆ 71.8  ┆ 190 ┆ 5.1  ┆ 1016.5     ┆ 2743     ┆ 16093      │
│ ...          ┆ ...                     ┆ ...   ┆ ...       ┆ ...   ┆ ... ┆ ...  ┆ ...        ┆ ...      ┆ ...        │
└──────────────┴─────────────────────────┴───────┴───────────┴───────┴─────┴──────┴────────────┴──────────┴────────────┘
```

## Finding Weather Stations

### Convenient Shorthand Syntax

Use `wv.country` and `wv.state` for clean, readable code with IDE autocomplete:

```python
# Search by country using convenient shorthand
de_stations = wv.search_stations(country_code=wv.country.DE)
de_stations.head()
```

Output:
```
shape: (5, 9)
┌──────────────┬──────────────────────────────────┬─────────────┬───────────────┬───────┬───────┬────────┬────────┬────────┐
│ id           ┆ name                             ┆ country     ┆ state         ┆ icao  ┆ lat   ┆ lon    ┆ elev   ┆ begin  │
│ ---          ┆ ---                              ┆ ---         ┆ ---           ┆ ---   ┆ ---   ┆ ---    ┆ ---    ┆ ---    │
│ str          ┆ str                              ┆ str         ┆ str           ┆ str   ┆ f64   ┆ f64    ┆ f64    ┆ str    │
╞══════════════╪══════════════════════════════════╪═════════════╪═══════════════╪═══════╪═══════╪════════╪════════╪════════╡
│ 100040-99999 ┆ JAN MAYEN                        ┆ NORWAY      ┆ null          ┆ ENJA  ┆ 70.93 ┆ -8.67  ┆ 9.0    ┆ 19210… │
│ 100050-99999 ┆ TWENTHE                          ┆ NETHERLANDS ┆ null          ┆ EHTW  ┆ 52.27 ┆ 6.89   ┆ 35.0   ┆ 19460… │
│ 100070-99999 ┆ FRIGG                            ┆ NORWAY      ┆ null          ┆ null  ┆ 59.9  ┆ 2.25   ┆ 47.0   ┆ 19780… │
│ 100080-99999 ┆ EKOFISK                          ┆ NORWAY      ┆ null          ┆ EKOF  ┆ 56.55 ┆ 3.22   ┆ 30.0   ┆ 19760… │
│ 100100-99999 ┆ HEIDRUN                          ┆ NORWAY      ┆ null          ┆ null  ┆ 65.33 ┆ 7.32   ┆ 222.0  ┆ 19940… │
└──────────────┴──────────────────────────────────┴─────────────┴───────────────┴───────┴───────┴────────┴────────┴────────┘
```

```python
# Search by US state
ca_stations = wv.search_stations(state=wv.state.CA)
ca_stations.head()
```

Output:
```
shape: (5, 9)
┌──────────────┬─────────────────────────────┬─────────┬───────┬───────┬───────┬──────────┬───────┬────────┐
│ id           ┆ name                        ┆ country ┆ state ┆ icao  ┆ lat   ┆ lon      ┆ elev  ┆ begin  │
│ ---          ┆ ---                         ┆ ---     ┆ ---   ┆ ---   ┆ ---   ┆ ---      ┆ ---   ┆ ---    │
│ str          ┆ str                         ┆ str     ┆ str   ┆ str   ┆ f64   ┆ f64      ┆ f64   ┆ str    │
╞══════════════╪═════════════════════════════╪═════════╪═══════╪═══════╪═══════╪══════════╪═══════╪════════╡
│ 690020-99999 ┆ NORTH ISLAND                ┆ US      ┆ CA    ┆ KNZY  ┆ 32.7  ┆ -117.21  ┆ 8.0   ┆ 19730… │
│ 690150-23174 ┆ TWENTYNINE PALMS            ┆ US      ┆ CA    ┆ KNXP  ┆ 34.3  ┆ -116.15  ┆ 626.0 ┆ 19420… │
│ 690190-93134 ┆ IMPERIAL BEACH              ┆ US      ┆ CA    ┆ KNRS  ┆ 32.57 ┆ -117.12  ┆ 6.0   ┆ 19580… │
│ 690230-23188 ┆ EDWARDS AFB                 ┆ US      ┆ CA    ┆ KEDW  ┆ 34.9  ┆ -117.88  ┆ 702.0 ┆ 19420… │
│ 690240-99999 ┆ VANDENBERG SFB              ┆ US      ┆ CA    ┆ KVBG  ┆ 34.73 ┆ -120.57  ┆ 112.0 ┆ 19730… │
└──────────────┴─────────────────────────────┴─────────┴───────┴───────┴───────┴──────────┴───────┴────────┘
```

### Search by Location (lat/long Bounding Box)

```python
# Search by coordinates (latitude/longitude range)
nyc_stations = wv.search_stations(
    lat_range=(40.5, 41.0),
    lon_range=(-74.5, -73.5)
)
nyc_stations
```

Output:
```
shape: (8, 9)
┌──────────────┬───────────────────────────────┬─────────┬───────┬───────┬───────┬─────────┬───────┬────────┐
│ id           ┆ name                          ┆ country ┆ state ┆ icao  ┆ lat   ┆ lon     ┆ elev  ┆ begin  │
│ ---          ┆ ---                           ┆ ---     ┆ ---   ┆ ---   ┆ ---   ┆ ---     ┆ ---   ┆ ---    │
│ str          ┆ str                           ┆ str     ┆ str   ┆ str   ┆ f64   ┆ f64     ┆ f64   ┆ str    │
╞══════════════╪═══════════════════════════════╪═════════╪═══════╪═══════╪═══════╪═════════╪═══════╪════════╡
│ 725020-14734 ┆ NEWARK LIBERTY INTERNATIONAL  ┆ US      ┆ NJ    ┆ KEWR  ┆ 40.7  ┆ -74.17  ┆ 4.0   ┆ 19730… │
│ 725025-14734 ┆ NEWARK LIBERTY INTERNATIONAL  ┆ US      ┆ NJ    ┆ KEWR  ┆ 40.7  ┆ -74.17  ┆ 4.0   ┆ 19510… │
│ 725030-14732 ┆ LA GUARDIA AIRPORT            ┆ US      ┆ NY    ┆ KLGA  ┆ 40.78 ┆ -73.88  ┆ 3.0   ┆ 19730… │
│ 725033-14732 ┆ LA GUARDIA AIRPORT            ┆ US      ┆ NY    ┆ KLGA  ┆ 40.78 ┆ -73.88  ┆ 3.0   ┆ 19380… │
│ 725037-94728 ┆ JOHN F KENNEDY INTL AP        ┆ US      ┆ NY    ┆ KJFK  ┆ 40.64 ┆ -73.78  ┆ 3.4   ┆ 19730… │
│ 744860-94728 ┆ JOHN F KENNEDY INTL AP        ┆ US      ┆ NY    ┆ KJFK  ┆ 40.64 ┆ -73.78  ┆ 3.4   ┆ 19491… │
│ 999999-14732 ┆ NEW YORK/LA GUARDIA           ┆ US      ┆ NY    ┆ null  ┆ 40.78 ┆ -73.88  ┆ 3.4   ┆ 19310… │
│ 999999-94728 ┆ NEW YORK/JFK                  ┆ US      ┆ NY    ┆ null  ┆ 40.64 ┆ -73.78  ┆ 3.4   ┆ 19310… │
└──────────────┴───────────────────────────────┴─────────┴───────┴───────┴───────┴─────────┴───────┴────────┘
```

### Search by Name or Country

```python
# Search by station name
airports = wv.search_stations(name="tokyo international")
airports
```

Output:
```
shape: (2, 9)
┌──────────────┬─────────────────────────────┬─────────┬───────┬───────┬───────┬────────┬───────┬────────┐
│ id           ┆ name                        ┆ country ┆ state ┆ icao  ┆ lat   ┆ lon    ┆ elev  ┆ begin  │
│ ---          ┆ ---                         ┆ ---     ┆ ---   ┆ ---   ┆ ---   ┆ ---    ┆ ---   ┆ ---    │
│ str          ┆ str                         ┆ str     ┆ str   ┆ str   ┆ f64   ┆ f64    ┆ f64   ┆ str    │
╞══════════════╪═════════════════════════════╪═════════╪═══════╪═══════╪═══════╪════════╪═══════╪════════╡
│ 476710-99999 ┆ TOKYO INTERNATIONAL AIRPORT ┆ JAPAN   ┆ null  ┆ RJTT  ┆ 35.55 ┆ 139.78 ┆ 4.0   ┆ 19730… │
│ 476770-99999 ┆ TOKYO INTERNATIONAL AIRPORT ┆ JAPAN   ┆ null  ┆ RJTT  ┆ 35.55 ┆ 139.78 ┆ 4.0   ┆ 19530… │
└──────────────┴─────────────────────────────┴─────────┴───────┴───────┴───────┴────────┴───────┴────────┘
```

```python
# Search by country name
uk_stations = wv.search_stations(country="United Kingdom")
uk_stations.head()
```

Output:
```
shape: (5, 9)
┌──────────────┬──────────────────────┬────────────────┬───────┬───────┬───────┬────────┬───────┬────────┐
│ id           ┆ name                 ┆ country        ┆ state ┆ icao  ┆ lat   ┆ lon    ┆ elev  ┆ begin  │
│ ---          ┆ ---                  ┆ ---            ┆ ---   ┆ ---   ┆ ---   ┆ ---    ┆ ---   ┆ ---    │
│ str          ┆ str                  ┆ str            ┆ str   ┆ str   ┆ f64   ┆ f64    ┆ f64   ┆ str    │
╞══════════════╪══════════════════════╪════════════════╪═══════╪═══════╪═══════╪════════╪═══════╪════════╡
│ 030050-99999 ┆ LERWICK              ┆ UNITED KINGDOM ┆ null  ┆ ENSL  ┆ 60.13 ┆ -1.18  ┆ 82.0  ┆ 19310… │
│ 030350-99999 ┆ KIRKWALL AIRPORT     ┆ UNITED KINGDOM ┆ null  ┆ EGPA  ┆ 58.95 ┆ -2.9   ┆ 26.0  ┆ 19730… │
│ 030510-99999 ┆ STORNOWAY            ┆ UNITED KINGDOM ┆ null  ┆ EGPO  ┆ 58.22 ┆ -6.32  ┆ 9.0   ┆ 19730… │
│ 030600-99999 ┆ CAPE WRATH           ┆ UNITED KINGDOM ┆ null  ┆ null  ┆ 58.63 ┆ -5.0   ┆ 122.0 ┆ 19310… │
│ 030630-99999 ┆ WICK                 ┆ UNITED KINGDOM ┆ null  ┆ EGPC  ┆ 58.45 ┆ -3.08  ┆ 36.0  ┆ 19730… │
└──────────────┴──────────────────────┴────────────────┴───────┴───────┴───────┴────────┴───────┴────────┘
```

### Get All Station Metadata

```python
# Get metadata for all 29,000+ stations
all_stations = wv.get_station_metadata()
all_stations.head()
```

Output:
```
shape: (5, 9)
┌──────────────┬───────────────────────────┬─────────┬───────┬───────┬────────┬─────────┬────────┬────────┐
│ id           ┆ name                      ┆ country ┆ state ┆ icao  ┆ lat    ┆ lon     ┆ elev   ┆ begin  │
│ ---          ┆ ---                       ┆ ---     ┆ ---   ┆ ---   ┆ ---    ┆ ---     ┆ ---    ┆ ---    │
│ str          ┆ str                       ┆ str     ┆ str   ┆ str   ┆ f64    ┆ f64     ┆ f64    ┆ str    │
╞══════════════╪═══════════════════════════╪═════════╪═══════╪═══════╪════════╪═════════╪════════╪════════╡
│ 007005-99999 ┆ CWOS 07005                ┆ null    ┆ null  ┆ null  ┆ null   ┆ null    ┆ null   ┆ 19710… │
│ 007011-99999 ┆ CWOS 07011                ┆ null    ┆ null  ┆ null  ┆ null   ┆ null    ┆ null   ┆ 19730… │
│ 007018-99999 ┆ WXPOD 7018                ┆ null    ┆ null  ┆ null  ┆ 0.0    ┆ 0.0     ┆ 7018.0 ┆ 20110… │
│ 007026-99999 ┆ WXPOD 7026                ┆ null    ┆ null  ┆ null  ┆ 0.0    ┆ 0.0     ┆ 7026.0 ┆ 20050… │
│ 007070-99999 ┆ WXPOD 7070                ┆ null    ┆ null  ┆ null  ┆ 0.0    ┆ 0.0     ┆ 7070.0 ┆ 20050… │
└──────────────┴───────────────────────────┴─────────┴───────┴───────┴────────┴─────────┴────────┴────────┘
```

## Weather Data Columns

The returned DataFrame includes:

| Column | Description |
|--------|-------------|
| `id` | Station identifier (USAF-WBAN format) |
| `time` | Observation time (local time by default) |
| `temp` | Air temperature (°C) |
| `dew_point` | Dew point temperature |
| `rh` | Relative humidity (%) |
| `wd` | Wind direction (degrees, 0-360) |
| `ws` | Wind speed (m/s) |
| `atmos_pres` | Sea level pressure (hPa) |
| `ceil_hgt` | Ceiling height (m, 22000 = unlimited) |
| `visibility` | Visibility (m, max 16000 = 10 miles) |

## Advanced Usage

### Include Station Metadata

Add station information (name, country, state, ICAO, coordinates, elevation) to each observation:

```python
weather = wv.get_weather_data(
    "725030-14732",
    years=2024,
    incl_stn_info=True
)
weather[["time", "temp", "name", "country"]].head()
```

Output:
```
shape: (5, 4)
┌─────────────────────────┬───────┬────────────────────┬─────────┐
│ time                    ┆ temp  ┆ name               ┆ country │
│ ---                     ┆ ---   ┆ ---                ┆ ---     │
│ datetime[μs, tz]        ┆ f64   ┆ str                ┆ str     │
╞═════════════════════════╪═══════╪════════════════════╪═════════╡
│ 2024-01-01 00:51:00 EST ┆ 12.8  ┆ LA GUARDIA AIRPORT ┆ US      │
│ 2024-01-01 01:51:00 EST ┆ 12.2  ┆ LA GUARDIA AIRPORT ┆ US      │
│ 2024-01-01 02:51:00 EST ┆ 11.7  ┆ LA GUARDIA AIRPORT ┆ US      │
│ 2024-01-01 03:51:00 EST ┆ 11.1  ┆ LA GUARDIA AIRPORT ┆ US      │
│ 2024-01-01 04:51:00 EST ┆ 10.6  ┆ LA GUARDIA AIRPORT ┆ US      │
└─────────────────────────┴───────┴────────────────────┴─────────┘
```

### Temperature Units

```python
# Get temperatures in Fahrenheit
weather = wv.get_weather_data("725030-14732", years=2024, temp_unit="f")
weather[["time", "temp", "dew_point"]].head()
```

Output:
```
shape: (5, 3)
┌─────────────────────────┬───────┬───────────┐
│ time                    ┆ temp  ┆ dew_point │
│ ---                     ┆ ---   ┆ ---       │
│ datetime[μs, tz]        ┆ f64   ┆ f64       │
╞═════════════════════════╪═══════╪═══════════╡
│ 2024-01-01 00:51:00 EST ┆ 55.0  ┆ 46.0      │
│ 2024-01-01 01:51:00 EST ┆ 54.0  ┆ 45.0      │
│ 2024-01-01 02:51:00 EST ┆ 53.1  ┆ 44.6      │
│ 2024-01-01 03:51:00 EST ┆ 52.0  ┆ 43.9      │
│ 2024-01-01 04:51:00 EST ┆ 51.1  ┆ 43.3      │
└─────────────────────────┴───────┴───────────┘
```

Supported values: `"c"`/`"celsius"`, `"f"`/`"fahrenheit"`, `"k"`/`"kelvin"`.

### Multiple Years

```python
# Get multiple years of data
weather = wv.get_weather_data(
    "725030-14732",
    years=[2022, 2023, 2024]
)
weather[["time", "temp"]].head()
```

Output:
```
shape: (5, 2)
┌─────────────────────────┬───────┐
│ time                    ┆ temp  │
│ ---                     ┆ ---   │
│ datetime[μs, tz]        ┆ f64   │
╞═════════════════════════╪═══════╡
│ 2022-01-01 00:51:00 EST ┆ 2.2   │
│ 2022-01-01 01:51:00 EST ┆ 1.7   │
│ 2022-01-01 02:51:00 EST ┆ 1.1   │
│ 2022-01-01 03:51:00 EST ┆ 0.6   │
│ 2022-01-01 04:51:00 EST ┆ 0.0   │
└─────────────────────────┴───────┘
```

### Hourly Resampling

```python
# Resample to regular hourly intervals (fills missing hours with None)
weather = wv.get_weather_data(
    "725030-14732",
    years=2024,
    make_hourly=True
)
weather[["time", "temp", "ws"]].head(10)
```

Output:
```
shape: (10, 3)
┌─────────────────────────┬───────┬──────┐
│ time                    ┆ temp  ┆ ws   │
│ ---                     ┆ ---   ┆ ---  │
│ datetime[μs, tz]        ┆ f64   ┆ f64  │
╞═════════════════════════╪═══════╪══════╡
│ 2024-01-01 00:00:00 EST ┆ null  ┆ null │
│ 2024-01-01 01:00:00 EST ┆ 12.8  ┆ 4.6  │
│ 2024-01-01 02:00:00 EST ┆ 12.2  ┆ 5.1  │
│ 2024-01-01 03:00:00 EST ┆ 11.7  ┆ 4.6  │
│ 2024-01-01 04:00:00 EST ┆ 11.1  ┆ 3.6  │
│ 2024-01-01 05:00:00 EST ┆ 10.6  ┆ 3.6  │
│ 2024-01-01 06:00:00 EST ┆ 10.0  ┆ 2.6  │
│ 2024-01-01 07:00:00 EST ┆ 10.0  ┆ 3.6  │
│ 2024-01-01 08:00:00 EST ┆ 10.0  ┆ 4.1  │
│ 2024-01-01 09:00:00 EST ┆ 10.6  ┆ 4.1  │
└─────────────────────────┴───────┴──────┘
```

### Keep UTC Time

```python
# Don't convert to local time (keep UTC time)
weather = wv.get_weather_data(
    "725030-14732",
    years=2024,
    convert_to_local=False
)
weather[["time", "temp"]].head()
```

Output:
```
shape: (5, 2)
┌─────────────────────────┬───────┐
│ time                    ┆ temp  │
│ ---                     ┆ ---   │
│ datetime[μs, UTC]       ┆ f64   │
╞═════════════════════════╪═══════╡
│ 2024-01-01 05:51:00 UTC ┆ 12.8  │
│ 2024-01-01 06:51:00 UTC ┆ 12.2  │
│ 2024-01-01 07:51:00 UTC ┆ 11.7  │
│ 2024-01-01 08:51:00 UTC ┆ 11.1  │
│ 2024-01-01 09:51:00 UTC ┆ 10.6  │
└─────────────────────────┴───────┘
```

### Smart Data Caching

Cache downloaded files for offline use or faster repeated access:

```python
# Cache in current directory
weather = wv.get_weather_data(
    "725030-14732",
    years=2024,
    cache_dir="."
)
weather[["time", "temp"]].head()
```

Output:
```
shape: (5, 2)
┌─────────────────────────┬───────┐
│ time                    ┆ temp  │
│ ---                     ┆ ---   │
│ datetime[μs, tz]        ┆ f64   │
╞═════════════════════════╪═══════╡
│ 2024-01-01 00:51:00 EST ┆ 12.8  │
│ 2024-01-01 01:51:00 EST ┆ 12.2  │
│ 2024-01-01 02:51:00 EST ┆ 11.7  │
│ 2024-01-01 03:51:00 EST ┆ 11.1  │
│ 2024-01-01 04:51:00 EST ┆ 10.6  │
└─────────────────────────┴───────┘
```

Weathervault automatically checks:

1. Specified `cache_dir=` (if provided)
2. Current working directory (for existing cached files)

and if no relevant data files are found, they are downloaded from NOAA.

## Data Inventory

Check what data is available:

```python
# Get the data inventory (record counts by station/year/month)
inventory = wv.get_inventory()
inventory.head()
```

Output:
```
shape: (5, 4)
┌──────────────┬──────┬───────┬────────┐
│ id           ┆ year ┆ month ┆ count  │
│ ---          ┆ ---  ┆ ---   ┆ ---    │
│ str          ┆ i32  ┆ i32   ┆ i32    │
╞══════════════╪══════╪═══════╪════════╡
│ 007005-99999 ┆ 1971 ┆ 5     ┆ 360    │
│ 007005-99999 ┆ 1971 ┆ 6     ┆ 356    │
│ 007005-99999 ┆ 1971 ┆ 7     ┆ 364    │
│ 007005-99999 ┆ 1971 ┆ 8     ┆ 363    │
│ 007005-99999 ┆ 1971 ┆ 9     ┆ 361    │
└──────────────┴──────┴───────┴────────┘
```

```python
# Filter to a specific station
import polars as pl
station_inv = inventory.filter(pl.col("id") == "725030-14732")
station_inv.head()
```

Output:
```
shape: (5, 4)
┌──────────────┬──────┬───────┬───────┐
│ id           ┆ year ┆ month ┆ count │
│ ---          ┆ ---  ┆ ---   ┆ ---   │
│ str          ┆ i32  ┆ i32   ┆ i32   │
╞══════════════╪══════╪═══════╪═══════╡
│ 725030-14732 ┆ 1973 ┆ 1     ┆ 744   │
│ 725030-14732 ┆ 1973 ┆ 2     ┆ 672   │
│ 725030-14732 ┆ 1973 ┆ 3     ┆ 744   │
│ 725030-14732 ┆ 1973 ┆ 4     ┆ 720   │
│ 725030-14732 ┆ 1973 ┆ 5     ┆ 744   │
└──────────────┴──────┴───────┴───────┘
```

## License

MIT License. See [LICENSE](LICENSE) for details.
