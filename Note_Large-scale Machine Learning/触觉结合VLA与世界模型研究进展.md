# 触觉结合 VLA 与世界模型研究进展

> 调研截止：2026-08-09。本文将同行评审论文与 arXiv 预印本分开标注；2026 年的触觉 VLA / World Model 研究大部分仍是预印本，其大规模结论尚需独立复现。

## 1. 核心结论

1. **触觉不只是额外的 RGB 相机。** 它仅在接触发生后才具有高信息量，并具有强局部性与高时频特征。把触觉 token 在所有时刻直接与视觉 token 拼接，往往既浪费计算，又可能干扰预训练 VLA 的视觉—语言表示。
2. **当前最清晰的 VLA 趋势是“接触门控 + 快慢双速率”。** 慢速 VLA 负责语义理解和动作块（action chunk），快速触觉通路在接触、滑移或力偏差出现时修正动作。RDP、AT-VLA、UniTacVLA 与 OmniVTA 都从不同角度走向这一结构。
3. **触觉 + World Model 正从“多一路输入”转向“显式建模接触动力学”。** 2026 年的 VT-WM、OmniVTA、ContactWorld、VT-WAM、ViTacWorld 和 FeelWorld 不再只用当前触觉辅助动作回归，而是预测未来触觉/接触状态，再用于规划、策略筛选或高频偏差修正。
4. **规模化瓶颈首先是数据与硬件，其次才是模型容量。** 触觉数据受传感器形态、弹性体老化、温漂、安装差异和时间对齐影响，目前缺少类似 Open X-Embodiment 的统一触觉数据协议。
5. **“触觉基础模型”不等于“触觉 VLA”。** UniTouch、Octopi、Sparsh 解决表示或语义理解，并不直接生成机器人动作；FuSe、TLA、TacVLA、AT-VLA 等才把触觉接入可执行策略。

---

## 2. 概念边界：触觉策略 vs. 触觉世界模型

### 2.1 触觉条件策略

触觉条件策略（tactile-conditioned policy）直接用当前或历史触觉生成动作：

$$
\boxed{
a_{t:t+H}\sim \pi_\theta\left(\cdot\mid o^{v}_{\le t},o^{\tau}_{\le t},q_{\le t},\ell\right)
}
$$

- $o^v$：视觉观测；$o^\tau$：触觉/力觉观测；$q$：本体感觉；$\ell$：语言指令。
- 直接目标是动作预测，不要求显式预测“下一时刻会触摸到什么”。
- 代表工作：FuSe、TLA、VLA-Touch、TacVLA、AT-VLA、TacFiLM。

### 2.2 触觉世界模型

视觉—触觉世界模型（visuo-tactile world model）显式学习动作条件动力学：

$$
\boxed{
p_\phi\left(z^{v}_{t+1:t+H},z^{\tau}_{t+1:t+H}\mid
z^{v}_{\le t},z^{\tau}_{\le t},a_{t:t+H-1}\right)
}
$$

然后用预测未来评估候选动作：

$$
\boxed{
a^*_{t:t+H-1}=\arg\min_{a_{t:t+H-1}}
\mathbb{E}_{p_\phi}\left[\sum_{k=1}^{H}c\left(z^v_{t+k},z^\tau_{t+k},\ell\right)\right]
}
$$

它可用于：

- **规划：** 用 CEM（交叉熵方法）等搜索预测后果最好的动作序列。
- **策略引导：** 在推理时修改预训练策略的动作。
- **数据扩增：** 生成视觉—触觉—动作 rollout。
- **异常检测：** 比较预期与实际触觉，对滑移、卡滞或过力做快速修正。

> 关键区别：**策略学习“现在触摸到这样时该怎么动”；世界模型学习“如果这样动，接下来会触摸到什么”。**

---

## 3. 为什么纯视觉不够

### 3.1 不可观测的接触状态

多个物理状态可以对应几乎相同的图像：

- 夹爪已包围物体，但可能是未接触、稳定接触或正在滑移。
- 插销遮挡孔口后，图像不能给出接触力方向。
- 擦拭末端位姿相同，但法向力、摩擦和清洁效果可能完全不同。
- 柔性物体的内部应力与脱落前的微小滑移通常不可见。

因此接触操作更接近部分可观测马尔可夫决策过程（Partially Observable Markov Decision Process, POMDP）。触觉的价值不只是增加信息量，而是缩小接触状态的信念不确定性（belief uncertainty）。

### 3.2 时间尺度冲突

VLA 通常生成动作块以降低大模型推理成本，但滑移、碰撞或卡滞可能在动作块执行期间发生。更合理的系统是：

~~~mermaid
flowchart LR
    VL["Vision + Language<br/>全局语义与任务阶段"] --> S["慢速 VLA<br/>生成动作块"]
    S --> E["动作执行"]
    T["高频触觉<br/>接触/滑移/力偏差"] --> F["快速反射或残差策略"]
    F --> E
    E --> T
~~~

这里的“快速”不是让大模型以控制环频率运行，而是让小型触觉控制器对慢速计划做局部修正。

---

## 4. 触觉输入与表示

| 模态 | 典型输出 | 优势 | 局限 | 适合的模型接口 |
|---|---|---|---|---|
| 腕部六维力/力矩 | $[F_x,F_y,F_z,M_x,M_y,M_z]$ | 频率高、控制成熟 | 只有合力，难定位指尖接触 | 数值 token、MLP、快速力控制 |
| 关节力矩/电流 | 各关节时序 | 不需额外指尖硬件 | 接触与本体动力学耦合 | 时序 Transformer、状态估计 |
| 压阻/电容/磁性阵列 | taxel 压力或磁场阵列 | 轻薄、可覆盖大面积 | 标定和传感器差异大 | 时空编码器、低维 tactile token |
| 视觉式触觉（GelSight / DIGIT / GelStereo） | 弹性体形变图像、marker 位移 | 接触几何分辨率高，可复用 ViT | 体积、耐用性、胶体老化和照明域偏移 | ViT、Sparsh 等预训练编码器 |
| 事件/振动/声学触觉 | 稀疏事件或高频波形 | 对初始滑移、摩擦和冲击敏感 | 与主流 VLA tokenization 差异大 | 小型快速编码器、异步事件通路 |

### 4.1 从原始信号到 tactile token

通用触觉编码器希望把原始信号压缩为控制相关表示：

$$
z_t^\tau=E_\tau\left(o^\tau_{t-K:t};s_{\text{sensor}}\right),
$$

其中 $s_{\text{sensor}}$ 是传感器类型/实例 token。理想的 $z_t^\tau$ 应保留接触位置、法向/切向力、滑移、局部形状与材料性质，同时尽量忽略灯光、marker 图案、胶体老化等任务无关因素。

三篇关键前置工作：

- **UniTouch（CVPR 2024）：** 将异构视觉式触觉对齐到已具备视觉—语言语义的图像嵌入，并加入传感器专属 token，证明跨传感器、跨模态对齐的可行性。
- **Octopi（RSS 2024）：** 将 GelSight 触觉视频与物理属性语言对齐，使大型视觉—语言模型可对触觉属性做中间推理；它不是动作策略。
- **Sparsh（CoRL 2024）：** 在 $460\text{k}+$ 触觉图像上用 MAE、DINO 和 I-JEPA 等自监督目标预训练，并以 TacBench 检验力、滑移、姿态、抓取稳定性与操作规划。它成为多个后续 VLA/WM 的触觉编码器。

---

## 5. 触觉 + VLA：方法谱系

### 5.1 语言作为异构传感器的对齐层

**FuSe / Beyond Sight（ICRA 2025）** 是重要起点。它通过多模态对比损失和感觉条件语言生成损失，把视觉、触觉、声音对齐到语言语义，再把方法用于 Octo 类通用策略和 PaliGemma-based 3B VLA。

它解决的是“这个感觉意味着什么”，并展示了小规模触觉数据可以接入已有通用策略；但语义对齐本身不等于毫秒级力控制。

### 5.2 将触觉编码成 token

**TLA（2025，arXiv）** 使用 Qwen2-VL 7B，把两个 GelStereo 指尖上连续 4 时刻、共 8 帧触觉图像排成网格图，再由 ViT 编码并生成离散化的 3-DoF 微调动作。它构建了 24k 个触觉—动作—指令样本，但数据主要来自高保真仿真，任务和动作空间较窄。

**VTLA（Biomimetic Intelligence and Robotics 2026）** 在 TLA 上增加视觉，并引入直接偏好优化（Direct Preference Optimization, DPO），用动作偏好缓解“下一 token 分类损失”与“连续动作质量”之间的不匹配。

此路线可直接复用 VLM token 接口；代价是高分辨率触觉时序会产生大量 token，而动作离散化误差对精密接触尤其敏感。

### 5.3 轻量融合与接触门控

直接拼接新模态 token 有两个问题：自由空间阶段的触觉大多是空白或噪声；VLA 预训练中没有触觉 token，强行注入可能破坏已有能力。2026 年出现三种典型解法：

- **TacVLA（arXiv 2026）：** 只在检测到接触时激活 tactile token。
- **AT-VLA（CVPR 2026）：** 自适应决定触觉注入时机与层位，并以快速触觉流修正慢速视觉—语言流。作者报告闭环反应时间为 $0.04\,\mathrm{s}$，并比较触觉图、marker 位移与 6D 力。
- **TacFiLM（ECCV 2026）：** 用预训练触觉特征对中间视觉特征做特征级线性调制（Feature-wise Linear Modulation, FiLM），避免大量增加 token。

门控融合可抽象为：

$$
h'_t=h_t^v+g_t C\left(h_t^v,z_t^\tau\right),\qquad
g_t=\sigma\left(f_{\text{contact}}(z_t^\tau,h_t^v)\right).
$$

自由空间中 $g_t\approx 0$，尽量保留原 VLA 表示；接触阶段 $g_t\to 1$，动作生成才强依赖触觉。

### 5.4 层级化与快慢系统

- **Reactive Diffusion Policy（RDP，2025 预印本）：** 慢速潜在扩散策略生成动作块，快速非对称 tokenizer 用触觉/力反馈修正。它不是 VLA，但清楚暴露了 action chunking 与高频接触反应的冲突，是后续触觉 VLA 的重要架构前驱。
- **VLA-Touch（2025 预印本）：** 不微调基础 VLA；高层以预训练触觉—语言模型产生语义反馈，低层以触觉条件扩散控制器精修 VLA 动作。
- **Tactile-VLA（2025 预印本，投稿 ICLR 2026）：** 把 VLM 的物理常识与混合位置—力控制器连接，强调以少量演示激活“轻柔、用力、易碎性”等语义先验。

### 5.5 从当前触觉到未来触觉

2026 年的新工作开始模糊 VLA 与 World Model 的边界：

- **UniTacVLA：** 联合学习当前触觉理解、触觉思维链（tactile chain-of-thought）和粗到细的未来触觉预测，再用触觉—动作混合控制器修正低频动作块。
- **$N_0$-VTLA：** 尝试在大规模视觉—触觉数据 NeoData 上预训练，再分阶段接入预测触觉通路和优势条件离线策略改进 ALTER。

这说明触觉正从被动 observation 变成模型要预测的动态变量。但两者截至调研日均为新近预印本，跨硬件泛化与第三方复现仍待检验。

---

## 6. 触觉 + World Model：从预测到规划

### 6.1 前驱：跨模态生成

VisGel、Touch and Go 和 *Generating Visual Scenes from Touch* 等早期工作主要研究 $p(o^\tau\mid o^v)$ 或 $p(o^v\mid o^\tau)$。它们证明材料、几何与触觉之间存在可学习映射，但通常不以机器人动作为条件，因此不是严格意义上可用于控制的世界模型。

### 6.2 联合潜在动力学

**Visuo-Tactile World Models（VT-WM，2026 预印本）** 使用：

- Cosmos 编码器提取外部视觉 latent；
- Sparsh-X 编码四个 Digit 360 指尖的触觉 latent；
- Transformer 交替执行时空自注意力和动作交叉注意力，预测下一步视觉与触觉 latent。

其数据为 124 条多任务示教（约 112k datapoints）。论文报告触觉可改善自回归 rollout 的物体持久性与运动物理一致性，并提升零样本真机规划。核心直觉是：触觉能减少纯视觉 rollout 中物体“消失、瞬移、无接触却运动”的幻觉。

### 6.3 预测 + 反馈的双通路

**OmniVTA（2026 预印本）** 将世界模型放入完整控制系统：

1. 自监督触觉编码器；
2. 预测短时接触演化的双流视觉—触觉世界模型；
3. 接触感知融合策略；
4. $60\,\mathrm{Hz}$ 反射控制器，比较预测与实际触觉并修正偏差。

其 OmniViTac 数据集声称包含 $21{,}000+$ 条轨迹、86 个任务与 $100+$ 个物体。这比“只做预测”更接近实际控制，但数据和代码可用程度仍应按官方发布进度核对。

### 6.4 表示结构比单纯增加模态更重要

**ContactWorld（2026 预印本）** 在 12 个接触密集任务、6 种感知模态上比较世界模型。其关键结论是：触觉能否帮助长时域规划，不只取决于“有没有触觉”，还取决于触觉与视觉表示的结构兼容性。

实验中，保留空间结构的点云视觉表示优于普通腕部/前视图像；再与保留空间结构和交互动力学的触觉力场结合，规划性能更好。这对“所有模态都压成几个全局 token”的设计提出警告。

### 6.5 世界预测与动作生成正在合流

- **VT-WAM（2026 预印本）：** 在统一流匹配（flow matching）框架内联合预测未来视觉、触觉形变与动作，并以接触门控的 Action-Visual-Tactile Attention Guidance 让动作查询在接触阶段真正使用触觉证据。
- **ViTaL Policy Steering（2026 预印本）：** 高层用视觉预测选择长时程行为模式，低层用触觉预测和文本条件触觉奖励编辑扩散策略动作；世界模型作为推理时 verifier（验证器），而不取代基础策略。
- **ViTacWorld（2026 预印本）：** 结合公开真实触觉数据和仿真，生成动作条件的视觉—触觉 rollout，用于策略数据扩增与策略评估。
- **FeelWorld（2026 预印本）：** 把触觉未来显式分为接触状态、3D 力相关 latent 和滑移状态，并以接触门控避免自由空间的无关触觉干扰视觉预测。

最新趋势不是简单的“VLA 还是 WM”二选一，而是：

$$
\boxed{
\text{语义先验（VLA）}
+\text{接触动力学预测（WM）}
+\text{高频闭环修正（Controller）}
}
$$

---

## 7. 代表工作对比

### 7.1 已同行评审的关键节点

| 工作 | 发表 | 定位 | 触觉形式 | 主要贡献 | 直接输出动作 |
|---|---|---|---|---|---|
| [UniTouch](https://openaccess.thecvf.com/content/CVPR2024/html/Yang_Binding_Touch_to_Everything_Learning_Unified_Multimodal_Tactile_Representations_CVPR_2024_paper.html) | CVPR 2024 | 通用多模态表示 | 多种视觉式触觉 | 触觉与视觉/语言/声音对齐，传感器 token | 否 |
| [Octopi](https://arxiv.org/abs/2405.02794) | RSS 2024 | 触觉—语言推理 | GelSight 视频 | 物理属性中间推理与 PhysiCLeAR | 否 |
| [Sparsh](https://arxiv.org/abs/2410.24090) | CoRL 2024 | 触觉基础表示 | 多种视觉式触觉 | $460\text{k}+$ 自监督预训练、TacBench | 否 |
| [Beyond Sight / FuSe](https://arxiv.org/abs/2501.04693) | ICRA 2025 | 异构感知通用策略 | 触觉 + 声音 + 视觉 | 以语言对齐稀缺传感器并接入通用策略/VLA | 是 |
| [VTLA](https://doi.org/10.1016/j.birob.2026.100333) | Biomimetic Intelligence and Robotics 2026 | 视觉—触觉—语言—动作 | GelStereo 2.0 + RGB | 视觉引导时序 token + DPO 连续动作偏好 | 是 |
| [AT-VLA](https://arxiv.org/abs/2605.07308) | CVPR 2026 | 触觉 VLA | 触觉图、marker、6D 力 | 自适应注入 + 快慢双流 | 是 |
| [TacFiLM](https://arxiv.org/abs/2603.14604) | ECCV 2026 | 轻量触觉 VLA | 预训练触觉特征 | 用 FiLM 做中间特征调制 | 是 |

### 7.2 需要谨慎解读的新近预印本

| 工作 | 时间 | 路线 | 真机验证 | 关键点 |
|---|---:|---|---|---|
| [TLA](https://arxiv.org/abs/2503.08548) | 2025-03 | Tactile-Language-Action | 是，插销 | 仅触觉 + 语言，Qwen2-VL 7B，24k 仿真样本 |
| [Reactive Diffusion Policy](https://arxiv.org/abs/2503.02881) | 2025-03 | 视觉—触觉策略 | 是，3 类任务 | 慢速动作块 + 快速触觉反应；不是 VLA |
| [Tactile-VLA](https://arxiv.org/abs/2507.09160) | 2025-07 | 语义物理先验 | 是 | VLM 常识 + 位置—力混合控制 |
| [VLA-Touch](https://arxiv.org/abs/2507.17294) | 2025-07 | 双层触觉反馈 | 是 | 高层语义触觉 + 低层扩散修正 |
| [VT-WM](https://arxiv.org/abs/2602.06001) | 2026-02 | 视觉—触觉 WM | 是，8 任务 | 联合潜在动力学，Digit 360 + Sparsh-X |
| [TacVLA](https://arxiv.org/abs/2603.12665) | 2026-03 | 接触门控 VLA | 是 | 只在接触时激活 tactile token |
| [OmniVTA](https://arxiv.org/abs/2603.19201) | 2026-03 | WM + 策略 + 反射 | 是，6 类交互 | OmniViTac + 短时预测 + 60 Hz 修正 |
| [ContactWorld](https://arxiv.org/abs/2606.13877) | 2026-06 | WM 基准 | 基准为主 | 12 任务、6 模态；空间结构与模态兼容性 |
| [ViTaL Policy Steering](https://arxiv.org/abs/2606.14981) | 2026-06 | WM 验证器 | 是，3 任务 | 视觉选行为模式，触觉精修局部接触 |
| [UniTacVLA](https://arxiv.org/abs/2606.31723) | 2026-06 | 预测型 VTLA | 是，4 类任务 | 触觉 CoT + 未来预测 + 混合控制 |
| [VT-WAM](https://arxiv.org/abs/2607.02503) | 2026-07 | World-Action Model | 是，6 任务 | 流匹配联合生成视觉、触觉与动作 |
| [ViTacWorld](https://arxiv.org/abs/2607.22530) | 2026-07 | 可扩展触觉 WM | 是 | 仿真 + 真实数据，生成 rollout 做扩增/评估 |
| [$N_0$-VTLA](https://arxiv.org/abs/2607.23782) | 2026-07 | 大规模 VTLA | 是 | 视触觉预训练 + 预测通路 + 离线策略改进 |
| [FeelWorld](https://arxiv.org/abs/2607.24267) | 2026-07 | 层级触觉 WM | 是，3 任务 | 显式预测接触、力相关 latent 与滑移 |

> “真机验证”只表示论文包含真实机器人实验，**不代表已证明跨传感器、跨机器人或大规模通用性**。

---

## 8. 数据、评测与规模化瓶颈

### 8.1 数据难以直接合并

触觉图像依赖胶体材料、厚度、镜头、照明、marker 图案、安装角度、预载荷、温度与磨损。同为 GelSight 也不代表数据可直接混合训练。

现实中仍需传感器实例 token、per-sensor normalization、时序增强、模态 dropout 和少量目标传感器校准。

### 8.2 时间对齐是隐藏的核心问题

真实系统中：

$$
t_{\text{camera}}\ne t_{\text{tactile}}\ne t_{\text{action-command}}\ne t_{\text{physical-response}}.
$$

若忽略传输、曝光、编码与机械响应延迟，模型可能学到错误因果关系；对世界模型而言，这会直接成为 rollout 的系统性偏差。

### 8.3 当前评估还不能回答“是否通用”

更有说服力的评估应同时包含：

- 未见物体、材料、摩擦、几何间隙和外部扰动；
- 未见传感器实例或传感器老化后的分布偏移；
- 模态缺失、触觉失效与时间延迟；
- 成功率以外的峰值力、力积分、滑移次数、物体损伤和控制频率；
- 跨机器人/夹爪迁移，以及相同计算预算下的纯视觉基线。

---

## 9. 当前共识与开放问题

### 9.1 证据相对稳固

- 触觉对遮挡、精密插入、滑移和力约束任务有明显价值。
- 触觉预训练表示比每个任务从零训练编码器更有数据效率。
- 触觉与视觉需要不同时间尺度；快慢分层是合理系统先验。
- 按接触状态切换融合强度，比全程无条件拼接更符合信号性质。

### 9.2 尚缺充分证据

- 单一触觉 VLA 已能跨传感器、跨机器人、跨任务通用。
- 触觉预训练已经出现与视觉—语言模型相当的 scaling law（规模定律）。
- 触觉世界模型可在长时域、多分支接触中稳定替代真实交互。
- 触觉仿真的 sim-to-real gap 必然小于视觉 gap。

### 9.3 最值得跟进的研究问题

1. **传感器不变表示：** 如何跨 GelSight、DIGIT、磁性阵列和 6D 力保留共享接触语义，同时不丢失精细空间信息？
2. **接触事件 tokenization：** 是否可只对接触开始、滑移、力突变和脱离等事件生成 token？
3. **因果接触世界模型：** 如何把外观相关性与动作造成的力学变化分开？
4. **不确定性感知规划：** 世界模型不仅预测未来，还应告诉规划器哪些接触结果不确定。
5. **边缘部署：** 将 tactile encoder、接触门控和快速残差控制器部署到夹爪/末端边缘计算单元，而把慢速 VLA/WM 放在主机，是自然的 edge intelligence 切入点。
6. **失败数据与自我改进：** 触觉可直接标识卡滞、过力、滑移与假抓取，适合离线 RL、偏好学习和自主数据筛选。

---

## 10. 初学者阅读路线

### 第一阶段：触觉表示

1. [Sparsh](https://arxiv.org/abs/2410.24090)：理解触觉自监督预训练与专用基准。
2. [Octopi](https://arxiv.org/abs/2405.02794)：理解触觉—语言对齐，以及感知模型与动作模型的区别。

### 第二阶段：触觉进入策略

1. [Beyond Sight / FuSe](https://arxiv.org/abs/2501.04693)：语言作为异构感知对齐层。
2. [Reactive Diffusion Policy](https://arxiv.org/abs/2503.02881)：为什么接触控制需要快慢分层。
3. [AT-VLA](https://arxiv.org/abs/2605.07308)：门控注入、多种触觉格式与双流 VLA。

### 第三阶段：触觉世界模型

1. [Visuo-Tactile World Models](https://arxiv.org/abs/2602.06001)：联合视觉—触觉潜在动力学的清晰入口。
2. [ContactWorld](https://arxiv.org/abs/2606.13877)：表示结构、模态兼容性与长时域误差。
3. [VT-WAM](https://arxiv.org/abs/2607.02503)：世界预测与动作生成的合流。

### 如果只读两篇

📄 [Beyond Sight: Finetuning Generalist Robot Policies with Heterogeneous Sensors via Language Grounding](https://arxiv.org/abs/2501.04693) — ICRA 2025  
用语言作为共享语义空间，将小规模触觉/声音数据接入通用机器人策略和 VLA。

📄 [Visuo-Tactile World Models](https://arxiv.org/abs/2602.06001) — arXiv 2026  
用动作条件的联合视觉—触觉潜在动力学生成更符合接触物理的未来，并用于真机规划。

---

## 11. 与现有笔记的关系

- [[World Model]]：世界模型的通用概念、Dreamer、JEPA 与视频生成路线。
- [[具身数据]]：真实、仿真、人类视频和神经数据扩增的数据金字塔。
- [[../5003 Tactile/Weekly meeting]]：触觉数据采集、GelSight 漂移、仿真与 UMI 迁移问题。
- [[../CS_Note/机器学习/机器人/VLA后训练]]：VLA 的下游适配与策略改进。

## 12. 参考文献

### 表示学习与触觉—语言

- Yang et al., [Binding Touch to Everything: Learning Unified Multimodal Tactile Representations](https://openaccess.thecvf.com/content/CVPR2024/html/Yang_Binding_Touch_to_Everything_Learning_Unified_Multimodal_Tactile_Representations_CVPR_2024_paper.html), CVPR 2024.
- Yu et al., [Octopi: Object Property Reasoning with Large Tactile-Language Models](https://arxiv.org/abs/2405.02794), RSS 2024.
- Higuera et al., [Sparsh: Self-supervised touch representations for vision-based tactile sensing](https://arxiv.org/abs/2410.24090), CoRL 2024.
- Yang et al., [Generating Visual Scenes from Touch](https://openaccess.thecvf.com/content/ICCV2023/html/Yang_Generating_Visual_Scenes_from_Touch_ICCV_2023_paper.html), ICCV 2023.

### 触觉策略与 VLA

- Jones et al., [Beyond Sight](https://arxiv.org/abs/2501.04693), ICRA 2025.
- Xue et al., [Reactive Diffusion Policy](https://arxiv.org/abs/2503.02881), arXiv 2025.
- Hao et al., [TLA](https://arxiv.org/abs/2503.08548), arXiv 2025.
- Zhang et al., [VTLA](https://doi.org/10.1016/j.birob.2026.100333), Biomimetic Intelligence and Robotics 2026.
- Huang et al., [Tactile-VLA](https://arxiv.org/abs/2507.09160), arXiv 2025.
- Bi et al., [VLA-Touch](https://arxiv.org/abs/2507.17294), arXiv 2025.
- Zhang et al., [TacVLA](https://arxiv.org/abs/2603.12665), arXiv 2026.
- Morissette et al., [Tactile Modality Fusion for Vision-Language-Action Models](https://arxiv.org/abs/2603.14604), ECCV 2026.
- Li et al., [AT-VLA](https://arxiv.org/abs/2605.07308), CVPR 2026.
- Zhang et al., [UniTacVLA](https://arxiv.org/abs/2606.31723), arXiv 2026.
- NeoteAI Team and Fudan TEAI Team, [$N_0$-VTLA](https://arxiv.org/abs/2607.23782), arXiv 2026.

### 视觉—触觉世界模型

- Higuera et al., [Visuo-Tactile World Models](https://arxiv.org/abs/2602.06001), arXiv 2026.
- Zheng et al., [OmniVTA](https://arxiv.org/abs/2603.19201), arXiv 2026.
- Zhang et al., [ContactWorld](https://arxiv.org/abs/2606.13877), arXiv 2026.
- Wu et al., [Inference-time Policy Steering via Vision and Touch](https://arxiv.org/abs/2606.14981), arXiv 2026.
- Tian et al., [VT-WAM](https://arxiv.org/abs/2607.02503), arXiv 2026.
- Huang et al., [ViTacWorld](https://arxiv.org/abs/2607.22530), arXiv 2026.
- Ma et al., [FeelWorld](https://arxiv.org/abs/2607.24267), arXiv 2026.
