# AliExpress Pricing Strategy Recommender
### ML-Powered Supply-Side Pricing Intelligence

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Scikit-Learn](https://img.shields.io/badge/ScikitLearn-1.3+-orange?style=flat-square&logo=scikit-learn)
![Streamlit](https://img.shields.io/badge/Streamlit-1.5+-red?style=flat-square&logo=streamlit)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

---

## Overview

This project addresses a critical gap in e-commerce analytics: **most pricing tools focus on the consumer side** (what buyers pay), while sellers lack actionable guidance on *which pricing strategy actually drives sales*.

We built a **supply-side ML pipeline** trained on **711,168 AliExpress products** across **300+ categories** that:

1. **Clusters** products into pricing strategy archetypes using K-Means
2. **Classifies** the optimal strategy for any new product using Random Forest
3. **Delivers** a full pricing report via an interactive Streamlit app

> **"Given a product's category, price, rating and shipping cost — what pricing strategy will maximize sales?"**

---

##  Research Question

> *What pricing strategies do sellers adopt, and which strategy performs best per product category?*

---

##  Pipeline Architecture

```
Raw Data (864k products)
        ↓
┌─────────────────────┐
│  1. EDA             │  → Distributions, correlations, outliers
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  2. Preprocessing   │  → Deduplication, missing values, outlier capping
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  3. Feature Eng.    │  → 13 engineered features (discount aggressiveness,
└─────────┬───────────┘      value score, price rank, store avg sold...)
          ↓
┌─────────────────────┐
│  4. Feature Sel.    │  → Correlation filter (>0.85) + Mutual Information
└─────────┬───────────┘      → 11 features → 7 final features
          ↓
┌─────────────────────┐
│  5. Clustering      │  → K-Means (K=3, Silhouette=0.31)
└─────────┬───────────┘      → 3 strategy archetypes discovered
          ↓
┌─────────────────────┐
│  6. Classification  │  → Random Forest (94.17% accuracy)
└─────────┬───────────┘      → Hyperparameter tuning + Cross-validation
          ↓
┌─────────────────────┐
│  7. Evaluation      │  → Confusion matrix, AUC-ROC, Precision-Recall
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  8. Pricing Report  │  → Streamlit app — input → strategy report
└─────────────────────┘
```

---

##  Discovered Pricing Strategies

| Strategy | Avg Sold | Avg Price | Avg Rating | Prevalence |
|---|---|---|---|---|
|  **Smart Discounter** | **131.78** | 46 DT | **4.77** | 36.7% |
|  Overpriced Low Performer | 7.27 | 1,252 DT | 1.32 | 8.2% |
|  Underperformer | 2.12 | 94 DT | 0.70 | 55.1% |

> **Smart Discounter wins in 99.3% of all 300+ categories.**

---

##  Model Performance

| Model | Accuracy | F1 Score |
|---|---|---|
| Logistic Regression | 91.71% | 91.76% |
| **Random Forest (Tuned)** | **94.17%** | **94.19%** |
| XGBoost | 93.77% | 93.79% |

**Cross-validation:** Mean F1 = 93.28% | Std = 0.12% >> Stable

**Per-class F1:**
- Overpriced Low Performer: **0.98**
- Smart Discounter: **0.92**
- Underperformer: **0.95**

---

##  Top Features (by importance)

| Rank | Feature | Importance | What it captures |
|---|---|---|---|
| 1 | `rating` | **0.3427** | Product quality signal |
| 2 | `price` | **0.2105** | Raw price positioning |
| 3 | `effective_price` | **0.1744** | Real price after discount |
| 4 | `price_vs_category_avg` | 0.1076 | Competitive positioning |
| 5 | `shippingCost` | 0.0737 | Shipping strategy |
| 6 | `price_rank_in_category` | 0.0724 | Market rank |
| 7 | `category_id` | 0.0187 | Category context |

> Category barely matters (2%) — Smart Discounter wins everywhere.

---

##  Project Structure

```
📁 Aliexpress-pricing-strategy-ML/
│
├── 📓 notebook_1_EDA.ipynb
├── 📓 notebook_2_preprocessing.ipynb
├── 📓 notebook_3_feature_engineering.ipynb
├── 📓 notebook_4_feature_selection.ipynb
├── 📓 notebook_5_clustering.ipynb
├── 📓 notebook_6_classification.ipynb
├── 📓 notebook_7_evaluation.ipynb
├── 📓 notebook_8_explainability.ipynb
├── 📓 notebook_9_pricing_report.ipynb
│
├── 🐍 app.py                    ← Streamlit app
│
├── 📦 best_model.pkl            ← Tuned Random Forest
├── 📦 label_encoder.pkl         ← Strategy label encoder
├── 📦 scaler_clf.pkl            ← Feature scaler
├── 📦 kmeans_model.pkl          ← K-Means clustering model
├── 📦 app_artifacts.pkl         ← All artifacts for deployment
│
├── 📄 df_enriched.csv           ← After preprocessing + feature engineering
├── 📄 df_final.csv              ← After feature selection
├── 📄 df_clustered.csv          ← After clustering (with strategy labels)
│
└── 📄 README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/Aliexpress-pricing-strategy-ML.git
cd Aliexpress-pricing-strategy-ML
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit app
```bash
streamlit run app.py
```

### 4. Open in browser
```
http://localhost:8501
```

---

##  Requirements

```txt
pandas>=1.5.0
numpy>=1.23.0
scikit-learn>=1.3.0
xgboost>=2.0.0
matplotlib>=3.6.0
seaborn>=0.12.0
streamlit>=1.25.0
plotly>=5.15.0
joblib>=1.3.0
scipy>=1.10.0
```

---

##  App Features

| Feature | Description |
|---|---|
|  Product Input | Category + Price + Rating + Shipping |
|  Strategy Prediction | ML-powered with confidence score |
|  Probability Chart | Visual breakdown of all 3 strategies |
|  Radar Chart | Your product vs ideal Smart Discounter |
|  Recommendations | Discount range + shipping + key action |
|  Action Plan | 3-step personalized improvement guide |
|  Category Insights | Winning strategy + avg sold in your category |

---

##  Key Findings

1. **84% of AliExpress products are discounted** — discounting is the norm
2. **50% discount is the most popular tier** — psychological pricing at round numbers
3. **Smart Discounter sells 18x more** than Overpriced Low Performer
4. **Rating is the #1 predictor** of strategy success (34% importance)
5. **Category barely matters** — Smart Discounter dominates all 300+ categories
6. **Free shipping is a competitive advantage** — only 30% of products offer it

---

##  Authors

| Name | Role |
|---|---|
| Takwa Bennjima | ML Engineer & Data Scientist |
| Yayha Mabrouk | ML Engineer & Data Scientist |





- University project — Academic Year 2024/2025
