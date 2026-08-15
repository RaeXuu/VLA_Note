# CEG5306 HW1 - Robot Battery Policy Iteration

This project uses policy iteration to solve a deterministic robot battery-management MDP. The Jupyter Notebook contains the MDP formulation, algorithm, verification checks, optimal value function, optimal policy, and result figures.

## Setup

Run these commands from the `HW 1` directory:

```bash
python3 -m venv --prompt hw1 .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab
```

JupyterLab will open in a browser. Open `robot_battery_policy_iteration.ipynb`, then choose **Kernel > Restart Kernel and Run All Cells**.

## Verification

Run:

```bash
JUPYTER_PLATFORM_DIRS=1 .venv/bin/python -m pytest tests/test_notebook.py -v
```

Expected generated outputs:

- `output/optimal_policy.png`
- `output/value_heatmap.png`

## Environment

The virtual-environment directory is `.venv`, and its shell prompt name is `hw1`. All Python packages remain isolated from the macOS system Python.
