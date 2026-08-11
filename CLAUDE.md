# CLAUDE.md

## 这个 vault 是什么

Obsidian 知识库，系统学习机器人学。笔记通过 `[[wikilink]]` 互相链接，与同级的 `CS_Note` vault 有交叉引用。

## 目录结构

```
_机器人学导航.md                ← MOC 总入口
基础概念.md                     ← 术语速查
文献阅读索引.md                 ← 论文阅读清单（复选框）

感知 Perception/                ← 3D点云、6D姿态估计、相机标定
状态估计 State Estimation/      ← KF/EKF/粒子滤波/图优化
SLAM/                           ← LiDAR SLAM、视觉 SLAM
规划 Planning/                  ← A*/RRT*/轨迹优化
决策 Decision/                  ← FSM/行为树/MDP
控制 Control/                   ← 经典控制理论、PID
机器人学 Robotics/              ← ROS2、坐标系、运动学/动力学、Sim-to-Real
学习与智能/                     ← 待迁移内容

行业与公司/                     ← 各公司产品/路线分析
Robotics_Paper/                 ← 文献 PDF
Xingyu Liu/                     ← 文献 PDF
```

## 工作模式

**纯被动触发。** 只在用户明确要求"帮我写一篇 XX 笔记"时才创建/修改笔记。日常讨论中不主动提议写笔记。

## 写作风格

- **理论型笔记**（Diffusion、SLAM、规划）：推导驱动，公式 + 表格 + 直觉解释，关键公式用 `\boxed{}`
- **工具型笔记**（ROS2）：命令速查 + 最小示例 + 常见坑
- **概览型笔记**（Sim-to-Real）：全景图 + 方法对比表 + 选型指南
- **语言**：中文为主，英文术语首次出现加括号注中文翻译
- **深度标准**：研究生入门水平，不要教科书级别的穷举，抓核心直觉和关键公式
- **准确性优先**：类比和直觉可以辅助，但不能替代准确的技术描述

## 参考标准

内容以领域权威教材/论文为基准。写作时：
- 内容对齐对应领域的标准教材，不做野路子的"个人理解"
- 准确性优先于花哨

## 论文推荐

每次回答技术问题时，附带推荐 1-2 篇相关权威论文，格式如下：

```
📄 [论文标题](arxiv链接) — 会议/期刊 年份
一句话核心贡献
```

优先从以下来源选取：
- **会议**：CoRL、RSS、ICRA、IROS、NeurIPS、ICLR
- **期刊**：TRO、IJRR、RA-L、Science Robotics
- 优先推荐近年的论文，但经典奠基性论文（如 LOAM 2014、ORB-SLAM 2015、Probabilistic Robotics 等）不受时间限制
- 尽量选与用户学习方向（embodied AI、robot learning、edge intelligence）相关的

### 各方向参考来源

| 方向 | 参考 |
|------|------|
| 状态估计 | Thrun et al., *Probabilistic Robotics* |
| SLAM | Barfoot, *State Estimation for Robotics* |
| 规划 | LaValle, *Planning Algorithms*; Choset et al., *Principles of Robot Motion* |
| 运动学/动力学 | Siciliano et al., *Robotics: Modelling, Planning and Control*; Craig, *Introduction to Robotics* |
| 控制 | Ogata, *Modern Control Engineering* |
| 计算机视觉 | Szeliski, *Computer Vision: Algorithms and Applications*; Hartley & Zisserman, *Multiple View Geometry* |
| 强化学习 | Sutton & Barto, *Reinforcement Learning: An Introduction* |
| Diffusion/Flow Matching | 以原始论文为准（Ho et al. 2020, Song et al. 2021, Lipman et al. 2023） |

## 格式约定

不设模板，随内容自由发挥。但：
- 文件名用中文，简洁描述主题
- 代码块标注语言（```python、```bash 等）
- 公式用 LaTeX（Obsidian 原生支持）
- 写完新笔记后，顺手在相关旧笔记里补上反向 `[[链接]]`
- 附件在 `assets/` 下平铺，不建子文件夹

## 跨 vault 引用

同级 `CS_Note` vault 包含 ML/DL 基础笔记，机器人学笔记通过 `[[../CS_Note/...]]` 交叉引用。

## 环境约定

- 终端指令仅提供 **macOS（Homebrew）** 和 **Ubuntu 22（APT）**，无需 Windows 指令
- 涉及包管理时同时给出 `brew install` 和 `apt install`

## 注意事项

- 所有修改用户会 review，无额外限制
- Obsidian 插件 `obsidian-custom-attachment-location` 已删除，附件统一在 `assets/` 下
- Obsidian 设置 `"attachmentFolderPath": "assets"`，`"alwaysUpdateLinks": true`
