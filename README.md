# Binance Futures Testnet CLI Trading Bot

A command-line trading bot for Binance USDT-M Perpetual Futures on the **testnet** environment.

---

## Setup

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get testnet API keys

1. Visit [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Log in (GitHub account works)
3. Navigate to **API Key** in the top-right menu
4. Generate an API Key + Secret and copy them

### 4. Configure your environment

```bash
cp .env.example .env
# Open .env and paste your keys
```

`.env`:
```
BINANCE_API_KEY=your_actual_key
BINANCE_API_SECRET=your_actual_secret
```

---

## Usage

Run all commands from the `trading_bot/` directory:

```bash
python cli.py --symbol <SYMBOL> --side <BUY|SELL> --type <TYPE> --quantity <QTY> [options]
```

### Options

| Flag | Required | Description |
|------|----------|-------------|
| `--symbol` | ✅ | Trading pair, e.g. `BTCUSDT` |
| `--side` | ✅ | `BUY` or `SELL` |
| `--type` | ✅ | `MARKET`, `LIMIT`, `STOP_MARKET`, or `STOP_LIMIT` |
| `--quantity` | ✅ | Order size in base asset |
| `--price` | LIMIT / STOP_LIMIT | Limit price |
| `--stop-price` | STOP_MARKET / STOP_LIMIT | Trigger price |
| `--tif` | No | Time-in-force (default: `GTC`) |

---

## Examples

> **Note:** Prices and quantities below are illustrative. Always check current testnet orderbook prices before placing orders.

### MARKET — Buy 0.01 BTC

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### MARKET — Sell 0.01 BTC

```bash
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.01
```

### LIMIT — Buy 0.01 BTC at $60,000

```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.01 --price 60000
```

### LIMIT — Sell 0.01 BTC at $70,000

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 70000
```

### STOP_MARKET — Sell 0.01 BTC when price drops to $58,000

```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.01 --stop-price 58000
```

### STOP_MARKET — Buy 0.01 BTC when price rises to $72,000 (breakout)

```bash
python cli.py --symbol BTCUSDT --side BUY --type STOP_MARKET --quantity 0.01 --stop-price 72000
```

### STOP_LIMIT — Sell 0.01 BTC, trigger at $58,000, limit at $57,800

```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_LIMIT --quantity 0.01 \
  --stop-price 58000 --price 57800
```

### STOP_LIMIT — Buy 0.01 BTC, trigger at $72,000, limit at $72,200

```bash
python cli.py --symbol BTCUSDT --side BUY --type STOP_LIMIT --quantity 0.01 \
  --stop-price 72000 --price 72200
```

---

## Assumptions

- **Testnet only** — all requests go to `https://testnet.binancefuture.com`. Do not use real API keys.
- **USDT-M Perpetual Futures** — only USDT-margined perpetual contracts are supported.
- **GTC default** — time-in-force defaults to `GTC` (Good Till Cancelled) for LIMIT and STOP_LIMIT orders.
- Quantities and prices must conform to the symbol's filter rules (tick size, lot size) on the testnet exchange.

---

## Logs

All requests and responses are written to `logs/trading_bot.log` and also printed to the console.
