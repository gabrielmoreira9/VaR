import numpy as np
import pandas as pd
import yfinance as yf



PERIOD = "5y"
WORK_DAYS = 252
CRASH_OPTIONS = {1: -0.10, 2: -0.20, 3: -0.30, 4: -0.40, 5: -0.50}
BENCHMARK = "^GSPC"


def wants_to_exit(value):
    return value.strip().lower() == "exit"


def search_data(ticker):
    print(f"Searching data for {ticker}")
    try:
        data = yf.download(
            ticker,
            period=PERIOD,
            auto_adjust=True,
            progress=False,
        )
        if data.empty:
            print(f"No data found for {ticker}")
            return None

        if isinstance(data.columns, pd.MultiIndex):
            price = data["Close"].iloc[:, 0]
        else:
            price = data["Close"]

        price = price.dropna()
        if price.empty:
            print(f"No data found for {ticker}")
            return None
        return price
    except Exception as error:
        print(f"Error downloading {ticker}: {error}")
        return None


def income(price):
    return price.pct_change().dropna()


def statistics(returns):
    returns_mean = returns.mean()
    volatility = returns.std()
    return {
        "Returns": returns,
        "Volatility": volatility,
        "Returns_annualized": (1 + returns_mean) ** WORK_DAYS - 1,
        "Volatility_annualized": volatility * np.sqrt(WORK_DAYS),
    }


def betas(wallet, benchmark_returns):
    result = {}
    for asset in wallet:
        joint = pd.DataFrame(
            {"asset": asset["returns"], "market": benchmark_returns}
        ).dropna()

        market_variance = joint["market"].var()
        if len(joint) < 2 or market_variance == 0 or pd.isna(market_variance):
            print(
                f"Not enough common history for {asset['ticker']}; "
                "using beta = 1.0"
            )
            result[asset["ticker"]] = 1.0
            continue

        result[asset["ticker"]] = joint["asset"].cov(
            joint["market"]
        ) / market_variance
    return result


def create_wallet():
    while True:
        raw_capital = input("Enter the capital (or type 'exit'): ")
        if wants_to_exit(raw_capital):
            return None
        try:
            capital = float(raw_capital)
            if capital <= 0:
                print("Capital must be greater than 0")
                continue
            break
        except ValueError:
            print("Please enter a numeric value")

    while True:
        raw_quantity = input(
            "How many assets do you want to add? (or type 'exit'): "
        )
        if wants_to_exit(raw_quantity):
            return None
        try:
            quantity = int(raw_quantity)
            if quantity <= 0:
                print("Quantity must be greater than 0")
                continue
            break
        except ValueError:
            print("Please enter a numeric value")

    wallet = []
    remaining_capital = capital
    for index in range(quantity):
        print(f"\nAsset {index + 1}")
        remaining_percentage = remaining_capital / capital * 100
        print(
            f"Available capital: $ {remaining_capital:,.2f} "
            f"({remaining_percentage:.2f}% of total capital)"
        )
        while True:
            raw_ticker = input("Enter the ticker (or type 'exit'): ")
            if wants_to_exit(raw_ticker):
                return None
            ticker = raw_ticker.upper().strip()
            if not ticker:
                print("Please enter a ticker")
                continue
            price = search_data(ticker)
            if price is not None:
                break

        print("How do you want to define the position?")
        print("1 - Percentage")
        print("2 - Dollar")
        while True:
            change = input("Enter the option (or type 'exit'): ")
            if wants_to_exit(change):
                return None
            change = change.strip()
            if change in ("1", "2"):
                print(
                    "Selected position type: "
                    f"{'Percentage' if change == '1' else 'Dollar'}"
                )
                break
            print("Invalid input")

        while True:
            raw_value = input(
                "Enter the value "
                f"(up to {remaining_percentage:.2f}% or "
                f"$ {remaining_capital:,.2f}; type 'exit'): "
            )
            if wants_to_exit(raw_value):
                return None
            try:
                value = float(raw_value)
                if value <= 0:
                    print("Value must be greater than 0")
                    continue
                if change == "1":
                    if value > 100:
                        print("Percentage must be less than or equal to 100")
                        continue
                    peso = value / 100
                    dollar_invested = capital * peso
                else:
                    dollar_invested = value
                    peso = dollar_invested / capital

                if dollar_invested > remaining_capital:
                    print(f"Remaining capital: $ {remaining_capital:,.2f}")
                    print(
                        f"Remaining percentage: "
                        f"{remaining_capital / capital * 100:.2f}%"
                    )
                    print("Value higher than the available capital")
                    continue
                break
            except ValueError:
                print("Please enter a numeric value")

        returns = income(price)
        asset = {
            "ticker": ticker,
            "price": price,
            "returns": returns,
            "peso": peso,
            "dollar_invested": dollar_invested,
            "statistic": statistics(returns),
        }
        wallet.append(asset)
        remaining_capital -= dollar_invested
        print(f"{ticker} added to wallet")
        print(
            f"Remaining capital: $ {remaining_capital:,.2f} "
            f"({remaining_capital / capital * 100:.2f}% available)"
        )

    show_wallet(capital, wallet)
    return capital, wallet


def show_wallet(capital, wallet):
    invested = sum(asset["dollar_invested"] for asset in wallet)
    exposure = sum(asset["peso"] for asset in wallet)
    print("\nPortfolio")
    for asset in wallet:
        print(
            f"{asset['ticker']:<12}"
            f"{asset['peso'] * 100:>8.2f}%"
            f" $ {asset['dollar_invested']:>12,.2f}"
        )
    print(f"Invested: $ {invested:,.2f}")
    print(f"Cash on hand: $ {capital - invested:,.2f}")
    print(f"Exposure: {exposure * 100:.2f}%")


def matrix_returns(wallet):
    return pd.DataFrame(
        {asset["ticker"]: asset["returns"] for asset in wallet}
    ).dropna()


def monte_carlo(capital, wallet, simulation=100_000):
    return_df = matrix_returns(wallet)
    covariance_matrix = return_df.cov().values
    mean = return_df.mean().values
    weights = np.array([asset["peso"] for asset in wallet])
    simulated = np.random.multivariate_normal(
        mean, covariance_matrix, simulation
    )
    portfolio_returns = simulated @ weights
    final_value = capital * (1 + portfolio_returns)
    return portfolio_returns, final_value, covariance_matrix


def simulate_paths(
    capital,
    wallet,
    num_days=WORK_DAYS * 5,
    num_simulations=1_000,
):
    """Generate five-year daily portfolio paths."""
    return_df = matrix_returns(wallet)
    covariance_matrix = return_df.cov().values
    mean = return_df.mean().values
    weights = np.array([asset["peso"] for asset in wallet])

    simulated_returns = np.random.multivariate_normal(
        mean,
        covariance_matrix,
        size=(num_simulations, num_days),
    )
    portfolio_returns = simulated_returns @ weights
    paths = capital * np.cumprod(
        1 + portfolio_returns,
        axis=1,
    )
    paths = np.column_stack(
        [np.full(num_simulations, capital), paths]
    )
    return paths


def risk(capital, final_value):
    losses = final_value[final_value < capital]
    return {
        "Return_mean": np.mean(final_value / capital - 1),
        "Median": np.median(final_value),
        "Max": np.max(final_value),
        "Worst": np.min(final_value),
        "Percentile5": np.percentile(final_value, 5),
        "Percentile1": np.percentile(final_value, 1),
        "VaR_95": capital - np.percentile(final_value, 5),
        "VaR_99": capital - np.percentile(final_value, 1),
        "Prob_loss": np.mean(final_value < capital),
        "Mean_loss": np.mean(losses) if losses.size else capital,
    }


def show_statistics(wallet):
    for asset in wallet:
        data = asset["statistic"]
        print(f"\n{asset['ticker']}")
        print(f"Weight: {asset['peso'] * 100:.2f}%")
        print(f"Daily return: {data['Returns'].mean() * 100:.4f}%")
        print(f"Daily volatility: {data['Volatility'] * 100:.4f}%")
        print(
            f"Annualized return: "
            f"{data['Returns_annualized'] * 100:.4f}%"
        )
        print(
            f"Annualized volatility: "
            f"{data['Volatility_annualized'] * 100:.4f}%"
        )


def correlation(wallet):
    result = matrix_returns(wallet).corr()
    print("\nCorrelation matrix")
    print(result.round(3))
    return result


def show_risk(capital, wallet, risk_data):
    print("\nRisk metrics")
    print(f"Capital: $ {capital:,.2f}")
    print(
        f"Invested: $ "
        f"{sum(asset['dollar_invested'] for asset in wallet):,.2f}"
    )
    print(f"Mean return: {risk_data['Return_mean'] * 100:.2f}%")
    print(f"Median: $ {risk_data['Median']:,.2f}")
    print(f"Maximum: $ {risk_data['Max']:,.2f}")
    print(f"Worst case: $ {risk_data['Worst']:,.2f}")
    print(f"VaR 95%: $ {risk_data['VaR_95']:,.2f}")
    print(f"VaR 99%: $ {risk_data['VaR_99']:,.2f}")
    print(f"Probability of loss: {risk_data['Prob_loss'] * 100:.2f}%")
    print(f"Mean loss value: $ {risk_data['Mean_loss']:,.2f}")


def graphics(capital, final_value, paths):
    try:
        import matplotlib.pyplot as plt
    except ImportError as error:
        raise RuntimeError(
            "Install matplotlib to use the charts option."
        ) from error

    figure, axes = plt.subplots(
        1,
        2,
        figsize=(15, 8),
        gridspec_kw={"width_ratios": (1.7, 1)},
    )
    figure.subplots_adjust(
        left=0.06,
        right=0.97,
        bottom=0.12,
        top=0.92,
        wspace=0.24,
    )
    days = np.arange(paths.shape[1])
    final_values = paths[:, -1]
    low_extreme = np.percentile(final_values, 5)
    high_extreme = np.percentile(final_values, 95)

    normal = (final_values > low_extreme) & (final_values < high_extreme)
    low = final_values <= low_extreme
    high = final_values >= high_extreme
    normal_paths = paths[normal][:120]

    axes[0].plot(
        days,
        normal_paths.T,
        color="#4C78A8",
        alpha=0.045,
        linewidth=0.8,
    )
    axes[0].plot(
        days,
        paths[low].T,
        color="#D62728",
        alpha=0.22,
        linewidth=0.9,
        label="_nolegend_",
    )
    axes[0].plot(
        days,
        paths[high].T,
        color="#2CA02C",
        alpha=0.22,
        linewidth=0.9,
        label="_nolegend_",
    )
    axes[0].plot(
        [],
        [],
        color="#D62728",
        linewidth=2,
        label="Worst 5%",
    )
    axes[0].plot(
        [],
        [],
        color="#2CA02C",
        linewidth=2,
        label="Best 5%",
    )

    percentile_5_path = np.percentile(paths, 5, axis=0)
    percentile_25_path = np.percentile(paths, 25, axis=0)
    percentile_50_path = np.percentile(paths, 50, axis=0)
    percentile_75_path = np.percentile(paths, 75, axis=0)
    percentile_95_path = np.percentile(paths, 95, axis=0)
    axes[0].fill_between(
        days,
        percentile_5_path,
        percentile_95_path,
        color="#9ECAE1",
        alpha=0.28,
        label="Cone 5%-95%",
    )
    axes[0].fill_between(
        days,
        percentile_25_path,
        percentile_75_path,
        color="#3182BD",
        alpha=0.25,
        label="Majority 25%-75%",
    )
    axes[0].plot(
        days,
        percentile_50_path,
        color="#08306B",
        linewidth=2,
        label="Median",
    )
    axes[0].axhline(
        capital,
        color="black",
        linestyle="--",
        label="Initial capital",
    )
    axes[0].set_xlabel("Trading days (5 years)")
    axes[0].set_ylabel("Portfolio value")
    axes[0].set_title("Monte Carlo simulated paths")
    axes[0].legend(fontsize=8, loc="upper left")

    percentile_5 = np.percentile(final_value, 5)
    percentile_1 = np.percentile(final_value, 1)
    axes[1].hist(final_value, bins=100, color="skyblue", alpha=0.7)
    axes[1].axvline(
        percentile_5,
        color="orange",
        linestyle="--",
        label="5th percentile",
    )
    axes[1].axvline(
        percentile_1,
        color="red",
        linestyle="--",
        label="1st percentile",
    )
    axes[1].axvline(
        capital,
        color="black",
        linestyle="--",
        label="Initial capital",
    )
    axes[1].set_xlabel("Final value")
    axes[1].set_ylabel("Frequency")
    axes[1].set_title("Final value distribution")
    axes[1].legend(fontsize=8)
    plt.show()


def stress_test(capital, wallet):
    print("\nStress test")
    for option, shock in CRASH_OPTIONS.items():
        print(f"{option} - {abs(shock):.0%} down")

    while True:
        raw_option = input("Enter the option (or type 'exit'): ")
        if wants_to_exit(raw_option):
            return None
        try:
            option = int(raw_option)
            if option in CRASH_OPTIONS:
                print(
                    f"Selected stress scenario: "
                    f"{abs(CRASH_OPTIONS[option]):.0%} down"
                )
                break
            print("Invalid option")
        except ValueError:
            print("Please enter a numeric value")

    market_shock = CRASH_OPTIONS[option]
    benchmark_price = search_data(BENCHMARK)
    if benchmark_price is None:
        print(f"No data for {BENCHMARK}; falling back to beta = 1.0")
        asset_betas = {asset["ticker"]: 1.0 for asset in wallet}
    else:
        asset_betas = betas(wallet, income(benchmark_price))

    crashes = {
        ticker: beta * market_shock
        for ticker, beta in asset_betas.items()
    }
    total_loss = 0.0
    print(f"\nMarket shock: {market_shock:.0%} ({BENCHMARK})")
    for asset in wallet:
        ticker = asset["ticker"]
        loss = asset["dollar_invested"] * crashes[ticker]
        total_loss += loss
        print(
            f"{ticker:<12}"
            f" beta {asset_betas[ticker]:>6.2f}"
            f" shock {crashes[ticker]:>8.2%}"
            f" loss $ {loss:>12,.2f}"
        )

    final_value = capital + total_loss
    print(f"\nTotal loss: $ {total_loss:,.2f}")
    print(f"Value after shock: $ {final_value:,.2f}")
    print(f"Drawdown: {total_loss / capital:.2%}")
    return crashes, total_loss, final_value


def run_menu():
    capital = None
    wallet = []
    final_value = None

    while True:
        print("\n=== Portfolio Analysis ===")
        if wallet:
            tickers = ", ".join(asset["ticker"] for asset in wallet)
            print(f"Current portfolio: {tickers}")
        else:
            print("Current portfolio: not created")
        print("1 - Create portfolio")
        print("2 - View asset statistics")
        print("3 - Correlation")
        print("4 - Run Monte Carlo")
        print("5 - View VaR and risk metrics")
        print("6 - View charts")
        print("7 - Stress test")
        print("0 - Exit")
        option = input("Choose an option (or type 'exit'): ").strip()

        if option.lower() in {"0", "exit"}:
            print("Exiting.")
            break
        if option == "1":
            result = create_wallet()
            if result is not None:
                capital, wallet = result
                final_value = None
                print("Selected option: Create portfolio")
        elif option in {"2", "3", "4", "5", "6", "7"} and not wallet:
            print("Create a portfolio first.")
        elif option == "2":
            print("Selected option: View asset statistics")
            show_statistics(wallet)
        elif option == "3":
            print("Selected option: Correlation")
            correlation(wallet)
        elif option == "4":
            print("Selected option: Run Monte Carlo")
            _, final_value, _ = monte_carlo(capital, wallet)
            print(
                f"Monte Carlo completed. Mean final value: "
                f"$ {np.mean(final_value):,.2f}"
            )
        elif option == "5":
            print("Selected option: View VaR and risk metrics")
            if final_value is None:
                _, final_value, _ = monte_carlo(capital, wallet)
            show_risk(capital, wallet, risk(capital, final_value))
        elif option == "6":
            print("Selected option: View charts")
            paths = simulate_paths(capital, wallet)
            graphics(capital, paths[:, -1], paths)
        elif option == "7":
            print("Selected option: Stress test")
            stress_test(capital, wallet)
        else:
            print("Invalid option")


if __name__ == "__main__":
    run_menu()
