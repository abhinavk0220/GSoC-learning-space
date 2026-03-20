import os
import sys
from dotenv import load_dotenv
load_dotenv()
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import solara
from llm_opinion_dynamics.model import LLMOpinionDynamicsModel
from mesa.visualization import SolaraViz, make_plot_component
from mesa.visualization.utils import update_counter

model_params = {
    "n_agents": {
        "type": "SliderInt",
        "value": 4,
        "label": "Number of Agents",
        "min": 2,
        "max": 12,
        "step": 1,
    },
    "width": {
        "type": "SliderInt",
        "value": 5,
        "label": "Grid Width",
        "min": 3,
        "max": 10,
        "step": 1,
    },
    "height": {
        "type": "SliderInt",
        "value": 5,
        "label": "Grid Height",
        "min": 3,
        "max": 10,
        "step": 1,
    },
    "topic": {
        "type": "InputText",
        "value": "Should artificial intelligence be regulated by governments?",
        "label": "Debate Topic",
    },
}


def OpinionGridPlot(model):
    """Heatmap of the grid showing agent opinions as colors."""
    update_counter.get()

    width = model.grid.width
    height = model.grid.height

    grid_data = np.full((height, width), np.nan)
    agent_opinions = {}

    for agent in model.agents:
        if hasattr(agent, "cell") and agent.cell is not None:
            x, y = agent.cell.coordinate
            grid_data[y, x] = agent.opinion
            agent_opinions[(x, y)] = agent.opinion

    fig, ax = plt.subplots(figsize=(5, 5))
    fig.patch.set_facecolor("#1e1e2e")
    ax.set_facecolor("#1e1e2e")

    cmap = plt.cm.RdYlGn
    cmap.set_bad(color="#2a2a3e")

    im = ax.imshow(
        grid_data,
        cmap=cmap,
        vmin=0,
        vmax=10,
        interpolation="nearest",
        origin="lower",
    )

    for (x, y), opinion in agent_opinions.items():
        ax.text(
            x, y, f"{opinion:.1f}",
            ha="center", va="center",
            fontsize=11, fontweight="bold",
            color="white" if opinion < 3 or opinion > 7 else "#1e1e2e",
        )

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.yaxis.set_tick_params(color="white")
    cbar.set_label("Opinion Score", color="white", fontsize=10)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color="white")

    ax.set_title(
        f"Agent Opinion Grid  (Step {model.time:.0f})",
        color="white", fontsize=12, fontweight="bold", pad=10,
    )
    ax.set_xticks(range(width))
    ax.set_yticks(range(height))
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#444466")

    ax.set_xlabel("Grid X", color="white")
    ax.set_ylabel("Grid Y", color="white")

    plt.tight_layout()
    return solara.FigureMatplotlib(fig)


def OpinionTrajectoriesPlot(model):
    """Line chart of opinion trajectories for all agents over time."""
    update_counter.get()

    df = model.datacollector.get_agent_vars_dataframe()

    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor("#1e1e2e")
    ax.set_facecolor("#1e1e2e")

    if df.empty or len(df.index.get_level_values("Step").unique()) < 2:
        ax.text(
            0.5, 0.5, "Run the model to see opinion trajectories",
            ha="center", va="center", color="#aaaacc", fontsize=11,
            transform=ax.transAxes,
        )
    else:
        opinions = df["opinion"].unstack("AgentID")
        colors = plt.cm.tab20(np.linspace(0, 1, len(opinions.columns)))

        for agent_id, color in zip(opinions.columns, colors):
            ax.plot(
                opinions.index, opinions[agent_id],
                linewidth=2, alpha=0.85, color=color,
                label=f"Agent {agent_id}",
            )

        ax.legend(
            loc="upper right", fontsize=7, ncol=2,
            facecolor="#2a2a3e", edgecolor="#444466",
            labelcolor="white",
        )

    ax.set_xlabel("Time Step", color="white")
    ax.set_ylabel("Opinion  (0 = against  →  10 = for)", color="white")
    ax.set_title(
        f"Opinion Trajectories\nTopic: {model.topic[:55]}...",
        color="white", fontsize=11, fontweight="bold",
    )
    ax.set_ylim(-0.5, 10.5)
    ax.tick_params(colors="white")
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    for spine in ax.spines.values():
        spine.set_edgecolor("#444466")

    ax.axhline(5, color="#555577", linestyle="--", linewidth=0.8, alpha=0.6)
    ax.text(0.01, 0.52, "Neutral", transform=ax.transAxes,
            color="#888899", fontsize=8)

    plt.tight_layout()
    return solara.FigureMatplotlib(fig)


def MeanVariancePlot(model):
    """Dual-panel: mean opinion + variance over time."""
    update_counter.get()

    df_model = model.datacollector.get_model_vars_dataframe()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 4), sharex=True)
    fig.patch.set_facecolor("#1e1e2e")

    for ax in (ax1, ax2):
        ax.set_facecolor("#1e1e2e")
        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_edgecolor("#444466")

    if not df_model.empty and len(df_model) > 1:
        steps = df_model.index
        ax1.plot(steps, df_model["mean_opinion"], color="#4fc3f7", linewidth=2)
        ax1.fill_between(steps, df_model["mean_opinion"], 5,
                         alpha=0.15, color="#4fc3f7")
        ax1.axhline(5, color="#555577", linestyle="--", linewidth=0.8)
        ax1.set_ylim(0, 10)

        ax2.plot(steps, df_model["opinion_variance"], color="#ff8a65", linewidth=2)
        ax2.fill_between(steps, df_model["opinion_variance"], 0,
                         alpha=0.15, color="#ff8a65")
    else:
        for ax in (ax1, ax2):
            ax.text(0.5, 0.5, "Waiting for data...",
                    ha="center", va="center", color="#aaaacc",
                    transform=ax.transAxes)

    ax1.set_ylabel("Mean Opinion", color="white", fontsize=9)
    ax2.set_ylabel("Variance", color="white", fontsize=9)
    ax2.set_xlabel("Step", color="white", fontsize=9)
    ax1.set_title("Population Dynamics", color="white",
                  fontsize=11, fontweight="bold")
    ax1.tick_params(labelbottom=False)

    plt.tight_layout()
    return solara.FigureMatplotlib(fig)


model = LLMOpinionDynamicsModel()

page = SolaraViz(
    model,
    components=[
        OpinionGridPlot,
        OpinionTrajectoriesPlot,
        MeanVariancePlot,
    ],
    model_params=model_params,
    name="LLM Opinion Dynamics",
)
