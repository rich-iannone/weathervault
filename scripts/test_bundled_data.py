"""Quick test that bundled data works offline."""

import weathervault as wv

# Test: This should use bundled data (no network for the data itself!)
# Note: Station metadata still requires network on first call
print("Testing bundled data access...")

# Check what bundled years exist
from weathervault.weather import _get_bundled_years

for station in ["744860-94789", "725030-14732", "724050-13743"]:
    years = _get_bundled_years(station)
    print(f"  {station}: bundled years = {sorted(years)}")

print()
print("Fetching LaGuardia 2023 data...")
weather = wv.get_weather_data("725030-14732", years=2023)
print(f"Got {weather.height} rows")
print(weather.head(3))
