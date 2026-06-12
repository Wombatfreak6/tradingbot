import argparse
import sys

from bot.client import get_client
from bot.logging_config import setup_logger
from bot.orders import OrderError, get_account_balance, place_order
from bot.validators import ValidationError, validate_order


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance Futures Testnet CLI trading bot",
    )
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
    parser.add_argument(
        "--type",
        dest="order_type",
        required=True,
        choices=["MARKET", "LIMIT", "STOP_MARKET", "STOP_LIMIT"],
        metavar="TYPE",
        help="Order type: MARKET | LIMIT | STOP_MARKET | STOP_LIMIT",
    )
    parser.add_argument("--quantity", required=True, type=float)
    parser.add_argument("--price", type=float, default=None, help="Limit price (LIMIT / STOP_LIMIT)")
    parser.add_argument("--stop-price", type=float, default=None, dest="stop_price", help="Trigger price (STOP_MARKET / STOP_LIMIT)")
    parser.add_argument("--tif", default="GTC", dest="time_in_force", help="Time-in-force (default: GTC)")
    return parser


def print_request_summary(args: argparse.Namespace) -> None:
    print("\n─── Order Request ────────────────────────────────────────")
    print(f"  Symbol    : {args.symbol}")
    print(f"  Side      : {args.side}")
    print(f"  Type      : {args.order_type}")
    print(f"  Quantity  : {args.quantity}")
    if args.price is not None:
        print(f"  Price     : {args.price}")
    if args.stop_price is not None:
        print(f"  Stop Price: {args.stop_price}")
    print(f"  TIF       : {args.time_in_force}")
    print("──────────────────────────────────────────────────────────\n")


def print_response_summary(response: dict) -> None:
    print("\n─── Order Response ───────────────────────────────────────")
    print(f"  Order ID    : {response.get('orderId', 'N/A')}")
    print(f"  Status      : {response.get('status', 'N/A')}")
    print(f"  Executed Qty: {response.get('executedQty', 'N/A')}")
    print(f"  Avg Price   : {response.get('avgPrice', 'N/A')}")
    if "cumQuote" in response:
        print(f"  Cum Quote   : {response['cumQuote']}")
    print("──────────────────────────────────────────────────────────\n")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    logger = setup_logger()

    try:
        validate_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
        )
    except ValidationError as exc:
        logger.error(f"Validation failed: {exc}")
        print(f"ORDER FAILED: {exc}")
        sys.exit(1)

    try:
        client = get_client()
    except EnvironmentError as exc:
        logger.error(f"Client setup failed: {exc}")
        print(f"ORDER FAILED: {exc}")
        sys.exit(1)

    print_request_summary(args)

    try:
        balance = get_account_balance(client)
        if balance is not None:
            print(f"  USDT Futures Balance: {balance:.2f} USDT\n")
        else:
            print("  USDT Futures Balance: unavailable\n")
    except Exception as exc:
        logger.error(f"Balance fetch error: {exc}")
        print("  USDT Futures Balance: unavailable (error fetching)\n")

    try:
        response = place_order(
            client=client,
            logger=logger,
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
            time_in_force=args.time_in_force,
        )
        print_response_summary(response)
        print("ORDER PLACED SUCCESSFULLY")
    except OrderError as exc:
        logger.error(f"Order placement failed: {exc}")
        print(f"ORDER FAILED: {exc}")
        sys.exit(1)
    except Exception as exc:
        logger.error(f"Unexpected error: {exc}")
        print(f"ORDER FAILED: Unexpected error — {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
