# get-snirh

A Python package to automate the retrieval of water resource data from the Portuguese Environment Agency (SNIRH).

## Installation

```bash
pip install .
```

## Usage

### Basic Example

```python
from get_snirh import Snirh, Parameters

# Initialize the client
snirh = Snirh()

# 1. Get Stations
# Fetch all stations and filter by basin
stations = snirh.stations.get_stations_with_metadata(basin_filter=['RIBEIRAS DO ALGARVE'])
print(f"Found {len(stations)} stations.")

# Get the list of station codes (marker sites)
station_codes = stations['marker_site'].tolist()

# 2. Fetch Data
# Fetch daily rainfall data for the year 2023
df = snirh.data.get_timeseries(
    station_codes=station_codes[:5], # Limit to first 5 for demo
    parameter=Parameters.PRECIPITATION_DAILY,
    start_date='01/01/2023',
    end_date='31/12/2023'
)

print(df.head())

# 3. Save to CSV
df.to_csv('algarve_rainfall_2023.csv', index=False)
```

## Testing

To run the standard unit tests (mocked):
```bash
python -m unittest discover tests
```

To run the live integration tests (hits SNIRH servers):
```bash
RUN_LIVE_TESTS=1 python -m unittest tests/test_live.py
```

## Features

- **Automated Station Discovery**: Fetches the master list of stations and their metadata.
- **Data Retrieval**: Downloads time-series data for various parameters (Rainfall, Groundwater Level, Temperature, etc.).
- **Robust Parsing**: Handles SNIRH's specific CSV formats and encoding (ISO-8859-1).
- **Clean API**: Simple, object-oriented interface.

## Parameters

Available parameters in `get_snirh.Parameters`:
- `PRECIPITATION_DAILY`
- `PRECIPITATION_MONTHLY`
- `GWL_DEPTH`
- `AIR_TEMP_AVG_DAILY`
- And more...

## License

MIT
