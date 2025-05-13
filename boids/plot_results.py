
import pandas as pd
import os
import plotly.graph_objs as go
import plotly.offline as pyo

def plot_log(file_path, title_suffix=""):
    df = pd.read_csv(file_path)
    if df.empty or df.shape[0] == 0:
        print(f"\n[ERROR] The selected file '{file_path}' is empty. No data to plot.")
        return

    steps = df['Step']
    avg_dist = df['Avg Distance to Center']
    collisions = df['Collisions']

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=steps, y=avg_dist, mode='lines', name='Avg Distance to Center'))
    fig.add_trace(go.Scatter(x=steps, y=collisions, mode='lines', name='Collisions', line=dict(color='red')))

    fig.update_layout(
        title=f"Simulation Metrics {title_suffix}",
        xaxis_title='Step',
        yaxis_title='Metric Value',
        legend=dict(x=0.01, y=0.99),
        width=1200,
        height=600
    )

    pyo.plot(fig)

if __name__ == "__main__":
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    files = [f for f in os.listdir(results_dir) if f.startswith("simulation_log_") and f.endswith(".csv")]

    print("Available result files:")
    for idx, file in enumerate(files):
        print(f"{idx}: {file}")

    choice = int(input("Select file number to plot: "))
    selected_file = os.path.join(results_dir, files[choice])

    plot_log(selected_file, title_suffix=f"({files[choice]})")
