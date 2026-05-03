# AI / ML Interview Prep (Google SDE-2 L4)

For the AI-ML round in your loop. Confirm with your recruiter whether it is: theory-only, ML system design, stats/coding, or a mix. Cover all three lightly if unknown.

---

## Core ML concepts (must be fluent in 60-second explanations)

### Fundamentals

| Concept | What to say in 60s |
|---------|-------------------|
| **Supervised vs unsupervised** | Supervised: labeled data, learn mapping X→Y. Unsupervised: no labels, find structure (clustering, dimensionality reduction). Semi-supervised: a few labels + lots of unlabeled. |
| **Bias-variance tradeoff** | High bias = underfitting (model too simple). High variance = overfitting (model memorizes train data, fails on test). Regularization and more data reduce variance. |
| **Train / val / test split** | Train to fit, val to tune hyperparameters and detect overfitting, test to report final performance *once*. Never tune on test set. |
| **Overfitting** | Model performs well on train, poorly on val/test. Signs: big gap between train and val loss. Fixes: more data, dropout, regularization (L1/L2), early stopping, simpler model. |
| **Regularization** | L2 (ridge): penalizes large weights, shrinks toward 0. L1 (lasso): drives some weights to exactly 0 (sparse model). L1 better for feature selection. |

### Evaluation metrics — when each misleads

| Metric | Formula | When to use | When it misleads |
|--------|---------|-------------|-----------------|
| **Accuracy** | correct / total | Balanced classes | Imbalanced: 99% negative class → 99% accuracy with zero recall |
| **Precision** | TP / (TP+FP) | When false positives are costly (spam filter) | Ignores false negatives |
| **Recall** | TP / (TP+FN) | When false negatives are costly (cancer detection) | Ignores false positives |
| **F1** | 2×(P×R)/(P+R) | Need balance of P and R | Treats P and R equally; use Fβ if asymmetric |
| **AUC-ROC** | Area under ROC curve | Ranking quality across thresholds | Misleading when class imbalance is extreme |
| **Log loss** | -mean(y·log(p) + (1-y)·log(1-p)) | Probabilistic classifiers | Doesn't capture ranking |
| **RMSE / MAE** | Root mean sq. error / mean abs. error | Regression | RMSE penalizes outliers more; choose based on business tolerance for large errors |

### Models — when to use what

| Model | Strengths | Weaknesses | Use when |
|-------|-----------|------------|---------|
| **Linear / logistic regression** | Interpretable, fast, works on small data | Can't capture non-linearity without features | Features are already informative; need explainability |
| **Random Forest** | Handles non-linearity, robust to noise, feature importance | Slower, less interpretable than logistic | Tabular data, baseline before trying GBDT |
| **GBDT (XGBoost/LightGBM)** | State-of-art on tabular, handles missing values | Slower to train, many hyperparams | Structured/tabular data, Kaggle-style problems |
| **Neural nets** | Automatic feature learning, best on images/text/audio | Needs lots of data, compute, less interpretable | Unstructured data, sufficient training data |

### Deep learning (if on your resume)

**CNN:**
- Convolutional layers apply learned filters → detect edges, textures, shapes at each spatial location.
- Translation invariance: a filter recognizes a feature wherever it appears in the image.
- Pooling (max/avg) reduces spatial dimension, provides some shift invariance.
- Architecture progression: input → Conv+ReLU layers → Pooling → Fully connected → Softmax.
- Key insight: parameter sharing (same filter across all positions) → many fewer params than a fully connected layer on raw pixels.
- Used for: image classification (ResNet), object detection (YOLO, Faster R-CNN), medical imaging.

**RNN / LSTM:**
- RNN: hidden state `h_t = f(h_{t-1}, x_t)` — carries context forward. Problem: vanishing gradient over long sequences.
- LSTM: adds three gates (input, forget, output) + a cell state. Forget gate decides what to drop from memory. Input gate decides what new info to add. This lets gradients flow over hundreds of steps.
- GRU: simplified LSTM with two gates; faster to train, similar quality on many tasks.
- Use when: sequence-to-sequence tasks (translation), time series, when position matters.
- Mostly superseded by Transformers for NLP but still used for streaming/real-time with strict latency budgets.

**Transformer / Attention:**
- Self-attention: each token attends to every other token. Weight = softmax(QKᵀ / √d_k) × V.
- "Attention is a weighted average of value vectors, where weights come from query-key similarity."
- Multi-head attention: run attention in parallel with different weight matrices → captures different relationship types.
- Positional encoding: since Transformers have no recurrence, position is injected via sinusoidal vectors or learned embeddings.
- Why it beat RNNs: parallelizes over sequence length (no sequential dependency), attends to any position directly (path length O(1) vs O(N) for RNN).
- BERT: bidirectional, pre-trained on masked language modeling. GPT: autoregressive, left-to-right.

**Vanishing / exploding gradient:**
- Vanishing: gradients shrink exponentially through many layers → early layers receive near-zero update.
- Exploding: gradients grow exponentially → weights diverge (NaN loss).
- Fixes: ReLU (gradient = 1 in positive region), residual connections (skip connections add gradient highway), LSTM gates, gradient clipping (for exploding), batch norm.

**Batch norm / dropout / layer norm:**
- Batch norm: normalize activations across the batch at each layer. Speeds training, allows higher LR. Problem: noisy at small batch sizes.
- Layer norm: normalize across the feature dimension for one sample (not across batch). Preferred in Transformers.
- Dropout: randomly zero p% of activations during training. Forces the network to not rely on any single neuron → regularization. Disabled at inference.

---

## Data and features

| Issue | Description | Fix |
|-------|-------------|-----|
| **Missing values** | NaN in features | Impute (mean/median), add indicator feature, or model-specific handling (tree can handle NaN natively) |
| **Class imbalance** | 99:1 negative:positive | See imbalanced data section below |
| **Feature leakage** | Feature contains information from the future or the label itself | Strict temporal split; audit features before training |
| **Train-serving skew** | Feature computed differently at train time vs inference time | Share feature computation code; feature store |
| **Feature scaling** | Some models (SVM, neural nets, KNN) sensitive to scale | StandardScaler or MinMaxScaler; tree models generally don't need it |

### Handling class imbalance

| Technique | How | When to prefer |
|-----------|-----|---------------|
| **Class weights** | Set `class_weight='balanced'` in sklearn; loss weighted by inverse frequency | Default first move — no data change, just loss reweighting |
| **Oversampling minority** | Duplicate or synthesize (SMOTE) minority class samples | Small minority class and you have enough majority data |
| **Undersampling majority** | Randomly drop majority class rows | Majority class is very large; training time is a bottleneck |
| **Threshold tuning** | Lower classification threshold (e.g. 0.3 instead of 0.5) to increase recall | You have a trained model and want to trade precision for recall |
| **Different metric** | Optimize AUC-PR (precision-recall AUC) instead of accuracy | Standard AUC-ROC can look good even with near-random minority predictions |

**Interview answer:** "First I'd check severity — 10:1 is manageable with class weights; 1000:1 may need SMOTE. I'd switch my evaluation metric from accuracy to F1 or AUC-PR immediately. I'd also threshold tune after training to hit the precision/recall operating point the business needs."

**SMOTE in one sentence:** for each minority sample, find k nearest minority neighbors, generate new synthetic point on the line segment between them.

---

## ML system design (end-to-end)

For open-ended ML design questions, walk through this pipeline:

```
1. Problem definition
   - What is the label? How is it collected?
   - What metric maps to the business goal?
   - What is the acceptable latency / throughput?

2. Data
   - Sources: logs, user actions, external feeds
   - Volume: how much? how fresh?
   - Labeling: human annotations, click-through, engagement signals

3. Feature engineering
   - User features: demographics, history, preferences
   - Item features: content, metadata, embeddings
   - Context: time, device, location
   - Store in feature store for reuse + consistency

4. Model training
   - Offline: batch on historical data
   - Split: time-based (don't shuffle time-series)
   - Evaluation: val set, offline metrics (AUC, NDCG), business proxy

5. Deployment
   - Batch inference: precompute results, low latency, may be stale
   - Online inference: real-time, higher latency requirement, fresher
   - A/B test or shadow deploy before full rollout

6. Monitoring
   - Data drift: input feature distribution shifts
   - Concept drift: relationship between features and label changes
   - Metrics: model accuracy on production labels, downstream business metric
   - Alert and retrain trigger
```

### Example: Recommend YouTube videos (open-ended, 20 min)

**Problem:** Given a user's watch history, recommend 10 videos to surface.

**Two-stage approach (industry standard for large-scale rec):**
1. **Candidate generation** (recall): fast model to get top-500 from millions. Options: collaborative filtering (matrix factorization), embedding nearest-neighbor.
2. **Ranking** (precision): richer model (GBDT or neural) scores top-500, returns top-10. Features: video embeddings, user history, watch-time, recency, diversity.

**Key tradeoffs:**
- Freshness vs quality: newly uploaded videos have no engagement signals — use content features + model uncertainty
- Diversity: greedy top-K produces similar videos → add diversity constraint (MMR or category caps)
- Latency: ranking must complete in < 100ms → limit feature count, use approximate ANN

**What to monitor:** CTR, watch-time, session length, thumbs-down rate. Offline metric = AUC on click labels; proxy for business metric = watch-time.

---

## A/B testing and safe deployment

### A/B test setup (for a model change)

1. **Randomize by user**, not request — same user always sees the same variant to avoid inconsistency.
2. **Minimum detectable effect:** decide the smallest business lift you care about before you run the test. Use this to calculate required sample size (power analysis).
3. **Guard rails:** define metrics that must not degrade (e.g. latency p99, crash rate). If a guard rail breaks, roll back regardless of primary metric.
4. **Run duration:** at least one full weekly cycle (7 days) to capture day-of-week patterns. Don't stop early because the metric looks good — multiple looks inflate false positive rate (use sequential testing or Bonferroni if you must peek).
5. **Novelty effect:** a new feature may get engagement just because it's new. Monitor cohort behavior after week 2.

### Shadow deployment

Run new model in parallel with production model: serve production's answer to users, but log new model's predictions for offline comparison. No user impact.
- Use to: validate prediction distribution, catch regressions in latency, spot label distribution drift before launch.
- Limitation: you don't observe counterfactual outcomes (what happens if you showed new model's result).

### Staged rollout (safe deployment order)

```
Shadow (0% users, log only)
  → Canary (1–5% traffic, monitor guard rails 24h)
  → Ramp (20% → 50% → 100%)
  → Full rollout
  → Deprecate old model
```

**What to monitor at each stage:** prediction distribution vs old model, business metric delta (CTR, conversion, watch time), latency, error rate, guard-rail metrics.

---

## STAR stories for ML rounds (fill in with your experience)

### Story template for ML work

> "We had [problem with data/model/production]. My task was [metric / outcome]. I [investigation method, change made]. The result was [before/after metric]. Looking back, I would [improvement]."

**Metrics to mention:** precision/recall improvement, latency reduction, training time cut, reduction in false positives, AUC gain, A/B lift.

### Common prompts + what to show

| Prompt | Must show |
|--------|-----------|
| Walk me through an ML project end to end | All 6 pipeline stages; your specific decisions at each |
| A time a model underperformed in production | Diagnosis method (dashboards, error analysis, distribution shift check), root cause, fix |
| How did you measure success? | Business metric + proxy metric; offline ≠ online performance |
| Latency vs quality tradeoff | Concrete example: smaller model, quantization, two-stage, caching |
| How would you debug a 5% quality drop? | Check data pipeline first, then feature drift, then label shift, then model health |

---

## Quick vocabulary list (use these terms naturally)

- **Feature store:** central repo for computed features; ensures train/serve consistency
- **Data drift:** input distribution changes post-deployment
- **Concept drift:** the mapping from features to label changes over time
- **Shadow deployment:** run new model in parallel, log predictions, compare offline before switching
- **Champion/challenger:** production model vs candidate; route % of traffic to challenger
- **NDCG:** Normalized Discounted Cumulative Gain — ranking metric; higher-ranked relevant items score more
- **MMR:** Maximal Marginal Relevance — balance relevance vs diversity in ranked lists
- **ANN:** Approximate Nearest Neighbor search (e.g. FAISS, ScaNN) — fast vector similarity at scale
- **Embeddings:** dense vector representations; similar items cluster in embedding space
- **TPU:** Tensor Processing Unit — Google's ASIC for matrix operations; mention if discussing training at scale
