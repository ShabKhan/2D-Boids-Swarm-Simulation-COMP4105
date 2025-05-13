import plotly.express as px
import pandas as pd
import os
import re

def extract_metadata(filename):
    match = re.search(r'(\d+)boids_sep([\d.]+)_ali([\d.]+)_coh([\d.]+)(_pred)?', filename)
    if match:
        boids = match.group(1)
        sep = match.group(2)
        ali = match.group(3)
        coh = match.group(4)
        pred = match.group(5) is not None
        return f"{boids}b_sep{sep}_ali{ali}_coh{coh}", pred
    return filename, False

def plot_combined_metric(metric, label, ylabel):
    summary_file = os.path.join(os.path.dirname(__file__), "results", f"summary_{metric.replace(' ', '_')}.csv")
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    files = [f for f in os.listdir(results_dir) if f.endswith(".csv")]

    combined_data = []

    for file in sorted(files):
        path = os.path.join(results_dir, file)
        df = pd.read_csv(path)
        if metric not in df.columns:
            continue

        base_label, predator = extract_metadata(file)
        df['Label'] = f"{base_label} ({'Pred' if predator else 'NoPred'})"
        combined_data.append(df[['Step', metric, 'Label']])

    if not combined_data:
        print("No data found for metric:", metric)
        return

    all_data = pd.concat(combined_data, ignore_index=True)

    # Explicit numeric conversion to ensure clean data
    all_data["Step"] = pd.to_numeric(all_data["Step"], errors='coerce')
    all_data[metric] = pd.to_numeric(all_data[metric], errors='coerce')

    # Drop NaNs immediately to ensure clean plotting
    all_data.dropna(subset=["Step", metric], inplace=True)

    # Ensure data is sorted by Step
    all_data.sort_values(by="Step", inplace=True)

    # Generate and show plot
    fig = px.line(all_data, x='Step', y=metric, color='Label', title=label)
    fig.update_layout(yaxis_title=ylabel, xaxis_title='Step')
    fig.show()

    # Generate summary safely
    summary = all_data.groupby('Label', as_index=False).agg({metric: 'mean'})
    summary.columns = ['Label', f'Average {metric}']
    summary.to_csv(summary_file, index=False)

    print(f"Summary exported to {summary_file}")
if __name__ == "__main__":
    print("Plotting average distance (group cohesion)...")
    plot_combined_metric("Avg Distance to Center", "Average Distance to Center", "Avg Distance")

    print("Plotting collisions...")
    plot_combined_metric("Collisions", "Collision Count", "Number of Collisions")

# Optional: generate focused view for one config
def plot_focused_config(metric, config_name, label_suffix):
    summary_file = os.path.join(os.path.dirname(__file__), "results", f"summary_{metric.replace(' ', '_')}.csv")
    if not os.path.exists(summary_file):
        print(f"[⚠] Summary file not found: {summary_file}")
        return
    df = pd.read_csv(summary_file)
    filtered = df[df["Label"].str.contains(config_name)]
    if filtered.empty:
        print(f"[⚠] No matching data found for config: {config_name}")
        return

    fig = px.bar(filtered, x="Label", y=f"Average {metric}",
                 title=f"{metric} — Focused: {label_suffix}",
                 labels={f'Average {metric}': metric})
    fig.show()

# Call examples
plot_focused_config("Avg Distance to Center", "30b_sep1.0_ali1.0_coh1.0", "Predator Effect on Cohesion")
plot_focused_config("Collisions", "30b_sep1.0_ali1.0_coh1.0", "Predator Effect on Collisions")
plot_focused_config("Avg Distance to Center", "30b_sep0.5_ali2.0_coh1.5", "Predator Effect on Cohesion – High Cohesion")
plot_focused_config("Collisions", "30b_sep0.5_ali2.0_coh1.5", "Predator Effect on Collisions – High Cohesion")
