
# Nvidia的GR00T系列

**Isaac-GR00T：** [github](https://github.com/NVIDIA/Isaac-GR00T/tree/main) 

|             |                                                              |                                                              |      |
| ----------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
| GR00T  N1   | [paper](https://arxiv.org/pdf/2503.14734) [精读](https://blog.csdn.net/v_JULY_v/article/details/146376514?fromshare=blogdetail&sharetype=blogdetail&sharerId=146376514&sharerefer=PC&sharesource=m0_73994182&sharefrom=from_link) | 采用冻结的 Eagle VLM 搭配简化的适配器架构，并引入FLARE（未来潜变量对齐）损失函数。通过结合DreamGen 生成的合成轨迹与多源真实/仿真数据。 |      |
| GR00T  N1.5 | [website](https://research.nvidia.com/labs/gear/gr00t-n1_5/) [精读](https://blog.csdn.net/v_JULY_v/article/details/146376514?fromshare=blogdetail&sharetype=blogdetail&sharerId=146376514&sharerefer=PC&sharesource=m0_73994182&sharefrom=from_link) |                                                              |      |
| GR00T  N1.6 | [website](https://research.nvidia.com/labs/gear/gr00t-n1_6/) |                                                              |      |





## Nvidia GR00T

### **N1**

核心技术在于采用了仿生的“双系统”架构：利用预训练的视觉语言模型（Eagle-2）作为“系统2”处理低频（10Hz）的环境感知与语义推理，紧密耦合基于流匹配（Flow-matching）的Diffusion Transformer作为“系统1”来生成高频（120Hz）的闭环运动控制动作。

与 N1 类似，GR00T N1.5 也使用[NVIDIA Eagle](https://github.com/NVlabs/EAGLE) VLM 对文本和视觉观测进行编码。然后，DiT 会交叉关注来自 VLM 的视觉语言嵌入，并处理状态和带噪声的动作。

![[Nvidia GR00T/image-20260201173819981.png]]

为了解决机器人数据匮乏问题，它构建了“数据金字塔”训练策略：**底层利用“潜在动作（Latent Actions）”技术从海量无标签人类视频中提取通用行为先验，中层通过生成式AI合成反事实的“神![[1769871536723-8.png]]经轨迹（Neural Trajectories）”和仿真数据（DexMimicGen）进行大规模扩充，顶层结合少量高质量真机遥操作数据。**

![[Nvidia GR00T/1769871536723-8.png]]

 

### **N1.5**

N1.5与N1类似之处在于

1. GR00T使用NVIDIA Eagle VLM对文本和视觉观察进行编码。其中N1中使用的是Eagle-2。N1.5中升级成了Eagle2.5
2. 然后，**视觉语言嵌入通过VLM生成，再由DiT进行交叉注意力处理，DiT处理状态和加噪的动作**

N1.5与N1相比的主要区别如下：

1. VLM模型在预训练和微调过程中均处于冻结状态。
2. 将视觉编码器连接到LLM的适配器MLP进行了简化，并对输入到LLM的视觉和文本标记嵌入都添加了层归一化。

![[Nvidia GR00T/image-20260201173206790.png]]

- FLARE损失函数（未来潜在表征对齐）

FLARE的核心是从动作去噪网络的隐藏状态中预测机器人未来观测的紧凑表示。FLARE主要包括两个关键阶段

1. 首先，预训练一个紧凑且具备动作感知能力的观测嵌入模型。虽然通用嵌入模型也可用于目标未来嵌入，但作者发现，针对下游控制任务显式优化的动作感知嵌入，因其紧凑性和任务对齐性，能带来更优的性能和效率
2. 接下来，通过引入极少量的附加token，与diffusiontransformer协同训练，这些token被优化用于预测未来观测嵌入

最后，FLARE还支持从无动作标签的数据源中学习，例如人类视频。通过利用GoPro采集的人类第一视角演示视频——使用头戴式GoPro摄像机采集的以自我视角为主的人体视频数据集。并且每个物体仅需一条真实机器人演示，FLARE成功学习了新的抓取策略，凸显了其在利用非结构化数据源进行大规模机器人学习方面的潜力

为了使DiT模块中的潜在表示能够预测未来的潜在状态，作者在输入序列中添加了M个可学习的未来token嵌入，使得该序列包含三个组成部分：

![[Nvidia GR00T/1769871545667-14.png]]

![[Nvidia GR00T/1769871547919-17.png]]

FLARE的方法类似于表示对齐（REPA）[11]在提升文本到图像扩散模型中的应用，但由于潜在世界建模的设定，存在几个重要的不同之处

1. 首先，将DiT策略与未来嵌入对齐，而不是当前观测的嵌入
2. 其次，FLARE的架构引入了可学习的未来token，使得流匹配和对齐在DiT中沿着各自独立的路径进行，并通过自注意力机制相互作用。

通过这种方式，鼓励DiT模块在保持其通过动作流匹配进行动作预测能力的同时，能够在内部推理未来的潜在状态。



###  N1.6

建筑结构变更：

- 基础视觉语言模型 (VLM)：我们使用 NVIDIA Cosmos-2B 内部的 VLM 变体。该 VLM 支持灵活的分辨率，并且可以按图像的原始宽高比进行编码，无需填充。VLM 经过训练，既可用于通用视觉语言任务，也可用于具身推理任务，例如下一步动作预测。
- 使用 2 倍大的 DiT（N1.5 中为 16 层，而 **DiT 为 32 层**）。
- 移除 N1.5 的 VLM 后 4 层 Transformer 适配器。取而代之的是，我们在预训练期间解冻 VLM 的前 4 层。
- 对于大多数实施例，**预测的是状态相对动作块，而不是绝对关节角度或 EEF 位置**。

除了 N1.5 数据混合之外，N1.6 预训练数据还包括来自以下来源的数千小时远程操作数据：

- 双手动YAM臂
- AGIBot Genie1
- 在 BEHAVIOR 套件上模拟 Galaxea R1 Pro
- 使用 Unitree G1 进行全身运动控制



## **DreamGen**

(website:https://research.nvidia.com/labs/gear/dreamgen/)

为了超越远程操作数据进行概括，使人形机器人能够在新的环境中学习新任务，我们使用[DreamGen](https://research.nvidia.com/labs/gear/dreamgen) 生成合成机器人数据进行训练。

DreamGen是一个用于生成神经轨迹的四阶段流程，该流程利用视频世界模型生成合成机器人数据。这项工作首次实现了零样本行为泛化和零样本环境泛化：我们使人形机器人能够在已知和未知环境中执行22种新行为，而仅需来自单一环境中单个抓取放置任务的远程操作数据。

通过DreamGen，我们将机器人学习的范式从扩展人类远程操作数据转变为通过世界模型扩展GPU计算能力。

![[Nvidia GR00T/1769871553964-20.png]]

DreamGen分为4个步骤：

1. 我们首先在目标机器人上微调视频世界模型（图像到视频扩散模型），以学习给定机器人本体的动力学特性。
2. 我们通过**初始帧和语言指令**引导模型，生成机器人视频，这些视频不仅包含在既定领域内的行为，还包含在全新环境中的新颖行为。
3. [我们通过潜在动作模型](https://latentactionpretraining.github.io/)或[逆动力学模型](https://openai.com/index/vpt/)（IDM）提取伪机器人动作。
4. 我们将这些标有伪动作的视频（称为神经轨迹）用于**下游视觉运动策略学习**。



### **EgoScale**

**EgoScale**, a human-to-dexterous-manipulation transfer framework built on large-scale egocentric human data.

![](https://primebot.feishu.cn/space/api/box/stream/download/asynccode/?code=ZjQxMTdlYWVmYTExODU1NTcwYTFhOWNmNjFiMGJhNzlfbTFhdzZuRmsyNUFScmdLZ0UyZGFuSUdWZjR0ODVQR3pfVG9rZW46T2NPNWJkTlN6b2dZb214YnBScWN0TlBxbk1lXzE3NzY3NzAxNjY6MTc3Njc3Mzc2Nl9WNA)

  

![](https://primebot.feishu.cn/space/api/box/stream/download/asynccode/?code=ODg2ZTBiZDU1ZTk4MjVhN2JmNGIyYjdkODM3NGRmNmNfWUtwcmoxejk2NlJ2aHdRdlp4RzlGZ1VMa093dGVhb1hfVG9rZW46QUVLUmJGNzVib0pUWDR4a2xvM2N6ZDNIbkNlXzE3NzY3NzAxNjY6MTc3Njc3Mzc2Nl9WNA)



### **DreamGen**

Unlocking Genearlization in Robot Learning through Video World Models

We introduce **DreamGen**, a 4-stage pipeline to generate _**neural trajectories**_**, synthetic robot data** generated from video world models. This work is the first in literature to enable **zero-shot behavior generalization and zero-shot environment generalization**: we enable a humanoid robot to perform 22 new behaviors in both seen and unseen environments, while requiring teleoperation data from only a single pick-and-place task in one environment. Through DreamGen, we change the paradigm of robot learning **from scaling human teleoperation data to scaling GPU compute through world models.**

![](https://primebot.feishu.cn/space/api/box/stream/download/asynccode/?code=NWYyYjkzNWVjNjBjOWZjMmEzZWYyYTQ1OTczNWU5MWNfSGNVajJRTEhETTNXbjF6TGd0eDFJb3R1aEFmZDhqaEtfVG9rZW46QUhsNWJIUUJFb0l4NW14RjhPN2NndldPbkJnXzE3NzY3NzAxNjY6MTc3Njc3Mzc2Nl9WNA)

四个步骤：

1. We first finetune video world models (image-to-video diffusion models) on a target robot to learn the **dynamics** of the given robot embodiment.
    
2. We prompt the models with initial frames and language instructions, generating robot videos that not only include in-domain behaviors, but also novel behaviors in novel environments.
    
3. We extract pseudo robot actions via
    
    1. **[latent action model](https://latentactionpretraining.github.io/)** （LAPA: the first unsupervised method for pretraining Vision-Language-Action (VLA) models without ground-truth robot action labels）(We first train an action quantization model leveraging VQ- VAE-based objective to learn discrete latent actions between image frames, then pretrain a latent VLA model to predict these latent actions from observations and task descriptions, and finally finetune the VLA on small-scale robot manipulation data to map from latent to robot actions. )
        
    
    ![](https://primebot.feishu.cn/space/api/box/stream/download/asynccode/?code=ZDlhYWEwMjc1YTVjMDQ5M2E0YjliYzExNWE1MTZjY2RfdWl0T0pIall6S2wxNlN4aXhuMlk5OGUxbWVZU1J4SHlfVG9rZW46THJocGJJWWpkb1RIZ2F4Rm5kWmN4bWNWbm1oXzE3NzY3NzAxNjY6MTc3Njc3Mzc2Nl9WNA)
    
    2. **[inverse dynamics model](https://openai.com/index/vpt/)** (IDM).
        
    
      **the IDM can use past** _**and future**_ **information to guess the action at each step.** This task is much easier and thus requires far less data than the behavioral cloning task of predicting actions given _past video frames only_, which requires inferring what the person wants to do and how to accomplish it. We can then use the trained IDM to label a much larger dataset of online videos and learn to act via behavioral cloning.
    

![](https://primebot.feishu.cn/space/api/box/stream/download/asynccode/?code=YWVmNDQxMzlmYTRhZTEwMzIxNjMxYzdmNTViYmMzOTRfelpUTXl1YmRpQ0FmSHRxV1JSYXJ2T0ZvU1ZYUU1EdE5fVG9rZW46RTE5UGJ0ZEVHb0lJbXh4SnZsMWNDNTdabldmXzE3NzY3NzAxNjY6MTc3Njc3Mzc2Nl9WNA)

4. We use these videos labeled with pseudo actions, named as _**neural trajectories**_, for downstream visuomotor policy learning
    

DreamGen Bench，这是一个世界建模基准测试，旨在量化现有视频生成模型适应特定机器人形态的能力。我们测量了两个关键指标：指令遵循性（生成的视频是否严格遵循给定指令）和物理遵循性（评估生成视频的物理合理性）。




### **DreamZero**

State-of-the-art Vision-Language-Action (VLA) models excel at _semantic generalization_ but struggle to generalize to unseen physical motions in novel environments. We introduce DreamZero, a _World Action Model (WAM)_ built upon a **pretrained video diffusion backbone**. Unlike VLAs, WAMs learn physical dynamics by **jointly predicting future world states and actions, using video as a dense representation of how the world evolves**. By jointly modeling video and action, DreamZero learns diverse skills effectively from heterogeneous robot data without relying on repetitive demonstrations. This results in over 2x improvement in generalization to new tasks and environments compared to state-of-the-art VLAs in real-robot experiments. Crucially, through model and system optimizations, we enable a **14B autoregressive video diffusion model to perform real-time** _**closed-loop control at 7Hz**__._ Finally, we demonstrate two forms of cross-embodiment transfer: video-only demonstrations from humans or other robots yield over 42% improvement on unseen tasks with just 10–20 minutes of data. More surprisingly, DreamZero adapts to an entirely new robot (YAM) with only 30 minutes of play data while retaining zero-shot generalization.

![](https://primebot.feishu.cn/space/api/box/stream/download/asynccode/?code=NTdiOGMzNDUyMGU0NTA1YTY2ZjMxOTkzYjQyODE0MGJfNDRjY0lnNHZNU0dyYzM1VTZCRGpqRGpUZWtCRHdka25fVG9rZW46UVd3aGJjSk92b3B2S2l4TURKWWNiZ0l1bmpnXzE3NzY3NzAxNjY6MTc3Njc3Mzc2Nl9WNA)

![](https://primebot.feishu.cn/space/api/box/stream/download/asynccode/?code=ZGE5YzI0MWEzOTQzZmVkYTgxNjdjMDMxN2NmMmViMzBfdjg4Z2I1NXBBTHY5WEpZRzFybEpPdXhtWlNMVTN0QmRfVG9rZW46SFZudGJ1RzVTbzNmVGN4SkwxbGNjZnZWbnRnXzE3NzY3NzAxNjY6MTc3Njc3Mzc2Nl9WNA)