# Recursive Definition of the State-Value Function

## 1. State-value function

For a policy $\pi$, the state-value function is

$$
V^\pi(s)
=
\mathbb{E}_\pi[G_t\mid S_t=s],
$$

where the discounted return is

$$
G_t
=
\sum_{k=0}^{\infty}\gamma^kR_{t+k+1}.
$$

Therefore,

$$
V^\pi(s)
=
\mathbb{E}_\pi\left[
\sum_{k=0}^{\infty}\gamma^kR_{t+k+1}
\;\middle|\;S_t=s
\right].
$$

Our goal is to derive the recursive form

$$
\boxed{
V^\pi(s)
=
\mathbb{E}_\pi\left[
R_{t+1}+\gamma V^\pi(S_{t+1})
\;\middle|\;S_t=s
\right]
}.
$$

This is the **Bellman expectation equation（贝尔曼期望方程）**.

---

## 2. Separate the first reward

Start from the return:

$$
G_t
=
\sum_{k=0}^{\infty}\gamma^kR_{t+k+1}.
$$

Separate the term corresponding to $k=0$:

$$
G_t
=
R_{t+1}
+
\sum_{k=1}^{\infty}\gamma^kR_{t+k+1}.
$$

Hence,

$$
V^\pi(s)
=
\mathbb{E}_\pi\left[
R_{t+1}
+
\sum_{k=1}^{\infty}\gamma^kR_{t+k+1}
\;\middle|\;S_t=s
\right].
$$

---

## 3. Index shift

Consider the remaining infinite sum:

$$
\sum_{k=1}^{\infty}\gamma^kR_{t+k+1}.
$$

Let

$$
j=k-1,
\qquad k=j+1.
$$

When $k=1$, $j=0$. Therefore,

$$
\begin{aligned}
\sum_{k=1}^{\infty}\gamma^kR_{t+k+1}
&=
\sum_{j=0}^{\infty}\gamma^{j+1}R_{t+j+2}\\
&=
\gamma\sum_{j=0}^{\infty}\gamma^jR_{t+j+2}.
\end{aligned}
$$

The return starting at time $t+1$ is

$$
G_{t+1}
=
\sum_{j=0}^{\infty}\gamma^jR_{(t+1)+j+1}
=
\sum_{j=0}^{\infty}\gamma^jR_{t+j+2}.
$$

Thus,

$$
\boxed{G_t=R_{t+1}+\gamma G_{t+1}}.
$$

This identity follows only from the definition of the discounted return; it does not yet require the Markov property.

---

## 4. Linearity of conditional expectation

Substitute the recursive return into the value-function definition:

$$
V^\pi(s)
=
\mathbb{E}_\pi\left[
R_{t+1}+\gamma G_{t+1}
\;\middle|\;S_t=s
\right].
$$

Conditional expectation is linear:

$$
\mathbb{E}[X+cY\mid Z]
=
\mathbb{E}[X\mid Z]
+c\mathbb{E}[Y\mid Z].
$$

Therefore,

$$
V^\pi(s)
=
\mathbb{E}_\pi[R_{t+1}\mid S_t=s]
+
\gamma\mathbb{E}_\pi[G_{t+1}\mid S_t=s].
$$

Linearity allows the expectation to be separated. It does **not** by itself justify replacing $G_{t+1}$ with $V^\pi(S_{t+1})$.

---

## 5. Condition on the next state

Apply the **law of iterated expectation（迭代期望定律）**:

$$
\begin{aligned}
\mathbb{E}_\pi[G_{t+1}\mid S_t=s]
=
\mathbb{E}_\pi\Big[
&\mathbb{E}_\pi[
G_{t+1}
\mid S_t=s,S_{t+1}
]\\
&\mid S_t=s
\Big].
\end{aligned}
$$

Under the **Markov property（马尔可夫性质）**, once $S_{t+1}$ is known, the distribution of future rewards does not depend on the earlier state $S_t$:

$$
\mathbb{E}_\pi[
G_{t+1}mid S_t=s,S_{t+1}
]
=
\mathbb{E}_\pi[
G_{t+1}mid S_{t+1}
].
$$

Consequently,

$$
\mathbb{E}_\pi[G_{t+1}\mid S_t=s]
=
\mathbb{E}_\pi\left[
\mathbb{E}_\pi[G_{t+1}\mid S_{t+1}]
\;\middle|\;S_t=s
\right].
$$

---

## 6. Stationarity

At time $t+1$, the value of state $s'$ would generally be written as

$$
V_{t+1}^\pi(s')
=
\mathbb{E}_\pi[G_{t+1}\mid S_{t+1}=s'].
$$

If both the environment and policy are **stationary（平稳的）**, their rules do not depend on the absolute time index:

$$
p(s',r\mid s,a)
\text{ and }
\pi(a\mid s)
\quad\text{do not depend on }t.
$$

The value of a state therefore depends on the state itself, not on when the state is visited:

$$
V_{t+1}^\pi(s')=V_t^\pi(s')=V^\pi(s').
$$

Hence,

$$
\boxed{
\mathbb{E}_\pi[G_{t+1}\mid S_{t+1}]
=
V^\pi(S_{t+1})
}.
$$

---

## 7. Final recursive equation

Substituting the previous result gives

$$
V^\pi(s)
=
\mathbb{E}_\pi[R_{t+1}\mid S_t=s]
+
\gamma
\mathbb{E}_\pi[V^\pi(S_{t+1})\mid S_t=s].
$$

By linearity, combine the two expectations:

$$
\boxed{
V^\pi(s)
=
\mathbb{E}_\pi\left[
R_{t+1}+\gamma V^\pi(S_{t+1})
\;\middle|\;S_t=s
\right]
}.
$$

Expanding the expectation over actions, next states, and rewards gives

$$
\boxed{
V^\pi(s)
=
\sum_a\pi(a\mid s)
\sum_{s',r}p(s',r\mid s,a)
\left[r+\gamma V^\pi(s')\right]
}.
$$

---

## 8. Where each step is used

| Step | Purpose |
|---|---|
| Separate the first term | Isolates the immediate reward $R_{t+1}$ |
| Index shift | Recognizes the remaining sum as $\gamma G_{t+1}$ |
| Linearity | Separates or combines conditional expectations |
| Iterated expectation | Introduces the next state $S_{t+1}$ |
| Markov property | Makes earlier states irrelevant once $S_{t+1}$ is known |
| Stationarity | Identifies the next-state return with the same time-independent function $V^\pi$ |

The core mental model is

$$
\boxed{
\text{current value}
=
\text{expected immediate reward}
+
\text{discounted expected next-state value}
}.
$$

## Common mistakes

1. **Incorrect index shift:** forgetting that extracting one power of $\gamma$ produces $\gamma G_{t+1}$.
2. **Attributing everything to linearity:** linearity does not establish $\mathbb{E}[G_{t+1}\mid S_{t+1}]=V^\pi(S_{t+1})$; the Markov and stationarity assumptions are also needed.
3. **Confusing return and value:** $G_t$ is a random variable, while $V^\pi(s)$ is its conditional expectation.
4. **Ignoring policy stationarity:** if the policy changes with time, the value should generally be written as $V_t^\pi(s)$ rather than $V^\pi(s)$.
