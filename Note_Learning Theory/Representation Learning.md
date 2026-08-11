# Representation Learning（表示学习）

Representation learning aims to let a model automatically learn useful features from raw data instead of relying entirely on manually designed features.

Given an input $x$, an encoder maps it into a representation $z$:

$$
z=f_\theta(x)
$$

The representation $z$ should preserve information useful for downstream tasks while discarding irrelevant details. In robotics, the same learned representation may support object recognition, state estimation, contact detection, force estimation, slip detection, and manipulation.

---

## Self-Supervised Learning（自监督学习）

### Core Idea

Self-supervised learning（SSL）does not require manually annotated labels. Instead, it constructs a training target directly from the original data and uses that target as the supervision signal（监督信号）.

In supervised learning:

$$
x \rightarrow \text{human-annotated label }y
$$

In self-supervised learning:

$$
x \rightarrow \text{training target constructed from }x
$$

For example, part of an image can be masked and the model can be trained to predict the missing content:

$$
\text{masked image}\rightarrow\text{model}\rightarrow\text{reconstructed content}
$$

Although no human provides an object label, solving this task forces the model to learn the structure and semantics of the data.

### Main Goal: Learning Representations

The main goal of SSL is usually not the pretext task（代理任务）itself. Its purpose is to learn a reusable representation:

$$
x\rightarrow\boxed{\text{SSL encoder}}\rightarrow z
$$

The encoder is first pretrained on a large unlabeled dataset. The learned representation $z$ is then reused for downstream tasks（下游任务）, often with a much smaller labeled dataset:

$$
z\rightarrow
\begin{cases}
\text{classification}\\
\text{object recognition}\\
\text{state estimation}\\
\text{contact detection}\\
\text{force estimation}\\
\text{slip detection}
\end{cases}
$$

Therefore, SSL commonly serves as pretraining（预训练）.

### Common Method Families

#### 1. Reconstruction or Masked Prediction

Part of the input is removed, corrupted, or masked. The model must recover the original content:

$$
\tilde{x}\rightarrow\text{Encoder}\rightarrow\text{Decoder}\rightarrow x
$$

Examples include autoencoders and Masked Autoencoders（MAE）.

The model must understand meaningful data structure to reconstruct the missing information. However, spending model capacity on exact low-level reconstruction does not always produce the most useful semantic representation.

#### 2. Contrastive Learning（对比学习）

Two augmented views of the same sample form a positive pair（正样本对）. Their representations should be close, while representations of different samples should be distinguishable:

$$
x_1,x_2\rightarrow z_1,z_2,\qquad z_1\approx z_2
$$

The model therefore learns features that remain stable under selected data augmentations. Common methods include SimCLR and MoCo.

The choice of augmentation is important: it defines which changes the learned representation should ignore.

#### 3. Teacher–Student or Representation Prediction

A student network learns to predict the representation produced by a teacher network. The target is a feature representation rather than the original raw input.

Common methods include BYOL and DINO. These methods can learn useful representations without explicitly reconstructing pixels; some also avoid the need for negative samples.

### Relationship to Supervised and Unsupervised Learning

| Learning paradigm | Source of target | Main idea |
|---|---|---|
| Supervised learning | Human annotations | Learn a mapping from inputs to labeled targets |
| Self-supervised learning | Automatically constructed from the data | Learn reusable representations through a proxy objective |
| Unsupervised learning | No human annotations | Discover patterns, structures, or distributions in data |

Self-supervised learning is generally regarded as a form of unsupervised representation learning（无监督表示学习）. Its training procedure resembles supervised learning because it still has an input, a target, and a loss function. The key difference is that the target is generated automatically rather than annotated by a person.

### Why It Is Useful in Robotics

Robotics systems can collect large amounts of raw sensor data, but accurate labels are often expensive or difficult to obtain. For example, tactile data may require labels for:

- Contact state
- Contact force
- Slip occurrence
- Material properties
- Object identity
- Contact geometry

SSL allows a model to first learn from large-scale unlabeled visual, tactile, proprioceptive, or multimodal data. Only a small labeled dataset may then be needed for a specific downstream task.

A typical pipeline is:

$$
\text{large unlabeled sensor dataset}
\rightarrow\text{SSL pretraining}
\rightarrow\text{pretrained encoder}
\rightarrow\text{downstream-task fine-tuning}
$$

### Key Characteristics

1. Labels are generated from the data itself rather than manually annotated.
2. The main objective is usually to learn a transferable representation（可迁移表示）.
3. It can exploit large unlabeled datasets.
4. It is commonly used for pretraining before fine-tuning（微调）.
5. Its effectiveness depends heavily on the training objective, data augmentation, and data distribution.
6. It is especially valuable when raw data is abundant but task-specific labels are expensive.
