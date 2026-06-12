import os
from binance.client import Client
from dotenv import load_dotenv


def get_client() -> Client:
    load_dotenv()

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        raise EnvironmentError(
            "BINANCE_API_KEY and BINANCE_API_SECRET must be set in your .env file."
        )

    # testnet=True routes all futures endpoints to https://testnet.binancefuture.com/fapi
    client = Client(api_key, api_secret, testnet=True)
    return client
