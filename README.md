# weathervault

<div align="center">

[![Python versions](https://img.shields.io/pypi/pyversions/weathervault.svg)](https://pypi.org/project/weathervault/)
[![PyPI](https://img.shields.io/pypi/v/weathervault)](https://pypi.org/project/weathervault/#history)

[![Tests](https://github.com/rich-iannone/weathervault/actions/workflows/tests.yml/badge.svg)](https://github.com/rich-iannone/weathervault/actions/workflows/tests.yml)
[![Repo Status](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.1%20adopted-ff69b4.svg)](https://www.contributor-covenant.org/version/2/1/code_of_conduct.html)

</div>

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

weather
```

Output:
```
shape: (13_420, 10)
┌──────────────┬────────────────────────────────┬──────┬───────────┬──────┬──────┬──────┬────────────┬──────────┬────────────┐
│ id           ┆ time                           ┆ temp ┆ dew_point ┆ rh   ┆ wd   ┆ ws   ┆ atmos_pres ┆ ceil_hgt ┆ visibility │
│ ---          ┆ ---                            ┆ ---  ┆ ---       ┆ ---  ┆ ---  ┆ ---  ┆ ---        ┆ ---      ┆ ---        │
│ str          ┆ datetime[μs, America/New_York] ┆ f64  ┆ f64       ┆ f64  ┆ i32  ┆ f64  ┆ f64        ┆ i32      ┆ i32        │
╞══════════════╪════════════════════════════════╪══════╪═══════════╪══════╪══════╪══════╪════════════╪══════════╪════════════╡
│ 725030-14732 ┆ 2024-01-01 00:51:00 EST        ┆ 6.1  ┆ -2.8      ┆ 52.9 ┆ 230  ┆ 3.1  ┆ 1015.7     ┆ 1280     ┆ 16093      │
│ 725030-14732 ┆ 2024-01-01 01:00:00 EST        ┆ 6.1  ┆ -2.8      ┆ 52.9 ┆ 230  ┆ 3.1  ┆ 1015.7     ┆ null     ┆ 16000      │
│ 725030-14732 ┆ 2024-01-01 01:51:00 EST        ┆ 6.1  ┆ -2.8      ┆ 52.9 ┆ 270  ┆ 4.1  ┆ 1015.5     ┆ 1829     ┆ 16093      │
│ 725030-14732 ┆ 2024-01-01 02:51:00 EST        ┆ 5.6  ┆ -2.2      ┆ 57.2 ┆ 270  ┆ 4.1  ┆ 1015.5     ┆ 1097     ┆ 16093      │
│ 725030-14732 ┆ 2024-01-01 03:51:00 EST        ┆ 5.6  ┆ -1.7      ┆ 59.4 ┆ 280  ┆ 3.1  ┆ 1015.1     ┆ 1219     ┆ 16093      │
│ …            ┆ …                              ┆ …    ┆ …         ┆ …    ┆ …    ┆ …    ┆ …          ┆ …        ┆ …          │
│ 725030-14732 ┆ 2024-12-31 23:20:00 EST        ┆ 7.2  ┆ 4.4       ┆ 82.4 ┆ 50   ┆ 7.7  ┆ null       ┆ 335      ┆ 16093      │
│ 725030-14732 ┆ 2024-12-31 23:43:00 EST        ┆ 7.2  ┆ 5.0       ┆ 85.9 ┆ 40   ┆ 4.6  ┆ null       ┆ 671      ┆ 16093      │
│ 725030-14732 ┆ 2024-12-31 23:51:00 EST        ┆ 7.2  ┆ 5.0       ┆ 85.9 ┆ 40   ┆ 5.7  ┆ 998.9      ┆ 671      ┆ 16093      │
│ 725030-14732 ┆ 2024-12-31 23:59:00 EST        ┆ null ┆ null      ┆ null ┆ null ┆ null ┆ null       ┆ null     ┆ null       │
│ 725030-14732 ┆ 2024-12-31 23:59:00 EST        ┆ null ┆ null      ┆ null ┆ null ┆ null ┆ null       ┆ null     ┆ null       │
└──────────────┴────────────────────────────────┴──────┴───────────┴──────┴──────┴──────┴────────────┴──────────┴────────────┘
```

## Finding Weather Stations

### Convenient Shorthand Syntax

Use `wv.country` and `wv.state` for clean, readable code with IDE autocomplete:

```python
# Search by country using convenient shorthand
de_stations = wv.search_stations(country_code=wv.country.DE)
de_stations
```

Output:
```
shape: (503, 14)
┌──────────────┬────────┬───────┬─────────────────────────────┬──────────────┬─────────┬───────┬──────┬────────┬────────┬───────┬────────────┬────────────┬───────────────────┐
│ id           ┆ usaf   ┆ wban  ┆ name                        ┆ country_code ┆ country ┆ state ┆ icao ┆ lat    ┆ lon    ┆ elev  ┆ begin_date ┆ end_date   ┆ tz_name           │
│ ---          ┆ ---    ┆ ---   ┆ ---                         ┆ ---          ┆ ---     ┆ ---   ┆ ---  ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---        ┆ ---               │
│ str          ┆ str    ┆ str   ┆ str                         ┆ str          ┆ str     ┆ str   ┆ str  ┆ f64    ┆ f64    ┆ f64   ┆ date       ┆ date       ┆ str               │
╞══════════════╪════════╪═══════╪═════════════════════════════╪══════════════╪═════════╪═══════╪══════╪════════╪════════╪═══════╪════════════╪════════════╪═══════════════════╡
│ 090910-99999 ┆ 090910 ┆ 99999 ┆ ARKONA (CAPE)     &         ┆ DE           ┆ Germany ┆       ┆      ┆ 54.683 ┆ 13.433 ┆ 42.0  ┆ 1975-07-01 ┆ 2002-07-29 ┆ Europe/Berlin     │
│ 090930-99999 ┆ 090930 ┆ 99999 ┆ BOGUS GERMAN                ┆ DE           ┆ Germany ┆       ┆      ┆ null   ┆ null   ┆ null  ┆ 1990-12-03 ┆ 1991-10-31 ┆ null              │
│ 091610-99999 ┆ 091610 ┆ 99999 ┆ BOLTENHAGEN       &         ┆ DE           ┆ Germany ┆       ┆      ┆ 54.0   ┆ 11.2   ┆ 15.0  ┆ 1975-07-01 ┆ 1991-10-31 ┆ Europe/Berlin     │
│ 091620-99999 ┆ 091620 ┆ 99999 ┆ SCHWERIN          &         ┆ DE           ┆ Germany ┆       ┆      ┆ 53.633 ┆ 11.417 ┆ 59.0  ┆ 1975-07-01 ┆ 1992-05-17 ┆ Europe/Berlin     │
│ 091680-99999 ┆ 091680 ┆ 99999 ┆ BOGUS GERMAN                ┆ DE           ┆ Germany ┆       ┆      ┆ null   ┆ null   ┆ null  ┆ 1990-12-03 ┆ 1991-10-30 ┆ null              │
│ …            ┆ …      ┆ …     ┆ …                           ┆ …            ┆ …       ┆ …     ┆ …    ┆ …      ┆ …      ┆ …     ┆ …          ┆ …          ┆ …                 │
│ 119060-99999 ┆ 119060 ┆ 99999 ┆ LEST                        ┆ DE           ┆ Germany ┆       ┆      ┆ 48.35  ┆ 19.317 ┆ 720.0 ┆ 1952-11-06 ┆ 1953-12-31 ┆ Europe/Bratislava │
│ 693664-99999 ┆ 693664 ┆ 99999 ┆ COTTBUS DREWITZ             ┆ DE           ┆ Germany ┆       ┆ EDCD ┆ 51.889 ┆ 14.532 ┆ 83.5  ┆ 1981-01-15 ┆ 1990-12-14 ┆ Europe/Berlin     │
│ 749520-99999 ┆ 749520 ┆ 99999 ┆ SOSSENHEIM                  ┆ DE           ┆ Germany ┆       ┆      ┆ 50.133 ┆ 8.583  ┆ 130.0 ┆ 1946-08-31 ┆ 1947-02-14 ┆ Europe/Berlin     │
│ 749538-99999 ┆ 749538 ┆ 99999 ┆ OBERPFAFFENHOFEN GERMANY AD ┆ DE           ┆ Germany ┆       ┆      ┆ 48.083 ┆ 11.266 ┆ 580.0 ┆ 1946-08-14 ┆ 1949-07-31 ┆ Europe/Berlin     │
│ 999999-34196 ┆ 999999 ┆ 34196 ┆ GABLINGEN                   ┆ DE           ┆ Germany ┆       ┆ EDOX ┆ 48.45  ┆ 10.867 ┆ 466.0 ┆ 1963-09-10 ┆ 1967-12-29 ┆ Europe/Berlin     │
└──────────────┴────────┴───────┴─────────────────────────────┴──────────────┴─────────┴───────┴──────┴────────┴────────┴───────┴────────────┴────────────┴───────────────────┘
```

```python
# Search by US state
ca_stations = wv.search_stations(state=wv.state.CA)
ca_stations
```

Output:
```
shape: (499, 14)
┌──────────────┬────────┬───────┬──────────────────────────────┬──────────────┬───────────────┬───────┬──────┬────────┬──────────┬────────┬────────────┬────────────┬─────────────────────┐
│ id           ┆ usaf   ┆ wban  ┆ name                         ┆ country_code ┆ country       ┆ state ┆ icao ┆ lat    ┆ lon      ┆ elev   ┆ begin_date ┆ end_date   ┆ tz_name             │
│ ---          ┆ ---    ┆ ---   ┆ ---                          ┆ ---          ┆ ---           ┆ ---   ┆ ---  ┆ ---    ┆ ---      ┆ ---    ┆ ---        ┆ ---        ┆ ---                 │
│ str          ┆ str    ┆ str   ┆ str                          ┆ str          ┆ str           ┆ str   ┆ str  ┆ f64    ┆ f64      ┆ f64    ┆ date       ┆ date       ┆ str                 │
╞══════════════╪════════╪═══════╪══════════════════════════════╪══════════════╪═══════════════╪═══════╪══════╪════════╪══════════╪════════╪════════════╪════════════╪═════════════════════╡
│ 690020-93218 ┆ 690020 ┆ 93218 ┆ JOLON HUNTER LIGGETT MIL RES ┆ US           ┆ United States ┆ CA    ┆ KHGT ┆ 36.0   ┆ -121.233 ┆ 317.0  ┆ 1964-07-15 ┆ 1997-04-01 ┆ America/Los_Angeles │
│ 690020-99999 ┆ 690020 ┆ 99999 ┆ JOLON HUNTER LIGGETT MIL RES ┆ US           ┆ United States ┆ CA    ┆ KHGT ┆ 36.0   ┆ -121.233 ┆ 317.0  ┆ 2003-07-02 ┆ 2003-08-01 ┆ America/Los_Angeles │
│ 690070-93217 ┆ 690070 ┆ 93217 ┆ FRITZSCHE AAF                ┆ US           ┆ United States ┆ CA    ┆ KOAR ┆ 36.683 ┆ -121.767 ┆ 43.0   ┆ 1960-04-04 ┆ 1993-08-31 ┆ America/Los_Angeles │
│ 690080-99999 ┆ 690080 ┆ 99999 ┆ TARIN KOWT                   ┆ AF           ┆ Afghanistan   ┆ CA    ┆ KQA7 ┆ 32.6   ┆ 65.87    ┆ 1380.0 ┆ 2003-06-16 ┆ 2003-06-24 ┆ Asia/Kabul          │
│ 690140-93101 ┆ 690140 ┆ 93101 ┆ EL TORO MCAS                 ┆ US           ┆ United States ┆ CA    ┆ KNZJ ┆ 33.667 ┆ -117.733 ┆ 116.7  ┆ 1989-01-01 ┆ 1997-12-31 ┆ America/Los_Angeles │
│ …            ┆ …      ┆ …     ┆ …                            ┆ …            ┆ …             ┆ …     ┆ …    ┆ …      ┆ …        ┆ …      ┆ …          ┆ …          ┆ …                   │
│ 999999-93243 ┆ 999999 ┆ 93243 ┆ MERCED 23 WSW                ┆ US           ┆ United States ┆ CA    ┆      ┆ 37.238 ┆ -120.883 ┆ 23.8   ┆ 2004-03-25 ┆ 2025-08-28 ┆ America/Los_Angeles │
│ 999999-93245 ┆ 999999 ┆ 93245 ┆ BODEGA 6 WSW                 ┆ US           ┆ United States ┆ CA    ┆      ┆ 38.321 ┆ -123.075 ┆ 19.2   ┆ 2008-06-14 ┆ 2025-08-28 ┆ America/Los_Angeles │
│ A06854-00115 ┆ A06854 ┆ 00115 ┆ BIG BEAR CITY AIRPORT        ┆ US           ┆ United States ┆ CA    ┆ KL35 ┆ 34.264 ┆ -116.854 ┆ 2057.1 ┆ 2014-07-31 ┆ 2025-08-25 ┆ America/Los_Angeles │
│ A07049-00320 ┆ A07049 ┆ 00320 ┆ PETALUMA MUNICIPAL AIRPORT   ┆ US           ┆ United States ┆ CA    ┆ KO69 ┆ 38.25  ┆ -122.6   ┆ 27.1   ┆ 2014-07-31 ┆ 2025-08-25 ┆ America/Los_Angeles │
│ A07053-00346 ┆ A07053 ┆ 00346 ┆ TRINITY CENTER AIRPORT       ┆ US           ┆ United States ┆ CA    ┆ KO86 ┆ 40.983 ┆ -122.694 ┆ 728.2  ┆ 2014-07-31 ┆ 2025-08-25 ┆ America/Los_Angeles │
└──────────────┴────────┴───────┴──────────────────────────────┴──────────────┴───────────────┴───────┴──────┴────────┴──────────┴────────┴────────────┴────────────┴─────────────────────┘
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
uk_stations
```

Output:
```
shape: (706, 14)
┌──────────────┬────────┬───────┬─────────────────┬──────────────┬────────────────┬───────┬──────┬────────┬────────┬───────┬────────────┬────────────┬───────────────┐
│ id           ┆ usaf   ┆ wban  ┆ name            ┆ country_code ┆ country        ┆ state ┆ icao ┆ lat    ┆ lon    ┆ elev  ┆ begin_date ┆ end_date   ┆ tz_name       │
│ ---          ┆ ---    ┆ ---   ┆ ---             ┆ ---          ┆ ---            ┆ ---   ┆ ---  ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---        ┆ ---           │
│ str          ┆ str    ┆ str   ┆ str             ┆ str          ┆ str            ┆ str   ┆ str  ┆ f64    ┆ f64    ┆ f64   ┆ date       ┆ date       ┆ str           │
╞══════════════╪════════╪═══════╪═════════════════╪══════════════╪════════════════╪═══════╪══════╪════════╪════════╪═══════╪════════════╪════════════╪═══════════════╡
│ 030010-99999 ┆ 030010 ┆ 99999 ┆ MUCKLE FLUGGA   ┆ GB           ┆ United Kingdom ┆       ┆      ┆ 60.85  ┆ -0.883 ┆ 53.0  ┆ 1980-04-21 ┆ 1997-06-08 ┆ Europe/London │
│ 030020-99999 ┆ 030020 ┆ 99999 ┆ BALTASOUND NO.2 ┆ GB           ┆ United Kingdom ┆       ┆ EGPW ┆ 60.75  ┆ -0.85  ┆ 15.0  ┆ 1973-01-01 ┆ 2025-08-24 ┆ Europe/London │
│ 030023-99999 ┆ 030023 ┆ 99999 ┆ SAXA VORD       ┆ GB           ┆ United Kingdom ┆       ┆ EGQR ┆ 60.833 ┆ -0.833 ┆ 285.0 ┆ 2022-09-16 ┆ 2023-03-08 ┆ Europe/London │
│ 030030-99999 ┆ 030030 ┆ 99999 ┆ SUMBURGH        ┆ GB           ┆ United Kingdom ┆       ┆ EGPB ┆ 59.879 ┆ -1.296 ┆ 6.1   ┆ 1977-01-19 ┆ 2025-08-24 ┆ Europe/London │
│ 030040-99999 ┆ 030040 ┆ 99999 ┆ COLLAFIRTH HILL ┆ GB           ┆ United Kingdom ┆       ┆      ┆ 60.533 ┆ -1.383 ┆ 228.0 ┆ 1979-02-08 ┆ 2005-07-31 ┆ Europe/London │
│ …            ┆ …      ┆ …     ┆ …               ┆ …            ┆ …              ┆ …     ┆ …    ┆ …      ┆ …      ┆ …     ┆ …          ┆ …          ┆ …             │
│ 999999-35034 ┆ 999999 ┆ 35034 ┆ LAKENHEATH RAF  ┆ GB           ┆ United Kingdom ┆       ┆ EGUL ┆ 52.4   ┆ 0.567  ┆ 10.1  ┆ 1949-05-01 ┆ 1967-12-31 ┆ Europe/London │
│ 999999-35046 ┆ 999999 ┆ 35046 ┆ MILDENHALL      ┆ GB           ┆ United Kingdom ┆       ┆ EGUN ┆ 52.367 ┆ 0.483  ┆ 10.1  ┆ 1950-07-14 ┆ 1967-12-31 ┆ Europe/London │
│ 999999-35047 ┆ 999999 ┆ 35047 ┆ MANSTON         ┆ GB           ┆ United Kingdom ┆       ┆ EGUM ┆ 51.35  ┆ 1.367  ┆ 43.9  ┆ 1950-07-20 ┆ 1958-05-31 ┆ Europe/London │
│ 999999-35048 ┆ 999999 ┆ 35048 ┆ BENTWATERS      ┆ GB           ┆ United Kingdom ┆       ┆ EGVJ ┆ 52.133 ┆ 1.433  ┆ 25.9  ┆ 1951-06-01 ┆ 1967-12-31 ┆ Europe/London │
│ 999999-35049 ┆ 999999 ┆ 35049 ┆ STANTON         ┆ GB           ┆ United Kingdom ┆       ┆      ┆ 52.317 ┆ 0.917  ┆ 61.0  ┆ 1951-06-01 ┆ 1959-01-09 ┆ Europe/London │
└──────────────┴────────┴───────┴─────────────────┴──────────────┴────────────────┴───────┴──────┴────────┴────────┴───────┴────────────┴────────────┴───────────────┘
```

### Get All Station Metadata

```python
# Get metadata for all 29,000+ stations
all_stations = wv.get_station_metadata()
all_stations
```

Output:
```
shape: (29_661, 14)
┌──────────────┬────────┬───────┬─────────────────────────────────┬──────────────┬───────────────┬───────┬──────┬────────┬─────────┬────────┬────────────┬────────────┬─────────────────┐
│ id           ┆ usaf   ┆ wban  ┆ name                            ┆ country_code ┆ country       ┆ state ┆ icao ┆ lat    ┆ lon     ┆ elev   ┆ begin_date ┆ end_date   ┆ tz_name         │
│ ---          ┆ ---    ┆ ---   ┆ ---                             ┆ ---          ┆ ---           ┆ ---   ┆ ---  ┆ ---    ┆ ---     ┆ ---    ┆ ---        ┆ ---        ┆ ---             │
│ str          ┆ str    ┆ str   ┆ str                             ┆ str          ┆ str           ┆ str   ┆ str  ┆ f64    ┆ f64     ┆ f64    ┆ date       ┆ date       ┆ str             │
╞══════════════╪════════╪═══════╪═════════════════════════════════╪══════════════╪═══════════════╪═══════╪══════╪════════╪═════════╪════════╪════════════╪════════════╪═════════════════╡
│ 007018-99999 ┆ 007018 ┆ 99999 ┆ WXPOD 7018                      ┆ null         ┆ null          ┆       ┆      ┆ 0.0    ┆ 0.0     ┆ 7018.0 ┆ 2011-03-09 ┆ 2013-07-30 ┆ Etc/GMT         │
│ 007026-99999 ┆ 007026 ┆ 99999 ┆ WXPOD 7026                      ┆ AF           ┆ Afghanistan   ┆       ┆      ┆ 0.0    ┆ 0.0     ┆ 7026.0 ┆ 2012-07-13 ┆ 2017-08-22 ┆ Etc/GMT         │
│ 007070-99999 ┆ 007070 ┆ 99999 ┆ WXPOD 7070                      ┆ AF           ┆ Afghanistan   ┆       ┆      ┆ 0.0    ┆ 0.0     ┆ 7070.0 ┆ 2014-09-23 ┆ 2015-09-26 ┆ Etc/GMT         │
│ 008260-99999 ┆ 008260 ┆ 99999 ┆ WXPOD8270                       ┆ null         ┆ null          ┆       ┆      ┆ 0.0    ┆ 0.0     ┆ 0.0    ┆ 2005-01-01 ┆ 2012-07-31 ┆ Etc/GMT         │
│ 008268-99999 ┆ 008268 ┆ 99999 ┆ WXPOD8278                       ┆ AF           ┆ Afghanistan   ┆       ┆      ┆ 32.95  ┆ 65.567  ┆ 1156.7 ┆ 2010-05-19 ┆ 2012-03-23 ┆ Asia/Kabul      │
│ …            ┆ …      ┆ …     ┆ …                               ┆ …            ┆ …             ┆ …     ┆ …    ┆ …      ┆ …       ┆ …      ┆ …          ┆ …          ┆ …               │
│ A07355-00241 ┆ A07355 ┆ 00241 ┆ VIROQUA MUNICIPAL AIRPORT       ┆ US           ┆ United States ┆ WI    ┆ KY51 ┆ 43.579 ┆ -90.913 ┆ 394.1  ┆ 2014-07-31 ┆ 2025-08-25 ┆ America/Chicago │
│ A07357-00182 ┆ A07357 ┆ 00182 ┆ ELBOW LAKE MUNICIPAL PRIDE OF … ┆ US           ┆ United States ┆ MN    ┆ KY63 ┆ 45.986 ┆ -95.992 ┆ 367.3  ┆ 2014-07-31 ┆ 2025-08-25 ┆ America/Chicago │
│ A07359-00240 ┆ A07359 ┆ 00240 ┆ IONIA COUNTY AIRPORT            ┆ US           ┆ United States ┆ MI    ┆ KY70 ┆ 42.938 ┆ -85.061 ┆ 249.0  ┆ 2014-07-31 ┆ 2025-08-25 ┆ America/Detroit │
│ A51255-00445 ┆ A51255 ┆ 00445 ┆ DEMOPOLIS MUNICIPAL AIRPORT     ┆ US           ┆ United States ┆ AL    ┆ KDYA ┆ 32.464 ┆ -87.954 ┆ 34.1   ┆ 2014-07-31 ┆ 2025-08-26 ┆ America/Chicago │
│ A51256-00451 ┆ A51256 ┆ 00451 ┆ BRANSON WEST MUNICIPAL EMERSON… ┆ US           ┆ United States ┆ MO    ┆ KFWB ┆ 36.699 ┆ -93.402 ┆ 411.2  ┆ 2014-07-31 ┆ 2025-08-25 ┆ America/Chicago │
└──────────────┴────────┴───────┴─────────────────────────────────┴──────────────┴───────────────┴───────┴──────┴────────┴─────────┴────────┴────────────┴────────────┴─────────────────┘
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
