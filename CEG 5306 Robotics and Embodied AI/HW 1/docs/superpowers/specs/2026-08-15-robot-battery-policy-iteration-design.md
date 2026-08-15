# Robot Battery Policy Iteration - Design Specification

## Purpose

Build a small, deterministic finite Markov decision process (MDP) for the CEG5306 Lecture 1 homework. A robot repeatedly performs tasks in a task zone and returns to a charging zone when necessary. Policy iteration computes a policy that balances task rewards against charging, travel, and emergency-rescue costs.

The deliverable is a self-contained Jupyter Notebook that explains the MDP, implements policy iteration, verifies the result, and generates a final policy table and value-function heatmap.

## Project and Runtime

- Project directory: `CEG 5306 Robotics and Embodied AI/HW 1/`
- Notebook: `robot_battery_policy_iteration.ipynb`
- Virtual-environment directory: `.venv`
- Virtual-environment prompt name: `hw1`
- Runtime: browser-based JupyterLab
- Required packages: JupyterLab, NumPy, Matplotlib
- Generated figures: `output/optimal_policy.png` and `output/value_heatmap.png`

## MDP Definition

### State space

Each state is a pair:

$$
s=(L,B),
$$

where

$$
L\in\{\texttt{charging\_zone},\texttt{task\_zone}\}
$$

and

$$
B\in\{0,1,2,3,4,5\}.
$$

The model therefore contains 12 states.

### Actions

Actions are state-dependent:

- `recharge`
- `travel_to_task`
- `perform_task`
- `return_to_charging`
- `emergency_rescue`

### Transition and reward rules

| Location | Condition | Legal action | Next state | Reward |
|---|---|---|---|---:|
| `charging_zone` | Battery below 5 | `recharge` | Same location, battery +1 | -1.0 |
| `charging_zone` | Battery at least 1 | `travel_to_task` | `task_zone`, battery -1 | -0.5 |
| `task_zone` | Battery at least 1 | `perform_task` | Same location, battery -1 | +5.0 |
| `task_zone` | Battery at least 1 | `return_to_charging` | `charging_zone`, battery -1 | -0.5 |
| `task_zone` | Battery is 0 | `emergency_rescue` | `charging_zone`, battery remains 0 | -20.0 |

All transitions are deterministic. For every legal state-action pair, exactly one next state has probability 1. Illegal actions are excluded rather than assigned artificial penalties.

At `(charging_zone, 5)`, `travel_to_task` is the only legal action. At `(charging_zone, 0)`, `recharge` is the only legal action.

### Discount factor

Use

$$
\gamma=0.95.
$$

This continuing discounted MDP values long-term task completion while keeping the infinite return finite.

## Policy Iteration

### Initialization

Create a deterministic initial policy by selecting the first legal action for each state. A fixed initialization ensures reproducible results.

### Policy evaluation

For the current policy, construct

$$
T^\pi_{ij}=P(j\mid i,\pi(i))
$$

and

$$
r^\pi_i=r(i,\pi(i)).
$$

Solve the Bellman linear system directly:

$$
(I-\gamma T^\pi)V^\pi=r^\pi.
$$

Use `numpy.linalg.solve`; do not explicitly calculate a matrix inverse.

### Policy improvement

For every legal action, calculate

$$
Q^\pi(s,a)=r(s,a)+\gamma\sum_{s'}P(s'\mid s,a)V^\pi(s').
$$

Set

$$
\pi_{\mathrm{new}}(s)=\arg\max_a Q^\pi(s,a).
$$

Use the declared legal-action order as a deterministic tie-breaking rule.

### Termination

Stop when the policy is unchanged across a complete improvement step:

$$
\pi_{\mathrm{new}}=\pi.
$$

Record the number of outer policy-iteration rounds and the number of states whose actions change in every round.

## Notebook Structure

1. Title and problem motivation
2. MDP formulation
3. State enumeration and legal actions
4. Transition and reward construction
5. Policy evaluation implementation
6. Policy improvement implementation
7. Policy iteration implementation
8. Verification checks
9. Final policy table
10. Value-function heatmap
11. Short discussion and highlight statement

Markdown cells will explain the mathematics, while code cells will remain short and executable in top-to-bottom order.

## Verification

The Notebook must automatically check:

1. Exactly 12 unique states exist.
2. Every state has at least one legal action.
3. Every legal state-action transition has non-negative probabilities summing to 1.
4. Every next state belongs to the declared state space.
5. The evaluated value function has a small Bellman residual:

   \[
   \|V^\pi-(r^\pi+\gamma T^\pi V^\pi)\|_\infty<10^{-10}.
   \]

6. A final policy-improvement pass leaves the policy unchanged.
7. Re-running the complete Notebook from a fresh kernel produces the same policy and figures.

## Visualization

The policy table will use rows for location and columns for battery levels 0 through 5. Each cell will show the selected action using a short readable label.

The value heatmap will use the same two-by-six layout and annotate each cell with its numerical value. Both figures will include titles, axis labels, and a legend or color bar where appropriate.

## Scope Boundaries

This version intentionally excludes stochastic transitions, continuous battery levels, neural networks, Gymnasium, animation, cloud offloading, and multiple robots. These additions are unnecessary for demonstrating finite-MDP policy iteration and would make the homework harder to verify.

## Success Criteria

The project is complete when the Notebook runs from beginning to end without errors, all verification checks pass, policy iteration terminates at a stable policy, both requested figures are saved, and the final explanation clearly connects the implementation to the policy-iteration equations from Lecture 1.
