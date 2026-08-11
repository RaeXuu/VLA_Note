# SO(3)、SE(3)、Sim(3) 群

SO(3)、SE(3)、Sim(3) 是具有严格包含关系和不同物理意义的数学群（李群，Lie Group）。核心区别在于**自由度（Degrees of Freedom, DoF）**以及所允许的**几何变换类型**：

- **$\text{SO}(3)$**：只管**旋转**（3 自由度）
- **$\text{SE}(3)$**：主管**旋转 + 平移**（刚体运动，6 自由度）
- **$\text{Sim}(3)$**：主管**旋转 + 平移 + 缩放**（相似变换，7 自由度）

$$\text{SO}(3) \subset \text{SE}(3) \subset \text{Sim}(3)$$

---

## 一、$\text{SO}(3)$ —— 特殊正交群（Special Orthogonal Group）

$\text{SO}(3)$ 仅表示三维空间中的**纯旋转**。

**物理意义：** 一个刚体绕着原点转动，转完之后它的位置没变、大小没变，只是朝向（姿态）变了。

**矩阵形式：** $3 \times 3$ 矩阵 $\mathbf{R}$。

**数学约束：**

$$\mathbf{R}^T\mathbf{R} = \mathbf{I}, \quad \det(\mathbf{R}) = 1$$

$\det(\mathbf{R}) = 1$ 排除了镜像翻转，确保是物理上可实现的连续旋转。

**自由度：3**（绕 X、Y、Z 轴旋转的三个角度）。

---

## 二、$\text{SE}(3)$ —— 特殊欧几里得群（Special Euclidean Group）

$\text{SE}(3)$ 表示三维空间中的**刚体运动（旋转 + 平移）**。

**物理意义：** 刚体不仅可以转动，还可以在空间中平移。但刚体本身的**形状和大小绝对不能改变**（任意两点之间的欧氏距离保持不变）。

**矩阵形式：** 为把旋转和平移写进同一个矩阵，使用 $4 \times 4$ 的**齐次变换矩阵**：

$$\mathbf{T} = \begin{bmatrix} \mathbf{R} & \mathbf{p} \\ \mathbf{0}^T & 1 \end{bmatrix}$$

其中 $\mathbf{R} \in \text{SO}(3)$ 是旋转矩阵，$\mathbf{p} \in \mathbb{R}^3$ 是平移向量。

**自由度：6**（3 旋转 + 3 平移）。这是六自由度机械臂、无人机在空间中位姿的完全表述。

---

## 三、$\text{Sim}(3)$ —— 相似变换群（Similarity Transformation Group）

$\text{Sim}(3)$ 在 $\text{SE}(3)$ 的基础上，增加了一个**等比例缩放因子（Scale）**。

**物理意义：** 物体不仅可以旋转、平移，还可以**整体放大或缩小**。它保持了物体的"几何相似性"——三角形放大后还是相似三角形，角度不变，边长变了。

**矩阵形式：** 在旋转矩阵前引入一个缩放标量 $s$：

$$\mathbf{S} = \begin{bmatrix} s\mathbf{R} & \mathbf{p} \\ \mathbf{0}^T & 1 \end{bmatrix}$$

其中 $s \in \mathbb{R}^+$ 是一个正的缩放因子。

**自由度：7**（3 旋转 + 3 平移 + 1 缩放）。

### 为什么 SLAM 里需要 $\text{Sim}(3)$？

在视觉 SLAM 中，使用**单目相机（Monocular Camera）**时，由于单个摄像头无法直接获取绝对深度，算法重建出来的三维地图存在**尺度不确定性（Scale Ambiguity）**。

当单目 SLAM 发生闭环检测（Loop Closure）并进行全局优化时，两个历史轨迹之间不仅存在旋转和平移的偏差，还存在**尺度的不一致**。此时必须在 $\text{Sim}(3)$ 空间下进行位姿图优化（Pose Graph Optimization），把全局尺度校正回来。

---

## 总结对比

| 群 | 自由度 | 矩阵大小 | 包含变换 | 典型应用 |
|---|---|:---:|---|---|
| **$\text{SO}(3)$** | 3 | $3 \times 3$ | 纯旋转 | 惯导姿态、卫星姿态控制、机械臂末端朝向 |
| **$\text{SE}(3)$** | 6 | $4 \times 4$ | 旋转 + 平移 | 机械臂运动学、激光 SLAM、刚体轨迹规划 |
| **$\text{Sim}(3)$** | 7 | $4 \times 4$ | 旋转 + 平移 + 缩放 | 单目视觉 SLAM 闭环优化、多传感器尺度对齐 |

---

## 李代数对应

这些李群对应的李代数（Lie Algebra）分别是 $\mathfrak{so}(3)$、$\mathfrak{se}(3)$、$\mathfrak{sim}(3)$，维度与群的自由度一致。

| 群 | 李代数 | 维度 | 元素 |
|---|---|---|---|
| $\text{SO}(3)$ | $\mathfrak{so}(3)$ | 3 | $\boldsymbol{\phi} \in \mathbb{R}^3$（旋转向量 / 轴角） |
| $\text{SE}(3)$ | $\mathfrak{se}(3)$ | 6 | $\boldsymbol{\xi} = [\boldsymbol{\rho}, \boldsymbol{\phi}]^T \in \mathbb{R}^6$（twist 坐标） |
| $\text{Sim}(3)$ | $\mathfrak{sim}(3)$ | 7 | $[\boldsymbol{\rho}, \boldsymbol{\phi}, \lambda]^T \in \mathbb{R}^7$（增加尺度分量） |

李代数上的指数映射（$\exp$）将李代数元素映射回李群元素，对数映射（$\log$）反之。在优化问题（如 SLAM 后端）中，在 Lie 代数上做梯度下降，再用 $\exp$ 回到群流形上，从而自然地保持矩阵约束（如 $\mathbf{R}^T\mathbf{R} = \mathbf{I}$）。

---

## 相关笔记

- [[相机内外参]] — $\text{SO}(3)$ 和 $\text{SE}(3)$ 在投影模型中的具体使用
- [[3D点云]] — 点云配准中的刚体变换
- [[6D物体姿态估计]] — 物体 6DoF 位姿的估计
