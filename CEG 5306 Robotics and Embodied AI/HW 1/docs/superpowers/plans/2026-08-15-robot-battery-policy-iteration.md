# Robot Battery Policy Iteration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a self-contained Jupyter Notebook that formulates the deterministic robot-battery MDP, solves it with policy iteration, verifies the result, and exports the optimal-policy and value-function figures.

**Architecture:** The deliverable is one executable Notebook containing short Markdown explanations and focused Python functions for the MDP, policy evaluation, policy improvement, policy iteration, verification, and visualization. Tests execute the Notebook from a fresh kernel through `nbclient`, so the submitted artifact is tested in the same form the student runs it. The `.venv` directory remains local and is ignored by Git; its activation prompt is `hw1`.

**Tech Stack:** Python virtual environment, JupyterLab, NumPy, Matplotlib, nbformat, nbclient, pytest

## Global Constraints

- Work only inside `CEG 5306 Robotics and Embodied AI/HW 1/`.
- Use `.venv` as the environment directory and `hw1` as its display prompt.
- Use exactly 12 states: two locations and battery levels 0 through 5.
- Use `charging_zone` and `task_zone` as location names.
- Use deterministic transitions and discount factor `gamma = 0.95`.
- Use `numpy.linalg.solve`; never calculate a matrix inverse explicitly.
- Keep the Notebook self-contained and executable from top to bottom.
- Use Obsidian/Jupyter-compatible `$...$` and `$$...$$` math delimiters in Markdown cells.
- Do not add stochastic transitions, animation, Gymnasium, neural networks, cloud offloading, or multiple robots.
- Preserve unrelated changes in the surrounding Obsidian repository.

---

## File Structure

- Create: `.gitignore` - excludes `.venv`, Jupyter checkpoints, Python caches, and generated notebook execution artifacts.
- Create: `requirements.txt` - records the Python packages needed to run and verify the Notebook.
- Create: `robot_battery_policy_iteration.ipynb` - complete homework explanation, implementation, checks, tables, and figures.
- Create: `tests/test_notebook.py` - executes the Notebook from a fresh kernel and checks required outputs and displayed results.
- Create: `README.md` - gives exact environment setup and JupyterLab usage instructions.
- Create during execution: `output/optimal_policy.png` - final policy table figure.
- Create during execution: `output/value_heatmap.png` - final optimal value-function heatmap.

### Task 1: Reproducible project environment and Notebook smoke test

**Files:**
- Create: `CEG 5306 Robotics and Embodied AI/HW 1/.gitignore`
- Create: `CEG 5306 Robotics and Embodied AI/HW 1/requirements.txt`
- Create: `CEG 5306 Robotics and Embodied AI/HW 1/robot_battery_policy_iteration.ipynb`
- Create: `CEG 5306 Robotics and Embodied AI/HW 1/tests/test_notebook.py`

**Interfaces:**
- Consumes: Python 3 and the approved design specification.
- Produces: a valid Notebook file with kernel name `python3`; `execute_notebook() -> tuple[dict, list[str]]` in the test helper.

- [ ] **Step 1: Create the isolated environment**

Run from the HW 1 directory:

```bash
python3 -m venv --prompt hw1 .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install jupyterlab numpy matplotlib nbformat nbclient pytest
python -m pip freeze > requirements.txt
```

Expected: the shell prompt begins with `(hw1)`, and `python -c "import numpy, matplotlib, nbformat, nbclient"` exits successfully.

- [ ] **Step 2: Write the failing Notebook smoke test**

Create `tests/test_notebook.py` with:

```python
from pathlib import Path

import nbformat
from nbclient import NotebookClient


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = PROJECT_ROOT / "robot_battery_policy_iteration.ipynb"


def execute_notebook():
    notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=120,
        kernel_name="python3",
        resources={"metadata": {"path": str(PROJECT_ROOT)}},
    )
    executed = client.execute()
    text_outputs = [
        output.get("text", "")
        for cell in executed.cells
        if cell.cell_type == "code"
        for output in cell.get("outputs", [])
        if output.output_type == "stream"
    ]
    return executed, text_outputs


def test_notebook_executes_from_fresh_kernel():
    executed, _ = execute_notebook()
    assert all(
        output.output_type != "error"
        for cell in executed.cells
        if cell.cell_type == "code"
        for output in cell.get("outputs", [])
    )
```

- [ ] **Step 3: Run the smoke test and verify it fails**

Run:

```bash
.venv/bin/python -m pytest tests/test_notebook.py::test_notebook_executes_from_fresh_kernel -v
```

Expected: FAIL because `robot_battery_policy_iteration.ipynb` does not exist.

- [ ] **Step 4: Create the minimal valid Notebook**

Create `robot_battery_policy_iteration.ipynb` with one Markdown title cell and this first code cell:

```python
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path.cwd()
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

print("Robot Battery Policy Iteration notebook initialized.")
```

Set Notebook metadata to use the `python3` kernel.

- [ ] **Step 5: Add project ignore rules**

Create `.gitignore` with:

```gitignore
.venv/
.ipynb_checkpoints/
__pycache__/
.pytest_cache/
*.pyc
```

- [ ] **Step 6: Run the smoke test and verify it passes**

Run:

```bash
.venv/bin/python -m pytest tests/test_notebook.py::test_notebook_executes_from_fresh_kernel -v
```

Expected: `1 passed`.

- [ ] **Step 7: Commit the environment scaffold**

```bash
git add .gitignore requirements.txt robot_battery_policy_iteration.ipynb tests/test_notebook.py
git commit -m "chore: scaffold HW1 policy iteration notebook"
```

### Task 2: MDP state, action, transition, and reward model

**Files:**
- Modify: `CEG 5306 Robotics and Embodied AI/HW 1/robot_battery_policy_iteration.ipynb`
- Modify: `CEG 5306 Robotics and Embodied AI/HW 1/tests/test_notebook.py`

**Interfaces:**
- Consumes: Notebook setup from Task 1.
- Produces: `STATES`, `STATE_TO_INDEX`, `legal_actions(state) -> tuple[str, ...]`, and `transition(state, action) -> tuple[tuple[str, int], float]`.

- [ ] **Step 1: Add a failing model-output test**

Append to `tests/test_notebook.py`:

```python
def test_notebook_reports_valid_mdp():
    _, outputs = execute_notebook()
    combined = "".join(outputs)
    assert "MDP validation passed: 12 states" in combined
    assert "Initial state: ('charging_zone', 5)" in combined
```

- [ ] **Step 2: Run the new test and verify it fails**

Run:

```bash
.venv/bin/python -m pytest tests/test_notebook.py::test_notebook_reports_valid_mdp -v
```

Expected: FAIL because the Notebook does not yet define or validate the MDP.

- [ ] **Step 3: Add the MDP explanation and constants**

Add a Markdown section defining

$$
s=(L,B),\quad L\in\{\texttt{charging\_zone},\texttt{task\_zone}\},\quad B\in\{0,1,2,3,4,5\},
$$

the deterministic initial state, the five action names, rewards, and `gamma = 0.95`.

Add this code cell:

```python
LOCATIONS = ("charging_zone", "task_zone")
BATTERY_LEVELS = tuple(range(6))
STATES = tuple(
    (location, battery)
    for location in LOCATIONS
    for battery in BATTERY_LEVELS
)
STATE_TO_INDEX = {state: index for index, state in enumerate(STATES)}

INITIAL_STATE = ("charging_zone", 5)
GAMMA = 0.95

RECHARGE = "recharge"
TRAVEL_TO_TASK = "travel_to_task"
PERFORM_TASK = "perform_task"
RETURN_TO_CHARGING = "return_to_charging"
EMERGENCY_RESCUE = "emergency_rescue"
```

- [ ] **Step 4: Implement legal actions and deterministic transitions**

Add this code cell:

```python
def legal_actions(state):
    location, battery = state

    if location == "charging_zone":
        actions = []
        if battery < 5:
            actions.append(RECHARGE)
        if battery >= 1:
            actions.append(TRAVEL_TO_TASK)
        return tuple(actions)

    if battery == 0:
        return (EMERGENCY_RESCUE,)

    return (PERFORM_TASK, RETURN_TO_CHARGING)


def transition(state, action):
    location, battery = state
    if action not in legal_actions(state):
        raise ValueError(f"Illegal action {action!r} for state {state!r}")

    if action == RECHARGE:
        return ("charging_zone", battery + 1), -1.0
    if action == TRAVEL_TO_TASK:
        return ("task_zone", battery - 1), -0.5
    if action == PERFORM_TASK:
        return ("task_zone", battery - 1), 5.0
    if action == RETURN_TO_CHARGING:
        return ("charging_zone", battery - 1), -0.5
    return ("charging_zone", 0), -20.0
```

- [ ] **Step 5: Add executable MDP validation**

Add this code cell:

```python
assert len(STATES) == 12
assert len(set(STATES)) == 12
assert INITIAL_STATE in STATE_TO_INDEX

for state in STATES:
    actions = legal_actions(state)
    assert actions, f"No legal action for {state}"
    for action in actions:
        next_state, reward = transition(state, action)
        assert next_state in STATE_TO_INDEX
        assert np.isfinite(reward)

print(f"MDP validation passed: {len(STATES)} states")
print(f"Initial state: {INITIAL_STATE}")
```

- [ ] **Step 6: Run the model and smoke tests**

Run:

```bash
.venv/bin/python -m pytest tests/test_notebook.py -v
```

Expected: both tests PASS.

- [ ] **Step 7: Commit the MDP model**

```bash
git add robot_battery_policy_iteration.ipynb tests/test_notebook.py
git commit -m "feat: define deterministic robot battery MDP"
```

### Task 3: Policy evaluation, policy improvement, and convergence

**Files:**
- Modify: `CEG 5306 Robotics and Embodied AI/HW 1/robot_battery_policy_iteration.ipynb`
- Modify: `CEG 5306 Robotics and Embodied AI/HW 1/tests/test_notebook.py`

**Interfaces:**
- Consumes: `STATES`, `STATE_TO_INDEX`, `GAMMA`, `legal_actions`, and `transition` from Task 2.
- Produces: `evaluate_policy(policy) -> np.ndarray`, `improve_policy(values) -> dict`, and `policy_iteration() -> tuple[dict, np.ndarray, list[int]]`.

- [ ] **Step 1: Add failing convergence assertions**

Append to `tests/test_notebook.py`:

```python
def test_policy_iteration_converges_and_verifies_result():
    _, outputs = execute_notebook()
    combined = "".join(outputs)
    assert "Policy iteration converged" in combined
    assert "Bellman residual:" in combined
    assert "Policy stability check passed" in combined
    assert "Expected policy behavior check passed" in combined
```

- [ ] **Step 2: Run the convergence test and verify it fails**

Run:

```bash
.venv/bin/python -m pytest tests/test_notebook.py::test_policy_iteration_converges_and_verifies_result -v
```

Expected: FAIL because policy iteration has not been implemented.

- [ ] **Step 3: Implement exact policy evaluation**

Add a Markdown cell deriving

$$
(I-\gamma T^\pi)V^\pi=r^\pi.
$$

Add this code cell:

```python
def evaluate_policy(policy):
    num_states = len(STATES)
    transition_matrix = np.zeros((num_states, num_states))
    reward_vector = np.zeros(num_states)

    for state in STATES:
        row = STATE_TO_INDEX[state]
        action = policy[state]
        next_state, reward = transition(state, action)
        transition_matrix[row, STATE_TO_INDEX[next_state]] = 1.0
        reward_vector[row] = reward

    values = np.linalg.solve(
        np.eye(num_states) - GAMMA * transition_matrix,
        reward_vector,
    )
    return values
```

- [ ] **Step 4: Implement policy improvement**

Add this code cell:

```python
def action_value(state, action, values):
    next_state, reward = transition(state, action)
    return reward + GAMMA * values[STATE_TO_INDEX[next_state]]


def improve_policy(values):
    improved = {}
    for state in STATES:
        actions = legal_actions(state)
        improved[state] = max(
            actions,
            key=lambda action: action_value(state, action, values),
        )
    return improved
```

Explain in Markdown that deterministic transitions reduce the one-step lookahead to

$$
Q^\pi(s,a)=r(s,a)+\gamma V^\pi(f(s,a)).
$$

- [ ] **Step 5: Implement the outer policy-iteration loop**

Add this code cell:

```python
def policy_iteration():
    policy = {state: legal_actions(state)[0] for state in STATES}
    change_history = []

    while True:
        values = evaluate_policy(policy)
        improved_policy = improve_policy(values)
        changed_states = sum(
            improved_policy[state] != policy[state]
            for state in STATES
        )
        change_history.append(changed_states)

        if changed_states == 0:
            return policy, values, change_history

        policy = improved_policy


optimal_policy, optimal_values, change_history = policy_iteration()
print(f"Policy iteration converged in {len(change_history)} rounds")
print(f"Changed states per round: {change_history}")
```

- [ ] **Step 6: Add numerical and behavioral verification**

Add this code cell:

```python
final_values = evaluate_policy(optimal_policy)
bellman_update = np.array([
    action_value(state, optimal_policy[state], final_values)
    for state in STATES
])
bellman_residual = np.max(np.abs(final_values - bellman_update))

assert bellman_residual < 1e-10
assert improve_policy(final_values) == optimal_policy
assert optimal_policy[("charging_zone", 4)] == RECHARGE
assert optimal_policy[("charging_zone", 5)] == TRAVEL_TO_TASK
assert optimal_policy[("task_zone", 2)] == PERFORM_TASK
assert optimal_policy[("task_zone", 1)] == RETURN_TO_CHARGING

print(f"Bellman residual: {bellman_residual:.3e}")
print("Policy stability check passed")
print("Expected policy behavior check passed")
```

- [ ] **Step 7: Run all tests**

Run:

```bash
.venv/bin/python -m pytest tests/test_notebook.py -v
```

Expected: all tests PASS, with the Notebook reporting convergence and a Bellman residual below `1e-10`.

- [ ] **Step 8: Commit the policy-iteration implementation**

```bash
git add robot_battery_policy_iteration.ipynb tests/test_notebook.py
git commit -m "feat: implement and verify policy iteration"
```

### Task 4: Value table, policy table, and figure exports

**Files:**
- Modify: `CEG 5306 Robotics and Embodied AI/HW 1/robot_battery_policy_iteration.ipynb`
- Modify: `CEG 5306 Robotics and Embodied AI/HW 1/tests/test_notebook.py`
- Create during execution: `CEG 5306 Robotics and Embodied AI/HW 1/output/optimal_policy.png`
- Create during execution: `CEG 5306 Robotics and Embodied AI/HW 1/output/value_heatmap.png`

**Interfaces:**
- Consumes: `optimal_policy`, `optimal_values`, `STATES`, and `STATE_TO_INDEX` from Task 3.
- Produces: `value_grid`, `policy_grid`, and two PNG files.

- [ ] **Step 1: Add failing output-artifact tests**

Append to `tests/test_notebook.py`:

```python
def test_notebook_exports_required_figures():
    execute_notebook()
    policy_path = PROJECT_ROOT / "output" / "optimal_policy.png"
    value_path = PROJECT_ROOT / "output" / "value_heatmap.png"
    assert policy_path.exists() and policy_path.stat().st_size > 10_000
    assert value_path.exists() and value_path.stat().st_size > 10_000
```

- [ ] **Step 2: Run the artifact test and verify it fails**

Run:

```bash
.venv/bin/python -m pytest tests/test_notebook.py::test_notebook_exports_required_figures -v
```

Expected: FAIL because the figures do not exist.

- [ ] **Step 3: Build and display the numerical result tables**

Add this code cell:

```python
short_labels = {
    RECHARGE: "Recharge",
    TRAVEL_TO_TASK: "Go to task",
    PERFORM_TASK: "Do task",
    RETURN_TO_CHARGING: "Return",
    EMERGENCY_RESCUE: "Rescue",
}

value_grid = np.array([
    [optimal_values[STATE_TO_INDEX[(location, battery)]] for battery in BATTERY_LEVELS]
    for location in LOCATIONS
])
policy_grid = np.array([
    [short_labels[optimal_policy[(location, battery)]] for battery in BATTERY_LEVELS]
    for location in LOCATIONS
])

print("Optimal value function V*:")
print(np.round(value_grid, 3))
print("Optimal policy pi*:")
print(policy_grid)
```

- [ ] **Step 4: Create the policy-table figure**

Add a code cell that creates a Matplotlib table from `policy_grid`, labels rows `Charging zone` and `Task zone`, labels columns `Battery 0` through `Battery 5`, uses a readable figure size, and saves with:

```python
policy_figure.tight_layout()
policy_figure.savefig(
    OUTPUT_DIR / "optimal_policy.png",
    dpi=200,
    bbox_inches="tight",
)
plt.show()
```

- [ ] **Step 5: Create the annotated value heatmap**

Add a code cell that displays `value_grid` with `imshow`, adds a color bar labeled `Expected discounted return`, annotates every cell using `f"{value_grid[row, column]:.2f}"`, and saves with:

```python
value_figure.tight_layout()
value_figure.savefig(
    OUTPUT_DIR / "value_heatmap.png",
    dpi=200,
    bbox_inches="tight",
)
plt.show()
```

- [ ] **Step 6: Run the complete test suite**

Run:

```bash
.venv/bin/python -m pytest tests/test_notebook.py -v
```

Expected: all tests PASS and both PNG files exceed 10 KB.

- [ ] **Step 7: Visually inspect both figures**

Open both PNGs and verify:

- all six battery columns are visible;
- both location labels are visible;
- no action label is clipped;
- all heatmap values are readable;
- the color bar and title are present.

- [ ] **Step 8: Commit the result presentation**

```bash
git add robot_battery_policy_iteration.ipynb tests/test_notebook.py output/optimal_policy.png output/value_heatmap.png
git commit -m "feat: visualize optimal robot battery policy"
```

### Task 5: Student-facing explanation and final reproducibility check

**Files:**
- Create: `CEG 5306 Robotics and Embodied AI/HW 1/README.md`
- Modify: `CEG 5306 Robotics and Embodied AI/HW 1/robot_battery_policy_iteration.ipynb`
- Modify: `CEG 5306 Robotics and Embodied AI/HW 1/tests/test_notebook.py`

**Interfaces:**
- Consumes: complete Notebook and generated artifacts from Tasks 1-4.
- Produces: beginner-friendly run instructions and a submission-ready Notebook.

- [ ] **Step 1: Add the final content test**

Append to `tests/test_notebook.py`:

```python
def test_notebook_contains_required_explanation():
    notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
    markdown = "\n".join(
        cell.source for cell in notebook.cells if cell.cell_type == "markdown"
    )
    assert "Policy Evaluation" in markdown
    assert "Policy Improvement" in markdown
    assert "Value Function" in markdown
    assert "Why this submission should be highlighted" in markdown
```

- [ ] **Step 2: Run the content test and verify it fails**

Run:

```bash
.venv/bin/python -m pytest tests/test_notebook.py::test_notebook_contains_required_explanation -v
```

Expected: FAIL until the final discussion and highlight section is present.

- [ ] **Step 3: Add the final Notebook discussion**

Add concise Markdown explaining:

- why the state is Markov;
- why deterministic transitions simplify the Bellman expectation;
- how policy evaluation calculates `V^pi`;
- how greedy policy improvement changes the policy;
- why the final stable policy is optimal;
- what the final value heatmap means.

End with this heading and two-sentence statement:

```markdown
## Why this submission should be highlighted

This submission shows how policy iteration enables an autonomous robot to balance productive work against charging and travel costs. The final policy and value-function heatmap make the robot's long-term energy-management strategy directly interpretable for every battery level.
```

- [ ] **Step 4: Write beginner-friendly README instructions**

Create `README.md` containing:

````markdown
# CEG5306 HW1 - Robot Battery Policy Iteration

## Setup

```bash
python3 -m venv --prompt hw1 .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab
```

Open `robot_battery_policy_iteration.ipynb`, then choose **Kernel > Restart Kernel and Run All Cells**.

## Verification

```bash
.venv/bin/python -m pytest tests/test_notebook.py -v
```

Expected outputs:

- `output/optimal_policy.png`
- `output/value_heatmap.png`
````

- [ ] **Step 5: Run the Notebook from a fresh kernel and save outputs**

Run:

```bash
.venv/bin/jupyter nbconvert \
  --to notebook \
  --execute robot_battery_policy_iteration.ipynb \
  --output robot_battery_policy_iteration.executed.ipynb \
  --ExecutePreprocessor.timeout=120
mv robot_battery_policy_iteration.executed.ipynb robot_battery_policy_iteration.ipynb
```

Expected: execution completes without an error and all Notebook cells contain fresh outputs.

- [ ] **Step 6: Run final verification**

Run:

```bash
.venv/bin/python -m pytest tests/test_notebook.py -v
git diff --check
git status --short
```

Expected:

- all tests PASS;
- no whitespace errors;
- only intended HW 1 files are changed or untracked.

- [ ] **Step 7: Perform final visual inspection**

Inspect `optimal_policy.png` and `value_heatmap.png` at original resolution. Verify that the figures match the numerical table printed in the executed Notebook and contain no clipped labels, overlaps, or unreadable text.

- [ ] **Step 8: Commit the submission-ready project**

```bash
git add README.md robot_battery_policy_iteration.ipynb tests/test_notebook.py requirements.txt output/optimal_policy.png output/value_heatmap.png
git commit -m "docs: finalize CEG5306 HW1 submission"
```
