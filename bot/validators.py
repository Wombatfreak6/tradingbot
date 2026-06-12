VALID_SIDES = {"BUY", "SELL"}
# Binance Futures API order types:
#   STOP       = stop-limit order (conditional; triggerPrice + limit price + timeInForce)
#   STOP_MARKET = stop-market order (conditional; triggerPrice only)
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET", "STOP"}
PRICE_REQUIRED_TYPES = {"LIMIT", "STOP"}
STOP_PRICE_REQUIRED_TYPES = {"STOP_MARKET", "STOP"}


class ValidationError(Exception):
    pass


def validate_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None = None,
    stop_price: float | None = None,
) -> None:
    if not symbol or not symbol.isalnum() or symbol != symbol.upper():
        raise ValidationError(
            f"Invalid symbol '{symbol}': must be a non-empty uppercase alphanumeric string."
        )

    if side not in VALID_SIDES:
        raise ValidationError(
            f"Invalid side '{side}': must be one of {sorted(VALID_SIDES)}."
        )

    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(
            f"Invalid order type '{order_type}': must be one of {sorted(VALID_ORDER_TYPES)}."
        )

    if not isinstance(quantity, (int, float)) or quantity <= 0:
        raise ValidationError(
            f"Invalid quantity '{quantity}': must be a positive number."
        )

    if order_type in PRICE_REQUIRED_TYPES:
        if price is None or price <= 0:
            raise ValidationError(
                f"Order type '{order_type}' requires a positive price."
            )

    if order_type in STOP_PRICE_REQUIRED_TYPES:
        if stop_price is None or stop_price <= 0:
            raise ValidationError(
                f"Order type '{order_type}' requires a positive stop_price."
            )
