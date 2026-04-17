# Complete Machine Learning Notes
> **Learning Strategy:** One ML type → study all its algorithms one by one daily
> **Current Progress:** Supervised → Unsupervised → **Semi-Supervised** → Reinforcement

---

## Table of Contents
- [1.1 Introduction to Machine Learning](#11-introduction-to-machine-learning)
- [1.2 Data Understanding & Preparation](#12-data-understanding--preparation)
- [1.3 Supervised Learning – Regression](#13-supervised-learning--regression)
- [1.4 Supervised Learning – Classification](#14-supervised-learning--classification)
- [1.5 Model Evaluation & Validation](#15-model-evaluation--validation)
- [1.6 Optimization Techniques](#16-optimization-techniques)
- [1.7 Unsupervised Learning](#17-unsupervised-learning)
- [1.8 Semi-Supervised Learning ✅ NEW](#18-semi-supervised-learning)
- [1.9 Reinforcement Learning](#19-reinforcement-learning)

---

## 1.1 Introduction to Machine Learning

### What is Machine Learning?
Machine Learning is a subset of AI where computers **learn patterns from data** and make predictions or decisions without being explicitly programmed.

> **Key Idea:** Instead of coding rules manually, you train a model on data.

### Mathematical View
- Dataset: `X = {x1, x2, ..., xn}`
- Labels: `Y = {y1, y2, ..., yn}`
- ML learns a function: `f: X → Y`
- For new input `x_new`, model predicts `y_new ≈ f(x_new)`

### Real-World Examples

| Problem | ML Application |
|---------|---------------|
| Email | Spam detection |
| Bank | Credit risk scoring |
| Healthcare | Disease prediction |
| E-commerce | Product recommendation |
| Self-driving | Object detection |
| NLP | Chatbots, translation |

---

### ML vs Traditional Programming

| Feature | Traditional Programming | Machine Learning |
|---------|------------------------|-----------------|
| Input | Data + Rules | Data |
| Process | Programmer-defined rules | Model learns rules |
| Output | Result | Prediction / Decision |
| Adaptability | Static | Learns & adapts |

**Example:**
- Traditional: Spam → programmer writes keyword rules ("buy now", "click here")
- ML: Train a classifier on labeled emails → model learns complex patterns automatically

---

### Types of Machine Learning

#### 1. Supervised Learning
- Learns from **labeled data** (input + output known)
- Subtypes: **Regression** (continuous) and **Classification** (discrete)
- Examples: House price prediction, Spam detection

#### 2. Unsupervised Learning
- Learns patterns from **unlabeled data**
- Tasks: Clustering, Dimensionality Reduction, Anomaly Detection
- Examples: Customer segmentation, Fraud detection

#### 3. Semi-Supervised Learning
- Uses **small labeled + large unlabeled** data
- When labeling is expensive but unlabeled data is abundant
- Examples: Medical imaging, Speech recognition

#### 4. Reinforcement Learning
- Agent learns by **interacting with environment** and receiving rewards/penalties
- Maximize: `E[∑ Rt]`
- Examples: Chess AI, Self-driving cars, Stock trading

---

### All 4 Types – Quick Comparison

| ML Type | Data | Goal | GenAI Use |
|---------|------|------|-----------|
| Supervised | Labeled (X, Y) | Predict output | LLM fine-tuning, classification |
| Unsupervised | Unlabeled (X only) | Find structure | Embedding clustering, RAG |
| Semi-Supervised | Few labeled + many unlabeled | Learn with less | Few-shot learning |
| Reinforcement | Reward signals | Maximize reward | RLHF (ChatGPT training) |

---

## 1.2 Data Understanding & Preparation

> 80% of real ML work is data preparation. A great model on bad data = bad results.

### Types of Data

#### 1. Numerical Data
- **Continuous** → infinite values (salary, temperature, height)
- **Discrete** → countable (number of clicks, purchases)

#### 2. Categorical Data
- **Nominal** → no order (gender, city)
- **Ordinal** → ordered (low, medium, high)
- ⚠️ ML models cannot directly understand categories → must be **encoded**

#### 3. Text Data
- Unstructured natural language (emails, reviews, documents for RAG)
- Models: NLP, Transformers, LLMs

#### 4. Image Data
- Represented as pixels (RGB → 3 channels, values 0–255)
- Models: CNNs, Vision Transformers (ViT)

---

### Feature Engineering
Turning raw data into meaningful signals to improve model performance.

| Raw Feature | Engineered Feature |
|-------------|-------------------|
| Date: 2026-02-11 | Day, Month, Year, Weekend/Weekday |
| "This product is amazing" | Word count, Sentiment score, Embedding |
| Total purchases | Avg purchase per month, Last purchase recency |

---

### Feature Scaling

**Why Scaling is Needed:**
| Feature | Range |
|---------|-------|
| Age | 0–100 |
| Salary | 0–1,00,00,000 |

Salary dominates learning → biased model

**Algorithms sensitive to scaling:** Gradient Descent, kNN, SVM, Neural Networks, K-Means

---

### Normalization
Scales values into range **[0, 1]**

```
x_norm = (x - x_min) / (x_max - x_min)
```

**Example:** min=10, max=50, x=30 → `x_norm = (30-10)/(50-10) = 0.5`

**When to use:** Image data, Neural networks, when min/max known

---

### Standardization
Centers data around mean=0, std=1

```
x_std = (x - μ) / σ
```

**Example:** mean=50, std=10, x=60 → `x_std = (60-50)/10 = 1`

**When to use:** Gaussian data, Linear/Logistic Regression, SVM, PCA

---

### Handling Missing Data

| Technique | When to Use |
|-----------|-------------|
| Remove rows | When missing data is very small |
| Mean/Median imputation | Numerical data |
| Mode imputation | Categorical data |
| Model-based imputation | When patterns exist |

---

### Outliers
Data points very far from normal range.

**Detection:**
- Z-score
- IQR (Interquartile Range)
- Box plot visualization

**Handling:**
- Remove
- Cap (Winsorization)
- Log transformation

---

## 1.3 Supervised Learning – Regression

### What is Regression?
Regression predicts a **continuous numerical value** from input features.

### Linear Regression

**Formula (single feature):** `y = mx + b`

**Formula (multiple features):** `y = w1x1 + w2x2 + ... + wnxn + b`

Where: `w` = weights, `b` = bias, `x` = input, `y` = predicted output

**Real-World Example:**
```
Price = (5000 × Area) + (10,000 × Bedrooms) + b
```

---

### Cost Function – MSE (Mean Squared Error)

```
MSE = (1/n) × Σ(yi - ŷi)²
```

**Worked Example:**

| Actual | Predicted |
|--------|-----------|
| 50 | 45 |
| 60 | 65 |

`MSE = ((50-45)² + (60-65)²) / 2 = (25 + 25) / 2 = 25`

**Why square errors?** Penalizes large errors, differentiable (needed for optimization)

---

### Gradient Descent (Intuition)
Adjusts weights to minimize MSE.

**Steps:**
1. Compute error
2. Compute gradient
3. Update weights
4. Repeat

---

### Assumptions of Linear Regression *(Important for interviews)*

| Assumption | What It Means |
|------------|---------------|
| Linearity | Relationship between input & output is linear |
| Independence | Observations are independent |
| Homoscedasticity | Constant variance of errors |
| Normality of Errors | Residuals follow normal distribution |
| No Multicollinearity | Features shouldn't be highly correlated |

---

### Polynomial Regression
Used when the relationship is **curved** (linear model fails).

**Formula:** `y = w0 + w1x + w2x² + w3x³`

**When to use:** Salary vs Experience (fast early growth, slow later)

⚠️ Risk: **Overfitting** → Solution: Regularization (Ridge/Lasso)

---

### Regression Examples

| Problem | Model |
|---------|-------|
| House price | Linear / Polynomial |
| Stock trend | Polynomial |
| Energy consumption | Linear |
| LLM inference cost | Linear Regression |

---

## 1.4 Supervised Learning – Classification

### What is Classification?
Predicts **discrete labels** (categories) instead of continuous values.

### Logistic Regression

**Linear combination:** `z = w1x1 + w2x2 + ... + b`

**Sigmoid function:**
```
P(y=1|x) = 1 / (1 + e^(-z))
```

- Output range: 0 to 1
- Decision boundary: if probability ≥ 0.5 → Class 1

**Cost Function – Binary Cross-Entropy:**
```
L = -[y·log(p) + (1-y)·log(1-p)]
```

✅ Interpretable | ✅ Fast | ✅ Probabilistic output

---

### k-Nearest Neighbors (kNN)
Distance-based classification. "Tell me who your neighbors are, I'll tell you who you are."

**How it works:**
1. Choose k
2. Measure distance (Euclidean, Cosine)
3. Take majority vote

✅ Simple | ✅ No training phase | ❌ Slow on large data | ❌ Sensitive to scaling

**GenAI:** Embedding similarity, Vector database retrieval

---

### Decision Trees
A tree of rules that splits data based on conditions.

**Splitting Criteria:** Gini Impurity, Entropy (Information Gain)

**Example Rule:**
```
If income > 5 LPA:
    Approve loan
Else:
    Reject loan
```

✅ Highly interpretable | ✅ Handles non-linearity | ❌ Overfitting

---

### Random Forest
Ensemble of multiple decision trees → majority vote.

✅ High accuracy | ✅ Robust to noise | ✅ Handles missing values

**Real-World:** Fraud detection, Credit risk, Medical diagnosis

---

### Support Vector Machine (SVM)
Finds the **best boundary (maximum margin)** separating classes.

- **Support vectors** = closest points to boundary
- **Kernel trick** = handles non-linear problems by mapping to higher dimensions

✅ Works well in high dimensions | ❌ Slow for very large datasets

---

### Algorithm Comparison Table

| Algorithm | Fast | Interpretable | Handles Non-linear | Scales Well |
|-----------|------|---------------|-------------------|-------------|
| Logistic Regression | ✅ | ✅ | ❌ | ✅ |
| kNN | ❌ | ❌ | ✅ | ❌ |
| Decision Tree | ✅ | ✅ | ✅ | ❌ |
| Random Forest | ❌ | ❌ | ✅ | ✅ |
| SVM | ❌ | ❌ | ✅ | ❌ |

---

## 1.5 Model Evaluation & Validation

### Train / Validation / Test Split

**Typical Split:**
- 70% Training → learn model parameters
- 15% Validation → tune hyperparameters, choose best model
- 15% Test → final evaluation only

> ⚠️ Never evaluate on training data → false confidence

---

### Cross-Validation (k-Fold)
1. Split data into k folds
2. Train on k-1 folds, test on remaining
3. Repeat k times
4. Average results

**Why needed:** Small datasets, stable evaluation

---

### Bias vs Variance Tradeoff

| Model | Bias | Variance |
|-------|------|----------|
| Linear model (too simple) | High | Low |
| Deep neural net (too complex) | Low | High |

**Goal:** Low bias + low variance

---

### Overfitting vs Underfitting

| | Underfitting | Overfitting |
|--|-------------|------------|
| Cause | Too simple model | Too complex model |
| Training performance | Poor | Great |
| Testing performance | Poor | Poor |
| Solution | Complex model, more features | Regularization, dropout, more data |

**GenAI:** Overfitting → hallucinations | Underfitting → generic responses

---

### Confusion Matrix

| Actual \ Predicted | Positive | Negative |
|--------------------|----------|----------|
| **Positive** | TP | FN |
| **Negative** | FP | TN |

---

### Evaluation Metrics

**Accuracy:**
```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```
⚠️ Don't use for imbalanced datasets

**Precision:**
```
Precision = TP / (TP + FP)
```
Use when false positives are costly (spam detection, fraud)

**Recall:**
```
Recall = TP / (TP + FN)
```
Use when false negatives are costly (disease detection, security)

**F1 Score:**
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```
Balance between precision & recall

**ROC-AUC:** TPR vs FPR curve. AUC = 0.5 (random) → 1.0 (perfect)

---

### Metric Selection Guide

| Problem | Best Metric |
|---------|-------------|
| Spam detection | Precision |
| Disease detection | Recall |
| Balanced classification | F1 |
| Imbalanced data | ROC-AUC |
| GenAI safety | Precision + Recall |

---

## 1.6 Optimization Techniques

### Loss Functions

| Problem | Loss Function | Formula |
|---------|--------------|---------|
| Regression | MSE | `(y - ŷ)²` |
| Classification | Cross-Entropy | `-[y·log(p) + (1-y)·log(1-p)]` |
| LLMs | Cross-Entropy | Token-level loss |

---

### Gradient Descent

**Weight update rule:**
```
w = w - α × (∂L/∂w)
```

Where `α` = learning rate, `∂L/∂w` = gradient

---

### Types of Gradient Descent

| Type | Uses | Speed | Stable | Used Where |
|------|------|-------|--------|-----------|
| Batch GD | Entire dataset | Slow | ✅ | Small datasets |
| SGD | Single data point | Fast | ❌ (noisy) | LLM ideas |
| Mini-Batch GD | Small batches (32/64) | ✅ | ✅ | Deep Learning, Transformers |

**Industry standard = Mini-Batch GD**

---

### Learning Rate

| Learning Rate | Problem |
|---------------|---------|
| Too high | Overshoots minimum |
| Too low | Very slow training |

**Learning Rate Scheduling:** Step decay, Exponential decay, Warm-up (Transformers)

---

### Local vs Global Minima

- **Global Minimum** = best possible solution
- **Local Minimum** = best in a small region
- In high-dimensional DL: most local minima are "good enough"
- SGD's noise helps escape bad local minima

---

## 1.7 Unsupervised Learning

### What is Unsupervised Learning?
Discovers **patterns in data without labels**.

**Goals:** Find structure, Find groups, Find compressed representations

---

### K-Means Clustering

**How it works:**
1. Choose K (number of clusters)
2. Randomly initialize centroids
3. Assign each point to nearest centroid
4. Update centroids (mean of points)
5. Repeat until convergence

**Objective:**
```
Minimize Σ Σ ||x - μi||²
```

✅ Simple | ✅ Fast | ✅ Scales well | ❌ Need to choose K | ❌ Sensitive to outliers

**GenAI:** Clustering embeddings in vector DBs, chunk grouping in RAG

---

### Hierarchical Clustering
Builds a tree of clusters (dendrogram).

- **Agglomerative (Bottom-Up):** Each point starts as cluster, merge closest
- **Divisive (Top-Down):** Start with all points, split recursively

**When used:** Small datasets, when cluster hierarchy matters

---

### PCA (Principal Component Analysis)
Linear dimensionality reduction.

**Core idea:** Find directions of maximum variance → project data onto those directions

**Steps:**
1. Standardize data
2. Compute covariance matrix
3. Find eigenvectors
4. Select top components

✅ Fast | ✅ Removes redundancy | ❌ Linear only

**GenAI:** Compress embeddings, preprocessing before clustering

---

### t-SNE
Non-linear dimensionality reduction for **visualization only**.

- Preserve local similarity
- Points close in high-D → close in low-D

❌ Not scalable | ❌ Not for training models | ❌ Non-deterministic

**GenAI:** Visualizing vector DB clusters, debugging RAG systems

---

### Algorithm Comparison

| Algorithm | Use Case | Scales Well | Interpretable |
|-----------|----------|-------------|---------------|
| K-Means | Clustering | ✅ | ❌ |
| Hierarchical | Hierarchy | ❌ | ✅ |
| PCA | Dim reduction | ✅ | ⚠️ |
| t-SNE | Visualization | ❌ | ❌ |

---

## 1.8 Semi-Supervised Learning

> **Your current topic to master ✅**

### What is Semi-Supervised Learning?
A learning approach that uses a **small amount of labeled data** combined with a **large amount of unlabeled data**.

It sits between Supervised (all labeled) and Unsupervised (no labels).

```
Supervised:      Labeled data only        → expensive, limited
Unsupervised:    Unlabeled data only      → no direct guidance
Semi-Supervised: Few labeled + many unlabeled → BEST of both worlds
```

---

### Why Semi-Supervised Learning?

**The Problem:**
- Labeling data is **expensive and slow** (requires human experts)
- Unlabeled data is **cheap and abundant**

**Real-World Challenge:**
- Medical imaging: labeling 10,000 X-rays needs 10,000 expert annotations → very costly
- But collecting 10,000 raw X-ray images is easy

**Semi-Supervised Solution:**
- Label just 100 images (cheap)
- Use 10,000 unlabeled images to improve accuracy

---

### Core Assumption
Semi-supervised learning works because of two key assumptions:

#### 1. Smoothness Assumption
Points that are **close together** in input space tend to have the **same label**.

```
If x1 ≈ x2  →  f(x1) ≈ f(x2)
```

**Example:** Two very similar X-ray images → likely same diagnosis

#### 2. Cluster Assumption
Points in the **same cluster** tend to have the **same label**.

**Example:** Cluster of customer transactions → likely same behavior type

#### 3. Manifold Assumption
High-dimensional data lies on a **lower-dimensional manifold** (structure).

**Example:** Images of cats all lie on a "cat manifold" in pixel space

---

### Mathematical View

Let:
- `L = {(x1,y1), (x2,y2), ..., (xl, yl)}` → small labeled dataset
- `U = {xl+1, xl+2, ..., xl+u}` → large unlabeled dataset
- Usually `u >> l` (much more unlabeled than labeled)

**Goal:** Learn `f(x)` that performs well on test data using both `L` and `U`

---

### Algorithms in Semi-Supervised Learning

#### Algorithm 1: Self-Training (Pseudo-Labeling)

**How it works:**
1. Train a model on labeled data `L`
2. Predict labels for unlabeled data `U` → these are **pseudo-labels**
3. Add high-confidence predictions to labeled set
4. Retrain model on original labels + pseudo-labels
5. Repeat until convergence

**Example:**
```
Step 1: Train on 100 labeled emails (spam/not spam)
Step 2: Predict 10,000 unlabeled emails
Step 3: Take predictions with confidence > 95% as pseudo-labels
Step 4: Retrain on 100 original + ~8000 pseudo-labeled
Step 5: Repeat → model keeps improving
```

**Strengths:**
- ✅ Simple and intuitive
- ✅ Works with any base classifier
- ✅ No model architecture changes needed

**Weaknesses:**
- ❌ Wrong pseudo-labels can hurt the model (confirmation bias)
- ❌ Model reinforces its own mistakes
- ❌ Confidence ≠ correctness

**GenAI Usage:**
- Fine-tuning LLMs with few labeled examples
- Document labeling in RAG pipelines

---

#### Algorithm 2: Label Propagation

**How it works:**
- Build a **graph** where nodes = data points, edges = similarity
- Spread labels from labeled nodes to nearby unlabeled nodes
- Label "propagates" through the graph like a wave

**Intuition:**
```
Labeled point [SPAM] →  
    → similar unlabeled point → [SPAM]  
        → similar unlabeled point → [SPAM]
```

**Example:**
- Customer A (labeled: premium) is similar to Customer B (unlabeled)
- Label propagates: Customer B is also likely premium

**Strengths:**
- ✅ Uses data structure/geometry
- ✅ Simple to understand
- ✅ No model retraining needed per step

**Weaknesses:**
- ❌ Expensive for very large graphs
- ❌ Requires good similarity metric
- ❌ Doesn't scale well to millions of points

**GenAI Usage:**
- Labeling documents in a knowledge base
- Propagating intent labels in conversational datasets

---

#### Algorithm 3: Co-Training

**How it works:**
1. Split features into **two independent views** (e.g., text content + metadata)
2. Train two separate classifiers, one on each view
3. Each classifier labels the unlabeled data
4. Each classifier teaches the other by sharing high-confidence predictions
5. Repeat

**Classic Example:**
- Web page classification
  - View 1: content of the web page
  - View 2: anchor text of links pointing to the page
- Two classifiers trained separately → each teaches the other

**Strengths:**
- ✅ Works when features have natural splits
- ✅ Reduces bias from single model
- ✅ Models cross-validate each other

**Weaknesses:**
- ❌ Need truly independent views
- ❌ Hard to find valid view splits in practice

**GenAI Usage:**
- Multi-modal models (text + image views)
- Code + comment as two views for code understanding

---

#### Algorithm 4: Semi-Supervised Generative Models

**How it works:**
- Use a **generative model** (e.g., VAE, GAN) to model the data distribution
- The model learns both labeled and unlabeled data structure
- Use learned distribution to improve classification

**Example:**
```
Train VAE on 100 labeled + 10,000 unlabeled images
→ VAE learns rich image representations
→ Use learned embeddings for classification
→ Better accuracy with few labels
```

**Key Models:**
- VAE (Variational Autoencoder) with labels
- Semi-supervised GAN

**GenAI Usage:**
- Pre-training embeddings
- Representation learning for downstream tasks

---

#### Algorithm 5: Consistency Regularization

**How it works:**
- Model should give **same prediction** for an input and its **slightly perturbed version**
- If prediction changes on minor noise → model is not confident → penalize

**Intuition:**
```
Image of a cat + small noise → still a cat
Model should agree with itself
```

**Formula:**
```
Loss = Supervised Loss (labeled) + λ × Consistency Loss (unlabeled)

Consistency Loss = distance(f(x), f(x + noise))
```

**Key Methods:**
- **Π-model (Pi-model):** Compare model output with vs without dropout
- **Mean Teacher:** Student model vs Teacher model (exponential moving average)
- **Virtual Adversarial Training (VAT):** Add adversarial noise to test consistency

**Strengths:**
- ✅ Very powerful for image and text tasks
- ✅ Used in state-of-the-art semi-supervised methods
- ✅ Forces model to learn stable, confident representations

**GenAI Usage:**
- Data augmentation consistency in fine-tuning
- Robust LLM training

---

#### Algorithm 6: MixMatch & FixMatch (Modern)

**MixMatch (2019):**
- Combines consistency regularization + pseudo-labeling
- Augment unlabeled images multiple times → average predictions → use as soft pseudo-label

**FixMatch (2020):**
- Weakly augmented image → generate pseudo-label
- Strongly augmented image → model must predict same label
- Only use pseudo-labels above confidence threshold

**Result:** State-of-the-art semi-supervised image classification with very few labels

**GenAI Usage:**
- Modern LLM fine-tuning with limited annotations
- Image-text alignment with few labeled pairs

---

### Real-World Examples

| Domain | Labeled Data | Unlabeled Data | Method |
|--------|-------------|----------------|--------|
| Medical imaging | 100 expert-labeled X-rays | 10,000 raw X-rays | Self-training |
| Speech recognition | 1 hour transcribed audio | 1000 hours raw audio | Pseudo-labeling |
| Document classification | 500 labeled docs | 50,000 unlabeled docs | Label propagation |
| Sentiment analysis | 200 labeled reviews | 20,000 raw reviews | Self-training |
| Web content classification | Few labeled pages | Millions of pages | Co-Training |

---

### Semi-Supervised Learning in GenAI

| Use Case | How |
|----------|-----|
| **Few-shot learning** | Train on few labeled examples + large unlabeled corpus |
| **LLM pre-training** | Massive unlabeled text → self-supervised objectives |
| **RAG document labeling** | Label few docs → propagate to similar docs |
| **Data-efficient fine-tuning** | Few labeled examples + consistency regularization |
| **Embedding generation** | Use unlabeled data to enrich representation |
| **Instruction tuning** | Few human instructions + many pseudo-instructions |

---

### How Self-Supervised Learning Relates

> **Important distinction for interviews:**

| Type | Labels |
|------|--------|
| Semi-supervised | Few human labels + many unlabeled |
| Self-supervised | **No human labels** – creates labels from data itself |

**Self-Supervised Examples:**
- GPT: predict next token → no human labels needed
- BERT: predict masked words → label comes from the text itself

**Key insight:** LLM pre-training is technically **self-supervised** → a special case of using unlabeled data effectively → closely related to semi-supervised philosophy.

---

### When to Use Semi-Supervised Learning

**Use it when:**
- ✅ Labeling is expensive (medical, legal, financial)
- ✅ Unlabeled data is easy to collect
- ✅ You have at least a small labeled set
- ✅ Domain experts are a bottleneck

**Don't use it when:**
- ❌ You have plenty of labeled data (use supervised)
- ❌ Unlabeled data is low quality
- ❌ Domain has very high labeling noise

---

### Semi-Supervised Learning – Algorithm Summary

| Algorithm | Core Idea | Best For | GenAI Use |
|-----------|-----------|----------|-----------|
| Self-Training | Pseudo-labels from confident predictions | General classification | Fine-tuning LLMs |
| Label Propagation | Spread labels through similarity graph | Graph-like data | Knowledge base labeling |
| Co-Training | Two views teach each other | Multi-view data | Multi-modal models |
| Generative Models | Learn data distribution + labels | Images, representation | VAE embeddings |
| Consistency Regularization | Same input → same output despite noise | Images, text | Robust fine-tuning |
| FixMatch | Weak aug → label, Strong aug → test | Image classification | Modern SSL SOTA |

---

### Interview Gold Points ✅

- Semi-supervised = few labels + many unlabeled
- Key assumptions: smoothness, cluster, manifold
- Self-training is the simplest → but risks confirmation bias
- Label propagation uses graph structure
- Consistency regularization is used in modern SOTA methods
- LLM pre-training is **self-supervised** (no labels) → related but distinct
- BERT/GPT succeed because they leverage massive unlabeled data
- FixMatch/MixMatch are state-of-the-art for image SSL

### Mental Model
```
Semi-Supervised = A student who studies a few solved examples
                  + teaches themselves from thousands of unsolved problems
```

---

## 1.9 Reinforcement Learning

### What is Reinforcement Learning?
An agent learns by **interacting with environment** and receiving **rewards or penalties**.

**Key Components:**
- **Agent** → Learner / decision-maker
- **Environment** → Where agent acts
- **Action** → Agent's move
- **Reward** → Feedback signal (+/-)
- **Policy** → Strategy to choose actions

**Mathematical Goal:**
```
Maximize E[Σ γᵗ Rₜ]
```
Where `γ` = discount factor, `Rₜ` = reward at time t

---

### Algorithms

#### Q-Learning
- Model-free learning
- Learns value of actions in states
- Used for: Game AI, Robotics

#### Deep Q Networks (DQN)
- Q-Learning + Neural Networks
- Handles large state spaces
- Used for: Atari games, Autonomous systems

#### Policy Gradient Methods
- Directly optimize policy
- Used for: Robotics, Finance (continuous action spaces)

#### PPO (Proximal Policy Optimization)
- Stable RL training
- **GenAI: Used in RLHF (ChatGPT training)**

---

### Real-World Examples

| Problem | Environment | Reward |
|---------|-------------|--------|
| Chess AI | Chess board | +1 win, -1 loss |
| Self-driving | Roads | +safe, -collision |
| Stock trading | Market | +profit, -loss |
| ChatGPT (RLHF) | Conversation | +human approval |

---

### RLHF (Reinforcement Learning from Human Feedback)
How ChatGPT / Claude are trained:
1. Pre-train LLM on unlabeled text (self-supervised)
2. Fine-tune on labeled instruction examples (supervised)
3. Train reward model from human preferences
4. Use PPO to optimize LLM against reward model (RL)

---

## Complete Algorithm Reference

### Supervised Learning
| Algorithm | Type | Use Case |
|-----------|------|----------|
| Linear Regression | Regression | House prices, salary |
| Polynomial Regression | Regression | Curved trends |
| Ridge/Lasso | Regression | High-dimensional, prevent overfitting |
| Logistic Regression | Classification | Spam, loan approval |
| kNN | Classification | Recommendation, image similarity |
| Decision Tree | Classification | Credit scoring, churn |
| Random Forest | Classification | Fraud detection, risk |
| SVM | Classification | Text, face recognition |
| Neural Networks | Both | Complex patterns |

### Unsupervised Learning
| Algorithm | Type | Use Case |
|-----------|------|----------|
| K-Means | Clustering | Customer segmentation |
| Hierarchical | Clustering | Document hierarchy |
| DBSCAN | Clustering + Anomaly | Fraud, GPS data |
| PCA | Dim Reduction | Feature compression, viz |
| t-SNE / UMAP | Visualization | Embedding analysis |
| Isolation Forest | Anomaly Detection | Fraud, intrusion |

### Semi-Supervised Learning
| Algorithm | Use Case |
|-----------|----------|
| Self-Training | General classification with few labels |
| Label Propagation | Graph-structured data |
| Co-Training | Multi-view data |
| Consistency Regularization | Images, text robustness |
| FixMatch / MixMatch | State-of-the-art image SSL |

### Reinforcement Learning
| Algorithm | Use Case |
|-----------|----------|
| Q-Learning | Game AI, robotics |
| DQN | Atari, autonomous systems |
| Policy Gradient | Continuous action spaces |
| PPO | RLHF, stable training |

---

## GenAI & LLM Connections Summary

| ML Concept | Where It Appears in GenAI/LLMs |
|------------|-------------------------------|
| Supervised (classification) | Fine-tuning, intent detection, toxicity filtering |
| Regression | Token cost estimation, reward modeling |
| Logistic Regression | Classification heads on LLMs |
| kNN | Vector database retrieval (semantic search) |
| Random Forest | Safety classification, ranking |
| K-Means | Embedding clustering, RAG chunk grouping |
| PCA | Embedding compression |
| t-SNE | Visualizing LLM embeddings |
| Self-Training | Data-efficient LLM fine-tuning |
| Label Propagation | RAG document labeling |
| Consistency Regularization | Robust fine-tuning |
| PPO (RL) | RLHF → ChatGPT, Claude training |
| Cross-Entropy Loss | Language model training (token prediction) |
| Mini-Batch GD | Transformer training |
| Warm-up LR Schedule | Transformer optimization |

---

*Notes maintained by: [Your Name]*
*Last updated: Daily as new algorithms are completed*
*Learning path: Supervised → Unsupervised → Semi-Supervised → Reinforcement*