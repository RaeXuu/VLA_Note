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


def test_notebook_reports_valid_mdp():
    _, outputs = execute_notebook()
    combined = "".join(outputs)
    assert "MDP validation passed: 12 states" in combined
    assert "Initial state: ('charging_zone', 5)" in combined


def test_policy_iteration_converges_and_verifies_result():
    _, outputs = execute_notebook()
    combined = "".join(outputs)
    assert "Policy iteration converged" in combined
    assert "Bellman residual:" in combined
    assert "Policy stability check passed" in combined
    assert "Expected policy behavior check passed" in combined


def test_notebook_exports_required_figures():
    execute_notebook()
    policy_path = PROJECT_ROOT / "output" / "optimal_policy.png"
    value_path = PROJECT_ROOT / "output" / "value_heatmap.png"
    assert policy_path.exists() and policy_path.stat().st_size > 10_000
    assert value_path.exists() and value_path.stat().st_size > 10_000


def test_notebook_contains_required_explanation():
    notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
    markdown = "\n".join(
        cell.source for cell in notebook.cells if cell.cell_type == "markdown"
    )
    assert "Policy Evaluation" in markdown
    assert "Policy Improvement" in markdown
    assert "Value Function" in markdown
    assert "Why this submission should be highlighted" in markdown


def test_notebook_uses_an_interactive_notebook_backend():
    _, outputs = execute_notebook()
    combined = "".join(outputs)
    assert "FigureCanvasAgg is non-interactive" not in combined
