# Options Signal Research

An experimental quantitative-research project that uses Alpaca market data to explore MACD, RSI, Momentum, and moving-average crossover signals for stocks and their options. The framework is intended to work with any supported stock. Apple (`AAPL`) is the initial machine-learning training example because its long, liquid price history makes it a useful case study.

The long-term goal is to train an **unsupervised machine-learning model** on approximately 10 years of AAPL history, identify market regimes, and use those findings to produce research buy/sell signals for short-dated, in-the-money (ITM) options across stocks.

> **Research only â€” not investment advice.** This repository is a prototype. It does not place orders, does not prove profitability, and should not be used for live trading without thorough validation, risk controls, and paper-trading tests.

## Strategy concept

The proposed strategy combines momentum indicators with a MACD signal-line crossover:

| Component | Bullish / gold-cross setup | Bearish / death-cross setup |
| --- | --- | --- |
| MACD | MACD crosses **above** its signal line while MACD is below zero | MACD crosses **below** its signal line; the exact mirrored threshold is a research parameter |
| RSI (14) | Below 30, indicating an oversold condition | Mirrored overbought condition (for example, above 70) to be tested |
| Momentum (10) | Below 0.00, then recovering with the crossover | Mirrored positive / weakening momentum to be tested |
| Intended action | Research a near-the-money ITM call expiring about five calendar days later | Research an exit, bearish signal, or ITM put scenario; this must be defined before backtesting |

In plain language: look for an **oversold, negative-momentum environment**, then act only when MACD confirms a potential reversal through a gold cross. A death cross is the opposing confirmation and is intended to drive the sell/bearish side of the system.

The precise death-cross action is deliberately left configurable: selling an existing call, buying a put, or simply moving to cash are materially different strategies and need separate backtests.

## Current repository status

The current code is an early Alpaca-connected prototype:

- `indicators.py` calculates MACD (12, 26, 9), RSI (14), and Momentum (10) using `pandas-ta`.
- `check_resonance_signal()` currently detects a **gold cross** together with RSI above 50 and rising, plus positive and rising Momentum. This is not yet the requested oversold reversal rule.
- `options.py` finds an available ITM **call contract** nearest the current share price. It selects contracts that have not expired, but it does not yet enforce a five-day expiration target or retrieve option premiums.
- `main.py` polls recent one-minute bars from Alpaca. The symbol will be configurable as the project develops.
- Tests cover indicator behavior with mock candles and an optional Alpaca connectivity/data check.

## Research workflow

Use approximately 10 years of AAPL daily bars from Alpaca to train the initial ML model. The data will be cleaned and documented, including timestamps, corporate-action treatment, and source. From it, build features such as returns, volatility, volume, MACD, RSI, Momentum, and crossover state, then normalize them without using future information.

An unsupervised method—such as K-Means, a Gaussian Mixture Model, or HDBSCAN—will group the data into market regimes. It describes market conditions; it does **not** learn profitable buy/sell labels directly. The gold- and death-cross rules can then be evaluated by regime with walk-forward testing, first using the underlying share-price return as a proxy. Historical option quotes are required before reporting an options P&L.

## Important limitation: option prices

Option **contract metadata** (symbol, strike, expiration) is not enough to calculate an options backtest. A realistic test needs historical bid/ask or trade prices for each selected contract, plus a clear execution assumption. Until that data is available, this project can validate the signal logic only with an AAPL underlying-price proxyâ€”not an options P&L.

## Setup

Use Python 3.10+ in a virtual environment, then install the libraries used by the prototype:

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\\Scripts\\Activate.ps1

pip install alpaca-py alpaca-trade-api pandas pandas-ta pytest
```

Create a local `config.py` file (it is intentionally ignored by Git):

```python
API_KEY = "your_alpaca_key"
SECRET_KEY = "your_alpaca_secret"
BASE_URL = "https://paper-api.alpaca.markets"
```

Never commit API keys, secret keys, certificates, or brokerage credentials.

## Running the prototype

After configuring Alpaca credentials, run:

```bash
python main.py
```

Run the tests with:

```bash
pytest
```

The connectivity test needs valid Alpaca credentials and market-data access. The indicator mock test can be used independently of live account access.

## Roadmap

- [ ] Retrieve and prepare approximately ten years of AAPL historical bars for initial ML-model training.
- [ ] Implement the requested oversold gold-cross entry: MACD below zero, RSI below 30, Momentum below 0, followed by confirmation.
- [ ] Define and implement the corresponding death-cross exit/bearish rule.
- [ ] Add regime clustering and walk-forward evaluation.
- [ ] Add reproducible backtest reports and visualizations.
- [ ] Enforce approximately five days to expiration and ITM contract selection.
- [ ] Integrate historical options pricing before evaluating options returns.
- [ ] Add position sizing, stop-loss/exit rules, transaction costs, and paper-trading safeguards.

## Project structure

```text
.
â”œâ”€â”€ main.py          # Prototype polling loop and signal scan
â”œâ”€â”€ indicators.py    # MACD, RSI, Momentum, and gold-cross logic
â”œâ”€â”€ options.py       # ITM option-contract selection
â”œâ”€â”€ tests/           # Indicator and Alpaca connectivity tests
â””â”€â”€ README.md
```

## License

No license has been selected yet. Add one before distributing or reusing this project publicly.
