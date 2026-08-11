# SLAM（Simultaneous Localization And Mapping）

边建图边定位——机器人学最经典的问题之一，曾经被称为"鸡生蛋蛋生鸡"问题：要定位需要地图，要建图需要知道自己在哪。

---

## 一、问题形式化

给定运动指令序列和传感器观测序列，同时估计机器人轨迹 $\mathcal{X}$ 和地图 $\mathcal{M}$：

$$p(\mathcal{X}, \mathcal{M} | \mathcal{Z}, \mathcal{U})$$

- $\mathcal{X} = \{x_0, x_1, \dots, x_T\}$ — 轨迹
- $\mathcal{M}$ — 地图（路标点、占据栅格、surfel...）
- $\mathcal{Z} = \{z_1, \dots, z_T\}$ — 传感器观测
- $\mathcal{U} = \{u_1, \dots, u_T\}$ — 里程计/IMU 的运动输入

---

## 二、SLAM 分类

| 维度 | 分类 |
|------|------|
| **传感器** | LiDAR SLAM / Visual SLAM / Visual-Inertial SLAM (VINS) |
| **地图表示** | 稀疏（路标点） / 半稠密 / 稠密 |
| **后端** | 滤波（EKF-SLAM） / 图优化（Factor Graph） |
| **前端** | 直接法（photometric error）/ 间接法（特征点/线/面） |

---

## 三、Factor Graph——现代 SLAM 的统一语言

SLAM 本质上是一个因子图上的非线性最小二乘问题：

$$X^* = \arg\min_X \underbrace{\sum_i \|r_{i}(x_i, x_{i+1}) - u_i\|^2_{\Sigma_i}}_{\text{里程计因子}} + \underbrace{\sum_j \|r_j(x_k, l_m) - z_j\|^2_{\Sigma_j}}_{\text{观测因子}}$$

| 因子类型 | 约束 | 来源 |
|---------|------|------|
| **先验因子** | 固定某个状态（如起始位姿 = 原点） | 初始化 |
| **里程计因子** | 相邻帧之间的相对运动 | IMU/轮式里程计/视觉里程计 |
| **观测因子** | 路标点在某一帧的观测 | 特征匹配/ICP |
| **闭环因子** | 非相邻帧之间的约束 | 地点识别（loop closure） |

### 闭环（Loop Closure）——SLAM 的灵魂

没有闭环检测的 SLAM 就是一个开环里程计，误差无限累积。一旦检测到"这个地方我见过"，添加一条闭环边，优化后整条轨迹被拉回正确位置。

```
开环前:  A━━━━━━━━━━━━━━━━━━━━A'
                    ├── drift ~ 1m

闭环后:  A━━━━━━━━━━━━━━━━━━━━A  (同一点)
```

---

## 四、LiDAR SLAM

### LOAM (2014) 框架——几乎所有 LiDAR SLAM 的祖先

1. **特征提取**：对每条 scan line 计算点的 roughness $c$

$$c = \frac{1}{|S| \cdot \|p_i\|}\left\| \sum_{j \in S, j \ne i} (p_i - p_j) \right\|$$

$c$ 大 → 边缘点（edge），$c$ 小 → 平面点（planar）

2. **Scan-to-Scan 匹配**（高频里程计 10Hz）：edge 点到前帧 edge 线的距离最小化，planar 点到前帧 planar 面的距离最小化

3. **Scan-to-Map 匹配**（低频建图 1Hz）：新扫到的点对齐到累积局部地图

### 代表系统

| 系统 | 特点 |
|------|------|
| **LOAM** | 祖师爷，旋转式 LiDAR |
| **LeGO-LOAM** | 地面优化，轻量级，户外 |
| **LIO-SAM** | IMU 紧耦合，因子图 |
| **FAST-LIO** | 迭代卡尔曼滤波 + IMU，极快 |
| **FastLIO2** | ikd-Tree 增量建图，100 倍快于 kd-tree |

---

## 五、视觉 SLAM

### 前端——怎么找对应关系

| 方法 | 原理 | 代表 |
|------|------|------|
| **特征法** | 提取→描述→匹配→几何验证 | ORB-SLAM3 |
| **直接法** | 直接用像素亮度残差，不提取特征 | DSO |
| **半直接法** | 特征跟踪 + 直接法优化 | SVO |

### 后端——怎么优化

用 Bundle Adjustment (BA) 同时优化相机位姿和 3D 路标点：

$$\arg\min_{T_i, p_j} \sum_{i,j} \|\pi(T_i, p_j) - z_{ij}\|^2$$

$\pi(\cdot)$ 是投影函数，将 3D 点 $p_j$ 投影到相机 $T_i$ 的图像平面，残差就是重投影误差（像素坐标差）。

### ORB-SLAM3 —— 视觉 SLAM 的集大成者

三个并行线程：
1. **Tracking**：每帧提取 ORB 特征，与局部地图匹配，估计当前位姿
2. **Local Mapping**：管理局部地图（新关键帧插入、局部 BA）
3. **Loop Closing**：词袋模型检测闭环 → Sim3 配准 → 位姿图优化 → 全局 BA

支持单目、双目、RGB-D、IMU。

### 视觉 vs LiDAR

| | 视觉 SLAM | LiDAR SLAM |
|------|------|------|
| **精度** | 依赖纹理，弱纹理场景（白墙）漂 | 几何信息稳定 |
| **成本** | 低（几百块相机） | 高（几千上万） |
| **光照** | 暗光/强光下失败 | 不依赖光照 |
| **语义** | 天然丰富 | 需要 RGB-LiDAR 融合 |
| **距离** | 近距为主 | 远距（100m+） |

---

## 六、SLAM 评价指标

| 指标 | 含义 |
|------|------|
| **ATE**（Absolute Trajectory Error） | 整条轨迹与真值的全局对齐误差，衡量全局一致性 |
| **RPE**（Relative Pose Error） | 相邻帧之间的相对误差，衡量局部漂移 |
| **闭环召回率** | 回到同一个地方时检测到闭环的概率 |

---

## 推荐阅读

📄 [LOAM: Lidar Odometry and Mapping in Real-time](https://www.ri.cmu.edu/pub_files/2014/7/Ji_LidarMapping_RSS2014_v8.pdf) — RSS, 2014
LiDAR SLAM 的奠基之作。特征提取（edge/planar points）、scan-to-scan 高频里程计 + scan-to-map 低频建图的框架影响至今几乎所有 LiDAR SLAM 系统。

📄 [ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual-Inertial, and Multimap SLAM](https://arxiv.org/abs/2007.11898) — IEEE TRO, 2021
视觉 SLAM 的集大成者。多地图系统（ATLAS）、视觉惯性紧耦合、支持单目/双目/RGB-D。看完这篇能理解现代视觉 SLAM 的完整架构。
