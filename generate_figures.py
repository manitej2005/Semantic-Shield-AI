"""
generate_figures.py

Extracts simulation records from the SQLite database at backend/semanticshield.db
and generates four publication-ready charts (PNG, 300 dpi) in the figures/ folder.

Charts generated:
1. figures/fig_5_6_decision_by_profile.png
   Grouped bar chart: count of VULNERABLE vs SAFE agent_decision values for each behavior_profile.
2. figures/fig_5_7_severity_distribution.png
   Bar chart: count of each threat_severity value.
3. figures/fig_5_8_confidence_by_profile.png
   Box plot: confidence_score for each behavior_profile.
4. figures/fig_5_9_avg_duration_by_profile.png
   Bar chart: mean duration_seconds per behavior_profile with values printed above each bar.

Styling:
- White background (#FFFFFF)
- Dark grey text (#333333)
- Grayscale / muted single-accent palette
- No gradients, no shadows, no 3D, no emojis
- Clear titles, labeled axes, integer/formatted ticks, and legends where applicable.
"""

import os
import sys
import sqlite3
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Color constants adhering to styling guidelines
TEXT_COLOR = '#333333'
SPINE_COLOR = '#CCCCCC'
GRID_COLOR = '#E5E7EB'
BG_COLOR = '#FFFFFF'

# Grayscale / muted palette
COLOR_DARK = '#374151'       # Dark slate grey for primary series (e.g. VULNERABLE)
COLOR_LIGHT = '#9CA3AF'      # Medium light grey for secondary series (e.g. SAFE)
COLOR_MUTED_BAR = '#4B5563'  # Muted grey for single-series bar charts
BOX_FACE = '#E5E7EB'         # Box plot fill
MEDIAN_COLOR = '#111827'     # High-contrast median line


def configure_matplotlib_defaults():
    """Configures global matplotlib styling rules."""
    plt.rcParams.update({
        'figure.facecolor': BG_COLOR,
        'axes.facecolor': BG_COLOR,
        'savefig.facecolor': BG_COLOR,
        'text.color': TEXT_COLOR,
        'axes.labelcolor': TEXT_COLOR,
        'axes.edgecolor': SPINE_COLOR,
        'xtick.color': TEXT_COLOR,
        'ytick.color': TEXT_COLOR,
        'font.size': 10,
        'axes.titlesize': 12,
        'axes.labelsize': 10,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'legend.fontsize': 9,
        'figure.titlesize': 13,
        'figure.dpi': 300,
        'font.family': 'sans-serif',
        'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica', 'sans-serif'],
    })


def validate_and_load_data(db_path: str) -> pd.DataFrame:
    """
    Validates existence of database file, simulations table, and required columns.
    Exits with a specific error message if any element is missing.
    """
    if not os.path.exists(db_path):
        print(f"[ERROR] Database file does not exist at: '{db_path}'", file=sys.stderr)
        sys.exit(1)

    try:
        conn = sqlite3.connect(db_path)
    except sqlite3.Error as err:
        print(f"[ERROR] Failed to connect to SQLite database '{db_path}': {err}", file=sys.stderr)
        sys.exit(1)

    cursor = conn.cursor()

    # 1. Check table existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='simulations';")
    table_match = cursor.fetchone()
    if not table_match:
        print("[ERROR] Table 'simulations' not found in database.", file=sys.stderr)
        conn.close()
        sys.exit(1)

    # 2. Check column existence
    cursor.execute("PRAGMA table_info(simulations);")
    table_info = cursor.fetchall()
    existing_columns = {col[1] for col in table_info}

    required_columns = [
        "behavior_profile",
        "agent_decision",
        "threat_severity",
        "confidence_score",
        "duration_seconds"
    ]
    missing_columns = [col for col in required_columns if col not in existing_columns]
    if missing_columns:
        print(f"[ERROR] Missing required column(s) in 'simulations' table: {', '.join(missing_columns)}", file=sys.stderr)
        conn.close()
        sys.exit(1)

    # 3. Read dataset
    query = """
    SELECT behavior_profile, agent_decision, threat_severity, confidence_score, duration_seconds
    FROM simulations
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        print("[ERROR] Table 'simulations' is empty (0 records found).", file=sys.stderr)
        sys.exit(1)

    return df


def format_profile_label(profile_name: str) -> str:
    """Converts snake_case profile names to Clean Title Case."""
    return profile_name.replace('_', ' ').title()


def plot_fig_5_6_decision_by_profile(df: pd.DataFrame, output_dir: str):
    """
    Figure 5.6: Grouped bar chart of the count of VULNERABLE vs SAFE agent_decision
    values for each behavior_profile.
    """
    # Canonical order if present, plus any additional profiles from DB
    known_order = ["trusting", "security_conscious", "overwhelmed", "executive"]
    existing_profiles = list(df["behavior_profile"].unique())
    profiles = [p for p in known_order if p in existing_profiles] + [p for p in existing_profiles if p not in known_order]
    profile_labels = [format_profile_label(p) for p in profiles]

    # Query counts from data
    crosstab = pd.crosstab(df["behavior_profile"], df["agent_decision"])
    
    # Ensure columns exist even if count is 0
    safe_counts = [int(crosstab.loc[p, "SAFE"]) if ("SAFE" in crosstab.columns and p in crosstab.index and "SAFE" in crosstab.loc[p]) else 0 for p in profiles]
    vuln_counts = [int(crosstab.loc[p, "VULNERABLE"]) if ("VULNERABLE" in crosstab.columns and p in crosstab.index and "VULNERABLE" in crosstab.loc[p]) else 0 for p in profiles]

    x = np.arange(len(profiles))
    width = 0.35

    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    ax.set_facecolor(BG_COLOR)

    # Bars: SAFE (light grey) and VULNERABLE (dark grey)
    rects_safe = ax.bar(x - width/2, safe_counts, width, label='Safe',
                        color=COLOR_LIGHT, edgecolor=TEXT_COLOR, linewidth=0.9)
    rects_vuln = ax.bar(x + width/2, vuln_counts, width, label='Vulnerable',
                        color=COLOR_DARK, edgecolor=TEXT_COLOR, linewidth=0.9)

    ax.set_title("Agent Decisions by Behavior Profile (Safe vs Vulnerable)", color=TEXT_COLOR, pad=12, fontweight='bold')
    ax.set_xlabel("Behavior Profile", color=TEXT_COLOR, labelpad=8)
    ax.set_ylabel("Count of Decisions", color=TEXT_COLOR, labelpad=8)
    ax.set_xticks(x)
    ax.set_xticklabels(profile_labels)

    # Upper y-limit with breathing room
    max_count = max(max(safe_counts), max(vuln_counts))
    ax.set_ylim(0, max_count + 3.5)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Add numeric labels on top of each bar
    ax.bar_label(rects_safe, padding=3, color=TEXT_COLOR, fontsize=8.5)
    ax.bar_label(rects_vuln, padding=3, color=TEXT_COLOR, fontsize=8.5)

    # Styling spines & grid
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.5, color=GRID_COLOR)
    ax.set_axisbelow(True)

    # Legend for multiple series
    legend = ax.legend(title="Agent Decision", title_fontsize=9, frameon=True,
                       facecolor=BG_COLOR, edgecolor=SPINE_COLOR)
    legend.get_title().set_color(TEXT_COLOR)
    for text in legend.get_texts():
        text.set_color(TEXT_COLOR)

    out_path = os.path.join(output_dir, "fig_5_6_decision_by_profile.png")
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"[OK] Generated: {out_path}")


def plot_fig_5_7_severity_distribution(df: pd.DataFrame, output_dir: str):
    """
    Figure 5.7: Bar chart of the count of each threat_severity value.
    """
    # Query exact counts directly from dataframe
    severity_counts = df["threat_severity"].value_counts().sort_index()
    categories = severity_counts.index.tolist()
    counts = severity_counts.values.tolist()

    x = np.arange(len(categories))
    width = 0.45

    fig, ax = plt.subplots(figsize=(5.5, 4.4))
    ax.set_facecolor(BG_COLOR)

    rects = ax.bar(x, counts, width, color=COLOR_MUTED_BAR, edgecolor=TEXT_COLOR, linewidth=0.9)

    ax.set_title("Distribution of Threat Severity Levels", color=TEXT_COLOR, pad=12, fontweight='bold')
    ax.set_xlabel("Threat Severity", color=TEXT_COLOR, labelpad=8)
    ax.set_ylabel("Count of Simulations", color=TEXT_COLOR, labelpad=8)
    ax.set_xticks(x)
    ax.set_xticklabels([cat.title() for cat in categories])

    max_count = max(counts)
    ax.set_ylim(0, max_count + 6)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Add numeric labels on top of each bar
    ax.bar_label(rects, padding=3, color=TEXT_COLOR, fontsize=9, fontweight='bold')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.5, color=GRID_COLOR)
    ax.set_axisbelow(True)

    out_path = os.path.join(output_dir, "fig_5_7_severity_distribution.png")
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"[OK] Generated: {out_path}")


def plot_fig_5_8_confidence_by_profile(df: pd.DataFrame, output_dir: str):
    """
    Figure 5.8: Box plot of confidence_score for each behavior_profile.
    """
    known_order = ["trusting", "security_conscious", "overwhelmed", "executive"]
    existing_profiles = list(df["behavior_profile"].unique())
    profiles = [p for p in known_order if p in existing_profiles] + [p for p in existing_profiles if p not in known_order]
    profile_labels = [format_profile_label(p) for p in profiles]

    # Data array for each profile
    data_by_profile = [df[df["behavior_profile"] == p]["confidence_score"].dropna().values for p in profiles]

    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    ax.set_facecolor(BG_COLOR)

    # Boxplot creation with muted grayscale styling
    bp = ax.boxplot(
        data_by_profile,
        tick_labels=profile_labels,
        patch_artist=True,
        widths=0.48,
        boxprops=dict(facecolor=BOX_FACE, color=TEXT_COLOR, linewidth=1.1),
        whiskerprops=dict(color=TEXT_COLOR, linewidth=1.1),
        capprops=dict(color=TEXT_COLOR, linewidth=1.1),
        medianprops=dict(color=MEDIAN_COLOR, linewidth=2.0),
        flierprops=dict(marker='o', markerfacecolor=TEXT_COLOR, markeredgecolor=TEXT_COLOR, markersize=5)
    )

    ax.set_title("Confidence Score Distribution by Behavior Profile", color=TEXT_COLOR, pad=12, fontweight='bold')
    ax.set_xlabel("Behavior Profile", color=TEXT_COLOR, labelpad=8)
    ax.set_ylabel("Confidence Score (%)", color=TEXT_COLOR, labelpad=8)

    # Set appropriate bounds for confidence scores (scores in data are 90-98)
    all_scores = df["confidence_score"].dropna()
    min_score = all_scores.min()
    max_score = all_scores.max()
    ax.set_ylim(min_score - 4, max_score + 3)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(2))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.5, color=GRID_COLOR)
    ax.set_axisbelow(True)

    out_path = os.path.join(output_dir, "fig_5_8_confidence_by_profile.png")
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"[OK] Generated: {out_path}")


def plot_fig_5_9_avg_duration_by_profile(df: pd.DataFrame, output_dir: str):
    """
    Figure 5.9: Bar chart of the mean duration_seconds per behavior_profile,
    with the value printed above each bar.
    """
    known_order = ["trusting", "security_conscious", "overwhelmed", "executive"]
    existing_profiles = list(df["behavior_profile"].unique())
    profiles = [p for p in known_order if p in existing_profiles] + [p for p in existing_profiles if p not in known_order]
    profile_labels = [format_profile_label(p) for p in profiles]

    # Calculate exact means from queried data
    mean_durations = [df[df["behavior_profile"] == p]["duration_seconds"].mean() for p in profiles]

    x = np.arange(len(profiles))
    width = 0.5

    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    ax.set_facecolor(BG_COLOR)

    rects = ax.bar(x, mean_durations, width, color=COLOR_MUTED_BAR, edgecolor=TEXT_COLOR, linewidth=0.9)

    ax.set_title("Average Simulation Duration by Behavior Profile", color=TEXT_COLOR, pad=12, fontweight='bold')
    ax.set_xlabel("Behavior Profile", color=TEXT_COLOR, labelpad=8)
    ax.set_ylabel("Mean Duration (seconds)", color=TEXT_COLOR, labelpad=8)
    ax.set_xticks(x)
    ax.set_xticklabels(profile_labels)

    max_mean = max(mean_durations)
    ax.set_ylim(0, max_mean * 1.18)

    # Print the value above each bar
    for rect, val in zip(rects, mean_durations):
        height = rect.get_height()
        ax.text(
            rect.get_x() + rect.get_width() / 2.0,
            height + (max_mean * 0.025),
            f"{val:.2f} s",
            ha='center',
            va='bottom',
            color=TEXT_COLOR,
            fontsize=9.5,
            fontweight='bold'
        )

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.5, color=GRID_COLOR)
    ax.set_axisbelow(True)

    out_path = os.path.join(output_dir, "fig_5_9_avg_duration_by_profile.png")
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"[OK] Generated: {out_path}")


def print_summary_table(df: pd.DataFrame):
    """
    Prints a formatted summary table of counts and averages to the console.
    """
    print("\n" + "=" * 80)
    print(" " * 24 + "SIMULATION DATA SUMMARY TABLE")
    print("=" * 80)

    # 1. Decision counts by profile
    print("\n[1] Agent Decision Counts by Behavior Profile:")
    ct = pd.crosstab(df["behavior_profile"], df["agent_decision"], margins=True, margins_name="Total")
    if "SAFE" not in ct.columns:
        ct["SAFE"] = 0
    if "VULNERABLE" not in ct.columns:
        ct["VULNERABLE"] = 0
    ct = ct[["SAFE", "VULNERABLE", "Total"]]
    ct.index = [format_profile_label(idx) if idx != "Total" else "TOTAL" for idx in ct.index]
    print(ct.to_string())

    # 2. Threat severity distribution
    print("\n[2] Threat Severity Distribution:")
    sev_counts = df["threat_severity"].value_counts()
    sev_pct = (sev_counts / len(df) * 100.0)
    sev_table = pd.DataFrame({
        "Count": sev_counts,
        "Percentage (%)": sev_pct.round(2)
    })
    sev_table.index.name = "Threat Severity"
    print(sev_table.to_string())

    # 3. Confidence score summary by profile
    print("\n[3] Confidence Score Statistics by Behavior Profile:")
    conf_summary = df.groupby("behavior_profile")["confidence_score"].agg(
        Count="count",
        Mean="mean",
        Std="std",
        Min="min",
        Median="median",
        Max="max"
    ).round(2)
    conf_summary.index = [format_profile_label(idx) for idx in conf_summary.index]
    print(conf_summary.to_string())

    # 4. Duration seconds summary by profile
    print("\n[4] Simulation Duration (Seconds) by Behavior Profile:")
    dur_summary = df.groupby("behavior_profile")["duration_seconds"].agg(
        Count="count",
        Mean="mean",
        Std="std",
        Min="min",
        Median="median",
        Max="max"
    ).round(2)
    dur_summary.index = [format_profile_label(idx) for idx in dur_summary.index]
    print(dur_summary.to_string())

    # 5. Overall aggregate metrics
    print("\n[5] Overall Dataset Aggregate Metrics:")
    print(f"  - Total Simulation Records: {len(df)}")
    print(f"  - Overall Mean Duration:   {df['duration_seconds'].mean():.2f} s (std: {df['duration_seconds'].std():.2f} s)")
    print(f"  - Overall Mean Confidence: {df['confidence_score'].mean():.2f} % (std: {df['confidence_score'].std():.2f} %)")
    total_vuln = (df['agent_decision'] == 'VULNERABLE').sum()
    print(f"  - Overall Vulnerability:   {total_vuln}/{len(df)} ({total_vuln/len(df)*100:.1f}%)")
    print("=" * 80 + "\n")


def main():
    # Resolve project root and paths
    project_root = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(project_root, "backend", "semanticshield.db")
    figures_dir = os.path.join(project_root, "figures")

    # If running with custom arguments
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    if len(sys.argv) > 2:
        figures_dir = sys.argv[2]

    print(f"[INFO] Connecting to SQLite database: {db_path}")
    df = validate_and_load_data(db_path)
    print(f"[INFO] Successfully loaded {len(df)} simulation records.")

    # Ensure figures directory exists
    os.makedirs(figures_dir, exist_ok=True)
    print(f"[INFO] Saving figures to: {figures_dir}")

    # Configure matplotlib styles
    configure_matplotlib_defaults()

    # Generate the four figures
    plot_fig_5_6_decision_by_profile(df, figures_dir)
    plot_fig_5_7_severity_distribution(df, figures_dir)
    plot_fig_5_8_confidence_by_profile(df, figures_dir)
    plot_fig_5_9_avg_duration_by_profile(df, figures_dir)

    # Print summary table to console
    print_summary_table(df)


if __name__ == "__main__":
    main()
