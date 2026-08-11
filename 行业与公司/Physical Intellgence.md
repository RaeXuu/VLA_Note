
Open Pi Github: [github](https://github.com/Physical-Intelligence/openpi)

|                        |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Paper摘要精简翻译                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Pi 0开源                 | [paper](https://arxiv.org/abs/2410.24164) [website](https://www.physicalintelligence.company/blog/pi0) [精读](https://blog.csdn.net/v_JULY_v/article/details/143472442?fromshare=blogdetail&sharetype=blogdetail&sharerId=143472442&sharerefer=PC&sharesource=m0_73994182&sharefrom=from_link) [源码剖析](https://blog.csdn.net/v_JULY_v/article/details/146068251?fromshare=blogdetail&sharetype=blogdetail&sharerId=146068251&sharerefer=PC&sharesource=m0_73994182&sharefrom=from_link) [微调方法论](https://blog.csdn.net/v_JULY_v/article/details/146125555?fromshare=blogdetail&sharetype=blogdetail&sharerId=146125555&sharerefer=PC&sharesource=m0_73994182&sharefrom=from_link) | 机器人学习在释放灵活、通用且灵巧的机器人系统的全部潜力，以及解决人工智能领域一些最深层次的问题方面前景广阔 。然而，要将机器人学习提升到构建有效现实世界系统所需的通用水平，目前在数据、泛化能力和鲁棒性方面仍面临重大障碍 。在本文中，我们探讨了通用机器人策略（即机器人基础模型）如何应对这些挑战，以及如何设计能够执行复杂且高度灵巧任务的有效通用机器人策略 。我们提出了一种**基于预训练视觉-语言模型（VLM）构建的新型流匹配（Flow Matching）架构**，旨在继承互联网规模的语义知识 。随后，我们讨论了如何在包含单臂机器人、双臂机器人和移动操作机器人等多种灵巧机器人平台的大规模多样化数据集上训练该模型。我们评估了模型通过直接提示执行任务的能力、遵循人类及高级 VLM 策略发出的语言指令的能力，以及通过微调习得新技能的能力 。                                                                                                                                                                                                                                     |
|                        | [LeRobot Pi 0剖析](https://blog.csdn.net/v_JULY_v/article/details/148370072?fromshare=blogdetail&sharetype=blogdetail&sharerId=148370072&sharerefer=PC&sharesource=m0_73994182&sharefrom=from_link)                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Pi0-FAST开源             | [paper](https://arxiv.org/pdf/2501.09747) [website](https://www.pi.website/research/fast) [pi0-FAST精读及源码解析](https://blog.csdn.net/v_JULY_v/article/details/145475733?fromshare=blogdetail&sharetype=blogdetail&sharerId=145475733&sharerefer=PC&sharesource=m0_73994182&sharefrom=from_link)                                                                                                                                                                                                                                                                                                                                                                                  | 自回归序列模型，例如基于 Transformer 的视觉-语言-动作（VLA）策略，在捕捉复杂且具有泛化性的机器人行为方面成效显著。然而，此类模型要求我们对连续动作信号选择一种**标记化（tokenization）**方式，这决定了模型预测的离散符号如何映射为连续的机器人动作。我们发现，当前基于简单的逐维度、逐时间步分箱（binning）方案的机器人动作标记化方法，在利用高频机器人数据学习灵巧技能时，表现通常不佳。为应对这一挑战，我们提出了一种基于**离散余弦变换（DCT）**的新型压缩式机器人动作标记化方案。我们的标记化方法——**频域动作序列标记化（Frequency-space Action Sequence Tokenization，简称 FAST）**，使我们能够针对标准离散化方法完全失效的高度灵巧及高频任务，训练自回归 VLA 模型。基于 FAST，我们发布了 FAST+，这是一种通用的机器人动作标记器，并在 100 万条真实机器人动作轨迹上进行了训练。它可以作为一个“黑盒”标记器，用于处理涵盖多样化动作空间和控制频率的广泛机器人动作序列。最后，我们展示了当与 Pi 0 VLA 结合使用时，我们的方法能够扩展至 10,000 小时的机器人数据训练规模，并在性能上匹配扩散（diffusion）VLA 模型，同时将训练时间缩短多达 5 倍 。              |
| Hi Robot(大脑加强版pi 0)不开源 | [paper ](https://arxiv.org/pdf/2502.19417)[website](https://www.pi.website/research/hirobot) [精读](https://blog.csdn.net/v_JULY_v/article/details/147090612?fromshare=blogdetail&sharetype=blogdetail&sharerId=147090612&sharerefer=PC&sharesource=m0_73994182&sharefrom=from_link)                                                                                                                                                                                                                                                                                                                                                                                            | 能够在开放世界环境中执行多种不同任务的通用机器人，不仅必须能够推理出完成目标所需的步骤，还必须能够处理复杂的指令、提示，甚至是任务执行过程中的反馈。错综复杂的指令（例如，“能不能给我做一个素食三明治？”或者“我不喜欢那个”）不仅要求机器人具备在物理上执行各个独立步骤的能力，还要求其能够将复杂的命令和反馈置于物理世界的情境中进行理解。在这项工作中，我们描述了一种在**分层结构**中使用视觉-语言模型（VLM）的系统。该系统首先对复杂的提示和用户反馈进行推理，以推断出完成任务最恰当的下一步骤，随后通过低层级的动作来执行该步骤。与那些只能完成简单命令（如“拿起杯子”）的直接指令跟随方法相比，我们的系统能够对复杂的提示进行推理，并在任务执行过程中结合情境化的反馈（如“那不是垃圾”）。我们在三种机器人平台上对该系统进行了评估，包括单臂机器人、双臂机器人和双臂移动机器人，展示了其处理清理凌乱桌面、制作三明治以及杂货购物等任务的能力。                                                                                                                                                                                      |
| Pi 0.5 不开源             | [paper ](https://www.pi.website/download/pi05.pdf)[website](https://www.pi.website/blog/pi05) [精读](https://blog.csdn.net/v_JULY_v/article/details/147443184?fromshare=blogdetail&sharetype=blogdetail&sharerId=147443184&sharerefer=PC&sharesource=m0_73994182&sharefrom=from_link)                                                                                                                                                                                                                                                                                                                                                                                           | 为了让机器人变得有用，它们必须在实验室之外的现实世界中执行具有实际相关性的任务。尽管视觉-语言-动作（VLA）模型在端到端机器人控制方面已经展示了令人印象深刻的结果，但此类模型在野外（真实环境）中能泛化多远仍然是一个悬而未决的问题。我们描述了 Pi 0.5，这是一个基于 Pi 0 的新模型，**它利用在异构任务上的协同训练来实现广泛的泛化能力。**Pi 0.5 使用来自多种机器人的数据、高层语义预测、网络数据以及其他来源的数据，以实现具有广泛泛化能力的现实世界机器人操作。我们的系统使用一种**协同训练和混合多模态示例**的组合，这些示例结合了图像观测、语言指令、物体检测、语义子任务预测和低层动作。我们的实验表明，这种类型的知识迁移对于有效的泛化是必不可少的，并且我们首次证明了端到端学习赋能的机器人系统可以在全新的家庭中执行长程且灵巧的操作技能，例如清洁厨房或卧室。                                                                                                                                                                                                                   |
| Pi 0.5Ki 改进版部分开源       | [paper ](https://arxiv.org/pdf/2505.23705)[website ](https://www.pi.website/research/knowledge_insulation)[精读](https://blog.csdn.net/v_JULY_v/article/details/149227640?fromshare=blogdetail&sharetype=blogdetail&sharerId=149227640&sharerefer=PC&sharesource=m0_73994182&sharefrom=from_link)                                                                                                                                                                                                                                                                                                                                                                               | 视觉-语言-动作（VLA）模型通过将端到端学习与源自网络规模视觉-语言模型（VLM）训练的语义知识迁移相结合，为训练物理系统（如机器人）的控制策略提供了一种强大的方法 。然而，**实时控制的约束往往与 VLM 的设计相冲突**：最强大的 VLM 拥有数百亿甚至数千亿的参数，这对实时推理构成了障碍，且它们基于离散标记（tokens）运作，而非控制机器人所需的连续值输出 。**为了应对这一挑战，近期的 VLA 模型采用了专门的模块来实现高效的连续控制，例如动作专家（action experts）或连续输出头（continuous output heads），这通常需要在预训练的 VLM 骨干网络中添加未经训练的新参数 。虽然这些模块提升了实时性和控制能力，但它们究竟是保留还是削弱了预训练 VLM 中蕴含的语义知识，以及它们对 VLA 训练动态有何影响，仍然是一个悬而未决的问题** 。在本文中，我们在包含连续扩散（diffusion）或流匹配（flow matching）动作专家的 VLA 背景下研究了这一问题，结果表明，简单直接地（naively）引入此类专家会显著损害训练速度和知识迁移 。我们对各种设计选择及其对性能和知识迁移的影响进行了广泛的分析，并提出了一种在 VLA 训练期间对 VLM 骨干网络进行**“隔离”（insulating）**的技术，从而有效缓解了这一问题 。 |
| RTC实时动作分块              | [paper ](https://arxiv.org/pdf/2506.07339)[follow-up paper](https://arxiv.org/pdf/2512.05964) [website](https://www.pi.website/research/real_time_chunking) [精读](https://blog.csdn.net/v_JULY_v/article/details/149352338?fromshare=blogdetail&sharetype=blogdetail&sharerId=149352338&sharerefer=PC&sharesource=m0_73994182&sharefrom=from_link)                                                                                                                                                                                                                                                                                                                             | 现代人工智能系统，特别是那些与物理世界交互的系统，越来越需要实时性能。然而，最先进的通用模型，包括最近的视觉-语言-动作模型（VLA），其高延迟构成了一个重大挑战。**虽然动作分块（action chunking）已在高频控制任务中实现了时间一致性，但它并未完全解决延迟问题，导致在分块边界处出现停顿或分布外（out-of-distribution）的抖动动作。**本文提出了一种新颖的推理时算法，能够**实现动作分块策略的平滑异步执行**。我们的方法，即**实时分块（Real-Time Chunking，简称 RTC）**，适用于任何基于扩散（diffusion）或流（flow）的 VLA 模型，开箱即用，无需重新训练。**它在执行当前动作块的同时生成下一个动作块，“冻结”那些保证会被执行的动作，并“修复（inpainting）”剩余部分。**为了测试 RTC，我们在 Kinetix 模拟器中引入了一个包含 12 项高动态任务的新基准，并评估了 6 项具有挑战性的现实世界双手操作任务。结果表明，RTC 速度快、性能好，并且对推理延迟具有独特的鲁棒性，显著提高了任务吞吐量，并在诸如划火柴等精确任务中实现了高成功率——即使在存在显著延迟的情况下也是如此。                                                                  |
| Pi* 0.6不开源             | [paper ](https://www.pi.website/download/pistar06.pdf)[website](https://www.pi.website/blog/pistar06) [精读](https://blog.csdn.net/v_JULY_v/article/details/154989166?fromshare=blogdetail&sharetype=blogdetail&sharerId=154989166&sharerefer=PC&sharesource=m0_73994182&sharefrom=from_link)                                                                                                                                                                                                                                                                                                                                                                                   | 我们研究了视觉-语言-动作（VLA）模型如何通过强化学习（RL）在现实世界的部署中得到改进。我们提出了一种通用方法，即**“通过优势条件策略进行带有经验和修正的强化学习”（RECAP）**，该方法通过优势调节（advantage conditioning）实现了 VLA 的 RL 训练。我们的方法将异构数据整合到自我改进过程中，包括演示数据、来自同策略（on-policy）采集的数据，以及在自主执行期间提供的专家遥操作干预数据。RECAP 首先使用离线 RL（Offline RL）预训练一个通用的 VLA 模型，我们称之为  Pi * 0.6，随后可以通过在机器人上收集数据，使其针对下游任务进行专业化以获得高性能。我们展示了使用完整的 RECAP 方法训练出的 Pi * 0.6 模型能够在真实的家庭环境中折叠衣物、可靠地组装盒子，并使用专业意式咖啡机制作浓缩咖啡饮品。在一些最困难的任务上，RECAP 使任务吞吐量翻了一倍以上，并大约将任务失败率减半。                                                                                                                                                                       |
| Human to Robot         | [paper ](https://www.pi.website/download/human_to_robot.pdf)[website](https://www.pi.website/research/human_to_robot) [精读](https://blog.csdn.net/v_JULY_v/article/details/156545611?fromshare=blogdetail&sharetype=blogdetail&sharerId=156545611&sharerefer=PC&sharesource=m0_73994182&sharefrom=from_link)                                                                                                                                                                                                                                                                                                                                                                   | 视觉-语言-动作（VLA）模型能够实现广泛的开放世界泛化，但需要大量且多样化的数据集 。考虑到人类视频涵盖了多样的现实世界场景且易于获取，探究是否可以从中使用部分数据是很有吸引力的 。然而，仅使用人类视频训练 VLA 模型非常困难，而且建立人类与机器人之间的映射需要手动工程，是一个重大的研究挑战 。受到大型语言模型进展的启发——即从多样化监督中学习的能力会随着规模的扩大而涌现——我们探讨这种现象是否也存在于包含人类视频数据的 VLA 模型中 。我们引入了一种简单的协同训练方法，并发现一旦 VLA 模型在足够多的场景、任务和具身（embodiments）上进行了预训练，人类到机器人的迁移能力就会涌现 。我们的分析表明，这种涌现的能力源于多样化的预训练为人类和机器人数据生成了与具身无关的表征 。我们通过一系列探究人类到机器人技能迁移的实验验证了这些发现，结果表明，在进行足够多样化的机器人预训练后，我们的方法可以将仅在人类数据中出现的泛化设置上的性能提高近一倍 。                                                                                                                                                                   |

 

## 1. Pi 0

![[1769871624800-53.png]]

## 整体理解Pi 0

### 预训练的视觉-语言模型VLM主干 + 动作专家通过「流匹配」输出动作

机器人基础模型三大挑战：大规模预训练、模型架构、训练策略

#### 大规模预训练

首先利用一个预训练的视觉-语言模型(VLM)来导入互联网规模的经验。基于VLM构建他们的模型，使其继承了语言模型和视觉-语言模型的通用知识、语义推理和问题解决能力

其次，进一步训练模型以整合机器人动作，使其成为一个视觉-语言-动作(VLA)模型。为了能够利用多种不同的机器人数据源，作者采用跨体态训练，即将多种类型机器人的数据合并到同一个模型中。

 

![[1769871627625-56.png]]

#### 模型架构

为了能够执行高度灵巧和复杂的物理任务，作者使用<u>**带有流匹配的动作分块架构来表示复杂的连续动作分布**</u>。

通过流匹配微调VLM以生成动作(且是多时间步的动作块)。

> 那为何要这么做呢？原因也很简单，VLM可以有效地从网络上传输语义知识，但它们经过训练只能输出**离散语言token**。灵巧的机器人操作需要π0以高频率(比如高达每秒 50 次)输出运动命令。为了提供这种级别的灵活性，**他们通过流匹配为预训练的 VLM 提供连续动作输出**

总之，这使得他们的模型能够以高达50Hz的频率控制机器人进行诸如叠衣服。且为了将流匹配与VLM结合，他们使用了一种新颖的动作专家，它通过流式输出(flow-based outputs)增强了标准VLM。

![[1769871630777-59.png]]

#### 训练策略

模型首先在极大且多样化的语料库上进行预训练，然后在更狭窄且经过精心筛选的数据上进行微调，以引导出所需的行为模式。

> **流匹配（Flow Matching）**
>
> 流匹配方法能够高精度地建模复杂多峰分布，非常适合高频灵巧操作任务
>
> 训练时，随机对动作施加高斯噪声，并训练模型输出去噪向量场
>
> 推理时，从高斯噪声开始，**通过数值积分向量场生成动作序列**
>
> **不同之处在于：**
>
> 1. 流匹配直接对数据和噪声分布之间的**映射场(vector field)**进行建模，训练目标是匹配这一映射场
> 2. 扩散模型通常学习的是**每个去噪步骤的条件分布**
>



## 模型架构与模型推理

### **整体理解：PaliGemma + 动作专家 + 流匹配Flow matching**

作者首先组建了一个预训练混合数据集，该数据集由他们自有的灵巧操作数据集(涵盖7种不同的机器人配置，涉及68项任务)与Open X-Embodiment数据集(包含22种机器人的数据)的加权组合而成。

- 预训练阶段还使用了多样化的语言标签，结合了任务名称和片段标注(对子轨迹的细粒度标签，通常长度约为2秒)。预训练阶段的目的是训练一个基础模型，使其具备广泛的能力和泛化能力，但不必针对任何单一任务达到高性能。

- 对于复杂且需要灵巧操作的任务，随后采用后训练流程，利用高质量的精心策划数据将模型适配到特定的下游任务。

  他们研究了数据量较小至中等的高效后训练，以及针对如折叠衣物和移动操作等复杂任务，采用较大规模数据集的高质量后训练——即<u>微调</u>

![[1769871634182-62.png]]

π0模型主要由一个语言模型transformer骨干组成。遵循标准的**后期融合视觉语言模型（VLM）方法，图像编码器将机器人获取的图像观测嵌入到与语言token相同的嵌入空间中**。且进一步通过机器人相关的特定输入和输出——即本体感觉状态和机器人动作来进行增强。

π0使用条件流匹配来建模动作的连续分布。流匹配为他们的模型提供了高精度和多模态建模能力，使其特别适合高频率的灵巧操作任务

> 该架构的灵感来源于**Transfusion** ：该方法通过多目标训练单一transformer，其token对应的连续输出(比如机器人的动作)通过流匹配(扩散风格)损失进行监督，离散输出的token通过交叉熵损失进行监督
>
> 在Transfusion的基础上，他们还发现，为机器人特定的(动作和状态)token使用一套单独的权重能够提升性能。这种设计类似于专家混合模型（MoE）（但略有不同，本质上是是第一个expert输出KV cache，然后action expert不用单独处理图像文本，只接受kv cache然后进行特征交互，最终输出action），其中有两大模块
>
> 1. 第一大模块用于**图像和文本(比如人类指令)输入**
> 2. 第二大模块用于**机器人特定的输入(比如机器人的状态)**，和**输出(比如预测的机器人动作)**，该第二组权重称为动作专家
>
> 两大模块各司其职，各自处理各自接收到的输入
>

![[image-20260201190334640.png]]



- **动作模块Action Expert**

不是直接把自己的参数塞进VLM模型中，变成一个整体大模型来输出动作，而是**基于文本指令去噪**。action expert 根据文本指令去噪生成**具体的连续的动作**——而无需像RT-2那样对其进行离散化或token化(discretize or tokenize)

![[image-20260201190654283.png]]

![[image-20260201190846249.png]]



- **视觉-语言模型VLM骨干**

采用PaliGemma [5-PaliGemma: A versatile 3B VLM for transfer]作为他们的基础模型。

![[44f146a005dc431bb1b73cf8a22adeb2.png]]

1. 其中的PaliGemma是一个开源的30亿参数VLM，基于SigLIP和Gemma而构建，在模型规模和性能之间提供了便利的权衡
2. 作者为动作专家添加了3亿参数(从头初始化)。π0在实际实现时，用的gemma_300m定义的动作专家

### 深入细节：对PaliGemma的改造——增加额外的输入输出、引入流匹配时间步、加上动作专家权重

![[image-20260201191247560.png]]

- **具体的改动，分别涉及以下几点**

![[image-20260201191339377.png]]

![[image-20260201191431265.png]]

![[image-20260201191452517.png]]



### **模型推理**

![[image-20260201192753400.png]]

![[image-20260201192818579.png]]



## 数据收集以及预训练-微调方案

| 预训练                                                       | 后训练                                                       |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 目标是让模型接触到各种各样的任务，以便它能够获得广泛适用和一般的物理能力 | 目标是使模型能够熟练和流畅地执行所需的下游任务。             |
| 数据集应涵盖尽可能多的任务，并在每个任务中涵盖多样化的行为。 | 数据集则应涵盖有助于有效任务执行的行为，这些行为应表现出一致且流畅的策略。 |

 

直观地说，多样化(但质量较低)的预训练数据允许模型从错误中恢复并处理高度变化的情况，这些情况可能在高质量的后训练数据中不会出现，而后训练数据教会模型良好地执行任务

该预训练混合物由

- OXE[Open X-Embodiment]的一个子集OXE Magic Soup
- π数据集

组成。

注意，由于每个训练样本对应一个时间步——即一个元组

，——在本次讨论中，将以时间步来量化数据。

训练混合数据集中有9.1%来自开源数据集，包括

- 22个机器人数据的OXE
- Bridgev2 [BridgeData v2: A dataset for robot learning at scale]
- DROID [DROID: A large-scale in-the-wild robot manipulation dataset]

这些数据集中的机器人和任务通常配备一到两个摄像头，并采用低频率控制，频率在 2 到 10 Hz 之间。然而，这些数据集涵盖了广泛的物体和环境。

为了学习灵巧且更复杂的任务，作者还使用了来自他们自有的数据集，总计903M时间步长的数据，其中

- 106M步来自单臂机器人
- 797M步来自双臂机器人

这些数据涵盖了68个任务，每个任务都由复杂的行为组成——例如，“清理餐具”任务包括将各种各样的盘子、杯子和餐具放入餐具回收箱，以及将各种垃圾物品扔进垃圾桶

请注意，这里的任务定义与以往工作有显著不同，之前的工作通常使用任何名词和动词的组合(例如，“捡起杯子”与“捡起盘子”)视为不同的任务。因此，作者数据集中实际的行为范围远比“任务”数量所暗示的要广泛得多。

此外，由于数据集在规模上存在一定的不平衡(例如，更难的叠衣任务样本数量较多)，作者对每个任务-机器人组合按

进行加权，其中n为该组合的样本数量，从而对样本数量过多的组合进行降权

1. 配置向量
2. 和动作向量
3. 始终具有数据集中最大机器人的维度(在作者的案例中为18，以适应两个6-DoF机械臂、两个夹爪、一个移动底座和一个垂直驱动的躯干)
4. 对于配置和动作空间维度较低的机器人，对配置和动作向量进行零填充。对于少于三张图像的机器人，还会屏蔽掉缺失的图像槽
5. 在训练后阶段，使用一个较小的任务特定数据集对模型进行微调，以使其专门化用于特定的下游应用

## 2. Pi 0源码

[π0源码(openpi)剖析——从π0模型架构的实现：如何基于PaLI-Gemma和扩散策略去噪生成动作，到基于C/S架构下的模型训练与部署](https://blog.csdn.net/v_JULY_v/article/details/146068251?fromshare=blogdetail&sharetype=blogdetail&sharerId=146068251&sharerefer=PC&sharesource=m0_73994182&sharefrom=from_link)

 

![[1769871683031-98.png]]

 

## 3. 复现部署

### [openpi π₀ 项目部署运行逻辑（一）——综述](https://blog.csdn.net/qq_28912651/article/details/147816917?fromshare=blogdetail&sharetype=blogdetail&sharerId=147816917&sharerefer=PC&sharesource=m0_73994182&sharefrom=from_link)

#### Open Pi 综述

Open Pi 托管着由 Physical Intelligence team 发布的机器人开源模型与软件包。

1. π0本身的代码和权重
2. 特定平台上特定任务的微调checkpoint
3. 推理代码
4. 微调代码

当前仓库包含两类核心模型：

- the π₀  model - 基于流式扩散架构的视觉-语言-动作多模态模型（VLA）
- the π₀ - FAST  model - 采用 FAST 动作分词器的自回归式VLA模型

两类模型均提供了 base model checkpoints（基于10k+小时机器人数据预训练），并包含开箱即用案例及自定义数据集微调示例

#### 运行要求

 

![[1769871686400-101.png]]

#### 安装指南

克隆仓库时请同步更新子模块：

- uv ([uv](https://docs.astral.sh/uv/)) ([installation instruction](https://docs.astral.sh/uv/getting-started/installation/))
- Docker ([setup](https://github.com/Physical-Intelligence/openpi/blob/main/docs/docker.md))

 

#### 模型检查点

两个基础模型

特定平台特定任务的微调模型

#### 预训练模型推理

 

**远程推理（**[remote_inference.md](https://github.com/Physical-Intelligence/openpi/blob/main/docs/remote_inference.md)**）：**该项目提供了远程运行模型推理的 [examples and code](https://github.com/Physical-Intelligence/openpi/blob/main/docs/remote_inference.md)：模型可以在不同的服务器上运行，并通过 websocket 连接将 actions 传输给机器人。这使得在机器人之外使用更强大的 GPUs 并实现机器人端与计算资源解耦

 

#### 自定义数据微调指南

如何在自己的数据集上微调一个base model

1. 将数据格式转换为 LeRobot dataset (用于训练)
2. 配置训练参数并训练
3. 启动策略服务器并运行推理

 

此项目在以下 README 文档中提供了更多关于如何在 ALOHA 平台上进行模型微调和推理的示例：[ALOHA Simulator](https://github.com/Physical-Intelligence/openpi/blob/main/examples/aloha_sim)、[ALOHA Real](https://github.com/Physical-Intelligence/openpi/blob/main/examples/aloha_real)、[UR5](https://github.com/Physical-Intelligence/openpi/blob/main/examples/ur5)

 

### [Model 复现系列（三）π0 -- Physical Intelligence Pi-zero（Pi0）](https://blog.csdn.net/nenchoumi3119/article/details/148688800?fromshare=blogdetail&sharetype=blogdetail&sharerId=148688800&sharerefer=PC&sharesource=m0_73994182&sharefrom=from_link)

根据官方 ReadMe 文件的描述，他们使用了 Libero 数据集的格式作为输入，这个数据集是在一系列 **仿真** 环境下构建的 **单臂** 操作数据集

![[1769871690173-104.png]]

 



## 4. 微调

### [Model 复现系列（三）π0 -- Physical Intelligence Pi-zero（Pi0）](https://blog.csdn.net/nenchoumi3119/article/details/148688800?fromshare=blogdetail&sharetype=blogdetail&sharerId=148688800&sharerefer=PC&sharesource=m0_73994182&sharefrom=from_link)

#### 使用自己的数据进行微调

这部分内容是依照源码中 examples/libero/convert_libero_data_to_lerobot.py 的部分，涉及到的内容为以下两个链接：

Pi0 Convert Data to Lerobot：Fine-Tuning Base Models on Your Own Data

Pi0 Convert Data to Aloha：convert_aloha_data_to_lerobot

因为在这部分中每人使用的数据集在格式上存在不少差异，但受限于精力，我这里只对 rosbag、libero、HDF5 三种形式进行 lerobot 转译与微调；

 

【Note】：考虑到有些人是第一次使用 uv 方式管理包，在适配自己数据集的时候难免出现缺包的情况，想要不污染自己默认环境则使用下面的命令补装 uv 包，前面一定要带上 uv。[ $ uv pip install <package_name> ]

#### rosbag转译

#### 微调模型

根据 ReadMe 文件的介绍，最好在正式训练之前对数据进行一次统计以检查，这一步比较耗时目的是统计整个模型中被激活和冻结的部分，参数 --config-name 表示你想要微调配置：

【Note】：这一步首次执行是需要联网的，建议设置好环境变量后再执行。

如果你不清楚这里的配置是什么意思，可以去查看src/openpi/training/config.py 文件：

### [π0的微调——如何基于各种开源数据集、以及私有数据集微调openpi(含我司七月的微调实践及openpi在国产臂上的部署)](https://blog.csdn.net/v_JULY_v/article/details/146125555?fromshare=blogdetail&sharetype=blogdetail&sharerId=146125555&sharerefer=PC&sharesource=m0_73994182&sharefrom=from_link)



![[65e41f2dc2774011837d41d19228f7c2.png]]


### Precise Manipulation with Efficient Online RL

RLT adds a special output token that provides a compact interface between the VLA and a lightweight RL policy.

We train the VLA to produce an "RL token" that can then provide a concise summary of the VLA's internal representations. This RL token is then used as the input into a much smaller model that can be trained with RL in real time.

The RL token is used by an actor and critic, which are trained with a sample-efficient off-policy RL method. Because the actor and critic operate on this compact representation, they can be represented with small networks that are trained directly on the robot, with hundreds of updates per second. This makes RL training responsive enough to improve the behavior after each attempt.

![[feishu_1776845754644_1.png]]

![[feishu_1776845755197_2.png]]

**First**, the RL policy predicts action chunks, _matching the action structure used by the VLA_ rather than acting at individual low-level control steps. This lets the online policy adapt the same temporally extended motions that matter in our tasks. **Second**, the RL policy does not act from scratch: the actor receives the VLA’s predicted action as input, so it learns to edit the VLA action rather than replace it entirely. We regularize the policy update toward this reference action, so the exploration stays close to the VLA when its behavior is already reasonable and deviates only when the critic identifies a better alternative. To prevent the policy from simply copying the VLA early in training, we also apply reference-action dropout, which forces the actor to maintain an independent action-generation pathway. **Finally**, we can optionally incorporate human interventions directly into the RL update, folding corrections back into training when the robot gets stuck or makes a mistake. These choices make online RL a reusable recipe that can be attached to a pretrained VLA across different tasks without task-specific engineering.

![[feishu_1776845755713_3.png]]

### **MEM by Pi**

![[Screenshot 2026-04-22 at 8.41.28 PM.png]]

![[feishu_1776845756222_4.png]]


### Pi 0.7

What makes π0.7 generalize so broadly? The key to generalization for foundation models is to use broad and diverse data, which in our case includes data from many different robots, human data, and even autonomous episodes collected by running various policies. Merging all these data sources naively does not lead to good results. We find that the key to using all of these data sources to attain compositional generalization is to add **_diverse context_** to the prompt: training the model with a variety of multimodal prompt structures that specify **not only _what_ the robot should do, but _how_ it should do it**. The prompt can include not just a textual description of the task, but a variety of other **annotations and modalities**. For example, providing the model with a visual subgoal defines a precise spatial layout of objects. Providing the desired length of the episode specifies how quickly the task should be done. **Critically, all of these pieces of information disambiguate the behavior, enabling diverse data with different strategies, behaviors, and levels of proficiency to be included in training.** At test time, our model accepts standard language instructions, but also information about the desired strategy, and even synthetically generated visual subgoals produced by a lightweight world model. We show some examples of what π0.7 can do below.

#### Leveraging more data with diverse conditioning

The different prompt modalities allow π0.7 to integrate a wide range of diverse data sources, including data from different robots and control modalities, human videos, and autonomous data. While our prior models also used some of these data sources (e.g., [videos](https://www.pi.website/research/human_to_robot)), π0.7 unifies these under a single prompting framework, supporting:

- **Diverse language** that describes the task and individual sub-steps.
    
- **Metadata** that describes _how_ the task was performed, such as speed and quality.
    
- **Control modality labels** that indicate whether to use joint or end-effector control.
    
- **Visual subgoal images** that show what the end of the current sub-step should _look like_. These images can be generated at test time by a world model that provides for visual generalization.
    

With these different annotation sources, π0.7 can leverage more types of data. For example, suboptimal autonomous evaluation data, which would ordinarily risk teaching the model to perform lower-quality actions, can be incorporated by annotating it with appropriate metadata (e.g., lower quality or lower speed).
![[Screenshot 2026-04-22 at 5.26.18 PM.png]]


![[Screenshot 2026-04-22 at 7.01.23 PM.png]]

![[Screenshot 2026-04-22 at 7.36.18 PM.png]]


### V. 提示多样化 (Diversifying the Prompt)

$\pi_{0.7}$ 的训练旨在处理包含多种组件的提示。为了增强测试时的灵活性，模型在训练期间会随机丢弃（Dropout）这些组件，使其能够处理任何子集的组合。

#### A. 子任务指令 (Subtask Instructions)

除了总体文本任务描述 $\ell_t$（如“清理厨房”）外，模型还包含捕获语义子任务的中间层文本 $\hat{\ell}_t$（如“打开冰箱门”）。

- **来源：** 在推理时，$\hat{\ell}_t$ 可由学习到的高级策略产生、由人类提供或省略。
    
- **功能：** **逐步教练：** 允许人类通过实时指令引导模型完成新任务（如“将红薯放入空气炸锅”）。
    
    - **策略微调：** 训练数据可用于将 $\pi_{0.7}$ 微调为高级策略，将观察结果和任务规格映射为具体的子任务指令。
        

#### B. 子目标图像 (Subgoal Images)

子任务指令虽然有效，但往往缺乏执行细节。子目标图像通过描绘场景的近期期望状态，提供了更丰富的规格说明。

- **多视图子目标：** $g_t = [G^1_t, \dots, G^n_t]$。通过多视图（如底座视图和腕部视图）同时指定环境、物体及机械臂/夹具的状态，改善空间接地（Spatial Grounding）。
    
- **生成机制：** 运行时由轻量级**世界模型** $g_\psi$ 生成。该模型基于 BAGEL（14B 参数的混合专家模型）初始化，并在视频和图像编辑数据上进行了预训练。
    
- **训练目标：** 使用标准流匹配损失（Flow Matching Loss）：
    $$\max_{\psi} \mathbb{E}_{\mathcal{D}_g} [L_{CFM}(g^\star_t, g_\psi(o_t, \hat{\ell}_t, m))]$$
    
    其中 $g^\star_t = o_{t_{end}}$ 是片段末尾的真实图像。

#### C. 片段元数据 (Episode Metadata)

为了利用低质量演示、失败案例及自主采集的数据，模型引入了片段元数据 $m$，以便在推理时引导模型选择高性能的动作。

- **总速度 (Overall speed)：** 离散化的时间步长度（如 500 步为一个区间）。
    
- **总质量 (Overall quality)：** 1 到 5 分的任务执行质量评分。
    
- **错误 (Mistake)：** 布尔值，指示机器人是否在特定动作片段中犯错（如抓取失败）。
    

> **推理优势：** 在运行时，可以通过提示词要求模型以“高速度、高质量、无错误”的状态执行任务。

#### D. 控制模式 (Control Mode)

模型支持不同的底层动作执行模式，通过文本标识符 $c \in \{\text{joint, ee}\}$ 进行指定：

- **Joint：** 关节空间控制。
    
- **EE：** 末端执行器（End-effector）控制。
    

#### E. 完整提示示例与训练细节

#### 提示词示例

> **Task:** peel vegetables. **Subtask:** pick up the peeler. **Speed:** 8000. **Quality:** 5. **Mistake:** false. **Control Mode:** joint.

##### 训练策略（随机丢弃比例）

为了提高鲁棒性，模型在训练时对各组件应用了不同的丢弃概率：

| **组件**         | **丢弃概率** | **备注**                                  |
| -------------- | -------- | --------------------------------------- |
| **视觉子目标图像**    | 75%      | 仅 25% 的样本包含图像；加入图像可使任务转化为“逆动力学”问题，加速收敛。 |
| **子任务指令**      | 30%      | 仅在存在子目标图像的情况下进行丢弃。                      |
| **片段元数据 (整体)** | 15%      | 整体完全丢弃的概率。                              |
| **具体元数据项**     | 5%       | 速度、质量、错误标签各自独立丢弃的概率。                    |
| **控制模式**       | 0%       | 不应用丢弃。                                  |

