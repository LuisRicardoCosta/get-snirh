import unittest
import os
from get_snirh import Snirh, Parameters

@unittest.skipUnless(os.getenv('RUN_LIVE_TESTS'), "Skipping live tests. Set RUN_LIVE_TESTS=1 to run.")
class TestLiveIntegration(unittest.TestCase):
    """
    These tests hit the actual SNIRH servers.
    They are skipped by default to prevent network dependency in standard test runs.
    """
    def setUp(self):
        self.snirh = Snirh(network='meteorologica')

    def test_fetch_stations_and_data(self):
        # 1. Fetch Stations
        print("\n[Live] Fetching station list...")
        # Using default bundled files (no arguments needed now)
        
        stations = self.snirh.stations.get_stations_with_metadata(
            basin_filter=['RIBEIRAS DO ALGARVE']
        )
        
        self.assertGreater(len(stations), 0, "Should find stations in Algarve")
        
        # Take the first station that likely has data (e.g., Faro or similar if possible, but first is fine)
        # We'll try to fetch data for the first 3 stations to increase chance of hitting one with data
        target_stations = stations.head(3)
        
        print(f"[Live] Fetching data for stations: {target_stations['estacao'].tolist()}")

        # 2. Fetch Data (Rainfall)
        # Use a recent short period (1 month)
        # Pass the DataFrame to test the new functionality
        df = self.snirh.data.get_timeseries(
            station_codes=target_stations,
            parameter=Parameters.PRECIPITATION_DAILY,
            start_date='01/01/2023',
            end_date='31/01/2023'
        )

        print(f"[Live] Fetched {len(df)} rows.")
        
        # Basic assertions
        self.assertIsNotNone(df)
        self.assertIn('site_name', df.columns)
        self.assertIn('value', df.columns)
        self.assertIn('date', df.columns)
        self.assertIn('parameter', df.columns)
        
        # If we got data, verify structure
        if not df.empty:
             # Check that site_name contains station names, not codes
             # We expect names like '3/N1' etc.
             first_id = df['site_name'].iloc[0]
             self.assertIn(first_id, target_stations['estacao'].values)
             
             # Check Parameter column
             self.assertEqual(df['parameter'].iloc[0], 'PRECIPITATION_DAILY')

             assert df.shape[0] > 0, "DataFrame should have rows of data"


if __name__ == '__main__':
    unittest.main()
