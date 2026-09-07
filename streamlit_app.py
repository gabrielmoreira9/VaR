import numpy as np
import pandas as pd
import streamlit as st

import main


st.set_page_config(
    page_title="Portfolio Analysis",
    page_icon="📈",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --navy: #071525;
        --navy-light: #10243a;
        --ink: #162333;
        --muted: #6b7785;
        --line: #dce3ea;
        --red: #c6283d;
        --red-dark: #982034;
        --paper: #f5f7fa;
    }

    html,
    body,
    .stApp {
        color-scheme: light !important;
    }

    .stApp {
        background: var(--paper);
        color: var(--ink);
    }

    .block-container {
        max-width: 1440px;
        padding-top: 3rem;
        padding-right: 3rem;
        padding-bottom: 3rem;
        padding-left: 3rem;
    }

    [data-testid="stHeader"] {
        background: #071525 !important;
        border-bottom: 1px solid #1b344d;
        height: 3.25rem;
    }

    [data-testid="stHeader"] button,
    [data-testid="stToolbar"] button,
    [data-testid="stToolbar"] svg,
    [data-testid="stToolbar"] path {
        color: #ffffff !important;
        fill: #ffffff !important;
        filter: none !important;
        stroke: #ffffff !important;
    }

    [data-testid="stToolbar"] {
        background: #071525 !important;
        border-radius: 5px;
        padding: 0.15rem 0.35rem;
    }

    [data-testid="stSidebar"] {
        background: var(--navy);
        border-right: 1px solid #1b344d;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }

    [data-testid="stSidebar"] * {
        color: #e8eef5 !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        color: #e8eef5 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: var(--navy-light);
        border-color: #2c4660;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] *,
    [data-testid="stSidebar"] [data-baseweb="popover"] * {
        background: var(--navy-light) !important;
        color: #e8eef5 !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        padding: 0.35rem 0;
        font-size: 0.9rem;
    }

    .sidebar-nav-title {
        border-bottom: 1px solid #2c4660;
        color: #aebdcb !important;
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.16em;
        margin: 1.65rem 0 0.7rem;
        padding-bottom: 0.55rem;
        text-transform: uppercase;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] > div {
        gap: 0.15rem;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        align-items: center;
        border-left: 2px solid transparent;
        border-radius: 6px;
        display: flex;
        margin: 0.1rem 0;
        padding: 0.58rem 0.65rem;
        transition: background 120ms ease, border-color 120ms ease;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: rgba(255, 255, 255, 0.045);
        border-left-color: #c6283d;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        background: rgba(198, 40, 61, 0.12);
        border-left-color: #c6283d;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label p {
        color: #e8eef5 !important;
        font-size: 0.86rem;
        font-weight: 600;
    }

    h1, h2, h3 {
        color: var(--navy);
        letter-spacing: -0.02em;
    }

    h1 {
        font-size: 2.25rem !important;
        font-weight: 700 !important;
        margin-top: 0 !important;
        margin-bottom: 0.4rem !important;
    }

    h2 {
        border-bottom: 2px solid var(--red);
        padding-bottom: 0.45rem;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }

    h3 {
        margin-top: 1.2rem !important;
        margin-bottom: 0.65rem !important;
    }

    .platform-kicker {
        color: var(--red);
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .platform-subtitle {
        color: var(--muted);
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    .metric-card {
        background: white;
        border: 1px solid var(--line);
        border-top: 3px solid var(--red);
        border-radius: 4px;
        padding: 1rem 1.15rem;
        box-shadow: 0 4px 16px rgba(7, 21, 37, 0.05);
    }

    .stButton > button {
        background: var(--red);
        border: 1px solid var(--red);
        border-radius: 3px;
        color: white;
        font-weight: 700;
        letter-spacing: 0.02em;
    }

    .stButton > button:hover {
        background: var(--red-dark);
        border-color: var(--red-dark);
        color: white;
    }

    [data-testid="column"] {
        min-width: 0;
        padding: 0.15rem 0.4rem;
    }

    [data-baseweb="input"],
    [data-baseweb="select"] {
        min-height: 42px;
    }

    [data-testid="stWidgetLabel"] {
        line-height: 1.25;
        margin-bottom: 0.3rem;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        box-shadow: 0 3px 12px rgba(7, 21, 37, 0.04);
    }

    .analysis-table {
        border-collapse: collapse;
        border: 1px solid #d7e0e8;
        border-radius: 8px;
        box-shadow: 0 5px 18px rgba(7, 21, 37, 0.06);
        margin: 0.75rem 0 1.5rem;
        overflow: hidden;
        width: 100%;
    }

    .analysis-table th {
        background: #0b1f33;
        color: #ffffff;
        font-size: 0.78rem;
        letter-spacing: 0.03em;
        padding: 0.8rem 0.9rem;
        text-align: left;
        white-space: nowrap;
    }

    .analysis-table td {
        background: #ffffff;
        border-bottom: 1px solid var(--line);
        color: var(--ink);
        font-size: 0.88rem;
        padding: 0.75rem 0.9rem;
    }

    .analysis-table tbody tr:nth-child(even) td {
        background: #f2f6f9;
    }

    .analysis-table tbody tr:last-child td {
        border-bottom: 0;
    }

    .duplicate-warning {
        background: #fff4e5;
        border: 1px solid #f0b866;
        border-left: 4px solid #c6283d;
        border-radius: 5px;
        color: #4a2a00 !important;
        font-size: 0.88rem;
        margin: 0.35rem 0 0.8rem;
        padding: 0.65rem 0.8rem;
    }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid var(--line);
        border-radius: 4px;
        padding: 0.75rem;
    }

    [data-testid="stAppViewContainer"] [data-testid="stWidgetLabel"] p,
    [data-testid="stAppViewContainer"] [data-testid="stWidgetLabel"] label {
        color: var(--ink) !important;
    }

    [data-testid="stAppViewContainer"] [data-baseweb="input"] input,
    [data-testid="stAppViewContainer"] [data-baseweb="select"] *,
    [data-testid="stAppViewContainer"] [data-baseweb="popover"] * {
        background: white !important;
        color: var(--ink) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def load_prices(ticker):
    return main.search_data(ticker)


def parse_number(value):
    return float(value.replace("$", "").replace(",", "").strip())


def format_number_input(key, integer=False):
    raw_value = st.session_state[key]
    try:
        number = parse_number(raw_value)
        if number < 0:
            raise ValueError
    except ValueError:
        st.session_state[key] = st.session_state[f"{key}_last"]
        return

    formatted = f"{int(number):,}" if integer else f"{number:,.2f}"
    st.session_state[key] = formatted
    st.session_state[f"{key}_last"] = formatted


def adjust_number_input(key, delta, maximum=None):
    try:
        current = parse_number(st.session_state[key])
    except ValueError:
        current = 0.0
    updated = max(current + delta, 0.0)
    if maximum is not None:
        updated = min(updated, maximum)
    formatted = f"{updated:,.2f}"
    st.session_state[key] = formatted
    st.session_state[f"{key}_last"] = formatted


def formatted_number_input(
    label,
    key,
    default,
    integer=False,
    help=None,
    placeholder=None,
):
    if key not in st.session_state:
        formatted_default = ""
        if default is not None:
            formatted_default = (
                f"{int(default):,}" if integer else f"{default:,.2f}"
            )
        st.session_state[key] = formatted_default
        st.session_state[f"{key}_last"] = formatted_default

    value = st.text_input(
        label,
        key=key,
        on_change=format_number_input,
        args=(key, integer),
        help=help,
        placeholder=placeholder,
    )
    try:
        return parse_number(value)
    except ValueError:
        return 0.0


def build_asset(ticker, price, invested, capital):
    returns = main.income(price)
    return {
        "ticker": ticker,
        "price": price,
        "returns": returns,
        "peso": invested / capital,
        "dollar_invested": invested,
        "statistic": main.statistics(returns),
    }


def portfolio_summary(capital, wallet):
    invested = sum(asset["dollar_invested"] for asset in wallet)
    return pd.DataFrame(
        [
            {
                "Ticker": asset["ticker"],
                "Weight": asset["peso"],
                "Invested": asset["dollar_invested"],
            }
            for asset in wallet
        ]
    ), invested, capital - invested


def render_table(table, include_index=False):
    if hasattr(table, "set_table_attributes"):
        html = table.set_table_attributes(
            'class="analysis-table"'
        ).to_html(index=include_index)
    else:
        html = pd.DataFrame(table).style.set_table_attributes(
            'class="analysis-table"'
        ).to_html(index=include_index)
    st.markdown(html, unsafe_allow_html=True)


def calculate_stress(capital, wallet, market_shock):
    benchmark_price = load_prices(main.BENCHMARK)
    if benchmark_price is None:
        asset_betas = {asset["ticker"]: 1.0 for asset in wallet}
        benchmark_status = "Benchmark unavailable; beta 1.0 was used."
    else:
        asset_betas = main.betas(wallet, main.income(benchmark_price))
        benchmark_status = f"Benchmark: {main.BENCHMARK}"

    rows = []
    total_loss = 0.0
    for asset in wallet:
        ticker = asset["ticker"]
        shock = asset_betas[ticker] * market_shock
        loss = asset["dollar_invested"] * shock
        total_loss += loss
        rows.append(
            {
                "Ticker": ticker,
                "Beta": asset_betas[ticker],
                "Shock": shock,
                "Loss": loss,
            }
        )

    return pd.DataFrame(rows), total_loss, benchmark_status


def render_chart(paths):
    try:
        import matplotlib.pyplot as plt
    except ImportError as error:
        raise RuntimeError(
            "Install matplotlib to use the charts page."
        ) from error

    final_values = paths[:, -1]
    days = np.arange(paths.shape[1])
    low_extreme = np.percentile(final_values, 5)
    high_extreme = np.percentile(final_values, 95)
    normal = (final_values > low_extreme) & (final_values < high_extreme)
    low = final_values <= low_extreme
    high = final_values >= high_extreme

    figure, axes = plt.subplots(
        1,
        2,
        figsize=(15, 8),
        dpi=150,
        gridspec_kw={"width_ratios": (1.7, 1)},
    )
    figure.subplots_adjust(
        left=0.06,
        right=0.97,
        bottom=0.12,
        top=0.92,
        wspace=0.24,
    )

    axes[0].plot(
        days,
        paths[normal][:120].T,
        color="#4C78A8",
        alpha=0.05,
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

    p05 = np.percentile(paths, 5, axis=0)
    p25 = np.percentile(paths, 25, axis=0)
    p50 = np.percentile(paths, 50, axis=0)
    p75 = np.percentile(paths, 75, axis=0)
    p95 = np.percentile(paths, 95, axis=0)
    axes[0].fill_between(
        days,
        p05,
        p95,
        color="#9ECAE1",
        alpha=0.28,
        label="Cone 5%-95%",
    )
    axes[0].fill_between(
        days,
        p25,
        p75,
        color="#3182BD",
        alpha=0.25,
        label="Majority 25%-75%",
    )
    axes[0].plot(days, p50, color="#08306B", linewidth=2, label="Median")
    axes[0].set_title("Monte Carlo simulated paths")
    axes[0].set_xlabel("Trading days")
    axes[0].set_ylabel("Portfolio value")
    axes[0].grid(
        True,
        color="#D9E2EC",
        linestyle="--",
        linewidth=0.6,
        alpha=0.7,
    )
    axes[0].set_axisbelow(True)
    axes[0].legend(fontsize=8)

    axes[1].hist(final_values, bins=80, color="#6BAED6", alpha=0.8)
    axes[1].axvline(
        np.percentile(final_values, 5),
        color="#F39C12",
        linestyle="--",
        label="5th percentile",
    )
    axes[1].axvline(
        np.percentile(final_values, 1),
        color="#D62728",
        linestyle="--",
        label="1st percentile",
    )
    axes[1].axvline(
        paths[0, 0],
        color="black",
        linestyle="--",
        label="Initial capital",
    )
    axes[1].set_title("Final value distribution")
    axes[1].set_xlabel("Final value")
    axes[1].set_ylabel("Frequency")
    axes[1].grid(
        True,
        axis="y",
        color="#D9E2EC",
        linestyle="--",
        linewidth=0.6,
        alpha=0.7,
    )
    axes[1].set_axisbelow(True)
    axes[1].legend(fontsize=8)
    return figure


def require_portfolio():
    if not st.session_state.wallet:
        st.warning("Create a portfolio first.")
        return False
    return True


if "capital" not in st.session_state:
    st.session_state.capital = 0.0
if "wallet" not in st.session_state:
    st.session_state.wallet = []
if "final_value" not in st.session_state:
    st.session_state.final_value = None
if "paths" not in st.session_state:
    st.session_state.paths = None


st.markdown('<div class="platform-kicker">Investment Research / Risk Platform</div>',
            unsafe_allow_html=True)
st.title("Portfolio Analysis")
st.markdown(
    '<div class="platform-subtitle">Market intelligence, portfolio construction and risk analytics</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        '<div class="platform-kicker">Portfolio Desk</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sidebar-nav-title">Research modules</div>',
        unsafe_allow_html=True,
    )
    page = st.radio(
        " ",
        [
            "Create Portfolio",
            "Asset Statistics",
            "Correlation",
            "Monte Carlo",
            "Risk Metrics",
            "Charts",
            "Stress Test",
        ],
        label_visibility="collapsed",
    )

    if st.session_state.wallet:
        st.divider()
        st.subheader("Current portfolio")
        st.write(
            ", ".join(
                asset["ticker"] for asset in st.session_state.wallet
            )
        )


if page == "Create Portfolio":
    st.header("Create Portfolio")
    capital = formatted_number_input(
        "Total capital ($)",
        "capital_input",
        st.session_state.capital if st.session_state.capital > 0 else None,
        help="Enter a number. It will be formatted with thousands separators.",
        placeholder="1,000.00",
    )

    quantity = st.number_input(
        "Number of assets",
        min_value=1,
        max_value=20,
        value=1,
        step=1,
    )

    ticker_suggestions = [
        "NVDA",
        "MSFT",
        "AAPL",
        "AMZN",
        "GOOGL",
        "META",
        "AVGO",
        "TSLA",
        "NFLX",
        "COST",
        "AMD",
        "PLTR",
        "CSCO",
        "LIN",
        "QCOM",
        "AMAT",
        "INTU",
        "MU",
        "TXN",
        "PEP",
        "ADI",
        "ISRG",
        "AMGN",
        "BKNG",
        "CMCSA",
        "BTC-USD",
        "ETH-USD",
        "USDT-USD",
        "BNB-USD",
        "XRP-USD",
        "Other",
    ]
    allocation_mode = st.selectbox(
        "Allocation type for all assets",
        ["Percentage", "Dollar"],
        key="allocation_mode_global",
    )
    st.caption(
        "The selected allocation type applies to every asset in this portfolio."
    )

    entries = []
    allocated_so_far = 0.0
    selected_symbols = []
    for index in range(int(quantity)):
        st.subheader(f"Asset {index + 1}")
        remaining_capital = max(capital - allocated_so_far, 0.0)
        remaining_percentage = (
            remaining_capital / capital * 100 if capital > 0 else 0.0
        )
        st.caption(
            f"Available for this asset: $ {remaining_capital:,.2f} "
            f"({remaining_percentage:.2f}%)"
        )
        ticker, value = st.columns([2, 2])
        with ticker:
            suggestion = st.selectbox(
                "Ticker",
                ticker_suggestions,
                key=f"ticker_suggestion_{index}",
            )
            if suggestion == "Other":
                symbol = st.text_input(
                    "Other ticker",
                    key=f"custom_ticker_{index}",
                    placeholder="AAPL",
                )
            else:
                symbol = suggestion
        with value:
            if allocation_mode == "Percentage":
                allocation_value = formatted_number_input(
                    "Allocation (%)",
                    f"allocation_percentage_masked_{index}",
                    None,
                    help=(
                        f"Enter up to {remaining_percentage:.2f}%. "
                        "Use increments of 10% when allocating."
                    ),
                    placeholder="10.00",
                )
                plus, minus = st.columns(2)
                with plus:
                    st.button(
                        "+10%",
                        key=f"allocation_plus_masked_{index}",
                        on_click=adjust_number_input,
                        args=(
                            f"allocation_percentage_masked_{index}",
                            10.0,
                            remaining_percentage,
                        ),
                    )
                with minus:
                    st.button(
                        "-10%",
                        key=f"allocation_minus_masked_{index}",
                        on_click=adjust_number_input,
                        args=(
                            f"allocation_percentage_masked_{index}",
                            -10.0,
                        ),
                    )
            else:
                allocation_value = formatted_number_input(
                    "Allocation ($)",
                    f"allocation_dollar_masked_{index}",
                    None,
                    help="Enter a number. It will be formatted automatically.",
                    placeholder="1,000.00",
                )
        entries.append((symbol, allocation_mode, allocation_value))
        selected_symbols.append(symbol.strip().upper())
        invested = (
            capital * float(allocation_value) / 100
            if allocation_mode == "Percentage"
            else float(allocation_value)
        )
        allocated_so_far += invested

        if symbol.strip().upper() in selected_symbols[:-1] and symbol.strip():
            st.markdown(
                f'<div class="duplicate-warning">'
                f"{symbol.upper()} is already selected for another asset."
                "</div>",
                unsafe_allow_html=True,
            )

    st.info(
        f"Remaining allocation: $ {max(capital - allocated_so_far, 0.0):,.2f} "
        f"({max(100 - allocated_so_far / capital * 100, 0.0) if capital > 0 else 0.0:.2f}%)"
    )

    submitted = st.button("Create portfolio")

    if submitted:
        allocations = []
        total_invested = 0.0
        error = None
        seen_symbols = set()
        for symbol, mode, value in entries:
            symbol = symbol.strip().upper()
            value = float(value)
            if not symbol or value <= 0:
                error = "Every asset needs a ticker and a positive allocation."
                break
            if symbol in seen_symbols:
                error = f"{symbol} cannot be selected more than once."
                break
            seen_symbols.add(symbol)
            if mode == "Percentage" and not 0 <= value <= 100:
                error = "Percentage allocation must be between 0% and 100%."
                break
            invested = capital * value / 100 if mode == "Percentage" else value
            allocations.append((symbol, invested))
            total_invested += invested

        if error is None and capital <= 0:
            error = "Enter a valid capital amount."
        if error is None and total_invested > capital:
            error = "Total allocation cannot exceed the available capital."
        if error:
            st.error(error)
        else:
            wallet = []
            progress = st.progress(0)
            for index, (symbol, invested) in enumerate(allocations):
                price = load_prices(symbol)
                if price is None:
                    error = f"No data found for {symbol}."
                    break
                wallet.append(build_asset(symbol, price, invested, capital))
                progress.progress((index + 1) / len(allocations))

            if error:
                st.error(error)
            else:
                st.session_state.capital = capital
                st.session_state.wallet = wallet
                st.session_state.final_value = None
                st.session_state.paths = None
                st.success("Portfolio created successfully.")

if page == "Asset Statistics" and require_portfolio():
    st.header("Asset Statistics")
    st.info(
        "This table summarizes the main historical parameters of each asset. "
        "Weight is the share of total capital allocated to the asset. Daily "
        "return and volatility describe typical one-day behavior. Annualized "
        "return compounds the average daily return over 252 trading days, "
        "while annualized volatility scales daily volatility by the square "
        "root of 252. Higher return can come with higher volatility and risk."
    )
    rows = []
    for asset in st.session_state.wallet:
        data = asset["statistic"]
        rows.append(
            {
                "Ticker": asset["ticker"],
                "Weight": asset["peso"],
                "Daily return": data["Returns"].mean(),
                "Daily volatility": data["Volatility"],
                "Annualized return": data["Returns_annualized"],
                "Annualized volatility": data["Volatility_annualized"],
            }
        )
    render_table(
        pd.DataFrame(rows).style.format(
            {
                "Weight": "{:.2%}",
                "Daily return": "{:.4%}",
                "Daily volatility": "{:.4%}",
                "Annualized return": "{:.2%}",
                "Annualized volatility": "{:.2%}",
            }
        ).hide(axis="index")
    )

if page == "Correlation" and require_portfolio():
    st.header("Correlation Matrix")
    st.info(
        "A correlation matrix measures how two assets move in relation to "
        "each other. Values range from -1 to 1: values near 1 indicate that "
        "assets tend to move together, values near -1 indicate opposite "
        "movement, and values near 0 indicate little linear relationship. "
        "Lower or negative correlations can improve diversification, while "
        "high positive correlations can concentrate portfolio risk."
    )
    render_table(
        main.correlation(st.session_state.wallet)
        .style.format("{:.3f}", na_rep="0.000"),
        include_index=True,
    )

if page == "Monte Carlo" and require_portfolio():
    st.header("Monte Carlo Simulation")
    st.info(
        "Monte Carlo simulation generates many possible portfolio outcomes "
        "by repeatedly sampling returns from the historical mean, volatility "
        "and covariance of your assets. The number of simulations is the "
        "number of scenarios calculated: more scenarios generally produce a "
        "smoother distribution, but take longer to compute. These scenarios "
        "are estimates based on historical behavior, not guaranteed forecasts."
    )
    simulations = formatted_number_input(
        "Number of simulations",
        "simulations_input",
        10_000,
        integer=True,
        help="Enter an integer between 100 and 100,000.",
    )
    if not 100 <= simulations <= 100_000:
        st.error("Number of simulations must be between 100 and 100,000.")
    if st.button("Run Monte Carlo"):
        if not 100 <= simulations <= 100_000:
            st.stop()
        _, final_value, _ = main.monte_carlo(
            st.session_state.capital,
            st.session_state.wallet,
            int(simulations),
        )
        st.session_state.final_value = final_value
        st.success("Simulation completed.")
        st.metric("Mean final value", f"$ {np.mean(final_value):,.2f}")
        mean_return = np.mean(final_value / st.session_state.capital - 1)
        probability_loss = np.mean(
            final_value < st.session_state.capital
        )
        percentile_5 = np.percentile(final_value, 5)
        st.info(
            f"Interpretation: the simulation estimates an average return of "
            f"{mean_return:.2%}. The 5th percentile is "
            f"$ {percentile_5:,.2f}, meaning approximately 95% of simulated "
            f"outcomes were above this value. The probability of ending below "
            f"the initial capital was {probability_loss:.2%}. These are "
            "statistical scenarios based on historical returns, not forecasts "
            "or guarantees."
        )

if page == "Risk Metrics" and require_portfolio():
    st.header("Risk Metrics")
    st.info(
        "These metrics summarize the distribution of simulated portfolio "
        "values. VaR estimates the potential loss at the 95% and 99% "
        "confidence levels, while probability of loss measures how often a "
        "simulation ends below the initial capital. Risk metrics can only be "
        "evaluated after running the Monte Carlo simulation."
    )
    if st.session_state.final_value is None:
        st.warning(
            "Run Monte Carlo first. The risk metrics are unavailable until "
            "the simulation has been completed."
        )
    else:
        data = main.risk(
            st.session_state.capital,
            st.session_state.final_value,
        )
        metrics = {
            "Mean return": data["Return_mean"],
            "Median": data["Median"],
            "Maximum": data["Max"],
            "Worst case": data["Worst"],
            "VaR 95%": data["VaR_95"],
            "VaR 99%": data["VaR_99"],
            "Probability of loss": data["Prob_loss"],
            "Mean loss value": data["Mean_loss"],
        }
        risk_rows = [
            {"Metric": "Mean return", "Value": f"{data['Return_mean']:.2%}"},
            {"Metric": "Median", "Value": f"$ {data['Median']:,.2f}"},
            {"Metric": "Maximum", "Value": f"$ {data['Max']:,.2f}"},
            {"Metric": "Worst case", "Value": f"$ {data['Worst']:,.2f}"},
            {"Metric": "VaR 95%", "Value": f"$ {data['VaR_95']:,.2f}"},
            {"Metric": "VaR 99%", "Value": f"$ {data['VaR_99']:,.2f}"},
            {
                "Metric": "Probability of loss",
                "Value": f"{data['Prob_loss']:.2%}",
            },
            {"Metric": "Mean loss value", "Value": f"$ {data['Mean_loss']:,.2f}"},
        ]
        render_table(
            pd.DataFrame(risk_rows).style.hide(axis="index")
        )

if page == "Charts" and require_portfolio():
    st.header("Monte Carlo Charts")
    st.info(
        "The chart shows simulated portfolio paths over five years. The "
        "shaded bands represent percentile ranges: the 25%-75% band contains "
        "the central half of scenarios, while the 5%-95% cone captures a "
        "broader range of outcomes. The median line represents the middle "
        "scenario, not a guaranteed expected return. Wider cones indicate "
        "greater uncertainty and risk dispersion."
    )
    if st.button("Generate five-year paths"):
        with st.spinner("Generating simulations..."):
            st.session_state.paths = main.simulate_paths(
                st.session_state.capital,
                st.session_state.wallet,
            )
    if st.session_state.paths is not None:
        st.pyplot(
            render_chart(st.session_state.paths),
            use_container_width=True,
        )
    else:
        st.info("Generate the paths to display the charts.")

if page == "Stress Test" and require_portfolio():
    st.header("Beta-based Stress Test")
    st.info(
        "The stress test applies a market decline to the portfolio and "
        "adjusts each asset's impact by its beta against the S&P 500. Beta "
        "above 1.0 indicates greater historical sensitivity than the market; "
        "beta below 1.0 indicates lower sensitivity. The available scenarios "
        "are market declines of 10%, 20%, 30%, 40% and 50%."
    )
    selected_shock = st.selectbox(
        "Market shock",
        list(main.CRASH_OPTIONS),
        format_func=lambda option: (
            f"{abs(main.CRASH_OPTIONS[option]):.0%} market decline"
        ),
    )
    if st.button("Run stress test"):
        table, total_loss, status = calculate_stress(
            st.session_state.capital,
            st.session_state.wallet,
            main.CRASH_OPTIONS[selected_shock],
        )
        st.caption(status)
        render_table(
            table.style.format(
                {"Beta": "{:.2f}", "Shock": "{:.2%}", "Loss": "$ {:,.2f}"}
            ).hide(axis="index")
        )
        final_value = st.session_state.capital + total_loss
        st.metric("Value after shock", f"$ {final_value:,.2f}")
        st.metric(
            "Drawdown",
            f"{total_loss / st.session_state.capital:.2%}",
        )
