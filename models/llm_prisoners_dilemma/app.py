import os
import sys
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

import matplotlib.pyplot as plt
import solara
from mesa.visualization import SolaraViz, make_plot_component

from llm_prisoners_dilemma.model import PrisonersDilemmaModel

plt.style.use("dark_background")


def agent_portrayal(agent):
    """Color agents by their last action and score."""
    if not hasattr(agent, "last_action"):
        return {"color": "gray", "size": 40}

    color_map = {
        "cooperate": "#2ecc71",   # Green
        "defect":    "#e74c3c",   # Red
        "none":      "#95a5a6",   # Gray (first round)
    }
    color = color_map.get(agent.last_action, "gray")

    # Size reflects score — higher score = bigger circle
    size = 30 + min(agent.score * 2, 80)

    return {"color": color, "size": size}


model_params = {
    "num_agents": {
        "type": "SliderInt",
        "value": 2,
        "label": "Number of Agents",
        "min": 2,
        "max": 10,
        "step": 2,
    },
    "llm_model": {
        "type": "Select",
        "value": "groq/llama-3.1-8b-instant",
        "label": "LLM Model",
        "values": [
            "groq/llama-3.1-8b-instant",
            "gpt-4o-mini",
            "gpt-4o",
        ],
    },
}

CoopPlot = make_plot_component(
    {
        "cooperation_rate": "#2ecc71",
    }
)

ScorePlot = make_plot_component(
    {
        "total_cooperations": "#2ecc71",
        "total_defections":   "#e74c3c",
    }
)

model = PrisonersDilemmaModel()

page = SolaraViz(
    model,
    components=[CoopPlot, ScorePlot],
    model_params=model_params,
    name="LLM Prisoner's Dilemma",
)
