"""Curriculum definitions for 3D Vision Foundation Models, DINOv2 Latent Representations, and Visual-Inertial Odometry (VIO)."""

VISION_SESSIONS = [
    {
        "session_num": 1,
        "slug": "session-01-foundations-of-metric-3d-reconstruction",
        "title": "Session 1: Foundations of Metric 3D Reconstruction & Multi-View Geometry",
        "instructors": "Prof. Davide Scaramuzza, Prof. Luca Carlone",
        "summary": "Pinhole camera models, epipolar geometry, essential matrix estimation, triangulation, and bundle adjustment.",
        "content": """### Lecture Objectives
1. Formulate projective camera geometry and coordinate transformations from world to camera frames.
2. Derive the Epipolar Constraint: $x_2^T K^{-T} E K^{-1} x_1 = 0$ where $E = [t]_\\times R$.
3. Analyze the 5-point and 8-point algorithms for relative pose recovery and metric scale ambiguity.
4. Understand Nonlinear Least Squares Bundle Adjustment minimizing reprojection error:
$$\\min_{\\{T_i\\}, \\{X_j\\}} \\sum_{i,j} \\| x_{ij} - \\pi(T_i, X_j) \\|_{\\Sigma}^2$$

### Recommended Literature & Syllabus Links
- ETH Zurich / UZH Vision Algorithms for Mobile Robotics (Lecture 3 & 4).
- Hartley & Zisserman, *Multiple View Geometry in Computer Vision*.
- Related concepts: [[concepts/mapanything-feedforward-metric-3d]], [[differentials/mapanything-feedforward-vs-classical-sfm]]."""
    },
    {
        "session_num": 2,
        "slug": "session-02-feedforward-3d-foundation-models-dust3r-and-mapanything",
        "title": "Session 2: Feed-Forward 3D Foundation Models: DUSt3R, MASt3R & MapAnything",
        "instructors": "Meta Reality Labs & Carnegie Mellon University",
        "summary": "Paradigm shift from iterative optimization to feed-forward regression of point maps, ray maps, and metric scale.",
        "content": """### Lecture Objectives
1. Understand the limitations of classical SfM pipelines (feature detection, matching, RANSAC, incremental bundle adjustment).
2. Examine **DUSt3R** (CVPR 2024): Regression of 3D pointmaps directly in camera space without explicit intrinsics.
3. Deep-dive into **MapAnything** (Meta Reality Labs & CMU, 2025/2026):
   - Factored representation: Depth maps $D$, local ray maps $R$, camera poses $T$, and global metric scale factor $S$.
   - Universal unification: Single transformer solving 12+ tasks (SfM, MVS, monocular depth, camera localization, depth completion).
   - Feed-forward inference: Dense metric 3D point clouds in $<500\\text{ms}$ without test-time optimization.

### Key References
- MapAnything: Universal Feed-Forward Metric 3D Reconstruction (arXiv:2509.13414).
- Related entities: [[entities/mapanything-model]], [[entities/dust3r]]."""
    },
    {
        "session_num": 3,
        "slug": "session-03-dinov2-self-supervised-features-and-latent-manifolds",
        "title": "Session 3: DINOv2: Self-Supervised Vision Representations & Latent Space Geometry",
        "instructors": "Meta AI Research",
        "summary": "Self-distillation without labels, patch tokens vs [CLS], emergent geometric alignment, and dense correspondence.",
        "content": """### Lecture Objectives
1. Analyze self-supervised Vision Transformers trained with DINOv2 objective: cross-entropy loss between student and teacher network output distributions with centering and sharpening.
2. Contrast global representations (`[CLS]` token) against dense spatial patch embeddings ($z_i \\in \\mathbb{R}^D$).
3. Explore the latent manifold metric structure: Points sharing semantic and geometric identity cluster tightly under cosine similarity:
$$\\text{sim}(z_A, z_B) = \\frac{z_A \\cdot z_B}{\\|z_A\\| \\|z_B\\|}$$
4. Observe emergent multi-view correspondence: DINOv2 features align across wide baselines, lighting variations, and non-rigid deformations without explicit multi-view training.

### Key References
- DINOv2: Learning Robust Visual Features without Supervision (Oquab et al., Meta AI, TMLR 2023).
- Related concepts: [[concepts/dinov2-dense-latent-space-geometry]], [[differentials/vit-patch-tokens-vs-cls-token]]."""
    },
    {
        "session_num": 4,
        "slug": "session-04-3d-feature-fields-and-latent-world-models",
        "title": "Session 4: 3D Feature Fields, Gaussian Splatting & Latent World Models",
        "instructors": "MIT, CMU & Berkeley AI Research",
        "summary": "Distilling 2D DINOv2/CLIP latents into 3D Gaussians (LangSplat), open-set mapping (ConceptFusion), and DINO-WM.",
        "content": """### Lecture Objectives
1. **3D Feature Fields**: Extending 3D scene representations (NeRF and 3D Gaussian Splatting) from RGB to dense feature embeddings.
2. **ConceptFusion** (Jatavallabhula et al., MIT, RSS 2023): Pixel-aligned multimodal mapping fusing DINOv2 geometric latents with CLIP semantic language features.
3. **DINO-WM** (ICML 2024): DINO World Models for visual dynamics and zero-shot robot planning:
   - Operating completely within frozen DINOv2 latent patch space without expensive pixel-level decoding.
   - Autoregressive transition models predicting future latent states $z_{t+1} = f(z_t, a_t)$.

### Key References
- DINO-WM: DINO World Model for Visual Navigation (ICML 2024).
- Related concepts: [[concepts/dino-world-models-and-latent-planning]], [[concepts/3d-gaussian-splatting-and-feature-fields]]."""
    },
    {
        "session_num": 5,
        "slug": "session-05-visual-inertial-odometry-and-imu-preintegration",
        "title": "Session 5: Visual-Inertial Odometry (VIO) & IMU Preintegration on SO(3) Manifolds",
        "instructors": "Prof. Luca Carlone (MIT SPARK Lab)",
        "summary": "Lie algebra, IMU measurement kinematics, on-manifold preintegration, and bias covariance propagation.",
        "content": """### Lecture Objectives
1. Review rotation representations on the Special Orthogonal Group $SO(3)$ and Lie algebra $\\mathfrak{so}(3)$.
2. Explain why naive numerical integration of high-rate IMU accelerations and angular velocities drifts and requires re-evaluating state history during nonlinear optimization.
3. Formulate **IMU Preintegration** on manifolds (Forster et al., Carlone et al., IEEE T-RO):
$$\\Delta R_{ij} = \\prod_{k=i}^{j-1} \\text{Exp}\\left((\\tilde{\\omega}_k - b_{g,i})\\Delta t\\right)$$
4. Derive first-order linear updates for bias shifts $\\Delta R_{ij}(b_{g,i} + \\delta b_g) \\approx \\Delta R_{ij}(b_{g,i}) \\text{Exp}(J_{R}^{b_g} \\delta b_g)$.

### Key References
- MIT 16.485 Visual Navigation for Autonomous Vehicles (VNAV), Lecture 11-13.
- Forster et al., *On-Manifold Preintegration for Real-Time Visual-Inertial Odometry*.
- Related concepts: [[concepts/imu-preintegration-on-so3-manifolds]], [[exam_traps/naive-euler-imu-integration-drift]]."""
    },
    {
        "session_num": 6,
        "slug": "session-06-optimization-vs-filtering-vins-mono-and-msckf",
        "title": "Session 6: VIO Architectures: Sliding-Window Optimization (VINS-Mono) vs. Filtering (MSCKF)",
        "instructors": "Prof. Davide Scaramuzza, Prof. Shaojie Shen",
        "summary": "State estimation paradigms: EKF multi-state constraint filter vs factor graphs, Schur complement marginalization, and DROID-SLAM.",
        "content": """### Lecture Objectives
1. Compare filter-based state estimation (**MSCKF**) with optimization-based sliding window estimators (**VINS-Mono**, **OKVIS**).
2. Understand Marginalization via the **Schur Complement**: Retaining historical measurement constraints while bounding computational complexity.
3. Analyze observability properties in VIO: Absolute position and yaw are unobservable under gravity, while 4 degrees of freedom are gauge freedoms.
4. Examine Deep Learning visual SLAM (**DROID-SLAM**): Differentiable recurrent iterative bundle adjustment layers operating on optical flow correlation volumes.

### Key References
- Mourikis & Roumeliotis, *A Multi-State Constraint Kalman Filter for Vision-aided Inertial Navigation* (ICRA 2007).
- Qin, Li, Shen, *VINS-Mono: A Robust and Versatile Monocular Visual-Inertial State Estimator* (IEEE T-RO 2018).
- Teed & Deng, *DROID-SLAM: Deep Visual SLAM for Monocular, Stereo, and RGB-D Cameras* (NeurIPS 2021).
- Related differentials: [[differentials/sliding-window-vins-vs-filtering-msckf]]."""
    }
]

VISION_CONCEPTS = [
    {
        "slug": "mapanything-feedforward-metric-3d",
        "title": "MapAnything: Universal Metric 3D Reconstruction Foundation Model",
        "domain": "Computer Science",
        "field": "3D Computer Vision & Robotics",
        "course": "MIT 16.485 / Vision & Robotics",
        "tags": ["3d-reconstruction", "foundation-models", "mapping", "mapanything", "transformer"],
        "summary": "A unified transformer-based foundation model for metric 3D scene reconstruction from heterogeneous camera inputs.",
        "content": """### Theoretical Overview
Traditional 3D reconstruction requires distinct algorithms for Structure-from-Motion (SfM), Multi-View Stereo (MVS), monocular depth estimation, camera relocalization, and depth completion. **MapAnything** (Meta Reality Labs & Carnegie Mellon University, 2025/2026) unifies over 12 tasks into a single feed-forward transformer without test-time bundle adjustment.

### Factored Geometric Representation
MapAnything models multi-view scenes by factoring the 3D geometry into:
1. **Per-View Depth Maps** $D_i(u, v)$: Dense metric distance along optical rays.
2. **Local Ray Maps** $R_i(u, v)$: Unit direction vectors characterizing camera optical geometries.
3. **Relative Camera Poses** $T_i \\in SE(3)$: 6-DoF transformations between viewpoint coordinate frames.
4. **Global Metric Scale Factor** $S \\in \\mathbb{R}^+$: Upgrades arbitrary uncalibrated scenes into globally metric meters.

```
Input Images (1..N) ────► [ ViT Encoder Backbone ]
                                │
                          [ Cross-View Attention ]
                                │
       ┌────────────────────────┼────────────────────────┐
       ▼                        ▼                        ▼
[ Depth Maps D_i ]     [ Ray Maps R_i ]         [ Poses T_i ∈ SE(3) ]
       │                        │                        │
       └────────────────────────┼────────────────────────┘
                                ▼
         Global Metric Point Cloud P = S · T_i · (D_i · R_i)
```

### Advantages Over Iterative Pipelines
- **Single Feed-Forward Pass**: Bypasses costly iterative non-linear optimization (Levenberg-Marquardt) and RANSAC matching.
- **Heterogeneous Inputs**: Ingests mono images, stereo pairs, sparse video frames, or partial depth maps seamlessly.
- **Zero Drift in Wide Baselines**: Cross-attention resolves extreme viewpoint shifts where classical local descriptors fail.

Related: [[entities/mapanything-model]], [[differentials/mapanything-feedforward-vs-classical-sfm]]."""
    },
    {
        "slug": "dinov2-dense-latent-space-geometry",
        "title": "DINOv2 Latent Space: Dense Feature Manifolds & Geometric Alignment",
        "domain": "Computer Science",
        "field": "Deep Learning & Representation Learning",
        "course": "MIT 16.485 / Vision & Robotics",
        "tags": ["dinov2", "latent-space", "dense-features", "self-supervised-learning", "vit"],
        "summary": "Properties of self-supervised Vision Transformer latent representations and their dense geometric correspondence manifolds.",
        "content": """### Latent Space Architecture
DINOv2 (Oquab et al., Meta AI, 2023) is a self-supervised Vision Transformer trained with student-teacher self-distillation on 142M images. Unlike language-supervised models (CLIP), DINOv2 generates an exceptionally rich **dense per-pixel feature space**.

### Spatial Patch Embeddings vs Global `[CLS]`
When an image $I \\in \\mathbb{R}^{H \\times W \\times 3}$ is partitioned into patches of size $p \\times p$:
- The `[CLS]` token produces a global classification vector $z_{\\text{cls}} \\in \\mathbb{R}^D$.
- The output tokens $Z_{\\text{patch}} = \\{z_1, z_2, \\dots, z_{N}\\} \\in \\mathbb{R}^{\\frac{H}{p} \\times \\frac{W}{p} \\times D}$ form a spatially grounded latent tensor.

```
Image Grid:                Patch Latent Manifold (D=1024):
┌───┬───┬───┐              ┌───────────────┐
│ 1 │ 2 │ 3 │   Vision     │  z₁   z₂   z₃ │  Cosine Similarity
├───┼───┼───┤ Transformer  │  z₄   z₅   z₆ │  sim(z_i, z_j) > 0.85
│ 4 │ 5 │ 6 │ ───────────► │  z₇   z₈   z₉ │  for corresponding 3D points
└───┴───┴───┘              └───────────────┘
```

### Emergent Properties in 3D Vision
1. **Zero-Shot Point Matching**: Two pixels $p_A$ and $p_B$ in different camera views observing the same 3D physical surface exhibit peak cosine similarity in feature space:
$$\\arg\\max_{p_B} \\frac{z(p_A) \\cdot z(p_B)}{\\|z(p_A)\\| \\|z(p_B)\\|}$$
2. **Smooth Feature Manifolds**: Semantic and geometric transitions across object surfaces are continuous and differentiable, enabling downstream decoders (depth, normals, segmentation) to train with frozen backbones.

Related: [[entities/dinov2-backbone]], [[differentials/vit-patch-tokens-vs-cls-token]]."""
    },
    {
        "slug": "imu-preintegration-on-so3-manifolds",
        "title": "IMU Preintegration on SO(3) Manifolds",
        "domain": "Engineering",
        "field": "Robotics & State Estimation",
        "course": "MIT 16.485 / Visual Navigation",
        "tags": ["vio", "imu-preintegration", "so3", "lie-algebra", "robotics"],
        "summary": "Mathematical derivation of on-manifold IMU preintegration to eliminate trajectory re-propagation in visual-inertial optimization.",
        "content": """### The Fundamental Problem of IMU Integration
An Inertial Measurement Unit (IMU) measures angular velocity $\\tilde{\\omega}_t = \\omega_t + b_{g,t} + \\eta_g$ and linear acceleration $\\tilde{a}_t = R_t^T(a_t - g) + b_{a,t} + \\eta_a$ at high frequencies (100–1000 Hz).
In standard integration, computing pose $R_j$ from $R_i$ depends explicitly on the initial orientation $R_i$:
$$R_j = R_i \\prod_{k=i}^{j-1} \\text{Exp}\\left((\\tilde{\\omega}_k - b_{g,k})\\Delta t\\right)$$

If the estimate of $R_i$ changes during nonlinear graph optimization, all intermediate IMU states between frame $i$ and $j$ must be numerically re-integrated, which is computationally prohibitive.

### Forster's On-Manifold Preintegration Solution
Forster et al. define the **relative preintegrated motion delta** isolated in the local coordinate frame of body $i$:
$$\\Delta R_{ij} \\triangleq R_i^T R_j = \\prod_{k=i}^{j-1} \\text{Exp}\\left((\\tilde{\\omega}_k - b_{g,i})\\Delta t\\right)$$
$$\\Delta v_{ij} \\triangleq R_i^T (v_j - v_i - g\\Delta t_{ij}) = \\sum_{k=i}^{j-1} \\Delta R_{ik} (\\tilde{a}_k - b_{a,i})\\Delta t$$
$$\\Delta p_{ij} \\triangleq R_i^T \\left(p_j - p_i - v_i \\Delta t_{ij} - \\frac{1}{2}g\\Delta t_{ij}^2\\right) = \\sum_{k=i}^{j-1} \\left[ \\Delta v_{ik}\\Delta t + \\frac{1}{2}\\Delta R_{ik}(\\tilde{a}_k - b_{a,i})\\Delta t^2 \\right]$$

### First-Order Bias Updates
When biases $b_{g,i}, b_{a,i}$ update by small increments $\\delta b$, preintegration is adjusted analytically without numerical loops using precomputed Jacobians:
$$\\Delta R_{ij}(b_{g,i} + \\delta b_g) \\approx \\Delta R_{ij}(b_{g,i}) \\text{Exp}\\left(J_{R}^{b_g} \\delta b_g\\right)$$

Related: [[entities/vins-mono]], [[exam_traps/naive-euler-imu-integration-drift]]."""
    },
    {
        "slug": "visual-inertial-state-estimation-and-marginalization",
        "title": "Visual-Inertial State Estimation & Schur Complement Marginalization",
        "domain": "Engineering",
        "field": "Robotics & State Estimation",
        "course": "MIT 16.485 / Visual Navigation",
        "tags": ["state-estimation", "factor-graphs", "marginalization", "schur-complement", "vins"],
        "summary": "Formulation of maximum-a-posteriori sliding window state estimation and information retention via the Schur complement.",
        "content": """### Maximum A Posteriori (MAP) Formulation
In Visual-Inertial Odometry, the full state vector over a sliding window of $N$ camera frames is:
$$\\mathcal{X} = \\left[ x_0, x_1, \\dots, x_N, \\lambda_0, \\lambda_1, \\dots, \\lambda_M \\right]$$
where $x_k = [p_k, v_k, R_k, b_{a,k}, b_{g,k}]$ and $\\lambda_l$ are visual feature inverse depths.

The MAP problem minimizes the sum of prior, IMU, and visual reprojection residuals:
$$\\min_{\\mathcal{X}} \\left\\{ \\| r_p - H_p \\mathcal{X} \\|^2 + \\sum_{k \\in \\mathcal{B}} \\| r_B(z_{k+1}^k, \\mathcal{X}) \\|_{P_{k+1}^k}^2 + \\sum_{(l,j) \\in \\mathcal{C}} \\| r_C(z_l^j, \\mathcal{X}) \\|_{P_l^j}^2 \\right\\}$$

### Marginalization via the Schur Complement
To maintain real-time performance, old states $x_m$ are removed from the active window while preserving their geometric constraints.
Partitioning the linearized normal equations $H \\delta \\mathcal{X} = b$:
$$\\begin{bmatrix} H_{mm} & H_{mr} \\\\ H_{rm} & H_{rr} \\end{bmatrix} \\begin{bmatrix} \\delta x_m \\\\ \\delta x_r \\end{bmatrix} = \\begin{bmatrix} b_m \\\\ b_r \\end{bmatrix}$$

Eliminating the marginalized state $\\delta x_m$ produces the Schur Complement on the remaining states $\\delta x_r$:
$$H_{\\text{prior}} = H_{rr} - H_{rm} H_{mm}^{-1} H_{mr}$$
$$b_{\\text{prior}} = b_r - H_{rm} H_{mm}^{-1} b_m$$

This Schur complement converts historical measurements into an exact Gaussian prior on remaining states.

Related: [[entities/gtsam-factor-graph]], [[differentials/sliding-window-vins-vs-filtering-msckf]]."""
    },
    {
        "slug": "dino-world-models-and-latent-planning",
        "title": "DINO World Models (DINO-WM): Latent-Space Dynamics & Robot Planning",
        "domain": "Computer Science",
        "field": "Deep Learning & Robotics",
        "course": "MIT 16.485 / Vision & Robotics",
        "tags": ["dino-wm", "world-models", "latent-space", "robotics", "planning"],
        "summary": "Operating visual dynamics and predictive planning directly within frozen DINOv2 latent space without pixel decoding.",
        "content": """### Motivation: Bypassing Pixel-Level Reconstruction
Traditional visual world models (e.g., Dreamer, Sora-style simulators) reconstruct RGB pixels via autoencoders or diffusion models. This introduces severe computational bottlenecks, blurriness, and sensitivity to task-irrelevant visual distractors (background foliage, lighting shifts).

### DINO-WM Architecture
**DINO-WM** (ICML 2024) models visual dynamics **entirely in the latent representation space of DINOv2**:

```
Observations O_t ──► [ Frozen DINOv2 Encoder ] ──► Latent State z_t
                                                          │
Control Action a_t ───────────────────────────────────────┤
                                                          ▼
                                              [ Autoregressive ViT ]
                                                          │
                                                          ▼
                                                Predicted Latent z_{t+1}
```

### Zero-Shot Model Predictive Control (MPC)
Because DINOv2 spatial features encode object boundaries and semantic affordances:
1. The user specifies a goal image $O_{\\text{goal}}$.
2. The frozen encoder computes goal latent embedding $z_{\\text{goal}}$.
3. The robot optimizes action sequences $[a_t, a_{t+1}, \\dots, a_{t+H}]$ minimizing the latent cosine distance:
$$\\mathcal{L}_{\\text{plan}} = \\| z_{t+H} - z_{\\text{goal}} \\|_2^2$$
No pixels are ever rendered during planning, enabling 100 Hz search over complex multi-particle manipulation and navigation trajectories.

Related: [[concepts/dinov2-dense-latent-space-geometry]], [[entities/dinov2-backbone]]."""
    },
    {
        "slug": "3d-gaussian-splatting-and-feature-fields",
        "title": "3D Gaussian Splatting & Distilled Feature Fields (LangSplat, ConceptFusion)",
        "domain": "Computer Science",
        "field": "3D Computer Vision",
        "course": "MIT 16.485 / Vision & Robotics",
        "tags": ["3dgs", "gaussian-splatting", "feature-fields", "conceptfusion", "langsplat"],
        "summary": "Explicit point-based 3D scene representation with volumetric rendering of RGB and distilled semantic feature embeddings.",
        "content": """### Mathematical Formulation of 3D Gaussians
A 3D Gaussian is parameterized by its world center $\\mu \\in \\mathbb{R}^3$, an opacity $\\alpha \\in [0, 1]$, and a 3D covariance matrix $\\Sigma \\in \\mathbb{S}_{++}^3$ decomposed into scaling $S$ and rotation quaternion $R$:
$$\\Sigma = R S S^T R^T$$
$$G(x) = \\exp\\left(-\\frac{1}{2}(x - \\mu)^T \\Sigma^{-1} (x - \\mu)\\right)$$

### Splatting Feature Fields
In standard 3DGS, each Gaussian carries spherical harmonics coefficients for view-dependent color $C$. In **Feature Splatting** and **LangSplat**, each Gaussian also stores a distilled latent vector $f_i \\in \\mathbb{R}^d$ corresponding to DINOv2 or CLIP embeddings:
$$F(p) = \\sum_{i \\in \\mathcal{N}} f_i \\alpha_i G_i^{\\text{2D}}(p) \\prod_{j=1}^{i-1}(1 - \\alpha_j G_j^{\\text{2D}}(p))$$

### Open-Set Multimodal Querying
Projecting rendered dense feature maps $F(p)$ against text prompts $\\text{CLIP}(\\text{\"red fire extinguisher\"})$ permits sub-millisecond open-vocabulary 3D semantic segmentation and robotic affordance extraction.

Related: [[differentials/3d-gaussian-splatting-vs-neural-radiance-fields]], [[entities/conceptfusion]]."""
    }
]

VISION_ENTITIES = [
    {
        "slug": "mapanything-model",
        "title": "MapAnything Model",
        "domain": "Computer Science",
        "category": "3D Foundation Model",
        "course": "3D Vision",
        "summary": "Universal feed-forward metric 3D scene reconstruction transformer by Meta Reality Labs and CMU.",
        "content": """**Architecture**: Vision Transformer backbone with cross-view cross-attention blocks.  
**Key Capability**: Predicts depth maps, ray maps, 6-DoF camera poses, and global metric scale in a single feed-forward pass across 12+ tasks."""
    },
    {
        "slug": "dinov2-backbone",
        "title": "DINOv2 Vision Transformer Backbone",
        "domain": "Computer Science",
        "category": "Self-Supervised Model",
        "course": "Deep Learning",
        "summary": "Meta AI's self-supervised ViT producing dense spatial patch embeddings for geometry and semantics.",
        "content": """**Models**: ViT-S/14, ViT-B/14, ViT-L/14, ViT-g/14 with registers.  
**Primary Utility**: Backbone for dense correspondence, zero-shot depth estimation, and latent world modeling."""
    },
    {
        "slug": "vins-mono",
        "title": "VINS-Mono State Estimator",
        "domain": "Engineering",
        "category": "VIO System",
        "course": "Robotics",
        "summary": "Real-time monocular visual-inertial state estimator by HKUST using sliding-window non-linear optimization.",
        "content": """**Features**: IMU preintegration, visual-inertial initialization, loop closure with 4-DoF pose graph optimization, Schur complement marginalization."""
    },
    {
        "slug": "msckf",
        "title": "Multi-State Constraint Kalman Filter (MSCKF)",
        "domain": "Engineering",
        "category": "Filter-based VIO",
        "course": "Robotics",
        "summary": "Landmark EKF-based visual-inertial odometry filter eliminating 3D landmark positions from state vector.",
        "content": """**Pioneered By**: Mourikis & Roumeliotis (ICRA 2007).  
**Key Trick**: Projects visual reprojection residuals onto the nullspace of the landmark Jacobian, bounding computational cost."""
    },
    {
        "slug": "dust3r",
        "title": "DUSt3R 3D Pointmap Regressor",
        "domain": "Computer Science",
        "category": "3D Vision Model",
        "course": "3D Vision",
        "summary": "NAVER LABS Europe model reformulating multi-view stereo directly as regression of 3D pointmaps.",
        "content": """**Breakthrough**: Eliminates calibration, epipolar rectification, and manual feature matching."""
    },
    {
        "slug": "droid-slam",
        "title": "DROID-SLAM",
        "domain": "Computer Science",
        "category": "Deep Visual SLAM",
        "course": "3D Vision & SLAM",
        "summary": "End-to-end differentiable deep visual SLAM system using recurrent iterative bundle adjustment.",
        "content": """**Authors**: Teed & Deng (NeurIPS 2021).  
**Core Mechanism**: RAFT-inspired correlation pyramids and differentiable Dense Bundle Adjustment (DBA) update layers."""
    },
    {
        "slug": "gtsam-factor-graph",
        "title": "GTSAM (Georgia Tech Smoothing and Mapping)",
        "domain": "Engineering",
        "category": "Optimization Framework",
        "course": "Robotics",
        "summary": "C++ library implementing factor graphs and non-linear optimization algorithms (iSAM2, Levenberg-Marquardt).",
        "content": """**Utility**: Industry and academic standard for sensor fusion, visual-inertial odometry, and SLAM backends."""
    },
    {
        "slug": "conceptfusion",
        "title": "ConceptFusion",
        "domain": "Computer Science",
        "category": "Multimodal 3D Mapping",
        "course": "3D Vision & Robotics",
        "summary": "Open-set multimodal 3D mapping fusing DINO visual features and CLIP language embeddings.",
        "content": """**Pioneered By**: Krishna Murthy Jatavallabhula et al. (MIT, RSS 2023).  
**Capability**: Zero-shot semantic 3D querying from natural language, audio, and images."""
    }
]

VISION_DIFFERENTIALS = [
    {
        "slug": "mapanything-feedforward-vs-classical-sfm",
        "title": "Feed-Forward 3D Foundation Models (MapAnything) vs. Classical Structure-from-Motion (COLMAP)",
        "domain": "Computer Science",
        "summary": "Comparing modern feed-forward transformer 3D reconstruction against classical feature matching and bundle adjustment.",
        "content": """| Dimension | MapAnything / DUSt3R | Classical SfM (COLMAP) |
|---|---|---|
| **Architecture** | Feed-forward Vision Transformer | Pipeline: SIFT + RANSAC + Incremental BA |
| **Inference Speed** | Real-time / Sub-second (<500ms) | Minutes to hours for multi-view scenes |
| **Calibration Requirement** | Calibration-free (estimates rays & metric scale) | Requires known intrinsics or EXIF focal length |
| **Failure Modes** | Hallucinated geometry on untextured regions | Tracking loss on low-texture or wide-baseline pairs |
| **Metric Scale** | Directly predicted metric scale factor $S$ | Scale-ambiguous without ground-truth distance |
| **Differentiability** | Fully end-to-end differentiable | Non-differentiable discrete matching steps |"""
    },
    {
        "slug": "vit-patch-tokens-vs-cls-token",
        "title": "ViT Spatial Patch Tokens vs. Global [CLS] Token in Latent Spaces",
        "domain": "Computer Science",
        "summary": "Trade-offs between localized dense representations and global semantic abstraction in self-supervised ViTs.",
        "content": """| Feature | Spatial Patch Tokens $z_{\\text{patch}}$ | Global `[CLS]` Token $z_{\\text{cls}}$ |
|---|---|---|
| **Dimensionality** | $\\frac{H}{p} \\times \\frac{W}{p} \\times D$ (spatial tensor) | $1 \\times D$ (single vector) |
| **Primary Utility** | Dense correspondence, depth, segmentation, 3DGS | Image retrieval, zero-shot classification |
| **Geometric Retention** | Retains spatial coordinates and local topology | Discards coordinate layout for invariance |
| **Cosine Behavior** | Peaks on corresponding physical surface points | Peaks on images sharing holistic semantic category |
| **Memory Footprint** | Heavy ($O(N \\times D)$ per image) | Lightweight ($O(D)$ per image) |"""
    },
    {
        "slug": "sliding-window-vins-vs-filtering-msckf",
        "title": "Sliding-Window Optimization (VINS-Mono) vs. Extended Kalman Filtering (MSCKF)",
        "domain": "Engineering",
        "summary": "Comparing non-linear factor graph optimization against multi-state constraint Kalman filtering for VIO.",
        "content": """| Feature | Optimization-based (VINS-Mono, OKVIS) | Filter-based (MSCKF, OpenVINS) |
|---|---|---|
| **Mathematical Approach** | Iterative batch non-linear least squares | Extended Kalman Filter (EKF) state updates |
| **Relinearization** | Relinerarizes past states over sliding window | Evaluates Jacobians once at state arrival (cannot relinearize) |
| **Accuracy** | Higher (typically 2-3x lower drift) | Moderate (prone to linearization errors) |
| **Computational Cost** | High (solves $H \\delta x = b$ iteratively) | Extremely low (suitable for micro-controllers/drones) |
| **Marginalization** | Exact via Schur complement | Implicit via measurement update and camera drop |
| **Loop Closure** | Seamless pose-graph integration | Requires complex external graph manager |"""
    },
    {
        "slug": "deep-recurrent-slam-vs-classical-feature-vio",
        "title": "Deep Recurrent Visual SLAM (DROID-SLAM) vs. Classical Feature-based VIO",
        "domain": "Computer Science & Engineering",
        "summary": "Contrasting learned dense bundle adjustment networks against classical sparse feature trackers.",
        "content": """| Dimension | Learned SLAM (DROID-SLAM) | Classical Feature VIO (ORB-SLAM3 / VINS) |
|---|---|---|
| **Front-End** | Dense correlation volume from deep features | Sparse corner detection (FAST/ORB) + KLT |
| **Robustness to Blur/Lighting** | Extremely high (robust to motion blur) | Fragile (feature tracking easily lost in low light) |
| **Compute Hardware** | Requires modern GPU / NPU acceleration | Runs on standard single-core CPU |
| **Scale Drift** | Virtually zero on stereo/RGB-D; robust on mono | Monocular scale accumulates drift over trajectories |
| **Interpretability** | Black-box weights + differentiable layer | Explicit covariance matrices and error bounds |"""
    },
    {
        "slug": "3d-gaussian-splatting-vs-neural-radiance-fields",
        "title": "3D Gaussian Splatting (3DGS) vs. Neural Radiance Fields (NeRF)",
        "domain": "Computer Science",
        "summary": "Comparing explicit 3D Gaussian primitive rendering against implicit continuous neural volumetric representations.",
        "content": """| Attribute | 3D Gaussian Splatting | Neural Radiance Fields (NeRF) |
|---|---|---|
| **Representation** | Explicit point cloud of anisotropic Gaussians | Implicit continuous coordinate MLP $F_\\theta(x, d)$ |
| **Rendering Algorithm** | Tile-based rasterization ($\alpha$-blending) | Volumetric ray marching with quadrature |
| **Rendering Speed** | Real-time (>100 FPS at 1080p) | Slow (<1 to 15 FPS without specialized grids) |
| **Training Duration** | Fast (15–30 minutes) | Moderate to Slow (hours to days) |
| **Feature Embedding** | Direct storage of latent vectors per Gaussian | Requires high-dimensional feature MLP branch |
| **Editing & Dynamic Control** | Trivial (translate, scale, delete Gaussians) | Hard (requires deformation networks or retraining) |"""
    }
]

VISION_TRAPS = [
    {
        "slug": "naive-euler-imu-integration-drift",
        "title": "Engineering Trap: Naive Global-Frame IMU Numerical Integration",
        "domain": "Engineering",
        "system": "Visual-Inertial Navigation",
        "course": "MIT 16.485",
        "summary": "Why naive forward Euler integration of raw IMU measurements causes explosive quadratic drift in trajectory estimation.",
        "content": """### The Anti-Pattern
A developer integrates raw accelerometer $\\tilde{a}_t$ and gyroscope $\\tilde{\\omega}_t$ readings directly in world coordinates:
$$v_{t+1} = v_t + (R_t \\tilde{a}_t + g)\\Delta t$$
$$p_{t+1} = p_t + v_t \\Delta t + \\frac{1}{2}(R_t \\tilde{a}_t + g)\\Delta t^2$$

### Why It Fails Catastrophically
1. **Uncorrected Gyroscope Bias**: Accelerometer measurements must be rotated by $R_t$. If gyroscope bias induces a 1° angular orientation error, the rotated gravity vector $R_t^T g$ projects false acceleration into horizontal components:
$$a_{\\text{false}} \\approx g \\cdot \\sin(1^\\circ) \\approx 0.17 \\text{ m/s}^2$$
2. **Double Integration Drift**: In 10 seconds, this slight angular misalignment causes position error:
$$\\Delta p = \\frac{1}{2}(0.17)(10)^2 = 8.5 \\text{ meters!}$$
3. **Graph Optimization Invalidation**: Whenever the optimization changes the orientation estimate $R_0$, all subsequent integrated positions become completely invalid unless **On-Manifold IMU Preintegration** is utilized."""
    },
    {
        "slug": "scale-ambiguity-in-monocular-vision",
        "title": "Engineering Trap: Monocular Metric Scale Ambiguity & Hallucination",
        "domain": "Computer Science",
        "system": "3D Reconstruction",
        "course": "3D Vision",
        "summary": "The physical impossibility of resolving absolute metric scale from monocular RGB without inertial or depth baselines.",
        "content": """### The Anti-Pattern
Relying on monocular feed-forward depth estimation to determine absolute metric clearance for autonomous drone or robot navigation.

### The Physics Constraint
In pure monocular pinhole optics, an object of size $S$ at distance $Z$ generates an identical image projection as an object of size $2S$ at distance $2Z$:
$$x = f \\frac{X}{Z}$$
Without an explicit metric baseline (stereo baseline $B$, known camera height, or accelerometer gravity scale $g = 9.81 \\text{ m/s}^2$), monocular models only infer **relative projective depth**. Even foundation models (MapAnything, DUSt3R) rely on statistical size priors of familiar objects, which fail catastrophically in non-canonical environments."""
    },
    {
        "slug": "yaw-unobservability-under-constant-acceleration",
        "title": "Engineering Trap: Unobservable Yaw and Gyro Bias Under Constant Acceleration",
        "domain": "Engineering",
        "system": "Visual-Inertial Navigation",
        "course": "MIT 16.485",
        "summary": "Degenerate motion profiles in VIO where yaw orientation and accelerometer biases become mathematically indistinguishable.",
        "content": """### The Degenerate Motion
A quadrotor or autonomous vehicle moves at constant velocity or under zero linear acceleration (hovering).

### Mathematical Degeneracy
In Visual-Inertial Odometry, the system has **4 unobservable directions**:
- 3 degrees of freedom: Absolute 3D position in the world frame ($x, y, z$).
- 1 degree of freedom: Rotation around the gravity vector (**Yaw**).

Under zero angular motion and constant velocity, the accelerometer only senses pure gravity $g$. Any rotation around the gravity vector produces identical accelerometer readouts and identical visual relative motions, causing the estimator covariance for yaw to explode unless magnetometer, GPS, or active angular excitation maneuvers are performed."""
    },
    {
        "slug": "uncalibrated-feature-drift-in-dino-embeddings",
        "title": "Engineering Trap: 'Slow Feature' Drift in DINOv2 Latent World Models",
        "domain": "Computer Science",
        "system": "Latent Representation Learning",
        "course": "Deep Learning",
        "summary": "Sensitivity of self-supervised patch tokens to task-irrelevant environmental changes during predictive planning.",
        "content": """### The Failure Mode
In DINO World Models (DINO-WM), an agent optimizes actions to match a target latent state $z_{\\text{goal}}$. 
However, DINOv2 spatial features are sensitive to **\"slow features\"**—gradual visual shifts in background lighting, shadow movement, or incidental object textures.

### Consequences
The Model Predictive Control (MPC) optimizer may discover actions that alter camera exposure or background shadows to minimize latent MSE loss, while failing to execute the primary physical task (e.g. pushing an object). Robust latent world models require bisimulation metrics or contrastive masking to separate task-salient latents from visual distractors."""
    },
    {
        "slug": "covariance-underestimation-in-visual-filtering",
        "title": "Engineering Trap: Inconsistent Covariance & Filter Divergence in EKF-VIO",
        "domain": "Engineering",
        "system": "Visual-Inertial Navigation",
        "course": "Robotics",
        "summary": "Spurious information gain caused by evaluating Jacobians at changing state estimates in standard EKF frameworks.",
        "content": """### The Inconsistency Mechanism
In an ideal estimator, the observability matrix for unobservable dimensions (yaw around gravity) must have a nullspace.
In standard Extended Kalman Filters (EKF), the state estimate changes between propagation and update. Evaluating Jacobians $H$ at the current state estimate rather than a fixed linearization point introduces **spurious information** along the unobservable yaw axis:
- The filter falsely believes yaw uncertainty is decreasing.
- The filter becomes overconfident, ignores real visual measurements, and eventually diverges.

**The Solution**: First-Estimates Jacobian (FEJ) estimators or on-manifold sliding window optimization (VINS-Mono)."""
    }
]

VISION_FLASHCARDS = [
    {
        "type": "cloze",
        "text": "MapAnything replaces classical multi-step Structure-from-Motion by predicting {{c1::depth maps}}, {{c2::local ray maps}}, {{c3::camera poses}}, and a global metric scale factor in a {{c4::single feed-forward pass}}.",
        "pearl": "MapAnything (Meta Reality Labs & CMU) unifies 12+ 3D reconstruction tasks without requiring test-time bundle adjustment.",
        "tags": ["PaideiaGenesis", "3D-Vision", "MapAnything", "Foundation-Models"],
        "source": "concepts/mapanything-feedforward-metric-3d"
    },
    {
        "type": "cloze",
        "text": "In self-supervised Vision Transformers (DINOv2), dense cross-view point correspondences are extracted from {{c1::spatial patch tokens}} rather than the {{c2::global [CLS] token}} using {{c3::cosine similarity}}.",
        "pearl": "DINOv2 patch tokens exhibit emergent geometric correspondence across wide baselines without explicit multi-view supervision.",
        "tags": ["PaideiaGenesis", "Deep-Learning", "DINOv2", "Latent-Space"],
        "source": "concepts/dinov2-dense-latent-space-geometry"
    },
    {
        "type": "cloze",
        "text": "The primary advantage of on-manifold IMU Preintegration (Forster et al.) is that intermediate high-rate inertial measurements {{c1::do not need to be re-integrated}} when past camera poses are updated during {{c2::non-linear graph optimization}}.",
        "pearl": "Relative preintegrated rotation, velocity, and position deltas are formulated in the local frame of the initial keyframe.",
        "tags": ["PaideiaGenesis", "Robotics", "VIO", "IMU-Preintegration"],
        "source": "concepts/imu-preintegration-on-so3-manifolds"
    },
    {
        "type": "cloze",
        "text": "In Visual-Inertial Odometry, the system possesses exactly {{c1::4 unobservable degrees of freedom}}: {{c2::3D global position}} ($x, y, z$) and {{c3::yaw rotation around the gravity vector}}.",
        "pearl": "Roll and pitch are observable through the accelerometer gravity vector; yaw is unobservable without magnetic or global references.",
        "tags": ["PaideiaGenesis", "Robotics", "VIO", "Observability"],
        "source": "exam_traps/yaw-unobservability-under-constant-acceleration"
    },
    {
        "type": "cloze",
        "text": "DINO-WM (DINO World Model) enables zero-shot robot planning by predicting transition dynamics entirely within {{c1::frozen DINOv2 latent patch space}} without {{c2::decoding RGB pixels}}.",
        "pearl": "Operating in latent space eliminates pixel diffusion rendering costs, allowing 100 Hz Model Predictive Control.",
        "tags": ["PaideiaGenesis", "Robotics", "DINO-WM", "World-Models"],
        "source": "concepts/dino-world-models-and-latent-planning"
    },
    {
        "type": "cloze",
        "text": "In sliding-window VIO (VINS-Mono), marginalization of old camera keyframes preserves their geometric information using the {{c1::Schur Complement}} to construct a {{c2::Gaussian prior}} on remaining states.",
        "pearl": "The Schur Complement eliminates marginalized poses while maintaining exact historical constraints on remaining landmarks and poses.",
        "tags": ["PaideiaGenesis", "Robotics", "VIO", "Marginalization"],
        "source": "concepts/visual-inertial-state-estimation-and-marginalization"
    },
    {
        "type": "cloze",
        "text": "A 1-degree gyroscope bias error in naive global IMU integration projects gravity into false horizontal acceleration of $\\approx$ {{c1::0.17 m/s²}}, resulting in {{c2::8.5 meters}} of position error in just 10 seconds.",
        "pearl": "Double integration of accelerometer bias and rotated gravity tilt errors produces quadratic divergence over time.",
        "tags": ["PaideiaGenesis", "Robotics", "VIO", "IMU-Drift"],
        "source": "exam_traps/naive-euler-imu-integration-drift"
    }
]

VISION_CURRICULUM_TOPICS = [
    {"name": "MapAnything & Universal Feed-Forward Metric 3D Reconstruction", "priority": "CRITICAL"},
    {"name": "DINOv2 Latent Space Geometry & Dense Point Correspondence", "priority": "CRITICAL"},
    {"name": "On-Manifold IMU Preintegration in Visual-Inertial Odometry", "priority": "CRITICAL"},
    {"name": "DINO World Models (DINO-WM) & Latent-Only Planning", "priority": "HIGH"},
    {"name": "Sliding-Window Optimization (VINS-Mono) vs Filtering (MSCKF)", "priority": "HIGH"},
    {"name": "3D Gaussian Splatting & Distilled Feature Fields (ConceptFusion)", "priority": "MEDIUM"},
    {"name": "Unobservable Degeneracies & Covariance Consistency in VIO", "priority": "MEDIUM"}
]
