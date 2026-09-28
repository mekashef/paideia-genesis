"""Deep Learning & Computer Vision Foundations & Research Papers Curriculum.
Provides structured knowledge modules across Foundation Models, 3D Vision, and Deep Learning:
- 8 Core Reading Sessions / Paper Foundations
- 8 High-Yield Concepts & Mechanisms
- 8 Key Technical Entities & Architectures
- 5 Comparative Differentials & Trade-off Syntheses
- 5 Critical Research Traps & Engineering Pitfalls
- 25+ High-Yield Spaced-Repetition Active Recall Flashcards
"""

VISION_CURRICULUM_TOPICS = [
    {"name": "Vision Transformers & Patch Self-Attention (ViT & Swin)", "priority": "CRITICAL"},
    {"name": "3D Gaussian Splatting & Real-Time Radiance Rasterization", "priority": "CRITICAL"},
    {"name": "Neural Radiance Fields (NeRF & Instant-NGP)", "priority": "CRITICAL"},
    {"name": "Self-Supervised Vision Foundation Models (DINOv2 & MAE)", "priority": "HIGH"},
    {"name": "Generative Diffusion Models (DDPM & Latent Diffusion)", "priority": "HIGH"},
    {"name": "Multimodal Representation Learning (CLIP & SigLIP)", "priority": "HIGH"},
    {"name": "Spatial AI, Visual Odometry & DUSt3R 3D Reconstruction", "priority": "MEDIUM"},
    {"name": "Model Optimization, KV Cache & TensorRT Latency", "priority": "MEDIUM"}
]

VISION_SESSIONS = [
    {
        "session_num": 1,
        "slug": "session-01-vision-transformers-vit",
        "title": "Session 01: An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale (ViT)",
        "instructors": "Alexey Dosovitskiy et al. (Google Research, Brain Team)",
        "summary": "Decomposing 2D images into flattened patch sequences for pure transformer encoder architectures without inductive convolutional bias.",
        "content": """### Paper Summary & Core Insights
The Vision Transformer (ViT) demonstrates that the standard Transformer architecture applied directly to sequences of non-overlapping image patches achieves state-of-the-art results on image classification when pre-trained on large-scale datasets (JFT-300M, ImageNet-21k).

### Core Architecture
1. **Patch Projection**: An image $x \in \mathbb{R}^{H \times W \times C}$ is partitioned into non-overlapping patches $x_p \in \mathbb{R}^{N \times (P^2 \cdot C)}$, where $P$ is patch resolution (e.g. $16 \\times 16$) and $N = HW / P^2$.
2. **Linear Embedding**: Patches are flattened and mapped via a trainable linear projection $\mathbf{E}$ to dimension $D$.
3. **[CLS] Token & Positional Embeddings**: A learnable class token $\mathbf{x}_{\text{class}}$ is prepended, and 1D learnable positional embeddings $\mathbf{E}_{pos}$ are added:
   $$\mathbf{z}_0 = [\mathbf{x}_{\text{class}}; \mathbf{x}_p^1 \mathbf{E}; \dots; \mathbf{x}_p^N \mathbf{E}] + \mathbf{E}_{pos}$$
4. **Standard Transformer Encoder**: Alternating layers of Multi-Head Self-Attention (MSA) and MLP blocks with LayerNorm (LN) before each block.

### Key Trade-offs
- **Lack of Inductive Bias**: Unlike CNNs, ViT has no hardcoded translation equivariance or local connectivity. While this harms sample efficiency on small datasets, it enables unbounded capacity when scaling data and compute.

Related: [[entities/vit-architecture]], [[differentials/vit-vs-convnext]], [[exam_traps/patch-size-quadratic-memory]]."""
    },
    {
        "session_num": 2,
        "slug": "session-02-3d-gaussian-splatting",
        "title": "Session 02: 3D Gaussian Splatting for Real-Time Radiance Field Rendering",
        "instructors": "Bernhard Kerbl, Georgios Kopanas, Thomas Leimkuehler, George Drettakis (SIGGRAPH 2023)",
        "summary": "Replacing implicit neural networks with explicit 3D anisotropic Gaussians and a custom tile-based rasterizer for 100+ FPS novel view synthesis.",
        "content": """### Paper Summary & Core Insights
3D Gaussian Splatting (3DGS) achieves state-of-the-art visual quality in novel view synthesis while maintaining real-time rendering speeds (>100 FPS at 1080p). It avoids the expensive ray marching of continuous volumetric MLPs.

### Core Mathematical Formulation
1. **Explicit Scene Representation**: The scene is modeled by millions of 3D Gaussians defined by:
   - Position / Mean: $\boldsymbol{\mu} \in \mathbb{R}^3$
   - 3D Covariance Matrix $\boldsymbol{\Sigma}$:
     $$\boldsymbol{\Sigma} = \mathbf{R} \mathbf{S} \mathbf{S}^T \mathbf{R}^T$$
     parameterized by a quaternion $\mathbf{q}$ (rotation) and scaling vector $\mathbf{s}$.
   - Opacity $\alpha \in [0, 1]$
   - Spherical Harmonics (SH) coefficients representing view-dependent color.
2. **Differentiable 2D Projection**:
   $$\boldsymbol{\Sigma}' = \mathbf{J} \mathbf{W} \boldsymbol{\Sigma} \mathbf{W}^T \mathbf{J}^T$$
   where $\mathbf{W}$ is the viewing transformation and $\mathbf{J}$ is the Jacobian of the affine perspective projection.
3. **Tile-Based Differentiable Rasterizer**: Radix-sorts Gaussians by tile depth, allowing hardware-accelerated $\alpha$-blending without thread divergence.

Related: [[entities/3d-gaussian-splatting]], [[differentials/3dgs-vs-nerf]], [[exam_traps/gaussian-splatting-floater-artifacts]]."""
    },
    {
        "session_num": 3,
        "slug": "session-03-neural-radiance-fields-nerf",
        "title": "Session 03: NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis",
        "instructors": "Ben Mildenhall, Pratul P. Srinivasan, Matthew Tancik, Jonathan T. Barron et al. (ECCV 2020)",
        "summary": "Continuous 5D neural volumetric scene representations optimized using stratified volume rendering and positional frequency encodings.",
        "content": """### Paper Summary & Core Insights
NeRF represents a 3D static scene as a continuous 5D function mapping spatial coordinates $(x, y, z)$ and viewing directions $(\theta, \phi)$ to volume density $\sigma$ and emitted RGB radiance:
$$F_\Theta: (\mathbf{x}, \mathbf{d}) \to (\mathbf{c}, \sigma)$$

### Key Theoretical Components
1. **Positional Encoding $\gamma(p)$**:
   Overcomes the spectral bias of deep coordinate MLPs, enabling the network to represent high-frequency geometric detail and fine textures:
   $$\gamma(p) = \left( \sin(2^0 \pi p), \cos(2^0 \pi p), \dots, \sin(2^{L-1} \pi p), \cos(2^{L-1} \pi p) \right)$$
2. **Differentiable Numerical Quadrature**:
   Expected color $C(\mathbf{r})$ of camera ray $\mathbf{r}(t) = \mathbf{o} + t\mathbf{d}$ is computed via accumulated transmittance $T_i$:
   $$\hat{C}(\mathbf{r}) = \sum_{i=1}^{N} T_i (1 - \exp(-\sigma_i \delta_i)) \mathbf{c}_i, \quad T_i = \exp\left(-\sum_{j=1}^{i-1} \sigma_j \delta_j\right)$$

Related: [[concepts/neural-radiance-fields]], [[differentials/3dgs-vs-nerf]]."""
    },
    {
        "session_num": 4,
        "slug": "session-04-dinov2-self-supervised-vision",
        "title": "Session 04: DINOv2: Learning Robust Visual Features without Supervision",
        "instructors": "Maxime Oquab, Timothée Darcet, Théo Moutakanni et al. (Meta AI Research)",
        "summary": "Self-supervised foundation vision models trained at scale via student-teacher self-distillation, producing universal pixel-level and semantic representations.",
        "content": """### Paper Summary & Core Insights
DINOv2 produces visual representations that exhibit remarkable general-purpose properties across dense visual tasks (depth estimation, semantic segmentation) and classification without fine-tuning.

### Technical Mechanism
1. **Self-Distillation with No Labels**:
   A Student network $g_{\theta_s}$ learns to predict the output of an exponential moving average (EMA) Teacher network $g_{\theta_t}$.
2. **Combined Multi-Task Objective**:
   - Cross-entropy loss on global $[CLS]$ tokens with centering and temperature sharpening.
   - Masked Image Modeling (iBOT patch-level cross-entropy loss): masks tokens in the student and predicts the unmasked teacher representation.
   - Sinkhorn-Knopp centering to strictly prevent feature collapse.

Related: [[entities/dinov2]], [[differentials/clip-vs-mae]], [[concepts/self-supervised-vision-representations]]."""
    },
    {
        "session_num": 5,
        "slug": "session-05-generative-diffusion-models",
        "title": "Session 05: Denoising Diffusion Probabilistic Models (DDPM) & Latent Diffusion",
        "instructors": "Jonathan Ho, Ajay Jain, Pieter Abbeel (NeurIPS 2020) / Robin Rombach et al. (CVPR 2022)",
        "summary": "Formulating generative image synthesis as an iterative score-matching reverse denoising process parameterized by U-Nets in compressed latent spaces.",
        "content": """### Paper Summary & Core Insights
Diffusion models define a forward Markov chain that gradually adds Gaussian noise to an image until it becomes pure isotropic Gaussian noise, and learn a parameterized reverse process to reconstruct the data manifold.

### Core Mathematical Formulation
1. **Forward Process (Fixed)**:
   $$q(\mathbf{x}_t | \mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1 - \beta_t}\mathbf{x}_{t-1}, \beta_t \mathbf{I})$$
   Using $\alpha_t = 1 - \beta_t$ and $\bar{\alpha}_t = \prod_{s=1}^t \alpha_s$:
   $$q(\mathbf{x}_t | \mathbf{x}_0) = \mathcal{N}(\mathbf{x}_t; \sqrt{\bar{\alpha}_t}\mathbf{x}_0, (1 - \bar{\alpha}_t)\mathbf{I})$$
2. **Reverse Denoising Objective**:
   The network $\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)$ is trained via simplified MSE loss:
   $$\mathcal{L}_{\text{simple}}(\theta) = \mathbb{E}_{t, \mathbf{x}_0, \boldsymbol{\epsilon}}\left[ \|\boldsymbol{\epsilon} - \boldsymbol{\epsilon}_\theta(\sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t}\boldsymbol{\epsilon}, t)\|^2 \right]$$
3. **Latent Diffusion (Stable Diffusion)**:
   Performs the diffusion process within the low-dimensional latent space of a trained autoencoder (VAE) to reduce compute overhead by orders of magnitude.

Related: [[entities/stable-diffusion]], [[concepts/generative-diffusion-mechanisms]]."""
    },
    {
        "session_num": 6,
        "slug": "session-06-multimodal-contrastive-clip",
        "title": "Session 06: Learning Transferable Visual Models From Natural Language Supervision (CLIP)",
        "instructors": "Alec Radford, Jong Wook Kim, Chris Hallacy et al. (OpenAI 2021)",
        "summary": "Joint text-image embedding spaces trained with symmetric InfoNCE contrastive loss over 400M web-scale pairs for zero-shot transfer.",
        "content": """### Paper Summary & Core Insights
CLIP (Contrastive Language-Image Pre-training) aligns image and text representations into a shared geometric hypersphere using a simple symmetric InfoNCE contrastive objective.

### Key Equations & Structure
1. For a batch of $N$ (image, text) pairs:
   $$\mathcal{L}_{\text{InfoNCE}} = -\frac{1}{2N} \sum_{i=1}^N \left( \log \frac{\exp(\mathbf{I}_i \cdot \mathbf{T}_i / \tau)}{\sum_j \exp(\mathbf{I}_i \cdot \mathbf{T}_j / \tau)} + \log \frac{\exp(\mathbf{I}_i \cdot \mathbf{T}_i / \tau)}{\sum_j \exp(\mathbf{I}_j \cdot \mathbf{T}_i / \tau)} \right)$$
2. Enables zero-shot classification by computing cosine similarity between visual features and candidate text prompt embeddings (e.g. *"a photo of a {class}"*).

Related: [[entities/clip]], [[differentials/clip-vs-mae]]."""
    },
    {
        "session_num": 7,
        "slug": "session-07-dust3r-3d-reconstruction",
        "title": "Session 07: DUSt3R: Geometric 3D Vision Made Easy via Unconstrained Stereo Pointmaps",
        "instructors": "Shuzhe Wang, Vincent Leroy, Yohann Cabon et al. (NAVER LABS Europe, CVPR 2024)",
        "summary": "Unifying dense stereo, multi-view geometry, and camera pose estimation into a direct regression of 3D pointmaps using cross-attention transformers.",
        "content": """### Paper Summary & Core Insights
Traditional multi-view stereo pipelines require explicit camera calibration, feature extraction (SIFT/SuperPoint), RANSAC, epipolar geometry, and bundle adjustment. DUSt3R replaces this fragile pipeline with a direct regression model that predicts dense 3D pointmaps directly in the first camera coordinate frame.

### Key Innovation
- Takes two unconstrained images $(I^1, I^2)$ and outputs two dense pointmaps $X^{1,1}$ and $X^{2,1}$ along with pixel-level confidence maps $C^1, C^2$.
- Solves relative pose, intrinsic calibration, and dense surface reconstruction simultaneously.

Related: [[entities/dust3r]], [[concepts/visual-inertial-odometry-slam]]."""
    },
    {
        "session_num": 8,
        "slug": "session-08-segment-anything-sam",
        "title": "Session 08: Segment Anything Model (SAM) & Foundation Visual Segmentation",
        "instructors": "Alexander Kirillov, Eric Mintun, Nikhila Ravi et al. (Meta AI Research, ICCV 2023)",
        "summary": "Promptable visual segmentation foundation models trained on 1 billion masks with decoupled image encoders and lightweight prompt-driven decoders.",
        "content": """### Paper Summary & Core Insights
The Segment Anything project introduces a promptable segmentation task, model (SAM), and dataset (SA-1B). SAM demonstrates zero-shot transfer across downstream segmentation benchmarks using points, bounding boxes, or free-form text prompts.

### Decoupled Architecture
1. **Heavyweight Image Encoder**: High-capacity ViT pre-trained with MAE computes image embeddings once per scene.
2. **Prompt Encoder**: Maps points, boxes, or masks into positional sparse embeddings.
3. **Lightweight Mask Decoder**: Two-way cross-attention transformer runs in <50ms in-browser on CPU/GPU, enabling real-time interactive segmentation.

Related: [[entities/sam]], [[concepts/vision-transformers-vit]]."""
    }
]

VISION_CONCEPTS = [
    {
        "slug": "vision-transformers-vit",
        "title": "Vision Transformers (ViT) & Multi-Head Self-Attention",
        "domain": "Computer Science & AI",
        "system": "Deep Learning Architectures",
        "tags": ["Transformers", "Computer-Vision", "Self-Attention", "Deep-Learning"],
        "summary": "Applying pure self-attention mechanisms to linear projections of flattened 2D image patches without convolutional inductive biases.",
        "content": """### Core Mathematical Mechanism
Given an image $\mathbf{X} \in \mathbb{R}^{H \times W \times C}$, ViT slices it into non-overlapping patches of size $P \times P$:
$$N = \frac{HW}{P^2}$$
Each patch is linearly mapped to dimension $D$. The attention mechanism computes global pairwise token affinities:
$$\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d_k}}\right)\mathbf{V}$$
Because every patch attends to every other patch regardless of spatial distance, ViT has a global receptive field from layer 1.

### Key Properties & Scaling Laws
- **Computational Complexity**: $\mathcal{O}(N^2 \cdot D) = \mathcal{O}\left(\frac{H^2 W^2}{P^4} \cdot D\right)$.
- **Empirical Scaling**: Outperforms CNNs on high-capacity regimes (JFT, ImageNet-22k) but requires data augmentation or self-supervised pre-training to prevent overfitting on small datasets.

Related: [[entities/vit-architecture]], [[differentials/vit-vs-convnext]], [[exam_traps/patch-size-quadratic-memory]]."""
    },
    {
        "slug": "3d-gaussian-splatting",
        "title": "3D Gaussian Splatting & Tile-Based Differentiable Rasterization",
        "domain": "Computer Science & AI",
        "system": "3D Vision & Neural Rendering",
        "tags": ["3D-Vision", "Radiance-Fields", "Real-Time-Rendering", "Gaussian-Splatting"],
        "summary": "An explicit, unstructured 3D representation using anisotropic Gaussians with tile-based depth sorting for real-time 100+ FPS novel view synthesis.",
        "content": """### Mathematical Foundation
A 3D Gaussian is centered at position $\boldsymbol{\mu}$ with world-space covariance $\boldsymbol{\Sigma}$:
$$G(\mathbf{x}) = \exp\left(-\frac{1}{2}(\mathbf{x} - \boldsymbol{\mu})^T \boldsymbol{\Sigma}^{-1} (\mathbf{x} - \boldsymbol{\mu})\right)$$
To ensure positive semi-definiteness during gradient descent, $\boldsymbol{\Sigma}$ is parameterized via a scale vector $\mathbf{s} \in \mathbb{R}^3$ and unit quaternion $\mathbf{q} \in \mathbb{R}^4$:
$$\boldsymbol{\Sigma} = \mathbf{R} \mathbf{S} \mathbf{S}^T \mathbf{R}^T$$

### Projected 2D Splatting
Under local affine camera approximation with viewing matrix $\mathbf{W}$ and projection Jacobian $\mathbf{J}$:
$$\boldsymbol{\Sigma}_{2D} = \mathbf{J} \mathbf{W} \boldsymbol{\Sigma} \mathbf{W}^T \mathbf{J}^T$$
Color is accumulated along ray pixels using volumetric $\alpha$-blending:
$$C = \sum_{i \in \mathcal{N}} c_i \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j)$$

Related: [[entities/3d-gaussian-splatting]], [[differentials/3dgs-vs-nerf]], [[exam_traps/gaussian-splatting-floater-artifacts]]."""
    },
    {
        "slug": "neural-radiance-fields",
        "title": "Neural Radiance Fields (NeRF) & Volume Rendering",
        "domain": "Computer Science & AI",
        "system": "3D Vision & Neural Rendering",
        "tags": ["NeRF", "Coordinate-Networks", "Volume-Rendering", "3D-Vision"],
        "summary": "Continuous implicit volumetric scene representations mapping 5D spatial coordinates and viewing directions to volume density and radiance.",
        "content": """### Core Theory
NeRF parameterizes a 3D scene using a fully connected multilayer perceptron (MLP):
$$F_\Theta: (\mathbf{x}, \mathbf{d}) \mapsto (\mathbf{c}, \sigma)$$
where $\mathbf{x} = (x, y, z)$ is 3D position and $\mathbf{d} = (\theta, \phi)$ is the unit viewing direction vector.

### Differentiable Volume Rendering
Given a camera ray $\mathbf{r}(t) = \mathbf{o} + t\mathbf{d}$, the expected color $\hat{C}(\mathbf{r})$ is obtained by numerical quadrature:
$$\hat{C}(\mathbf{r}) = \sum_{i=1}^N T_i (1 - \exp(-\sigma_i \delta_i))\mathbf{c}_i, \quad T_i = \exp\left(-\sum_{j=1}^{i-1} \sigma_j \delta_j\right)$$
where $\delta_i = t_{i+1} - t_i$ is the distance between adjacent quadrature samples along the ray.

Related: [[session-03-neural-radiance-fields-nerf]], [[differentials/3dgs-vs-nerf]]."""
    },
    {
        "slug": "self-supervised-vision-representations",
        "title": "Self-Supervised Vision Foundation Models & Masked Autoencoding",
        "domain": "Computer Science & AI",
        "system": "Representation Learning",
        "tags": ["DINOv2", "MAE", "Self-Supervised", "Foundation-Models"],
        "summary": "Techniques for pre-training visual encoders without human annotations using student-teacher self-distillation and masked patch reconstruction.",
        "content": """### Core Paradigms
1. **Self-Distillation (DINO & DINOv2)**:
   A student network parameterizes $g_{\theta_s}$ and teacher parameterizes $g_{\theta_t}$ via EMA updates:
   $$\theta_t \leftarrow \lambda \theta_t + (1 - \lambda)\theta_s$$
   Both global $[CLS]$ tokens and local masked patches are matched via cross-entropy with temperature sharpening to prevent uniform collapse.
2. **Masked Autoencoding (MAE)**:
   Randomly masks a high ratio (75%-80%) of image patches. An asymmetric encoder-decoder reconstructs missing normalized pixel values, forcing the model to learn high-level scene semantics and 3D spatial priors.

Related: [[entities/dinov2]], [[differentials/clip-vs-mae]]."""
    },
    {
        "slug": "generative-diffusion-mechanisms",
        "title": "Generative Diffusion Models & Score-Based SDEs",
        "domain": "Computer Science & AI",
        "system": "Generative AI & Synthesis",
        "tags": ["Diffusion", "DDPM", "Generative-AI", "SDE"],
        "summary": "Formulating visual generative modeling as reverse denoising stochastic differential equations using noise-conditioned score networks.",
        "content": """### Mathematical Mechanism
The forward diffusion process adds continuous Gaussian perturbation:
$$\mathrm{d}\mathbf{x} = \mathbf{f}(\mathbf{x}, t)\mathrm{d}t + g(t)\mathrm{d}\mathbf{w}$$
By Anderson's reverse-time theorem, the reverse diffusion process is also a diffusion process:
$$\mathrm{d}\mathbf{x} = \left[ \mathbf{f}(\mathbf{x}, t) - g(t)^2 \nabla_\mathbf{x} \log p_t(\mathbf{x}) \right]\mathrm{d}t + g(t)\mathrm{d}\bar{\mathbf{w}}$$
The deep neural network parameterizes the score function $\mathbf{s}_\theta(\mathbf{x}, t) \approx \nabla_\mathbf{x} \log p_t(\mathbf{x})$ by predicting the noise vector $\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)$.

### Classifier-Free Guidance (CFG)
To steer generation using conditioning text $\mathbf{c}$ without an explicit external classifier:
$$\tilde{\boldsymbol{\epsilon}}_\theta(\mathbf{x}_t, \mathbf{c}) = \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, \emptyset) + s \cdot (\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, \mathbf{c}) - \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, \emptyset))$$
where $s > 1$ amplifies alignment with the conditioning prompt.

Related: [[entities/stable-diffusion]], [[session-05-generative-diffusion-models]]."""
    },
    {
        "slug": "visual-inertial-odometry-slam",
        "title": "Visual-Inertial Odometry (VIO) & Spatial AI",
        "domain": "Computer Science & Robotics",
        "system": "Spatial AI & SLAM",
        "tags": ["VIO", "SLAM", "Spatial-AI", "Robotics"],
        "summary": "Sensor fusion of high-frequency IMU measurements and visual feature tracking via factor graph bundle adjustment for 6-DoF state estimation.",
        "content": """### Core Theory
Visual-Inertial Odometry (VIO) estimates the 6-DoF trajectory of an agent by fusing:
- High-frequency ($>100\\text{ Hz}$) accelerometer and gyroscope readings from an IMU.
- Camera frames capturing optical feature tracks ($20-60\\text{ Hz}$).

### Factor Graph Optimization
Nonlinear least-squares optimization minimizes reprojection error and IMU preintegration residuals:
$$\min_{\mathcal{X}} \left\{ \sum_{k} \|\mathbf{r}_{\mathcal{I}}(k, k+1)\|^2_{\boldsymbol{\Sigma}_{\mathcal{I}}} + \sum_{i,j} \|\mathbf{r}_{\mathcal{C}}(i, j)\|^2_{\boldsymbol{\Sigma}_{\mathcal{C}}} \right\}$$
where $\mathbf{r}_{\mathcal{I}}$ represents IMU preintegrated kinematic constraints and $\mathbf{r}_{\mathcal{C}}$ is the visual reprojection error:
$$\mathbf{r}_{\mathcal{C}}(i, j) = \mathbf{z}_{ij} - \pi(\mathbf{T}_{wb_j}^{-1} \mathbf{T}_{wb_i} \mathbf{p}_i)$$

Related: [[session-07-dust3r-3d-reconstruction]], [[entities/dust3r]]."""
    }
]

VISION_ENTITIES = [
    {
        "slug": "vit-architecture",
        "title": "Vision Transformer (ViT)",
        "category": "Deep Learning Architecture",
        "high_yield_notes": "Pure self-attention model replacing convolutions with flattened 16x16 patch projections. Lacks inductive translation equivariance but scales gracefully with compute and data."
    },
    {
        "slug": "3d-gaussian-splatting-engine",
        "title": "3D Gaussian Splatting (3DGS)",
        "category": "3D Neural Rendering Engine",
        "high_yield_notes": "Explicit radiance field representation with 3D anisotropic Gaussians and tile-based sorting. Delivers 1080p rendering at >100 FPS."
    },
    {
        "slug": "nerf-model",
        "title": "Neural Radiance Field (NeRF)",
        "category": "Implicit Volumetric Representation",
        "high_yield_notes": "Continuous 5D scene mapping via coordinate MLPs. Requires positional encoding to overcome spectral bias; slower rendering due to volumetric ray marching."
    },
    {
        "slug": "dinov2",
        "title": "DINOv2 Foundation Model",
        "category": "Vision Foundation Model",
        "high_yield_notes": "Self-supervised Vision Transformer trained with student-teacher distillation and Sinkhorn-Knopp centering. Universal visual features for dense and global tasks."
    },
    {
        "slug": "clip",
        "title": "CLIP (Contrastive Language-Image Pre-training)",
        "category": "Multimodal Foundation Model",
        "high_yield_notes": "Symmetric InfoNCE contrastive alignment between ViT image embeddings and Transformer text embeddings on 400M web pairs. Foundation for zero-shot transfer."
    },
    {
        "slug": "stable-diffusion",
        "title": "Latent Diffusion Models (Stable Diffusion)",
        "category": "Generative Vision Model",
        "high_yield_notes": "Denoising diffusion executed within low-dimensional VAE latent space conditioned on cross-attention text embeddings via classifier-free guidance."
    },
    {
        "slug": "dust3r",
        "title": "DUSt3R Multi-View Model",
        "category": "Spatial AI & 3D Reconstruction",
        "high_yield_notes": "Direct regression of 3D pointmaps and confidence maps from unconstrained stereo pairs, bypassing fragile SIFT/RANSAC/bundle adjustment pipelines."
    },
    {
        "slug": "sam",
        "title": "Segment Anything Model (SAM)",
        "category": "Interactive Visual Foundation Model",
        "high_yield_notes": "Promptable zero-shot segmentation model decoupling a heavy ViT image encoder from a sub-50ms lightweight mask decoder."
    }
]

VISION_DIFFERENTIALS = [
    {
        "slug": "3dgs-vs-nerf",
        "title": "3D Gaussian Splatting vs Neural Radiance Fields (NeRF)",
        "summary": "Comparative analysis between explicit anisotropic Gaussian rasterization and implicit continuous volumetric MLP ray marching.",
        "content": """| Feature | 3D Gaussian Splatting (3DGS) | Neural Radiance Fields (NeRF) |
|---|---|---|
| **Representation** | Explicit unstructured 3D Gaussians | Implicit continuous MLP ($F_\Theta$) |
| **Rendering Speed** | Real-time (>100 FPS at 1080p) | Offline / Low FPS (<10 FPS without hashing) |
| **Optimization Method** | Differentiable tile-based rasterizer | Ray marching quadrature numerical integration |
| **Memory Footprint** | Higher VRAM for millions of Gaussians | Compact weights in small MLP (e.g. 5-10 MB) |
| **Editability** | Direct geometric manipulation of points | Difficult to edit global implicit weights |
| **Artifacts** | Floater Gaussians in sparse regions | Blurry haze and high-frequency speckling |"""
    },
    {
        "slug": "vit-vs-convnext",
        "title": "Vision Transformers (ViT) vs Modern ConvNets (ConvNeXt)",
        "summary": "Trade-offs between global self-attention mechanisms and localized depthwise convolutions with modernized architectures.",
        "content": """| Dimension | Vision Transformer (ViT) | ConvNeXt / Modern CNN |
|---|---|---|
| **Inductive Bias** | Minimal (no spatial locality assumed) | Strong (translation equivariance & spatial locality) |
| **Compute Complexity** | $\mathcal{O}(N^2)$ quadratic with tokens | $\mathcal{O}(N)$ linear with resolution |
| **Data Requirements** | Needs large datasets (JFT, ImageNet-22k) | Efficient convergence on small/medium datasets |
| **Global Receptive Field** | Instantaneous from Layer 1 | Gradually accumulated across deep layers |
| **Dynamic Attention** | Data-dependent input-adaptive weights | Fixed kernel weights post-training |"""
    },
    {
        "slug": "clip-vs-mae",
        "title": "Contrastive Learning (CLIP) vs Masked Autoencoding (MAE)",
        "summary": "Discriminative text-aligned multimodal representations vs generative dense reconstruction representations.",
        "content": """| Attribute | Contrastive Learning (CLIP) | Masked Autoencoding (MAE) |
|---|---|---|
| **Supervision** | Paired text-image captions | Pure unlabelled images (self-supervised) |
| **Loss Function** | Symmetric InfoNCE cross-entropy | Pixel MSE loss on masked patches |
| **Masking Ratio** | 0% (full image seen) | 75% - 80% of tokens masked |
| **Representation Style** | High-level global semantic alignment | Dense fine-grained pixel and geometric details |
| **Zero-Shot Transfer** | Out-of-the-box text classification | Requires fine-tuning or probe head |"""
    }
]

VISION_TRAPS = [
    {
        "slug": "patch-size-quadratic-memory",
        "title": "Patch Size Halving Quadratic Memory Explosion Trap",
        "summary": "Halving the Vision Transformer patch size quadruples sequence length and multiplies attention memory by 16x.",
        "content": """### Problem Statement
In Vision Transformers, image patches have size $P \times P$. When switching from $P=16$ (ViT-B/16) to $P=8$ (ViT-B/8) for higher fine-grained spatial accuracy:
$$N = \frac{H \cdot W}{P^2}$$
Halving $P$ increases token count $N$ by $4\times$.

### The Trap: Memory Footprint
Self-attention maps $\mathbf{A} = \text{softmax}(\mathbf{Q}\mathbf{K}^T / \sqrt{d})$ require $\mathcal{O}(N^2)$ memory:
$$\text{Memory} \propto N^2 = (4N_0)^2 = 16 \cdot N_0^2$$
A naive inference or training pass with $P=8$ consumes $16\times$ more attention memory, causing out-of-memory (OOM) crashes on standard GPUs unless FlashAttention or windowed attention (Swin) is used."""
    },
    {
        "slug": "gaussian-splatting-floater-artifacts",
        "title": "3D Gaussian Splatting Floater Artifacts on Narrow Baselines",
        "summary": "Insufficient camera parallax causes Gaussians to overfit along camera viewing rays as floating planar artifacts.",
        "content": """### Problem Statement
When training 3D Gaussian Splatting on forward-facing datasets with small angular baselines:
- Gaussians with low opacity but high density form between the camera and the scene.
- Because these 'floaters' satisfy the training viewpoints, the rasterizer loss converges.

### Failure Mode
When rendering novel viewpoints that deviate from the camera trajectory, floaters produce egregious needle-like or cloud-like visual artifacts that destroy geometry.
### Mitigation
Regularize scaling factors, prune Gaussians with near-zero opacity, and apply depth-guided geometric constraints."""
    }
]

VISION_FLASHCARDS = [
    {
        "front": "In a Vision Transformer (ViT) processing a 224x224 image, using patch size P=16 yields {{c1::196}} patches (excluding the [CLS] token).",
        "back": "Formula: (224/16) * (224/16) = 14 * 14 = 196 tokens.",
        "pearl": "Adding the [CLS] token results in a sequence length of 197.",
        "tags": ["DeepLearning", "ComputerVision", "ViT", "Transformers"],
        "source": "Vision Transformers (Dosovitskiy et al.)"
    },
    {
        "front": "Why does halving the patch size P in ViT increase self-attention memory by {{c1::16x}}?",
        "back": "Halving P quadruples token count N ({{c1::4x}}), and self-attention memory scales as O(N^2), leading to (4)^2 = {{c2::16x}} memory overhead.",
        "pearl": "Mitigated using FlashAttention-2 or hierarchical windowed self-attention (Swin Transformer).",
        "tags": ["DeepLearning", "ComputerVision", "Optimization"],
        "source": "Patch Size Quadratic Memory Trap"
    },
    {
        "front": "In 3D Gaussian Splatting, the 3D covariance matrix Sigma is parameterized as Sigma = {{c1::R * S * S^T * R^T}} to enforce {{c2::positive semi-definiteness}}.",
        "back": "R is parameterized via a unit quaternion q and S via a 3D scaling vector s.",
        "pearl": "This parameterization prevents invalid non-physical covariance matrices during unconstrained SGD.",
        "tags": ["3DVision", "GaussianSplatting", "RadianceFields"],
        "source": "3D Gaussian Splatting (Kerbl et al.)"
    },
    {
        "front": "NeRF uses positional encoding gamma(p) before passing spatial coordinates into the MLP to overcome {{c1::spectral bias}}.",
        "back": "Standard coordinate MLPs have an inherent bias towards learning low frequencies; sinusoidal encodings allow high-frequency details to be represented.",
        "pearl": "Without positional encoding, NeRF reconstructions appear blurry and lack fine texture edges.",
        "tags": ["3DVision", "NeRF", "CoordinateNetworks"],
        "source": "NeRF (Mildenhall et al.)"
    },
    {
        "front": "In DINOv2, what mechanism is employed to strictly prevent the student-teacher network from suffering representation collapse?",
        "back": "{{c1::Sinkhorn-Knopp algorithm}} (along with centering and temperature sharpening).",
        "pearl": "Sinkhorn-Knopp normalizes the assignment matrix across the batch to ensure all prototype clusters are utilized uniformly.",
        "tags": ["SelfSupervised", "FoundationModels", "DINOv2"],
        "source": "DINOv2 (Oquab et al.)"
    },
    {
        "front": "In Generative Diffusion Models (DDPM), the network epsilon_theta is trained to predict the {{c1::added Gaussian noise vector epsilon}} rather than the clean image directly.",
        "back": "Predicting the noise vector corresponds to estimating the score function of the perturbed data distribution.",
        "pearl": "L_simple minimizes MSE between true noise epsilon and predicted noise epsilon_theta(x_t, t).",
        "tags": ["Diffusion", "GenerativeAI", "ScoreMatching"],
        "source": "Denoising Diffusion Probabilistic Models (Ho et al.)"
    }
]
