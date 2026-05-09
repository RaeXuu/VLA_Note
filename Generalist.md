# GEN-0

One core feature is Harmonic Reasoning, in which the models are trained to simultaneously think and act seamlessly.

To address this problem, Harmonic Reasoning involves a fundamentally new approach to training models, and creates a "harmonic" interplay between asynchronous, continuous-time streams of sensing and acting tokens.

We believe that GEN-0 marks the beginning of a new era: embodied foundation models whose capabilities predictably scale with physical interaction data – not just from text, images, or simulation – but the real world.

![[Screenshot 2026-04-23 at 4.05.51 PM.png]]


### 1. 均方误差 (MSE)：基础距离衡量

$$\text{MSE}_{\text{val}} = ||\mathbf{a}^\star - \hat{\mathbf{a}}||^2_2$$

- **含义**：这是最标准的误差计算。$\mathbf{a}^\star$ 是真实标签（真人的动作），$\hat{\mathbf{a}}$ 是模型预测的动作。
    
- **局限性**：MSE 倾向于计算所有可能动作的平均值。如果数据中既有向左走的样本，又有向右走的样本，最小化 MSE 的模型可能会选择“向前走”（左右的平均值），这在物理世界中通常会导致失败。

### 2. 逆向 KL 散度：捕捉“众数寻求”行为

文中提到 Reverse KL 能更好地衡量 **众数寻求（mode-seeking）** 行为。

- **为什么用“逆向”？**
    
    - **前向 KL ($D_{\text{KL}}(p||q)$)**：强迫模型 $q$ 覆盖真实分布 $p$ 的所有可能性，容易导致预测结果过于模糊（Mean-seeking）。
    - **逆向 KL ($D_{\text{KL}}(q||p)$)**：强迫模型的预测 $q$ 锁定在真实分布 $p$ 的某个高概率区域（即“众数”）。对于机器人来说，精准地选择一种可行的方案（比如坚定地向左走），比模糊地尝试所有方案要好。

### 3. 数学实现：如何计算这个散度？

由于模型输出通常是一组离散的采样点，直接计算连续分布的 KL 散度很困难，所以文中采用了**蒙特卡罗估计法（Monte-Carlo estimator）**。

#### A. 构建概率密度函数

为了计算，研究者将采样点“平滑”成了连续的分布：

- **策略密度 $q$**：将模型生成的 $M$ 个动作样本 $\{\hat{\mathbf{a}}_m\}$ 看作是一组**高斯混合模型**（Mixture of Gaussians）的中心。每个样本都被赋予一个单位方差的法向分布。
    
- **地面真值密度 $p$**：将真实动作 $\mathbf{a}^\star$ 看作是一个以它为中心的单一高斯分布 $\mathcal{N}(\mathbf{a}; \mathbf{a}^\star, \mathbf{I})$。
    

#### B. 蒙特卡罗近似公式

$$\widehat{D}_{\text{KL}}(q||p) \approx \frac{1}{M} \sum_{m=1}^{M} [\log q(\hat{\mathbf{a}}_m) - \log p(\hat{\mathbf{a}}_m)]$$

这个公式的作用是：

1. 从模型中抽取 $M$ 个样本。
    
2. 计算这些样本在模型自身分布 $q$ 下的对数概率。
    
3. 计算这些样本在目标真实分布 $p$ 下的对数概率。
    
4. **物理意义**：如果模型生成的样本 $\hat{\mathbf{a}}_m$ 距离真实动作 $\mathbf{a}^\star$ 非常远，那么 $\log p(\hat{\mathbf{a}}_m)$ 会变得非常小（即负值很大），从而导致整个 $D_{\text{KL}}$ 显著增大。


  
## The Dark Matter of Robotics: Physical Commonsense

This is **physical commonsense**. It is the reactive, closed-loop intelligence behind acting in the real world: an intuition for forces, friction, compliance, and uncertainty, learned through a lifetime of sensorimotor experience, compiled into reflex and muscle memory.

Polanyi’s point cuts deep here: physical commonsense is hard to describe _because_ it is not linguistic. It does not live in propositions — it lives in the loop between sensing and action.
Models trained on Internet text (and images) can learn a specific kind of _semantic_ commonsense: statistical regularities and patterns over words, facts, and symbols.