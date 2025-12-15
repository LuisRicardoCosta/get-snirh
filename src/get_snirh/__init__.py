import logging

# Configure default logging to INFO
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from .client import SnirhClient
from .stations import StationFetcher
from .data import DataFetcher
from .constants import Parameters
from .exceptions import SnirhError, SnirhNetworkError, SnirhParsingError

class Snirh:
    """
    Main entry point for the SNIRH package.
    """
    def __init__(self, network: str = "piezometria"):
        self.client = SnirhClient()
        self.stations = StationFetcher(self.client, network=network)
        self.data = DataFetcher(self.client)

__all__ = [
    'Snirh',
    'SnirhClient',
    'StationFetcher',
    'DataFetcher',
    'Parameters',
    'SnirhError',
    'SnirhNetworkError',
    'SnirhParsingError'
]
