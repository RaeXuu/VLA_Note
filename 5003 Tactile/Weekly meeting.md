## 触觉
geo-metric (e.g., size), material (e.g., hardness), and affective (e.g.,comfort)

Gelsight或许只适合解决material的问题（hardness, roughness, and bumpiness）

## 数据集
- 数据集简介
规模 每个物体 100/200/300条
数据比例 无标注：有标注
self-supervision 力和滑移的标签
重点是数据集？

- UMI 做 pretrain？
为什么是umi？ ego质量低
购买umi设备
replayable的数据？   “延迟匹配”和“相对轨迹动作”   视觉分布偏移
如果做水果：水果的尺寸比较大。。重量比较重
触觉对“夹爪UMI to 机械臂的迁移”有利

- 不用UMI
UMI是否有必要？
情况分为用SSL还是带有annotation的标注，个人觉得，前者相对来说适合UMI或者是两指驱动的夹爪，因为我们是为了获得可以用于大规模训练的数据。后者相对来说适合手持传感器。
问题在于，触觉本身的属性其实是比较难标注的（VLA-Touch中使用hardness, roughness, and bumpiness）这些属性其实标注的时候比较难以用清晰的分界线定性，个人的判断存在bias。

- 数据质量
Gelsight触觉数据：不同操作者不同的噪声分布，不同时间和温度baseline漂移，不同材质的接触区域，信号和噪声的比例不同
DL领域：augmentation、normalization、domain randomization 等成熟的方案

质量评估标准：信噪比、稳定性、一致性
触觉数据增强
不同采集条件下的数据分布差异

- 触觉数据难点
1) 传感器本身不稳定，baseline漂移，老化磨损的“退化问题”
2) 采集方式，摇操难以采到专家数据。（导纳控制提升数据质量）（手套精度差，特别是接触力的反馈）

- 触觉数据仿真
难以仿真。接触动力学差异和噪声建模。
real2sim再sim2real



## 数据集采集

有触觉反馈的摇操采集数据（摇操本身采集的是动作轨迹）

- 采集平台
**Gelsight mini**：接触面积比较小 25mm * 20mm。数据pipeline
**绑在**：增加了厚度 28mm * 2，剩下的两指宽度更小了
**UMI上**

**Webcam**

- 采集场景
Tabletop （indoor、outdoor）


- Objects
size
rigid / deformable


- OOD失败数据
Slippage、damage
Human in the loop？


## 数据模态
- 视觉
眼在手上

- 触觉
三维力

- 听觉

- 视触觉
模态掩码

视触觉
电容 分辨率 
压阻 受温度影响

## 状态估计

不是多模态分类

力过大对水果内部造成的损伤难以估计：可能需要放置一段时间才能显现


“More than a Feeling”
最小力的policy和最大成功率的policy，两者之间的成功率gap不大。但是用的DL


“Touch and Go: Learning from Human-Collected Vision and Touch”
1) self-supervised visuo-tactile feature learning, 
2) tactile-driven image stylization, i.e., making the visual appearance of an object more consistent with a given tactile signal 视觉和触觉预测双向可逆
3) predicting future frames of a tactile signal from visuo-tactile inputs.


“Connecting Touch and Vision via Cross-Modal Prediction” -- VisGel
1) synthesizing plausible tactile signals from visual inputs 
2) imagining how we interact with objects given tactile data as input.


“Touch100k: A Large-Scale Touch-Language-Vision Dataset for Touch-Centric Multimodal Representation”
1) material property identification
2) robot grasping prediction

“Sparsh: Self-supervised touch representations for vision-based tactile sensing”
[T1] Force estimation
[T1A] Force field visualization
[T2] Slip detection
[T3] Pose estimation
[T4] Grasp stability
[T5] Textile recognition
[T6] Bead maze





## Binghao Huang的survey
https://binghao-huang.github.io/blog/tactile-survey.html#intro

Hierarchy: ![[Screenshot 2026-08-22 at 2.06.22 PM.png]]


Properties: shape, surface material, object pose

## Policy Learning
![[Screenshot 2026-08-22 at 3.33.02 PM.png]]

## Foundation
![[Screenshot 2026-08-22 at 2.53.43 PM.png]]



## Application
![[Screenshot 2026-08-22 at 3.31.48 PM.png]]





