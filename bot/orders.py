import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException


class OrderError(Exception):
    pass


def place_order(
    client: Client,
    logger: logging.Logger,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None = None,
    stop_price: float | None = None,
    time_in_force: str = "GTC",
) -> dict:
    params: dict = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }

    # LIMIT and STOP (stop-limit) need a limit price and time-in-force
    if order_type in {"LIMIT", "STOP"}:
        params["price"] = price
        params["timeInForce"] = time_in_force

    # STOP_MARKET and STOP (stop-limit) need a trigger price.
    # Note: python-binance automatically renames stopPrice → triggerPrice for
    # conditional order types (STOP, STOP_MARKET) when routing to the algo endpoint.
    if order_type in {"STOP_MARKET", "STOP"}:
        params["stopPrice"] = stop_price

    logger.info(f"Placing order with params: {params}")

    try:
        response: dict = client.futures_create_order(**params)
    except BinanceAPIException as exc:
        logger.error(
            f"BinanceAPIException — status: {exc.status_code}, code: {exc.code}, message: {exc.message}"
        )
        raise OrderError(f"Binance API error {exc.code}: {exc.message}") from exc
    except BinanceRequestException as exc:
        logger.error(f"BinanceRequestException: {exc.message}")
        raise OrderError(f"Network/request error: {exc.message}") from exc

    logger.info(f"Order response: {response}")
    return response


def get_account_balance(client: Client) -> float | None:
    balances = client.futures_account_balance()
    for asset in balances:
        if asset.get("asset") == "USDT":
            return float(asset.get("balance", 0))
    return None
