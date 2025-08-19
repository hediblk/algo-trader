import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os


REPORTS_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), "reports")


def configure_plots():
    """Configure matplotlib plots with better defaults"""
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 12
    sns.set_palette("viridis")


def save_figure(fig, filename, reports_dir=REPORTS_DIR, dpi=300):
    """Save a matplotlib figure to the reports directory"""
    os.makedirs(os.path.join(reports_dir, "figures"), exist_ok=True)
    filepath = os.path.join(reports_dir, "figures", filename)
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
    print(f"Figure saved to {filepath}")
    return filepath


def plot_price(data, ticker, save=True, normalized=False):
    """
    Plot stock price data using Plotly
    """

    fig = go.Figure()

    y_plot = data['close']
    y_name = 'Close Price'
    Y_axis_title = 'Price ($)'

    if normalized:
        y_plot = data['close'] / data['close'].iloc[0]
        y_name = 'Total Return'
        Y_axis_title = 'Total Return'
    

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=y_plot,
            name=y_name,
            line=dict(color='#2856f7', width=2),
        )
    )

    layout_args = dict(
        title=f'{ticker} Stock Analysis',
        height=600,
        width=1200,
        template='plotly_white',
        xaxis_rangeslider_visible=False,
        yaxis_title=Y_axis_title,
    )

    fig.update_layout(**layout_args)

    if save:
        output_path = os.path.join(
            REPORTS_DIR, "figures", f"{ticker}_price_plot.html")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        fig.write_html(output_path)
        print(f"Interactive plot saved to {output_path}")

    return fig


def plot_returns(data, ticker, save=False):
    """
    Plot distribution of returns

    Args:
        data (pd.DataFrame): Data with returns
        ticker (str): Stock ticker symbol
        save (bool): Whether to save the figure

    Returns:
        matplotlib.figure.Figure: Figure object
    """
    configure_plots()

    fig, axes = plt.subplots(3, 1, figsize=(12, 15))

    data['daily_log_return'] = np.log1p(data['close'].pct_change())
    data['volatility_20d'] = data['daily_log_return'].rolling(window=20).std()

    axes[0].plot(data.index, data['daily_log_return'], color='#2856f7', alpha=0.7)
    axes[0].set_title(f'{ticker} Log Returns',
                      fontsize=16, fontweight='bold')
    axes[0].set_ylabel('Return (%)', fontsize=14)
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(data.index, data['volatility_20d'],
                 color='#ff5733', alpha=0.8)
    axes[1].set_title(f'{ticker} 20-Day Volatility',
                      fontsize=16, fontweight='bold')
    axes[1].set_ylabel('Volatility', fontsize=14)
    axes[1].grid(True, alpha=0.3)

    sns.histplot(data['daily_log_return'].dropna(),
                 kde=True, ax=axes[2], color='#2856f7')
    axes[2].set_title(f'{ticker} Return Distribution',
                      fontsize=16, fontweight='bold')
    axes[2].set_xlabel('Return (%)', fontsize=14)
    axes[2].set_ylabel('Frequency', fontsize=14)

    from scipy import stats
    x = np.linspace(data['daily_log_return'].min(),
                    data['daily_log_return'].max(), 100)
    mu, std = stats.norm.fit(data['daily_log_return'].dropna())
    p = stats.norm.pdf(x, mu, std)
    axes[2].plot(x, p * (len(data) * (x[1]-x[0])), 'r--', linewidth=2)

    stats_text = (f'Mean: {mu:.4f}\nStd Dev: {std:.4f}\n'
                  f'Skew: {stats.skew(data["daily_log_return"].dropna()):.4f}\n'
                  f'Kurtosis: {stats.kurtosis(data["daily_log_return"].dropna()):.4f}')
    axes[2].text(0.05, 0.95, stats_text, transform=axes[2].transAxes,
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

    plt.tight_layout()

    if save:
        save_figure(fig, f"{ticker}_returns_distribution.png")

    data.drop(columns=['daily_log_return', 'volatility_20d'], inplace=True)

    return fig


def plot_corr(data, ticker, save=False):
    """
    Plot correlation matrix of features

    Args:
        data (pd.DataFrame): Data with features
        ticker (str): Stock ticker symbol
        save (bool): Whether to save the figure

    Returns:
        matplotlib.figure.Figure: Figure object
    """
    configure_plots()

    numeric_data = data.select_dtypes(include=[np.number])

    corr = numeric_data.corr()

    mask = np.triu(np.ones_like(corr, dtype=bool))

    fig, ax = plt.subplots(figsize=(16, 14))

    sns.heatmap(corr, mask=mask, annot=False, cmap='viridis',
                vmax=1, vmin=-1, center=0, square=True, linewidths=.5,
                cbar_kws={"shrink": .5})

    title = f"{ticker} Feature Correlation Matrix"

    plt.title(title, fontsize=16, fontweight='bold')

    plt.tight_layout()

    if save:
        save_figure(fig, f"{ticker}_correlation_matrix.png")

    return fig
