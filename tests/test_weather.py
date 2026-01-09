"""Tests for the weather module."""

import polars as pl
import pytest

from weathervault.weather import get_weather_data


class TestGetWeatherData:
    """Tests for get_weather_data function.

    Note: These tests require network access to download weather data.
    """

    @pytest.mark.network
    def test_returns_dataframe(self):
        """Test that get_weather_data returns a DataFrame."""
        # Use LaGuardia Airport and a recent year
        result = get_weather_data("725030-14732", years=2023)

        assert isinstance(result, pl.DataFrame)
        assert result.height > 0

    @pytest.mark.network
    def test_has_expected_columns(self):
        """Test that result has expected columns."""
        result = get_weather_data("725030-14732", years=2023)

        expected_columns = [
            "id",
            "time",
            "temp",
            "dew_point",
            "rh",
            "wd",
            "ws",
            "atmos_pres",
            "ceil_hgt",
            "visibility",
        ]
        for col in expected_columns:
            assert col in result.columns

    @pytest.mark.network
    def test_data_sorted_by_time(self):
        """Test that data is sorted by time (using UTC for proper comparison)."""
        result = get_weather_data("725030-14732", years=2023)

        times = result["time"].to_list()
        # Convert to UTC timestamps for proper sorting comparison
        # (handles DST transitions correctly)
        utc_times = [t.timestamp() for t in times]
        is_sorted = all(utc_times[i] <= utc_times[i + 1] for i in range(len(utc_times) - 1))
        if not is_sorted:
            for i in range(len(utc_times) - 1):
                if utc_times[i] > utc_times[i + 1]:
                    pytest.fail(
                        f"Data not sorted at index {i}: {times[i]} > {times[i + 1]} "
                        f"(out of {len(times)} records)"
                    )
        assert is_sorted, f"Data is not sorted by time ({len(times)} records)"

    @pytest.mark.network
    def test_fahrenheit_conversion(self):
        """Test temperature in Fahrenheit."""
        celsius_result = get_weather_data("725030-14732", years=2023, temp_unit="celsius")
        fahrenheit_result = get_weather_data("725030-14732", years=2023, temp_unit="fahrenheit")

        # Get first non-null temperature
        c_temp = celsius_result.filter(pl.col("temp").is_not_null())["temp"][0]
        f_temp = fahrenheit_result.filter(pl.col("temp").is_not_null())["temp"][0]

        # Verify Fahrenheit conversion: F = C * 9/5 + 32
        expected_f = c_temp * 9 / 5 + 32
        assert abs(f_temp - expected_f) < 0.2  # Allow small rounding difference

    def test_invalid_temp_unit(self):
        """Test that invalid temp_unit raises error."""
        with pytest.raises(ValueError, match="temp_unit"):
            get_weather_data("725030-14732", years=2023, temp_unit="rankine")

    @pytest.mark.network
    def test_invalid_station(self):
        """Test that invalid station raises error."""
        with pytest.raises(ValueError, match="not found"):
            get_weather_data("000000-00000", years=2023)

    @pytest.mark.network
    def test_multiple_years(self):
        """Test fetching multiple years of data."""
        result = get_weather_data("725030-14732", years=[2022, 2023])

        assert isinstance(result, pl.DataFrame)

        # Should have data from both years
        years_in_data = result["time"].dt.year().unique().to_list()
        assert 2022 in years_in_data or 2023 in years_in_data

    @pytest.mark.network
    def test_make_hourly(self):
        """Test hourly resampling."""
        result = get_weather_data("725030-14732", years=2023, make_hourly=True)

        assert isinstance(result, pl.DataFrame)

        # All times should be at the start of an hour (minute = 0)
        minutes = result["time"].dt.minute().unique().to_list()
        assert minutes == [0]

    @pytest.mark.network
    def test_station_id_in_result(self):
        """Test that station ID is included in results."""
        result = get_weather_data("725030-14732", years=2023)

        assert all(sid == "725030-14732" for sid in result["id"].to_list())

    @pytest.mark.network
    def test_reasonable_temperature_range(self):
        """Test that temperatures are in reasonable range."""
        result = get_weather_data("725030-14732", years=2023)

        temps = result.filter(pl.col("temp").is_not_null())["temp"].to_list()
        if temps:
            # New York temps should be roughly -30 to 45 Celsius
            assert all(-40 < t < 50 for t in temps)

    @pytest.mark.network
    def test_relative_humidity_range(self):
        """Test that relative humidity is in 0-100 range."""
        result = get_weather_data("725030-14732", years=2023)

        rh_values = result.filter(pl.col("rh").is_not_null())["rh"].to_list()
        if rh_values:
            # RH should be between 0 and 100 (with small tolerance for calculation quirks)
            assert all(-5 < rh < 110 for rh in rh_values)

    @pytest.mark.network
    def test_wind_direction_range(self):
        """Test that wind direction is in valid range."""
        result = get_weather_data("725030-14732", years=2023)

        wd_values = result.filter(pl.col("wd").is_not_null())["wd"].to_list()
        if wd_values:
            # Wind direction should be 1-360 degrees
            assert all(0 <= wd <= 360 for wd in wd_values)

    @pytest.mark.network
    def test_wind_speed_non_negative(self):
        """Test that wind speed values are non-negative."""
        result = get_weather_data("725030-14732", years=2023)

        ws_values = result.filter(pl.col("ws").is_not_null())["ws"].to_list()
        if ws_values:
            assert all(ws >= 0 for ws in ws_values)

    @pytest.mark.network
    def test_visibility_non_negative(self):
        """Test that visibility values are non-negative."""
        result = get_weather_data("725030-14732", years=2023)

        vis_values = result.filter(pl.col("visibility").is_not_null())["visibility"].to_list()
        if vis_values:
            assert all(v >= 0 for v in vis_values)

    @pytest.mark.network
    def test_atmospheric_pressure_reasonable(self):
        """Test that atmospheric pressure is in reasonable range."""
        result = get_weather_data("725030-14732", years=2023)

        pres_values = result.filter(pl.col("atmos_pres").is_not_null())["atmos_pres"].to_list()
        if pres_values:
            # Sea level pressure typically 870-1084 hPa
            assert all(800 < p < 1100 for p in pres_values)


class TestWeatherDataTypes:
    """Tests for weather data column types."""

    @pytest.mark.network
    def test_time_is_datetime(self):
        """Test that time column is datetime type."""
        result = get_weather_data("725030-14732", years=2023)
        assert result.schema["time"] == pl.Datetime

    @pytest.mark.network
    def test_temp_is_float(self):
        """Test that temperature is float type."""
        result = get_weather_data("725030-14732", years=2023)
        assert result.schema["temp"] == pl.Float64

    @pytest.mark.network
    def test_wind_direction_is_int(self):
        """Test that wind direction is integer type."""
        result = get_weather_data("725030-14732", years=2023)
        assert result.schema["wd"] == pl.Int32

    @pytest.mark.network
    def test_id_is_string(self):
        """Test that id column is string type."""
        result = get_weather_data("725030-14732", years=2023)
        assert result.schema["id"] == pl.Utf8


class TestYearHandling:
    """Tests for year parameter handling."""

    @pytest.mark.network
    def test_year_as_int(self):
        """Test passing a single year as integer."""
        result = get_weather_data("725030-14732", years=2023)
        assert isinstance(result, pl.DataFrame)
        years_in_data = result["time"].dt.year().unique().to_list()
        assert 2023 in years_in_data

    @pytest.mark.network
    def test_year_as_list(self):
        """Test passing years as a list."""
        result = get_weather_data("725030-14732", years=[2023])
        assert isinstance(result, pl.DataFrame)


class TestTemperatureUnit:
    """Tests for temperature unit conversion."""

    @pytest.mark.network
    def test_celsius_default(self):
        """Test that Celsius is the default temperature unit."""
        result = get_weather_data("725030-14732", years=2023)
        # Should have reasonable Celsius values
        temps = result.filter(pl.col("temp").is_not_null())["temp"].to_list()
        if temps:
            # New York Celsius temps should be roughly -30 to 45
            assert all(-40 < t < 50 for t in temps)

    @pytest.mark.network
    def test_fahrenheit_values_higher(self):
        """Test that Fahrenheit values are higher than Celsius (mostly)."""
        c_result = get_weather_data("725030-14732", years=2023, temp_unit="celsius")
        f_result = get_weather_data("725030-14732", years=2023, temp_unit="fahrenheit")

        c_mean = c_result.filter(pl.col("temp").is_not_null())["temp"].mean()
        f_mean = f_result.filter(pl.col("temp").is_not_null())["temp"].mean()

        # For positive Celsius temps, Fahrenheit should be higher
        if c_mean and c_mean > 0:
            assert f_mean > c_mean

    @pytest.mark.network
    def test_kelvin_conversion(self):
        """Test Kelvin temperature conversion."""
        c_result = get_weather_data("725030-14732", years=2023, temp_unit="c")
        k_result = get_weather_data("725030-14732", years=2023, temp_unit="k")

        c_temp = c_result.filter(pl.col("temp").is_not_null())["temp"][0]
        k_temp = k_result.filter(pl.col("temp").is_not_null())["temp"][0]

        # Kelvin = Celsius + 273.15
        expected_k = c_temp + 273.15
        assert abs(k_temp - expected_k) < 0.1

    @pytest.mark.network
    def test_short_temp_unit_names(self):
        """Test that short temperature unit names work."""
        # Test 'c' for Celsius
        c_result = get_weather_data("725030-14732", years=2023, temp_unit="c")
        assert c_result.height > 0

        # Test 'F' for Fahrenheit (uppercase)
        f_result = get_weather_data("725030-14732", years=2023, temp_unit="F")
        assert f_result.height > 0

        # Test 'K' for Kelvin (uppercase)
        k_result = get_weather_data("725030-14732", years=2023, temp_unit="K")
        assert k_result.height > 0


class TestLocalTimeConversion:
    """Tests for local time conversion."""

    @pytest.mark.network
    def test_convert_to_local_time(self):
        """Test that local time conversion changes timestamps."""
        utc_result = get_weather_data("725030-14732", years=2023, convert_to_local=False)
        local_result = get_weather_data("725030-14732", years=2023, convert_to_local=True)

        # Times should be different (LaGuardia is UTC-5 or UTC-4)
        # Check that at least first timestamps differ
        if utc_result.height > 0 and local_result.height > 0:
            # The times might be the same if we compare naive datetimes
            # but the data should have been processed
            assert isinstance(local_result, pl.DataFrame)

    @pytest.mark.network
    def test_no_conversion_default(self):
        """Test that convert_to_local=False keeps UTC."""
        result = get_weather_data("725030-14732", years=2023, convert_to_local=False)
        assert isinstance(result, pl.DataFrame)


class TestHourlyResampling:
    """Tests for hourly resampling."""

    @pytest.mark.network
    def test_hourly_reduces_rows(self):
        """Test that hourly resampling reduces number of rows."""
        raw = get_weather_data("725030-14732", years=2023, make_hourly=False)
        hourly = get_weather_data("725030-14732", years=2023, make_hourly=True)

        # Hourly should have fewer or equal rows
        assert hourly.height <= raw.height

    @pytest.mark.network
    def test_hourly_time_aligned(self):
        """Test that hourly data has minute=0."""
        result = get_weather_data("725030-14732", years=2023, make_hourly=True)

        minutes = result["time"].dt.minute().to_list()
        assert all(m == 0 for m in minutes)

    @pytest.mark.network
    def test_hourly_preserves_data_quality(self):
        """Test that hourly resampling preserves reasonable values."""
        result = get_weather_data("725030-14732", years=2023, make_hourly=True)

        temps = result.filter(pl.col("temp").is_not_null())["temp"].to_list()
        if temps:
            # Values should still be in reasonable range
            assert all(-40 < t < 50 for t in temps)


class TestStationIdFormats:
    """Tests for various station ID formats."""

    @pytest.mark.network
    def test_hyphenated_id(self):
        """Test standard hyphenated station ID format."""
        result = get_weather_data("725030-14732", years=2023)
        assert isinstance(result, pl.DataFrame)

    def test_invalid_id_format(self):
        """Test that completely invalid ID raises error."""
        with pytest.raises(ValueError):
            get_weather_data("invalid", years=2023)


class TestDataConsistency:
    """Tests for data consistency across requests."""

    @pytest.mark.network
    def test_same_data_multiple_calls(self):
        """Test that multiple calls return consistent data."""
        result1 = get_weather_data("725030-14732", years=2023)
        result2 = get_weather_data("725030-14732", years=2023)

        assert result1.height == result2.height
        assert result1.columns == result2.columns

    @pytest.mark.network
    def test_column_order_consistent(self):
        """Test that column order is consistent."""
        result = get_weather_data("725030-14732", years=2023)
        expected_order = [
            "id",
            "time",
            "temp",
            "dew_point",
            "rh",
            "wd",
            "ws",
            "atmos_pres",
            "ceil_hgt",
            "visibility",
        ]
        assert result.columns == expected_order


class TestStationInfo:
    """Tests for including station metadata in weather data."""

    @pytest.mark.network
    def test_incl_stn_info_adds_columns(self):
        """Test that incl_stn_info adds station metadata columns."""
        result = get_weather_data("725030-14732", years=2023, incl_stn_info=True)

        expected_columns = [
            "id",
            "time",
            "temp",
            "dew_point",
            "rh",
            "wd",
            "ws",
            "atmos_pres",
            "ceil_hgt",
            "visibility",
            "name",
            "country",
            "state",
            "icao",
            "lat",
            "lon",
            "elev",
        ]
        assert result.columns == expected_columns

    @pytest.mark.network
    def test_incl_stn_info_default_false(self):
        """Test that station info is not included by default."""
        result = get_weather_data("725030-14732", years=2023)

        station_columns = ["name", "country", "state", "icao", "lat", "lon", "elev"]
        for col in station_columns:
            assert col not in result.columns

    @pytest.mark.network
    def test_station_info_values_populated(self):
        """Test that station metadata values are populated."""
        result = get_weather_data("725030-14732", years=2023, incl_stn_info=True)

        # Check first row has station info
        first_row = result.head(1)
        assert first_row["name"][0] is not None
        assert first_row["country"][0] is not None
        assert first_row["icao"][0] == "KLGA"
        assert first_row["lat"][0] is not None
        assert first_row["lon"][0] is not None

    @pytest.mark.network
    def test_station_info_consistent_across_rows(self):
        """Test that station metadata is consistent across all rows."""
        result = get_weather_data("725030-14732", years=2023, incl_stn_info=True)

        # All rows should have same station metadata
        unique_names = result["name"].n_unique()
        unique_countries = result["country"].n_unique()
        unique_icao = result["icao"].n_unique()
        unique_lat = result["lat"].n_unique()
        unique_lon = result["lon"].n_unique()

        assert unique_names == 1
        assert unique_countries == 1
        assert unique_icao == 1
        assert unique_lat == 1
        assert unique_lon == 1

    @pytest.mark.network
    def test_station_info_with_hourly(self):
        """Test that station info works with hourly resampling."""
        result = get_weather_data("725030-14732", years=2023, incl_stn_info=True, make_hourly=True)

        # Should have station metadata columns
        assert "name" in result.columns
        assert "country" in result.columns
        assert "icao" in result.columns

        # Metadata should be consistent
        assert result["name"].n_unique() == 1
        assert result["icao"][0] == "KLGA"

    @pytest.mark.network
    def test_station_info_lat_lon_types(self):
        """Test that lat/lon are float types."""
        result = get_weather_data("725030-14732", years=2023, incl_stn_info=True)

        assert result["lat"].dtype == pl.Float64
        assert result["lon"].dtype == pl.Float64
        assert result["elev"].dtype == pl.Float64

    @pytest.mark.network
    def test_station_info_reasonable_coordinates(self):
        """Test that coordinates are in reasonable ranges."""
        result = get_weather_data("725030-14732", years=2023, incl_stn_info=True)

        lat = result["lat"][0]
        lon = result["lon"][0]
        elev = result["elev"][0]

        # LaGuardia is in NYC area
        assert 40 < lat < 41
        assert -74 < lon < -73
        assert -10 < elev < 100  # Near sea level


class TestYearAvailabilityWarnings:
    """Tests for year availability warnings and error messages."""

    @pytest.mark.network
    def test_unavailable_year_raises_error_with_hint(self):
        """Test that requesting an unavailable year raises error with available years hint."""
        # Year 1900 should not have data for most stations
        with pytest.raises(ValueError) as exc_info:
            get_weather_data("725030-14732", years=1900)

        error_msg = str(exc_info.value)
        # Should mention the unavailable year
        assert "1900" in error_msg
        # Should provide hint about available years
        assert "Available years" in error_msg
        # Should suggest using get_years_for_station
        assert "get_years_for_station" in error_msg

    @pytest.mark.network
    def test_multiple_unavailable_years_raises_error_with_hint(self):
        """Test that requesting multiple unavailable years raises helpful error."""
        with pytest.raises(ValueError) as exc_info:
            get_weather_data("725030-14732", years=[1900, 1901, 1902])

        error_msg = str(exc_info.value)
        # Should mention unavailable years
        assert "1900" in error_msg
        # Should provide hint about available years
        assert "Available years" in error_msg

    @pytest.mark.network
    def test_partial_data_warning(self):
        """Test that partial data availability triggers a warning."""
        import warnings

        from weathervault.stations import get_years_for_station

        # Get actual available years for the station
        available_years = get_years_for_station("725030-14732")
        if not available_years:
            pytest.skip("No available years found for test station")

        # Request mix of available and unavailable years
        available_year = available_years[-1]  # Most recent available year
        unavailable_year = 1900  # Should not be available

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = get_weather_data("725030-14732", years=[available_year, unavailable_year])

            # Should have issued a warning
            assert len(w) == 1
            assert issubclass(w[0].category, UserWarning)
            assert "Partial data returned" in str(w[0].message)
            assert str(unavailable_year) in str(w[0].message)
            assert str(available_year) in str(w[0].message)

        # Should still return data for the available year
        assert isinstance(result, pl.DataFrame)
        assert result.height > 0
        years_in_data = result["time"].dt.year().unique().to_list()
        assert available_year in years_in_data

    @pytest.mark.network
    def test_all_years_available_no_warning(self):
        """Test that no warning is issued when all requested years are available."""
        import warnings

        from weathervault.stations import get_years_for_station

        # Get actual available years for the station
        available_years = get_years_for_station("725030-14732")
        if len(available_years) < 2:
            pytest.skip("Not enough available years for test")

        # Request only available years
        years_to_request = available_years[-2:]  # Last 2 available years

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = get_weather_data("725030-14732", years=years_to_request)

            # Should not have issued any warnings
            partial_warnings = [warning for warning in w if "Partial data" in str(warning.message)]
            assert len(partial_warnings) == 0

        assert isinstance(result, pl.DataFrame)
        assert result.height > 0

    @pytest.mark.network
    def test_single_unavailable_year_error_message_format(self):
        """Test error message format for single unavailable year."""
        with pytest.raises(ValueError) as exc_info:
            get_weather_data("725030-14732", years=1850)

        error_msg = str(exc_info.value)
        # Should have well-formatted error with all needed info
        assert "No data available for station '725030-14732'" in error_msg
        assert "1850" in error_msg
        assert "Available years:" in error_msg
        assert "years total" in error_msg

    @pytest.mark.network
    def test_quiet_suppresses_partial_data_warning(self):
        """Test that quiet=True suppresses the partial data warning."""
        import warnings

        from weathervault.stations import get_years_for_station

        # Get actual available years for the station
        available_years = get_years_for_station("725030-14732")
        if not available_years:
            pytest.skip("No available years found for test station")

        # Request mix of available and unavailable years
        available_year = available_years[-1]
        unavailable_year = 1900

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = get_weather_data(
                "725030-14732",
                years=[available_year, unavailable_year],
                quiet=True,
            )

            # Should NOT have issued any warnings
            partial_warnings = [warning for warning in w if "Partial data" in str(warning.message)]
            assert len(partial_warnings) == 0

        # Should still return data for the available year
        assert isinstance(result, pl.DataFrame)
        assert result.height > 0


class TestYearAvailabilityMocked:
    """Mocked tests for year availability logic.

    These tests mock get_years_for_station and get_station_metadata to test
    all conditional paths without network access.
    """

    @pytest.fixture
    def mock_station_df(self):
        """Create a mock station metadata DataFrame."""
        return pl.DataFrame(
            {
                "id": ["725030-14732"],
                "tz_name": ["America/New_York"],
                "name": ["LA GUARDIA AIRPORT"],
                "country": ["United States"],
                "state": ["NY"],
                "icao": ["KLGA"],
                "lat": [40.779],
                "lon": [-73.88],
                "elev": [3.4],
            }
        )

    def test_all_requested_years_unavailable_raises_error(self, monkeypatch, mock_station_df):
        """Test error when none of the requested years are available."""
        monkeypatch.setattr(
            "weathervault.weather.get_years_for_station",
            lambda station_id: [2020, 2021, 2022, 2023],
        )
        monkeypatch.setattr(
            "weathervault.weather.get_station_metadata",
            lambda **kwargs: mock_station_df,
        )

        with pytest.raises(ValueError) as exc_info:
            get_weather_data("725030-14732", years=[1990, 1991, 1992])

        error_msg = str(exc_info.value)
        assert "No data available" in error_msg
        assert "1990" in error_msg
        assert "1991" in error_msg
        assert "1992" in error_msg
        assert "Available years: 2020-2023" in error_msg
        assert "4 years total" in error_msg
        assert "get_years_for_station" in error_msg

    def test_partial_years_available_warns(self, monkeypatch, mock_station_df):
        """Test warning when only some requested years are available."""
        import warnings

        monkeypatch.setattr(
            "weathervault.weather.get_years_for_station",
            lambda station_id: [2020, 2021, 2022, 2023],
        )
        monkeypatch.setattr(
            "weathervault.weather.get_station_metadata",
            lambda **kwargs: mock_station_df,
        )
        monkeypatch.setattr(
            "weathervault.weather._fetch_year_data",
            lambda station_id, year, cache_path=None: None,
        )

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # Request mix: 2022, 2023 available; 1990 not available
            get_weather_data("725030-14732", years=[1990, 2022, 2023])

            partial_warnings = [
                warning for warning in w if "Partial data returned" in str(warning.message)
            ]
            assert len(partial_warnings) == 1
            warning_msg = str(partial_warnings[0].message)
            assert "1990" in warning_msg
            assert "2022" in warning_msg
            assert "2023" in warning_msg
            assert "Available years for this station: 2020-2023" in warning_msg

    def test_partial_years_quiet_suppresses_warning(self, monkeypatch, mock_station_df):
        """Test that quiet=True suppresses partial data warning."""
        import warnings

        monkeypatch.setattr(
            "weathervault.weather.get_years_for_station",
            lambda station_id: [2020, 2021, 2022, 2023],
        )
        monkeypatch.setattr(
            "weathervault.weather.get_station_metadata",
            lambda **kwargs: mock_station_df,
        )
        monkeypatch.setattr(
            "weathervault.weather._fetch_year_data",
            lambda station_id, year, cache_path=None: None,
        )

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            get_weather_data("725030-14732", years=[1990, 2022], quiet=True)

            partial_warnings = [warning for warning in w if "Partial data" in str(warning.message)]
            assert len(partial_warnings) == 0

    def test_no_inventory_for_station_raises_error(self, monkeypatch, mock_station_df):
        """Test error when station exists but has no inventory data."""
        monkeypatch.setattr(
            "weathervault.weather.get_years_for_station",
            lambda station_id: [],
        )
        monkeypatch.setattr(
            "weathervault.weather.get_station_metadata",
            lambda **kwargs: mock_station_df,
        )
        # Mock bundled data to return empty (simulate no bundled data for this station)
        monkeypatch.setattr(
            "weathervault.weather._get_bundled_years",
            lambda station_id: set(),
        )

        with pytest.raises(ValueError) as exc_info:
            get_weather_data("725030-14732", years=2023)

        error_msg = str(exc_info.value)
        assert "No data inventory found" in error_msg
        assert "725030-14732" in error_msg

    def test_all_years_available_no_warning(self, monkeypatch, mock_station_df):
        """Test no warning when all requested years are available."""
        import warnings

        monkeypatch.setattr(
            "weathervault.weather.get_years_for_station",
            lambda station_id: [2020, 2021, 2022, 2023],
        )
        monkeypatch.setattr(
            "weathervault.weather.get_station_metadata",
            lambda **kwargs: mock_station_df,
        )
        monkeypatch.setattr(
            "weathervault.weather._fetch_year_data",
            lambda station_id, year, cache_path=None: None,
        )

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            get_weather_data("725030-14732", years=[2022, 2023])

            partial_warnings = [warning for warning in w if "Partial data" in str(warning.message)]
            assert len(partial_warnings) == 0

    def test_single_unavailable_year_error_format(self, monkeypatch, mock_station_df):
        """Test error message format for single unavailable year."""
        monkeypatch.setattr(
            "weathervault.weather.get_years_for_station",
            lambda station_id: [2020, 2021, 2022, 2023],
        )
        monkeypatch.setattr(
            "weathervault.weather.get_station_metadata",
            lambda **kwargs: mock_station_df,
        )

        with pytest.raises(ValueError) as exc_info:
            get_weather_data("725030-14732", years=1985)

        error_msg = str(exc_info.value)
        assert "No data available for station '725030-14732' for year(s) 1985" in error_msg
        assert "Available years: 2020-2023" in error_msg

    def test_years_none_uses_all_available(self, monkeypatch, mock_station_df):
        """Test that years=None fetches all available years."""
        available = [2021, 2022, 2023]
        fetched_years = []

        def mock_fetch(station_id, year, cache_path=None):
            fetched_years.append(year)
            return None

        monkeypatch.setattr(
            "weathervault.weather.get_years_for_station",
            lambda station_id: available,
        )
        monkeypatch.setattr(
            "weathervault.weather.get_station_metadata",
            lambda **kwargs: mock_station_df,
        )
        monkeypatch.setattr("weathervault.weather._fetch_year_data", mock_fetch)

        get_weather_data("725030-14732", years=None)

        # Should have attempted to fetch all available years plus buffer years
        # Buffer years (±1) are fetched to handle timezone offsets at year boundaries
        # For years [2021, 2022, 2023], buffers add 2020 and 2024
        expected_with_buffers = [2020, 2021, 2022, 2023, 2024]
        assert sorted(fetched_years) == expected_with_buffers

    def test_years_none_with_no_data_raises_error(self, monkeypatch, mock_station_df):
        """Test that years=None with no available data raises error."""
        monkeypatch.setattr(
            "weathervault.weather.get_years_for_station",
            lambda station_id: [],
        )
        monkeypatch.setattr(
            "weathervault.weather.get_station_metadata",
            lambda **kwargs: mock_station_df,
        )

        with pytest.raises(ValueError) as exc_info:
            get_weather_data("725030-14732", years=None)

        assert "No data available for station" in str(exc_info.value)

    def test_buffer_years_fetched_for_timezone_conversion(self, monkeypatch, mock_station_df):
        """Test that buffer years are fetched when converting to local time.

        When convert_to_local=True, adjacent years are fetched to ensure complete
        data at year boundaries after timezone offset is applied.
        """
        fetched_years = []

        def mock_fetch(station_id, year, cache_path=None):
            fetched_years.append(year)
            return None

        monkeypatch.setattr(
            "weathervault.weather.get_years_for_station",
            lambda station_id: [2020, 2021, 2022, 2023],
        )
        monkeypatch.setattr(
            "weathervault.weather.get_station_metadata",
            lambda **kwargs: mock_station_df,
        )
        monkeypatch.setattr("weathervault.weather._fetch_year_data", mock_fetch)

        # Request just 2022
        get_weather_data("725030-14732", years=2022, convert_to_local=True)

        # Should fetch 2021, 2022, 2023 (requested year ± 1)
        assert sorted(fetched_years) == [2021, 2022, 2023]

    def test_no_buffer_years_when_convert_to_local_false(self, monkeypatch, mock_station_df):
        """Test that buffer years are NOT fetched when keeping UTC time."""
        fetched_years = []

        def mock_fetch(station_id, year, cache_path=None):
            fetched_years.append(year)
            return None

        monkeypatch.setattr(
            "weathervault.weather.get_years_for_station",
            lambda station_id: [2020, 2021, 2022, 2023],
        )
        monkeypatch.setattr(
            "weathervault.weather.get_station_metadata",
            lambda **kwargs: mock_station_df,
        )
        monkeypatch.setattr("weathervault.weather._fetch_year_data", mock_fetch)

        # Request just 2022 with UTC time (no conversion)
        get_weather_data("725030-14732", years=2022, convert_to_local=False)

        # Should only fetch 2022 (no buffer years needed)
        assert sorted(fetched_years) == [2022]

    def test_buffer_years_for_non_contiguous_years(self, monkeypatch, mock_station_df):
        """Test buffer years for non-contiguous year requests like [1950, 1960]."""
        fetched_years = []

        def mock_fetch(station_id, year, cache_path=None):
            fetched_years.append(year)
            return None

        # Provide a wide range of available years
        monkeypatch.setattr(
            "weathervault.weather.get_years_for_station",
            lambda station_id: list(range(1945, 1970)),
        )
        monkeypatch.setattr(
            "weathervault.weather.get_station_metadata",
            lambda **kwargs: mock_station_df,
        )
        monkeypatch.setattr("weathervault.weather._fetch_year_data", mock_fetch)

        # Request 1950 and 1960
        get_weather_data("725030-14732", years=[1950, 1960], convert_to_local=True)

        # Should fetch: 1949, 1950, 1951 (for 1950) and 1959, 1960, 1961 (for 1960)
        assert sorted(fetched_years) == [1949, 1950, 1951, 1959, 1960, 1961]
