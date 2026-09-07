# Portfolio Risk Analysis

A Python application for building an investment portfolio and analyzing its
risk using historical market data.

## Features

- Create a portfolio by percentage or dollar amount.
- Retrieve historical prices with `yfinance`.
- Analyze asset returns and volatility.
- Calculate the portfolio correlation matrix.
- Run Monte Carlo simulations.
- Simulate approximately five years of portfolio evolution using 1,260 trading days.
- Display a probability cone with:
  - The 5th to 95th percentile range.
  - The central 25th to 75th percentile range.
  - The median portfolio path.
  - Highlighted best and worst 5% scenarios.
- Calculate risk metrics and 95% and 99% Value at Risk (VaR).
- Run a beta-based stress test against the S&P 500 (`^GSPC`).
- Use `exit` to cancel an input and return to the menu.

## Requirements

- Python 3.9 or higher
- NumPy
- Pandas
- Matplotlib
- yfinance

Install the dependencies with:

```bash
pip install numpy pandas matplotlib yfinance
```

## Usage

Run the application with:

```bash
python main.py
```

The main menu provides the following options:

```text
1 - Create portfolio
2 - View asset statistics
3 - View correlation
4 - Run Monte Carlo
5 - View VaR and risk metrics
6 - View charts
7 - Run stress test
0 - Exit
```

During data entry, type `exit` to cancel the current operation and return to
the menu.

## Stress Test

The stress test applies a market shock selected by the user. The impact on
each asset is calculated as:

```text
asset shock = asset beta × market shock
```

Beta is estimated using the historical returns of each asset and the `^GSPC`
benchmark. If benchmark data is unavailable or there is not enough common
history, the application uses a beta of `1.0`.

## Notes

- Market data depends on Yahoo Finance availability and an internet
  connection.
- Simulations are statistical scenarios and do not guarantee future returns.
- Historical data is used to estimate returns, volatility, correlation, and
  beta.
