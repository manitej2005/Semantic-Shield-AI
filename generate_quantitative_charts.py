import os
import csv
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.makedirs("paper/figures", exist_ok=True)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'Liberation Serif', 'serif']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 7.5

def save_chart(fig, filename_base):
    png_path = f"paper/figures/{filename_base}.png"
    pdf_path = f"paper/figures/{filename_base}.pdf"
    fig.savefig(png_path, dpi=300, bbox_inches='tight', pad_inches=0.04)
    fig.savefig(pdf_path, bbox_inches='tight', pad_inches=0.04)
    plt.close(fig)
    print(f"Saved {png_path} and {pdf_path}")

def generate_all_charts():
    csv_path = "paper/data/results_all.csv"
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} does not exist yet.")
        return

    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} simulation records from {csv_path}")

    # Exclude fallback runs if any
    if "fallback_used" in df.columns:
        valid_df = df[df["fallback_used"].astype(str).str.lower() != "true"].copy()
    else:
        valid_df = df.copy()

    print(f"Valid runs evaluated: {len(valid_df)} (Excluded fallbacks: {len(df) - len(valid_df)})")

    # Split malicious scenarios vs control scenario
    malicious_df = valid_df[valid_df["scenario_id"] != "SIM-EML-007"].copy()
    control_df = valid_df[valid_df["scenario_id"] == "SIM-EML-007"].copy()

    # Profiles list
    profiles = ["trusting", "security_conscious", "overwhelmed", "executive"]
    profile_labels = ["Trusting", "Security-\nConscious", "Overwhelmed", "Executive"]

    # 1. Calculate Susceptibility Rate per Profile on Malicious Scenarios
    susc_rates = []
    for p in profiles:
        p_sub = malicious_df[malicious_df["behavior_profile"] == p]
        vuln_count = (p_sub["decision"] == "VULNERABLE").sum()
        total_count = len(p_sub)
        rate = (vuln_count / total_count * 100.0) if total_count > 0 else 0.0
        susc_rates.append(rate)

    # FIGURE 7: Grouped Bar Chart of Susceptibility Rate per Profile
    fig, ax = plt.subplots(figsize=(3.38, 2.3))
    x = np.arange(len(profiles))
    width = 0.55

    bars = ax.bar(x, susc_rates, width, color='#6C757D', edgecolor='#000000', linewidth=0.8, hatch='//')

    ax.set_ylabel("Susceptibility Rate (%)", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(profile_labels, fontsize=7)
    ax.set_ylim(0, 115)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle=':', alpha=0.6)

    # Value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, height + 2.5, f"{height:.1f}%",
                ha='center', va='bottom', fontsize=7, fontweight='bold')

    save_chart(fig, "fig7_susceptibility_rate")

    # FIGURE 8: Scenario by Profile Heatmap (Greyscale annotated)
    scenarios = sorted(valid_df["scenario_id"].unique())
    matrix = np.zeros((len(scenarios), len(profiles)))

    for i, sc in enumerate(scenarios):
        for j, p in enumerate(profiles):
            sub = valid_df[(valid_df["scenario_id"] == sc) & (valid_df["behavior_profile"] == p)]
            if len(sub) > 0:
                vuln_frac = (sub["decision"] == "VULNERABLE").sum() / len(sub)
                matrix[i, j] = vuln_frac

    fig, ax = plt.subplots(figsize=(3.38, 2.7))
    im = ax.imshow(matrix, cmap='Greys', vmin=0, vmax=1.0)

    ax.set_xticks(np.arange(len(profiles)))
    ax.set_yticks(np.arange(len(scenarios)))
    ax.set_xticklabels(profile_labels, fontsize=6.8)
    ax.set_yticklabels(scenarios, fontsize=6.8)

    # Annotate cell values
    for i in range(len(scenarios)):
        for j in range(len(profiles)):
            val = matrix[i, j]
            color = "white" if val > 0.5 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", color=color, fontsize=6.5, fontweight='bold')

    ax.set_xlabel("Behavioral Profile", fontsize=7.5)
    ax.set_ylabel("Scenario ID", fontsize=7.5)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=6.5)
    cbar.set_label("Vulnerability Fraction", fontsize=7)

    save_chart(fig, "fig8_scenario_profile_heatmap")

    # FIGURE 9: Composite Risk Score per Profile (Boxplot with jitter points)
    fig, ax = plt.subplots(figsize=(3.38, 2.3))
    risk_data = [valid_df[valid_df["behavior_profile"] == p]["risk_score"].values for p in profiles]

    bp = ax.boxplot(risk_data, patch_artist=True, tick_labels=profile_labels,
                    boxprops=dict(facecolor='#E9ECEF', color='#000000', linewidth=0.8),
                    medianprops=dict(color='#000000', linewidth=1.2),
                    whiskerprops=dict(color='#000000', linewidth=0.8),
                    capprops=dict(color='#000000', linewidth=0.8))

    # Add jitter points
    for i, data in enumerate(risk_data):
        y = data
        x = np.random.normal(i + 1, 0.04, size=len(y))
        ax.plot(x, y, 'o', color='#343A40', alpha=0.6, markersize=3)

    ax.set_ylabel("Composite Risk Score (0-100)", fontsize=8)
    ax.set_ylim(0, 105)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle=':', alpha=0.6)

    save_chart(fig, "fig9_risk_score_distribution")

    # FIGURE 10: Mean End-to-End Latency per Profile (Bar chart with standard deviation error bars)
    fig, ax = plt.subplots(figsize=(3.38, 2.3))

    mean_lats = []
    std_lats = []
    for p in profiles:
        sub = valid_df[valid_df["behavior_profile"] == p]["duration_seconds"]
        mean_lats.append(sub.mean())
        std_lats.append(sub.std())

    x_prof = np.arange(len(profiles))
    bars = ax.bar(x_prof, mean_lats, width, yerr=std_lats, capsize=3,
                  color='#ADB5BD', edgecolor='#000000', linewidth=0.8, hatch='\\\\')

    ax.set_ylabel("Mean Latency (seconds)", fontsize=8)
    ax.set_xticks(x_prof)
    ax.set_xticklabels(profile_labels, fontsize=7)
    ax.set_ylim(0, max(mean_lats) * 1.35)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle=':', alpha=0.6)

    for bar, m, s in zip(bars, mean_lats, std_lats):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, height + s + 1.2, f"{m:.1f}s",
                ha='center', va='bottom', fontsize=6.8, fontweight='bold')

    save_chart(fig, "fig10_latency_per_profile")

    # TABLE 4: Per-Profile Summary Stats
    summary_rows = []
    for p in profiles:
        p_all = valid_df[valid_df["behavior_profile"] == p]
        p_mal = malicious_df[malicious_df["behavior_profile"] == p]

        total_runs = len(p_all)
        vuln_count = (p_mal["decision"] == "VULNERABLE").sum()
        mal_runs = len(p_mal)
        susc_pct = (vuln_count / mal_runs * 100.0) if mal_runs > 0 else 0.0

        mean_risk = p_all["risk_score"].mean()
        mean_lat = p_all["duration_seconds"].mean()

        # Decision consistency across repetitions
        consistencies = []
        for sc in scenarios:
            sub = p_all[p_all["scenario_id"] == sc]
            if len(sub) > 0:
                most_common = sub["decision"].mode()[0]
                match_frac = (sub["decision"] == most_common).sum() / len(sub)
                consistencies.append(match_frac)
        avg_consist = (np.mean(consistencies) * 100.0) if consistencies else 100.0

        summary_rows.append({
            "profile": p,
            "total_runs": total_runs,
            "susc_pct": round(susc_pct, 1),
            "mean_risk": round(mean_risk, 1),
            "consistency_pct": round(avg_consist, 1),
            "mean_lat": round(mean_lat, 2)
        })

    print("\n--- TABLE 4 SUMMARY METRICS ---")
    for r in summary_rows:
        print(f"Profile: {r['profile']:<20} | Runs: {r['total_runs']} | Susceptibility: {r['susc_pct']}% | Mean Risk: {r['mean_risk']} | Consistency: {r['consistency_pct']}% | Latency: {r['mean_lat']}s")

if __name__ == "__main__":
    generate_all_charts()
